"""
src/metrics_engine.py
=====================
Computes baseline vs high-pressure metrics for batters and bowlers,
phase-adjusted expected values (runs saved / runs added), Empirical Bayes
shrinkage, clutch differentials, and match-to-match consistency scores.
"""

import pandas as pd
import numpy as np


def compute_batter_metrics(bbb: pd.DataFrame, min_hp_balls: int = 120) -> pd.DataFrame:
    """
    Computes comprehensive batting metrics comparing baseline performance
    with high-pressure performance (PI >= 0.60).
    """
    # 1. Baseline Performance (All balls faced)
    bat_base = bbb[bbb['is_batter_ball']].groupby(['striker_id', 'striker_name']).agg(
        balls_base=('runs', 'count'),
        runs_base=('runs', 'sum'),
        dismissals_base=('is_striker_out', 'sum'),
        dots_base=('runs', lambda s: (s == 0).sum()),
        fours_base=('is_four', 'sum'),
        sixes_base=('is_six', 'sum'),
        matches_base=('match_id', 'nunique')
    ).reset_index()

    # 2. High-Pressure Performance (PI >= 0.60)
    hp_mask = bbb['is_batter_ball'] & bbb['is_high_pressure']
    bat_hp = bbb[hp_mask].groupby(['striker_id', 'striker_name']).agg(
        balls_hp=('runs', 'count'),
        runs_hp=('runs', 'sum'),
        runs_added_hp=('runs_added', 'sum'),
        dismissals_hp=('is_striker_out', 'sum'),
        dots_hp=('runs', lambda s: (s == 0).sum()),
        fours_hp=('is_four', 'sum'),
        sixes_hp=('is_six', 'sum'),
        matches_hp=('match_id', 'nunique')
    ).reset_index()

    # Merge
    bat = bat_base.merge(bat_hp, on=['striker_id', 'striker_name'], how='inner')

    # Rates
    bat['sr_base'] = (bat['runs_base'] / bat['balls_base']) * 100.0
    bat['sr_hp'] = (bat['runs_hp'] / bat['balls_hp']) * 100.0
    bat['avg_base'] = bat['runs_base'] / np.maximum(1, bat['dismissals_base'])
    bat['avg_hp'] = bat['runs_hp'] / np.maximum(1, bat['dismissals_hp'])

    # Boundary and Dot percentages
    bat['bnd_pct_base'] = ((bat['fours_base'] + bat['sixes_base']) / bat['balls_base']) * 100.0
    bat['bnd_pct_hp'] = ((bat['fours_hp'] + bat['sixes_hp']) / bat['balls_hp']) * 100.0
    bat['dot_pct_base'] = (bat['dots_base'] / bat['balls_base']) * 100.0
    bat['dot_pct_hp'] = (bat['dots_hp'] / bat['balls_hp']) * 100.0

    # Differentials (Clutch Elevation)
    bat['delta_sr'] = bat['sr_hp'] - bat['sr_base']
    bat['delta_avg'] = bat['avg_hp'] - bat['avg_base']
    bat['delta_dot_pct'] = bat['dot_pct_base'] - bat['dot_pct_hp'] # Positive = fewer dots under pressure
    bat['delta_bnd_pct'] = bat['bnd_pct_hp'] - bat['bnd_pct_base']

    # Phase-adjusted runs added per 100 balls under pressure
    bat['runs_added_per_100'] = (bat['runs_added_hp'] / bat['balls_hp']) * 100.0

    # Empirical Bayes Shrinkage
    M_bat = 60.0
    mu_sr = 142.42
    bat['sr_bayes'] = (bat['balls_hp'] * bat['sr_hp'] + M_bat * mu_sr) / (bat['balls_hp'] + M_bat)

    K_bat = 4.0
    mu_avg = 21.52
    bat['avg_bayes'] = (bat['dismissals_hp'] * bat['avg_hp'] + K_bat * mu_avg) / (bat['dismissals_hp'] + K_bat)

    # 3. Match-by-Match Consistency
    match_bat = bbb[hp_mask].groupby(['striker_id', 'match_id']).agg(
        match_balls=('runs', 'count'),
        match_runs=('runs', 'sum'),
        match_runs_added=('runs_added', 'sum')
    ).reset_index()
    # Filter innings with at least 5 balls faced under pressure
    match_bat_filt = match_bat[match_bat['match_balls'] >= 5]
    match_bat_filt['positive_impact'] = (match_bat_filt['match_runs_added'] > 0) | (
        (match_bat_filt['match_runs'] / match_bat_filt['match_balls']) * 100.0 >= 135.0
    )
    consistency = match_bat_filt.groupby('striker_id')['positive_impact'].agg(
        cons_rate='mean',
        meaningful_hp_innings='count'
    ).reset_index()

    bat = bat.merge(consistency, on='striker_id', how='left')
    bat['cons_rate'] = bat['cons_rate'].fillna(0.40)
    bat['meaningful_hp_innings'] = bat['meaningful_hp_innings'].fillna(0)

    # Sample Confidence Weight
    bat['sample_conf'] = 1.0 - np.exp(-bat['balls_hp'] / 150.0)

    return bat


