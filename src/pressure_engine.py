"""
src/pressure_engine.py
======================
Core module for match state reconstruction, dynamic Win Probability estimation,
Leverage Index calculation, Phase & Collapse stress modeling, and ball-by-ball
Pressure Index (PI) synthesis.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression


def compute_delivery_team_runs(df: pd.DataFrame) -> pd.Series:
    """
    Computes total team runs conceded on each delivery event,
    properly accounting for wides, no-balls (Overstep), byes, legbyes, and penalties.
    """
    extra = df['extras_type']
    runs = df['runs']
    e2 = df['extras_2_runs'].fillna(0)
    
    team_runs = runs + e2
    # Add 1 penalty run for illegal deliveries and byes/legbyes
    mask_extra_1 = extra.isin(['wide', 'Overstep', 'legbyes', 'byes'])
    team_runs = np.where(mask_extra_1, team_runs + 1, team_runs)
    # Add 5 runs for penalty
    team_runs = np.where(extra == 'Penalty', team_runs + 5, team_runs)
    return team_runs


def load_and_enrich_match_data(workspace_dir: str = ".") -> pd.DataFrame:
    """
    Loads ball_by_ball, matches, competitions, and merges tournament context.
    Reconstructs complete chronological match states.
    """
    bbb = pd.read_csv(f"{workspace_dir}/ball_by_ball.csv")
    matches = pd.read_csv(f"{workspace_dir}/matches.csv")
    comps = pd.read_csv(f"{workspace_dir}/competitions.csv")
    
    # Merge competition and match metadata
    m_full = matches.merge(comps[['comp_id', 'match_format', 'season', 'comp_name']], on='comp_id')
    bbb = bbb.merge(
        m_full[['match_id', 'comp_id', 'season', 'win_team_id', 'revised_target', 'second_inn_revised_overs',
                'knock_out', 'stage', 'match_format', 'comp_name', 'match_date']],
        on='match_id', how='left'
    )
    
    # 1. Base delivery flags
    bbb['ball_runs'] = compute_delivery_team_runs(bbb)
    bbb['is_legal'] = ~bbb['extras_type'].isin(['wide', 'Overstep'])
    bbb['is_batter_ball'] = (bbb['extras_type'] != 'wide')
    bbb['is_bowler_wkt'] = bbb['is_wicket'] & (
        ~bbb['dismissal_type'].isin(['RunOut', 'Retire Out', 'Obstracting the field', 'Obstructing the field'])
    )
    bbb['bowler_runs'] = np.where(bbb['extras_type'].isin(['legbyes', 'byes']), 0, bbb['ball_runs'])
    bbb['is_striker_out'] = bbb['is_wicket'] & (bbb['dismissed_player_id'] == bbb['striker_id'])
    
    # 2. Innings 1 totals and Innings 2 Targets
    inn1_runs = bbb[bbb['innings'] == 1].groupby('match_id')['ball_runs'].sum().rename('inn1_total')
    bbb = bbb.merge(inn1_runs, on='match_id', how='left')
    bbb['target'] = np.where(bbb['revised_target'].notnull(), bbb['revised_target'], bbb['inn1_total'] + 1)
    
    # 3. Sort chronologically
    bbb = bbb.sort_values(['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)
    
    # 4. State variables before each ball
    bbb['cum_runs'] = bbb.groupby(['match_id', 'innings'])['ball_runs'].cumsum() - bbb['ball_runs']
    bbb['cum_wkts'] = bbb.groupby(['match_id', 'innings'])['is_wicket'].cumsum() - bbb['is_wicket']
    bbb['legal_balls'] = bbb.groupby(['match_id', 'innings'])['is_legal'].cumsum() - bbb['is_legal']
    
    # Total balls in innings (handling curtailed matches)
    total_balls_inn2 = np.where(
        bbb['second_inn_revised_overs'].notnull(),
        bbb['second_inn_revised_overs'] * 6,
        120
    )
    total_balls = np.where(bbb['innings'] == 2, total_balls_inn2, 120)
    bbb['balls_rem'] = np.maximum(1, total_balls - bbb['legal_balls'])
    bbb['wkts_in_hand'] = np.maximum(0, 10 - bbb['cum_wkts'])
    
    # 5. Innings 2 specific metrics
    bbb['runs_req'] = np.maximum(0, bbb['target'] - bbb['cum_runs'])
    bbb['rrr'] = (bbb['runs_req'] / bbb['balls_rem']) * 6.0
    bbb['crr'] = (bbb['cum_runs'] / np.maximum(1, bbb['legal_balls'])) * 6.0
    bbb['chase_win'] = (bbb['batting_team_id'] == bbb['win_team_id']).astype(int)
    
    # 6. Fit Win Probability Model for Innings 2
    inn2_mask = (bbb['innings'] == 2)
    features = ['runs_req', 'balls_rem', 'wkts_in_hand', 'rrr']
    train_df = bbb[inn2_mask].dropna(subset=features + ['chase_win'])
    
    wp_model = LogisticRegression(max_iter=1000, random_state=42)
    wp_model.fit(train_df[features], train_df['chase_win'])
    
    bbb['wp'] = 0.50
    bbb.loc[train_df.index, 'wp'] = wp_model.predict_proba(train_df[features])[:, 1]
    
    # 7. Tournament Stakes Multiplier
    is_ko = (bbb['knock_out'] == 1) | (bbb['stage'].isin(['Final', 'Qualifier', 'Eliminator', 'Semi Final', 'Super 4']))
    ko_mult = np.where(is_ko, 1.12, 1.0)
    
    # 8. Calculate Innings 2 Pressure
    li_wp = 4.0 * bbb['wp'] * (1.0 - bbb['wp'])
    s_rrr = np.clip((bbb['rrr'] - 6.0) / 8.0, 0.0, 1.0)
    s_wkt = np.clip((6.0 - bbb['wkts_in_hand']) / 5.0, 0.0, 1.0)
    s_phase_inn2 = np.power(np.clip((bbb['overid'] - 1) / 19.0, 0.0, 1.0), 1.2)
    pi_inn2 = (0.40 * li_wp + 0.30 * s_rrr * s_phase_inn2 + 0.20 * s_wkt * s_rrr + 0.10 * s_phase_inn2) * ko_mult
    
    # 9. Calculate Innings 1 Pressure
    over = bbb['overid']
    phase_base_inn1 = np.where(over >= 16, 0.70 + (over - 16) * 0.05, np.where(over >= 7, 0.45, 0.35))
    collapse_bonus = np.where(
        (over <= 6) & (bbb['cum_wkts'] >= 2), 0.25 + (bbb['cum_wkts'] - 2) * 0.10,
        np.where(
            (over <= 10) & (bbb['cum_wkts'] >= 3), 0.20 + (bbb['cum_wkts'] - 3) * 0.08,
            np.where((over <= 15) & (bbb['cum_wkts'] >= 5), 0.20, 0.0)
        )
    )
    wkt_pressure_inn1 = np.where(bbb['wkts_in_hand'] <= 3, 0.15, 0.0)
    pi_inn1 = (phase_base_inn1 + collapse_bonus + wkt_pressure_inn1) * ko_mult
    
    # 10. Super Overs: terminal maximum pressure
    pi_super = 1.00
    
    bbb['pressure_index'] = np.where(
        bbb['innings'] >= 3, pi_super,
        np.where(bbb['innings'] == 2, pi_inn2, pi_inn1)
    )
    bbb['pressure_index'] = np.clip(bbb['pressure_index'], 0.0, 1.0)
    
    # Pressure tiers
    bbb['is_high_pressure'] = (bbb['pressure_index'] >= 0.60)
    bbb['is_moderate_pressure'] = (bbb['pressure_index'] >= 0.40) & (bbb['pressure_index'] < 0.60)
    bbb['is_low_pressure'] = (bbb['pressure_index'] < 0.40)
    
    # 11. Phase Expected Runs (Baselines by innings and over)
    exp_bowl = bbb[bbb['is_legal']].groupby(['innings', 'overid'])['bowler_runs'].mean().rename('exp_bowl_runs')
    exp_bat = bbb[bbb['is_batter_ball']].groupby(['innings', 'overid'])['runs'].mean().rename('exp_bat_runs')
    bbb = bbb.merge(exp_bowl, on=['innings', 'overid'], how='left')
    bbb = bbb.merge(exp_bat, on=['innings', 'overid'], how='left')
    
    # Delivery value added vs phase par
    bbb['runs_saved'] = np.where(bbb['is_legal'], bbb['exp_bowl_runs'] - bbb['bowler_runs'], 0.0)
    bbb['runs_added'] = np.where(bbb['is_batter_ball'], bbb['runs'] - bbb['exp_bat_runs'], 0.0)
    
    return bbb, wp_model


# Comprehensive player name overrides for all top players across IPL history
IPL_NAME_OVERRIDES = {
    'V Kohli': 'Virat Kohli',
    'RG Sharma': 'Rohit Sharma',
    'S Dhawan': 'Shikhar Dhawan',
    'DA Warner': 'David Warner',
    'SK Raina': 'Suresh Raina',
    'MS Dhoni': 'MS Dhoni',
    'KL Rahul': 'KL Rahul',
    'AB de Villiers': 'AB de Villiers',
    'AM Rahane': 'Ajinkya Rahane',
    'CH Gayle': 'Chris Gayle',
    'RV Uthappa': 'Robin Uthappa',
    'KD Karthik': 'Dinesh Karthik',
    'F du Plessis': 'Faf du Plessis',
    'SV Samson': 'Sanju Samson',
    'AT Rayudu': 'Ambati Rayudu',
    'SA Yadav': 'Suryakumar Yadav',
    'G Gambhir': 'Gautam Gambhir',
    'JC Buttler': 'Jos Buttler',
    'MK Pandey': 'Manish Pandey',
    'SR Watson': 'Shane Watson',
    'SR Tendulkar': 'Sachin Tendulkar',
    'V Sehwag': 'Virender Sehwag',
    'R Dravid': 'Rahul Dravid',
    'SC Ganguly': 'Sourav Ganguly',
    'BB McCullum': 'Brendon McCullum',
    'JH Kallis': 'Jacques Kallis',
    'MEK Hussey': 'Michael Hussey',
    'DJ Bravo': 'Dwayne Bravo',
    'KA Pollard': 'Kieron Pollard',
    'Harbhajan Singh': 'Harbhajan Singh',
    'Z Khan': 'Zaheer Khan',
    'A Kumble': 'Anil Kumble',
    'M Muralitharan': 'Muttiah Muralitharan',
    'A Nehra': 'Ashish Nehra',
    'PV Tambe': 'Pravin Tambe',
    'PP Chawla': 'Piyush Chawla',
    'M Vijay': 'Murali Vijay',
    'YS Chahal': 'Yuzvendra Chahal',
    'B Kumar': 'Bhuvneshwar Kumar',
    'SP Narine': 'Sunil Narine',
    'R Ashwin': 'Ravichandran Ashwin',
    'JJ Bumrah': 'Jasprit Bumrah',
    'A Mishra': 'Amit Mishra',
    'RA Jadeja': 'Ravindra Jadeja',
    'SL Malinga': 'Lasith Malinga',
    'Rashid Khan': 'Rashid Khan',
    'HV Patel': 'Harshal Patel',
    'Sandeep Sharma': 'Sandeep Sharma',
    'Sandip Sharma': 'Sandeep Sharma',
    'UT Yadav': 'Umesh Yadav',
    'TA Boult': 'Trent Boult',
    'MM Sharma': 'Mohit Sharma',
    'Mohammed Shami': 'Mohammed Shami',
    'AR Patel': 'Axar Patel',
    'AD Russell': 'Andre Russell',
    'HH Pandya': 'Hardik Pandya',
    'Mohammed Siraj': 'Mohammed Siraj',
    'Arshdeep Singh': 'Arshdeep Singh',
    'K Rabada': 'Kagiso Rabada',
    'CV Varun': 'Varun Chakravarthy',
    'Kuldeep Yadav': 'Kuldeep Yadav',
    'Shubman Gill': 'Shubman Gill',
    'Ishan Kishan': 'Ishan Kishan',
    'SO Hetmyer': 'Shimron Hetmyer',
    'N Pooran': 'Nicholas Pooran',
    'MP Stoinis': 'Marcus Stoinis',
    'TH David': 'Tim David',
    'D Miller': 'David Miller',
    'DA Miller': 'David Miller',
    'RD Gaikwad': 'Ruturaj Gaikwad',
    'Tilak Varma': 'Tilak Varma',
    'R Parag': 'Riyan Parag',
    'YBK Jaiswal': 'Yashasvi Jaiswal',
    'Abhishek Sharma': 'Abhishek Sharma',
    'H Klaasen': 'Heinrich Klaasen',
    'SN Thakur': 'Shardul Thakur',
    'KH Pandya': 'Krunal Pandya',
    'Washington Sundar': 'Washington Sundar',
    'N Rana': 'Nitish Rana',
    'VR Iyer': 'Venkatesh Iyer',
    'SS Iyer': 'Shreyas Iyer',
    'Abdul Samad': 'Abdul Samad',
    'Shahrukh Khan': 'Shahrukh Khan',
    'R Tewatia': 'Rahul Tewatia',
    'JM Bairstow': 'Jonny Bairstow',
    'LS Livingstone': 'Liam Livingstone',
    'SM Curran': 'Sam Curran',
    'MM Ali': 'Moeen Ali',
    'Q de Kock': 'Quinton de Kock',
    'W Hasaranga': 'Wanindu Hasaranga',
    'PWH de Silva': 'Wanindu Hasaranga',
    'M Theekshana': 'Maheesh Theekshana',
    'Noor Ahmad': 'Noor Ahmad',
    'Fazalhaq Farooqi': 'Fazalhaq Farooqi',
    'Naveen-ul-Haq': 'Naveen-ul-Haq',
    'LH Ferguson': 'Lockie Ferguson',
    'JR Hazlewood': 'Josh Hazlewood',
    'PJ Cummins': 'Pat Cummins',
    'MA Starc': 'Mitchell Starc',
    'TG Southee': 'Tim Southee',
    'JD Unadkat': 'Jaydev Unadkat',
    'KK Ahmed': 'Khaleel Ahmed',
    'M Prasidh Krishna': 'Prasidh Krishna',
    'M Pathirana': 'Matheesha Pathirana',
    'M Jansen': 'Marco Jansen',
    'G Coetzee': 'Gerald Coetzee',
    'N Burger': 'Nandre Burger',
    'P Simran Singh': 'Prabhsimran Singh',
    'JM Sharma': 'Jitesh Sharma',
    'RM Patidar': 'Rajat Patidar',
    'MK Lomror': 'Mahipal Lomror',
    'Akash Deep': 'Akash Deep',
    'Mohsin Khan': 'Mohsin Khan',
    'Yash Thakur': 'Yash Thakur',
    'B Sai Sudharsan': 'Sai Sudharsan',
    'A Manohar': 'Abhinav Manohar',
    'WP Saha': 'Wriddhiman Saha',
    'RA Tripathi': 'Rahul Tripathi',
    'Nitish Kumar Reddy': 'Nitish Kumar Reddy',
    'Ashutosh Sharma': 'Ashutosh Sharma',
    'Shashank Singh': 'Shashank Singh',
    'Abishek Porel': 'Abishek Porel',
    'Harshit Rana': 'Harshit Rana',
    'Mayank Yadav': 'Mayank Yadav',
    'T Natarajan': 'T Natarajan',
    'Mukesh Kumar': 'Mukesh Kumar',
    'Avesh Khan': 'Avesh Khan',
    'GJ Maxwell': 'Glenn Maxwell',
    'DW Steyn': 'Dale Steyn',
    'IK Pathan': 'Irfan Pathan',
    'YK Pathan': 'Yusuf Pathan',
    'M Morkel': 'Morne Morkel',
    'JA Morkel': 'Albie Morkel',
    'RP Singh': 'RP Singh',
    'R Vinay Kumar': 'Vinay Kumar',
    'L Balaji': 'Lakshmipathy Balaji',
    'S Sreesanth': 'S Sreesanth',
    'SK Warne': 'Shane Warne',
    'A Symonds': 'Andrew Symonds',
    'Yuvraj Singh': 'Yuvraj Singh',
    'M Manhas': 'Mithun Manhas',
    'TL Suman': 'Tirumalasetti Suman',
    'STR Binny': 'Stuart Binny',
    'NLTC Perera': 'Thisara Perera',
    'JP Duminy': 'JP Duminy',
    'MN Samuels': 'Marlon Samuels',
    'BJ Hodge': 'Brad Hodge',
    'CL White': 'Cameron White',
    'KP Pietersen': 'Kevin Pietersen',
    'DPMD Jayawardene': 'Mahela Jayawardene',
    'KC Sangakkara': 'Kumar Sangakkara',
    'AC Gilchrist': 'Adam Gilchrist',
    'ML Hayden': 'Matthew Hayden',
    'PA Patel': 'Parthiv Patel',
    'NV Ojha': 'Naman Ojha',
    'KM Jadhav': 'Kedar Jadhav',
    'CA Lynn': 'Chris Lynn',
    'E Lewis': 'Evin Lewis',
    'C Munro': 'Colin Munro',
    'JC Archer': 'Jofra Archer',
    'AJ Tye': 'Andrew Tye',
    'CH Morris': 'Chris Morris',
    'DJ Willey': 'David Willey',
    'CR Woakes': 'Chris Woakes',
    'CJ Jordan': 'Chris Jordan',
    'MA Wood': 'Mark Wood',
    'SE Marsh': 'Shaun Marsh',
    'AJ Finch': 'Aaron Finch',
    'EJG Morgan': 'Eoin Morgan',
    'BA Stokes': 'Ben Stokes',
    'RR Pant': 'Rishabh Pant',
    'T Stubbs': 'Tristan Stubbs',
    'DL Chahar': 'Deepak Chahar',
    'RD Chahar': 'Rahul Chahar',
    'NM Coulter-Nile': 'Nathan Coulter-Nile',
    'WD Parnell': 'Wayne Parnell',
    'R Bhatia': 'Rajat Bhatia',
    'DP Nannes': 'Dirk Nannes',
    'MR Marsh': 'Mitchell Marsh',
    'KS Williamson': 'Kane Williamson',
    'SN Khan': 'Sarfaraz Khan',
}

KNOWN_BAT_HAND = {
    'Suresh Raina': 'LHB', 'Chris Gayle': 'LHB', 'Gautam Gambhir': 'LHB', 'Shikhar Dhawan': 'LHB',
    'David Warner': 'LHB', 'Yuvraj Singh': 'LHB', 'Matthew Hayden': 'LHB', 'Adam Gilchrist': 'LHB',
    'Kumar Sangakkara': 'LHB', 'Michael Hussey': 'LHB', 'Irfan Pathan': 'LHB', 'Albie Morkel': 'LHB',
    'Rishabh Pant': 'LHB', 'Nicholas Pooran': 'LHB', 'Shimron Hetmyer': 'LHB', 'Quinton de Kock': 'LHB',
    'Yashasvi Jaiswal': 'LHB', 'Abhishek Sharma': 'LHB', 'Ravindra Jadeja': 'LHB', 'Axar Patel': 'LHB',
    'Krunal Pandya': 'LHB', 'Sam Curran': 'LHB', 'Moeen Ali': 'LHB', 'Tilak Varma': 'LHB',
    'Rinku Singh': 'LHB', 'Sai Sudharsan': 'LHB', 'Shivam Dube': 'LHB', 'Ben Stokes': 'LHB',
    'Sourav Ganguly': 'LHB', 'Brian Lara': 'LHB',
}

KNOWN_BOWL_STYLE = {
    'Lasith Malinga': 'Right-Arm Pace', 'Dale Steyn': 'Right-Arm Pace', 'Shane Warne': 'Right-Arm Leg-Spin',
    'Anil Kumble': 'Right-Arm Leg-Spin', 'Muttiah Muralitharan': 'Right-Arm Off-Spin', 'Harbhajan Singh': 'Right-Arm Off-Spin',
    'Amit Mishra': 'Right-Arm Leg-Spin', 'Piyush Chawla': 'Right-Arm Leg-Spin', 'Dwayne Bravo': 'Right-Arm Pace',
    'Zaheer Khan': 'Left-Arm Pace', 'Ashish Nehra': 'Left-Arm Pace', 'RP Singh': 'Left-Arm Pace',
    'Irfan Pathan': 'Left-Arm Pace', 'Morne Morkel': 'Right-Arm Pace', 'Albie Morkel': 'Right-Arm Pace',
    'Pravin Tambe': 'Right-Arm Leg-Spin', 'Shane Watson': 'Right-Arm Pace', 'Jacques Kallis': 'Right-Arm Pace',
    'Sunil Narine': 'Right-Arm Off-Spin', 'Jasprit Bumrah': 'Right-Arm Pace', 'Bhuvneshwar Kumar': 'Right-Arm Pace',
    'Yuzvendra Chahal': 'Right-Arm Leg-Spin', 'Ravichandran Ashwin': 'Right-Arm Off-Spin', 'Trent Boult': 'Left-Arm Pace',
    'Mitchell Starc': 'Left-Arm Pace', 'Kagiso Rabada': 'Right-Arm Pace', 'Rashid Khan': 'Right-Arm Leg-Spin',
    'Varun Chakravarthy': 'Right-Arm Leg-Spin', 'Kuldeep Yadav': 'Left-Arm Wrist-Spin', 'Axar Patel': 'Slow Left-Arm Orthodox',
    'Ravindra Jadeja': 'Slow Left-Arm Orthodox', 'Wanindu Hasaranga': 'Right-Arm Leg-Spin', 'Noor Ahmad': 'Left-Arm Wrist-Spin',
    'Maheesh Theekshana': 'Right-Arm Off-Spin', 'Mohit Sharma': 'Right-Arm Pace', 'Sandeep Sharma': 'Right-Arm Pace',
    'Umesh Yadav': 'Right-Arm Pace', 'Mohammed Shami': 'Right-Arm Pace', 'Mohammed Siraj': 'Right-Arm Pace',
    'Arshdeep Singh': 'Left-Arm Pace', 'Harshal Patel': 'Right-Arm Pace', 'T Natarajan': 'Left-Arm Pace',
    'Avesh Khan': 'Right-Arm Pace', 'Khaleel Ahmed': 'Left-Arm Pace', 'Mukesh Kumar': 'Right-Arm Pace',
    'Mayank Yadav': 'Right-Arm Pace', 'Harshit Rana': 'Right-Arm Pace',
}


def load_and_enrich_ipl_history(workspace_dir: str = ".") -> pd.DataFrame:
    """
    Reconstructs complete chronological match states across ALL 19 seasons
    of Indian Premier League history (2008 through 2026).
    Combines Cricsheet historical IPL deliveries (2008-2025) with the official 2026 IPL dataset.
    """
    print("Loading full IPL historical delivery database (2008-2026)...")
    bbb = pd.read_csv(f"{workspace_dir}/ball_by_ball.csv")
    matches = pd.read_csv(f"{workspace_dir}/matches.csv")
    comps = pd.read_csv(f"{workspace_dir}/competitions.csv")
    m_full = matches.merge(comps[['comp_id', 'match_format', 'season', 'comp_name']], on='comp_id')

    # Build reference player style lookups from bbb
    bat_types = bbb.dropna(subset=['batting_type']).groupby('striker_name')['batting_type'].first().to_dict()
    bowl_types = bbb.dropna(subset=['bowling_type']).groupby('bowler_name')['bowling_type'].first().to_dict()
    bat_types.update(KNOWN_BAT_HAND)
    bowl_types.update(KNOWN_BOWL_STYLE)

    def map_player(name):
        if pd.isna(name):
            return name
        n_str = str(name).strip()
        return IPL_NAME_OVERRIDES.get(n_str, n_str)

    # 1. Historical IPL deliveries (2008-2025)
    df_ipl = pd.read_csv(f"{workspace_dir}/IPL.csv", low_memory=False)

    def clean_season(s):
        s_str = str(s).strip()
        if '/' in s_str:
            return int(s_str.split('/')[0])
        return int(s_str)

    df_ipl['clean_season'] = df_ipl['season'].apply(clean_season)
    df_ipl['clean_striker'] = df_ipl['batter'].apply(map_player)
    df_ipl['clean_bowler'] = df_ipl['bowler'].apply(map_player)
    df_ipl['clean_non_striker'] = df_ipl['non_striker'].apply(map_player)
    df_ipl['clean_out_player'] = df_ipl['player_out'].apply(map_player)

    df_ipl_clean = pd.DataFrame()
    df_ipl_clean['match_id'] = df_ipl['match_id']
    df_ipl_clean['match_date'] = pd.to_datetime(df_ipl['date'], format='mixed').dt.strftime('%Y-%m-%d')
    df_ipl_clean['season'] = df_ipl['clean_season']
    df_ipl_clean['comp_name'] = 'IPL ' + df_ipl_clean['season'].astype(str)
    df_ipl_clean['match_format'] = 'IPL'
    df_ipl_clean['innings'] = df_ipl['innings']
    df_ipl_clean['overid'] = df_ipl['over_no'] + 1
    df_ipl_clean['over_ball_num'] = df_ipl['ball']
    df_ipl_clean['striker_name'] = df_ipl['clean_striker']
    df_ipl_clean['bowler_name'] = df_ipl['clean_bowler']
    df_ipl_clean['non_striker_name'] = df_ipl['clean_non_striker']
    df_ipl_clean['runs'] = df_ipl['runs_batter']
    df_ipl_clean['ball_runs'] = df_ipl['runs_total']
    df_ipl_clean['bowler_runs'] = df_ipl['runs_bowler']
    df_ipl_clean['is_legal'] = (df_ipl['valid_ball'] == 1)
    df_ipl_clean['is_batter_ball'] = ~df_ipl['extra_type'].isin(['wides', 'wide'])
    df_ipl_clean['is_four'] = (df_ipl['runs_batter'] == 4)
    df_ipl_clean['is_six'] = (df_ipl['runs_batter'] == 6)
    df_ipl_clean['is_wicket'] = df_ipl['player_out'].notna()
    df_ipl_clean['dismissal_type'] = df_ipl['wicket_kind'].fillna('None')
    df_ipl_clean['is_bowler_wkt'] = df_ipl_clean['is_wicket'] & (
        ~df_ipl_clean['dismissal_type'].str.lower().isin(['run out', 'retired hurt', 'obstructing the field', 'retired out', 'none'])
    )
    df_ipl_clean['is_striker_out'] = df_ipl_clean['is_wicket'] & (df_ipl['clean_out_player'] == df_ipl_clean['striker_name'])
    df_ipl_clean['extras_type'] = df_ipl['extra_type']
    df_ipl_clean['target'] = df_ipl['runs_target']
    df_ipl_clean['batting_team'] = df_ipl['batting_team']
    df_ipl_clean['bowling_team'] = df_ipl['bowling_team']
    df_ipl_clean['win_team'] = df_ipl['match_won_by']
    df_ipl_clean['stage'] = df_ipl['stage'].fillna('League')
    df_ipl_clean['knock_out'] = df_ipl_clean['stage'].isin(['Final', 'Qualifier 1', 'Qualifier 2', 'Eliminator', 'Semi Final', 'Playoffs']).astype(int)

    # 2. IPL 2026 deliveries from official challenge dataset
    ipl_2026_m = m_full[m_full['comp_name'] == 'IPL 2026']
    bbb_2026 = bbb[bbb['match_id'].isin(ipl_2026_m['match_id'])].copy()
    bbb_2026 = bbb_2026.merge(
        ipl_2026_m[['match_id', 'match_date', 'season', 'comp_name', 'win_team_id', 'knock_out', 'stage', 'revised_target', 'home_team', 'away_team', 'home_team_id']],
        on='match_id', how='left'
    )
    bbb_2026['ball_runs'] = compute_delivery_team_runs(bbb_2026)
    bbb_2026['is_legal'] = ~bbb_2026['extras_type'].isin(['wide', 'Overstep'])
    bbb_2026['is_batter_ball'] = (bbb_2026['extras_type'] != 'wide')
    bbb_2026['is_bowler_wkt'] = bbb_2026['is_wicket'] & (
        ~bbb_2026['dismissal_type'].isin(['RunOut', 'Retire Out', 'Obstracting the field', 'Obstructing the field'])
    )
    bbb_2026['bowler_runs'] = np.where(bbb_2026['extras_type'].isin(['legbyes', 'byes']), 0, bbb_2026['ball_runs'])
    bbb_2026['is_striker_out'] = bbb_2026['is_wicket'] & (bbb_2026['dismissed_player_id'] == bbb_2026['striker_id'])

    inn1_runs_26 = bbb_2026[bbb_2026['innings'] == 1].groupby('match_id')['ball_runs'].sum().rename('inn1_total')
    bbb_2026 = bbb_2026.merge(inn1_runs_26, on='match_id', how='left')
    bbb_2026['target'] = np.where(bbb_2026['revised_target'].notnull(), bbb_2026['revised_target'], bbb_2026['inn1_total'] + 1)

    teams_df = pd.read_csv(f"{workspace_dir}/teams.csv")[['team_id', 'team_name']].drop_duplicates()
    t_map = teams_df.set_index('team_id')['team_name'].to_dict()
    bbb_2026['batting_team'] = bbb_2026['batting_team_id'].map(t_map)
    bbb_2026['bowling_team'] = bbb_2026['bowling_team_id'].map(t_map)
    bbb_2026['win_team'] = bbb_2026['win_team_id'].map(t_map)

    df_2026_clean = pd.DataFrame()
    df_2026_clean['match_id'] = bbb_2026['match_id']
    df_2026_clean['match_date'] = bbb_2026['match_date']
    df_2026_clean['season'] = 2026
    df_2026_clean['comp_name'] = 'IPL 2026'
    df_2026_clean['match_format'] = 'IPL'
    df_2026_clean['innings'] = bbb_2026['innings']
    df_2026_clean['overid'] = bbb_2026['overid']
    df_2026_clean['over_ball_num'] = bbb_2026['over_ball_num']
    df_2026_clean['striker_name'] = bbb_2026['striker_name'].apply(map_player)
    df_2026_clean['bowler_name'] = bbb_2026['bowler_name'].apply(map_player)
    df_2026_clean['non_striker_name'] = bbb_2026['non_striker_name'].apply(map_player)
    df_2026_clean['runs'] = bbb_2026['runs']
    df_2026_clean['ball_runs'] = bbb_2026['ball_runs']
    df_2026_clean['bowler_runs'] = bbb_2026['bowler_runs']
    df_2026_clean['is_legal'] = bbb_2026['is_legal']
    df_2026_clean['is_batter_ball'] = bbb_2026['is_batter_ball']
    df_2026_clean['is_four'] = bbb_2026['is_four']
    df_2026_clean['is_six'] = bbb_2026['is_six']
    df_2026_clean['is_wicket'] = bbb_2026['is_wicket']
    df_2026_clean['dismissal_type'] = bbb_2026['dismissal_type'].fillna('None')
    df_2026_clean['is_bowler_wkt'] = bbb_2026['is_bowler_wkt']
    df_2026_clean['is_striker_out'] = bbb_2026['is_striker_out']
    df_2026_clean['extras_type'] = bbb_2026['extras_type']
    df_2026_clean['target'] = bbb_2026['target']
    df_2026_clean['batting_team'] = bbb_2026['batting_team']
    df_2026_clean['bowling_team'] = bbb_2026['bowling_team']
    df_2026_clean['win_team'] = bbb_2026['win_team']
    df_2026_clean['stage'] = bbb_2026['stage'].fillna('League')
    df_2026_clean['knock_out'] = bbb_2026['knock_out']

    # 3. Concatenate
    ipl_all = pd.concat([df_ipl_clean, df_2026_clean], ignore_index=True)
    ipl_all['batting_type'] = ipl_all['striker_name'].map(bat_types).fillna('RHB')
    ipl_all['bowling_type'] = ipl_all['bowler_name'].map(bowl_types).fillna('Right-Arm Pace')

    # Bowling archetype categorization
    def quick_cat(btype):
        if pd.isna(btype): return "Unknown"
        bl = str(btype).lower()
        if "left-arm" in bl and any(x in bl for x in ["fast", "medium", "pace"]): return "Left-Arm Pace"
        if "right-arm" in bl and any(x in bl for x in ["fast", "medium", "pace"]): return "Right-Arm Pace"
        if "slow left-arm orthodox" in bl: return "Slow Left-Arm Orthodox"
        if "left-arm" in bl and any(x in bl for x in ["wrist", "unorthodox", "chinaman"]): return "Left-Arm Wrist-Spin"
        if any(x in bl for x in ["offbreak", "off-break", "off break", "off-spin"]): return "Right-Arm Off-Spin"
        if any(x in bl for x in ["leg-break", "legbreak", "leg break", "leg-spin", "googly"]): return "Right-Arm Leg-Spin"
        if "spin" in bl: return "Spin (Other)"
        return "Pace (Other)"

    ipl_all['bowling_category'] = ipl_all['bowling_type'].apply(quick_cat)
    ipl_all['pace_or_spin'] = np.where(ipl_all['bowling_category'].str.contains('Spin|Slow'), 'Spin', 'Pace')
    ipl_all['stroke'] = 'Unclassified'
    ipl_all['delivery_style'] = 'Standard'
    ipl_all['on_or_off'] = 'Unclassified'

    ipl_all['phase'] = np.where(
        ipl_all['overid'] <= 6, 'Powerplay (1-6)',
        np.where(ipl_all['overid'] <= 15, 'Middle (7-15)', 'Death (16-20)')
    )

    # 4. State variables
    ipl_all = ipl_all.sort_values(['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)
    ipl_all['cum_runs'] = ipl_all.groupby(['match_id', 'innings'])['ball_runs'].cumsum() - ipl_all['ball_runs']
    ipl_all['cum_wkts'] = ipl_all.groupby(['match_id', 'innings'])['is_wicket'].cumsum() - ipl_all['is_wicket']
    ipl_all['legal_balls'] = ipl_all.groupby(['match_id', 'innings'])['is_legal'].cumsum() - ipl_all['is_legal']
    ipl_all['balls_rem'] = np.maximum(1, 120 - ipl_all['legal_balls'])
    ipl_all['wkts_in_hand'] = np.maximum(0, 10 - ipl_all['cum_wkts'])

    inn1_runs = ipl_all[ipl_all['innings'] == 1].groupby('match_id')['ball_runs'].sum().rename('inn1_calc')
    ipl_all = ipl_all.merge(inn1_runs, on='match_id', how='left')
    ipl_all['target'] = np.where(ipl_all['target'].notnull(), ipl_all['target'], ipl_all['inn1_calc'] + 1)

    ipl_all['runs_req'] = np.maximum(0, ipl_all['target'] - ipl_all['cum_runs'])
    ipl_all['rrr'] = (ipl_all['runs_req'] / ipl_all['balls_rem']) * 6.0
    ipl_all['crr'] = (ipl_all['cum_runs'] / np.maximum(1, ipl_all['legal_balls'])) * 6.0
    ipl_all['chase_win'] = (ipl_all['batting_team'] == ipl_all['win_team']).astype(int)

    # Fit WP Model for Innings 2
    inn2_mask = (ipl_all['innings'] == 2)
    features = ['runs_req', 'balls_rem', 'wkts_in_hand', 'rrr']
    train_df = ipl_all[inn2_mask].dropna(subset=features + ['chase_win'])

    wp_model = LogisticRegression(max_iter=1000, random_state=42)
    wp_model.fit(train_df[features], train_df['chase_win'])

    ipl_all['wp'] = 0.50
    ipl_all.loc[train_df.index, 'wp'] = wp_model.predict_proba(train_df[features])[:, 1]

    ko_mult = np.where(ipl_all['knock_out'] == 1, 1.12, 1.0)
    li_wp = 4.0 * ipl_all['wp'] * (1.0 - ipl_all['wp'])
    s_rrr = np.clip((ipl_all['rrr'] - 6.0) / 8.0, 0.0, 1.0)
    s_wkt = np.clip((6.0 - ipl_all['wkts_in_hand']) / 5.0, 0.0, 1.0)
    s_phase_inn2 = np.power(np.clip((ipl_all['overid'] - 1) / 19.0, 0.0, 1.0), 1.2)
    pi_inn2 = (0.40 * li_wp + 0.30 * s_rrr * s_phase_inn2 + 0.20 * s_wkt * s_rrr + 0.10 * s_phase_inn2) * ko_mult

    over = ipl_all['overid']
    phase_base_inn1 = np.where(over >= 16, 0.70 + (over - 16) * 0.05, np.where(over >= 7, 0.45, 0.35))
    collapse_bonus = np.where(
        (over <= 6) & (ipl_all['cum_wkts'] >= 2), 0.25 + (ipl_all['cum_wkts'] - 2) * 0.10,
        np.where(
            (over <= 10) & (ipl_all['cum_wkts'] >= 3), 0.20 + (ipl_all['cum_wkts'] - 3) * 0.08,
            np.where((over <= 15) & (ipl_all['cum_wkts'] >= 5), 0.20, 0.0)
        )
    )
    wkt_pressure_inn1 = np.where(ipl_all['wkts_in_hand'] <= 3, 0.15, 0.0)
    pi_inn1 = (phase_base_inn1 + collapse_bonus + wkt_pressure_inn1) * ko_mult

    ipl_all['pressure_index'] = np.where(
        ipl_all['innings'] >= 3, 1.00,
        np.where(ipl_all['innings'] == 2, pi_inn2, pi_inn1)
    )
    ipl_all['pressure_index'] = np.clip(ipl_all['pressure_index'], 0.05, 1.0)
    ipl_all['is_high_pressure'] = (ipl_all['pressure_index'] >= 0.60)
    ipl_all['is_moderate_pressure'] = (ipl_all['pressure_index'] >= 0.40) & (ipl_all['pressure_index'] < 0.60)
    ipl_all['is_low_pressure'] = (ipl_all['pressure_index'] < 0.40)
    ipl_all['pressure_tier'] = np.where(
        ipl_all['is_high_pressure'], 'High Pressure',
        np.where(ipl_all['is_moderate_pressure'], 'Moderate Pressure', 'Low Pressure')
    )

    exp_bowl = ipl_all[ipl_all['is_legal']].groupby(['innings', 'overid'])['bowler_runs'].mean().rename('exp_bowl_runs')
    exp_bat = ipl_all[ipl_all['is_batter_ball']].groupby(['innings', 'overid'])['runs'].mean().rename('exp_bat_runs')
    ipl_all = ipl_all.merge(exp_bowl, on=['innings', 'overid'], how='left')
    ipl_all = ipl_all.merge(exp_bat, on=['innings', 'overid'], how='left')
    ipl_all['runs_saved'] = np.where(ipl_all['is_legal'], ipl_all['exp_bowl_runs'] - ipl_all['bowler_runs'], 0.0)
    ipl_all['runs_added'] = np.where(ipl_all['is_batter_ball'], ipl_all['runs'] - ipl_all['exp_bat_runs'], 0.0)

    # Assign persistent player IDs
    player_names = sorted(list(set(ipl_all['striker_name'].unique()).union(set(ipl_all['bowler_name'].unique()))))
    id_map = {name: idx + 1 for idx, name in enumerate(player_names)}
    ipl_all['striker_id'] = ipl_all['striker_name'].map(id_map)
    ipl_all['bowler_id'] = ipl_all['bowler_name'].map(id_map)
    ipl_all['dismissed_player_id'] = np.where(ipl_all['is_striker_out'], ipl_all['striker_id'], 0)

    print(f"Loaded and enriched {len(ipl_all):,} deliveries across {ipl_all['match_id'].nunique()} IPL matches (2008-2026).")
    return ipl_all, wp_model