def compute_bowler_metrics(bbb: pd.DataFrame, min_hp_balls: int = 150) -> pd.DataFrame:
    """
    Computes comprehensive bowling metrics comparing baseline performance
    with high-pressure performance (PI >= 0.60).
    """
    # 1. Baseline Performance (All legal balls bowled)
    bowl_base = bbb.groupby(['bowler_id', 'bowler_name']).agg(
        balls_base=('is_legal', 'sum'),
        runs_base=('bowler_runs', 'sum'),
        wkts_base=('is_bowler_wkt', 'sum'),
        dots_base=('ball_runs', lambda s: (s == 0).sum()),
        boundaries_base=('ball_runs', lambda s: (s >= 4).sum()),
        matches_base=('match_id', 'nunique')
    ).reset_index()

    # 2. High-Pressure Performance (PI >= 0.60)
    hp_mask = bbb['is_high_pressure']
    bowl_hp = bbb[hp_mask].groupby(['bowler_id', 'bowler_name']).agg(
        balls_hp=('is_legal', 'sum'),
        runs_hp=('bowler_runs', 'sum'),
        runs_saved_hp=('runs_saved', 'sum'),
        wkts_hp=('is_bowler_wkt', 'sum'),
        dots_hp=('ball_runs', lambda s: (s == 0).sum()),
        boundaries_hp=('ball_runs', lambda s: (s >= 4).sum()),
        matches_hp=('match_id', 'nunique')
    ).reset_index()

    # Merge
    bowl = bowl_base.merge(bowl_hp, on=['bowler_id', 'bowler_name'], how='inner')

    # Rates
    bowl['econ_base'] = (bowl['runs_base'] / bowl['balls_base']) * 6.0
    bowl['econ_hp'] = (bowl['runs_hp'] / bowl['balls_hp']) * 6.0
    bowl['sr_base'] = bowl['balls_base'] / np.maximum(1, bowl['wkts_base'])
    bowl['sr_hp'] = bowl['balls_hp'] / np.maximum(1, bowl['wkts_hp'])

    # Boundary and Dot percentages
    bowl['dot_pct_base'] = (bowl['dots_base'] / bowl['balls_base']) * 100.0
    bowl['dot_pct_hp'] = (bowl['dots_hp'] / bowl['balls_hp']) * 100.0
    bowl['bnd_pct_base'] = (bowl['boundaries_base'] / bowl['balls_base']) * 100.0
    bowl['bnd_pct_hp'] = (bowl['boundaries_hp'] / bowl['balls_hp']) * 100.0

    # Differentials (Clutch Suppression)
    bowl['delta_econ'] = bowl['econ_base'] - bowl['econ_hp'] # Positive = stingier under pressure
    bowl['delta_sr'] = bowl['sr_base'] - bowl['sr_hp']       # Positive = strikes faster under pressure
    bowl['delta_dot_pct'] = bowl['dot_pct_hp'] - bowl['dot_pct_base']
    bowl['delta_bnd_pct'] = bowl['bnd_pct_base'] - bowl['bnd_pct_hp'] # Positive = fewer boundaries conceded

    # Phase-adjusted runs saved per over
    bowl['runs_saved_per_over'] = (bowl['runs_saved_hp'] / (bowl['balls_hp'] / 6.0))

    # Empirical Bayes Shrinkage
    M_bowl = 60.0
    mu_econ = 8.89
    bowl['econ_bayes'] = (bowl['balls_hp'] * bowl['econ_hp'] + M_bowl * mu_econ) / (bowl['balls_hp'] + M_bowl)

    K_bowl = 4.0
    mu_sr_bowl = 15.94
    bowl['sr_bayes'] = (bowl['wkts_hp'] * bowl['sr_hp'] + K_bowl * mu_sr_bowl) / (bowl['wkts_hp'] + K_bowl)

    # 3. Match-by-Match Consistency
    match_bowl = bbb[hp_mask].groupby(['bowler_id', 'match_id']).agg(
        match_legal_balls=('is_legal', 'sum'),
        match_runs=('bowler_runs', 'sum'),
        match_runs_saved=('runs_saved', 'sum'),
        match_wkts=('is_bowler_wkt', 'sum')
    ).reset_index()
    # Filter spells with at least 5 balls bowled under pressure
    match_bowl_filt = match_bowl[match_bowl['match_legal_balls'] >= 5]
    match_bowl_filt['positive_impact'] = (match_bowl_filt['match_runs_saved'] > 0) | (
        (match_bowl_filt['match_wkts'] >= 1) & ((match_bowl_filt['match_runs'] / (match_bowl_filt['match_legal_balls'] / 6.0)) <= 8.5)
    )
    consistency = match_bowl_filt.groupby('bowler_id')['positive_impact'].agg(
        cons_rate='mean',
        meaningful_hp_spells='count'
    ).reset_index()

    bowl = bowl.merge(consistency, on='bowler_id', how='left')
    bowl['cons_rate'] = bowl['cons_rate'].fillna(0.40)
    bowl['meaningful_hp_spells'] = bowl['meaningful_hp_spells'].fillna(0)

    # Sample Confidence Weight
    bowl['sample_conf'] = 1.0 - np.exp(-bowl['balls_hp'] / 180.0)

    return bowl
