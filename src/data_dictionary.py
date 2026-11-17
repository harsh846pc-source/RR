"""
src/data_dictionary.py
======================
Comprehensive Data Dictionary, Mathematical Formula Specifications,
and Column Representation Reference for Rajasthan Royals SupeRR Selector.
Covers:
1. Delivery-Level Schema (70 columns)
2. Batting Pressure & Performance Metrics (37 columns)
3. Bowling Pressure & Performance Metrics (35 columns)
4. Theoretical Foundations & Mathematical Formulations
"""

import pandas as pd
from typing import List, Dict, Any

# ==============================================================================
# 1. DELIVERY-LEVEL SCHEMA (70 COLUMNS)
# ==============================================================================
DELIVERY_COLUMNS_INFO = [
    # Metadata & Identifiers
    {
        "column_name": "match_id",
        "category": "Metadata & Identifiers",
        "data_type": "int64",
        "description": "Unique identifier assigned to each professional match across competitions.",
        "representation": "Integer ID (e.g., 1426239, 1304047)",
        "formula": "Primary key from matches table / Cricsheet record",
        "interpretation": "Part of composite primary key (match_id, innings, overid, over_ball_num)."
    },
    {
        "column_name": "innings",
        "category": "Metadata & Identifiers",
        "data_type": "int64",
        "description": "Innings index within the match.",
        "representation": "1 = First Innings, 2 = Second Innings (Chase), 3/4 = Super Over",
        "formula": "Raw match innings index",
        "interpretation": "Innings 1 involves target setting and collapse crisis; Innings 2 evaluates real-time chase dynamics."
    },
    {
        "column_name": "overid",
        "category": "Match State",
        "data_type": "int64",
        "description": "1-based over sequence number in the innings.",
        "representation": "Integer 1 through 20 (or curtailed over limit)",
        "formula": "Over number (1-based: 1 to 20)",
        "interpretation": "Overs 1-6 = Powerplay, Overs 7-15 = Middle, Overs 16-20 = Death."
    },
    {
        "column_name": "over_ball_num",
        "category": "Match State",
        "data_type": "int64",
        "description": "Sequential delivery count bowled within the current over.",
        "representation": "Integer 1 to 6 (or higher if extras bowled)",
        "formula": "Delivery sequence within over",
        "interpretation": "Can exceed 6 when wides or no-balls occur."
    },
    {
        "column_name": "innings_ball_num",
        "category": "Match State",
        "data_type": "int64",
        "description": "Absolute cumulative delivery number bowled in the innings.",
        "representation": "Integer from 1 upwards (typically 1 to 135)",
        "formula": "Sequential ball counter across entire innings",
        "interpretation": "Tracks chronological sequence of events including illegal deliveries."
    },
    {
        "column_name": "batting_team_id",
        "category": "Metadata & Identifiers",
        "data_type": "int64",
        "description": "Unique identifier of the batting franchise or national team.",
        "representation": "Team ID integer (e.g., 661 for Rajasthan Royals)",
        "formula": "Foreign key referencing teams table",
        "interpretation": "Identifies the side at the crease."
    },
    {
        "column_name": "bowling_team_id",
        "category": "Metadata & Identifiers",
        "data_type": "int64",
        "description": "Unique identifier of the bowling franchise or national team.",
        "representation": "Team ID integer",
        "formula": "Foreign key referencing teams table",
        "interpretation": "Identifies the fielding side."
    },
    {
        "column_name": "striker_id",
        "category": "Metadata & Identifiers",
        "data_type": "int64",
        "description": "Unique persistent player ID of the batter facing the delivery.",
        "representation": "Player ID integer",
        "formula": "Foreign key referencing player roster",
        "interpretation": "Primary key for batter aggregations and matchup queries."
    },
    {
        "column_name": "striker_name",
        "category": "Metadata & Identifiers",
        "data_type": "object (str)",
        "description": "Clean, standardized full display name of the facing batsman.",
        "representation": "String (e.g. 'Suryakumar Yadav', 'AB de Villiers', 'Jos Buttler')",
        "formula": "Standardized via NAME_OVERRIDES dictionary",
        "interpretation": "Cleaned across historical initials and official rosters."
    },
    {
        "column_name": "non_striker_id",
        "category": "Metadata & Identifiers",
        "data_type": "int64",
        "description": "Unique player ID of the batsman at the non-striker's crease.",
        "representation": "Player ID integer",
        "formula": "Foreign key referencing player roster",
        "interpretation": "Tracks running between wickets and partnership context."
    },
    {
        "column_name": "non_striker_name",
        "category": "Metadata & Identifiers",
        "data_type": "object (str)",
        "description": "Clean, standardized full display name of the non-striker.",
        "representation": "String (e.g., 'Sanju Samson', 'Virat Kohli')",
        "formula": "Standardized via NAME_OVERRIDES dictionary",
        "interpretation": "Cleaned across historical and official rosters."
    },
    {
        "column_name": "bowler_id",
        "category": "Metadata & Identifiers",
        "data_type": "int64",
        "description": "Unique persistent player ID of the active bowler delivering the ball.",
        "representation": "Player ID integer",
        "formula": "Foreign key referencing player roster",
        "interpretation": "Primary key for bowler aggregations and matchup queries."
    },
    {
        "column_name": "bowler_name",
        "category": "Metadata & Identifiers",
        "data_type": "object (str)",
        "description": "Clean, standardized full display name of the active bowler.",
        "representation": "String (e.g. 'Sunil Narine', 'Jasprit Bumrah', 'Lasith Malinga')",
        "formula": "Standardized via NAME_OVERRIDES dictionary",
        "interpretation": "Cleaned across historical initials and official rosters."
    },
    {
        "column_name": "batting_type",
        "category": "Player Profile",
        "data_type": "object (str)",
        "description": "Batting handedness of the striker at the crease.",
        "representation": "Categorical: 'RHB' (Right-Handed) or 'LHB' (Left-Handed)",
        "formula": "Roster mapping / delivery metadata",
        "interpretation": "Essential for matchup split modeling (RHB vs LHB)."
    },
    {
        "column_name": "bowling_type",
        "category": "Player Profile",
        "data_type": "object (str)",
        "description": "Official granular bowling style classification.",
        "representation": "String (e.g., 'Right-Arm Fast', 'Slow Left-Arm Orthodox', 'Right-Arm Leg-Spin')",
        "formula": "Roster mapping / competition registration",
        "interpretation": "Raw bowling style from which archetypes are synthesized."
    },
    {
        "column_name": "batting_order",
        "category": "Player Profile",
        "data_type": "float64 / int64",
        "description": "Batting position of the striker in the team's lineup.",
        "representation": "Integer 1 to 11",
        "formula": "Player's entry index in team innings",
        "interpretation": "1-3: Top Order, 4-7: Middle Order, 8-11: Lower Order / Tail."
    },
    {
        "column_name": "runs",
        "category": "Ball Outcome",
        "data_type": "int64",
        "description": "Runs scored directly off the bat by the striker on this delivery.",
        "representation": "Integer 0, 1, 2, 3, 4, 5, 6",
        "formula": "Direct bat runs recorded in scorebook",
        "interpretation": "Counts toward batter's individual score and strike rate."
    },
    {
        "column_name": "is_four",
        "category": "Ball Outcome",
        "data_type": "bool / int",
        "description": "Flag indicating if the delivery resulted in a boundary four.",
        "representation": "Boolean (True / False) or 1 / 0",
        "formula": "runs == 4",
        "interpretation": "Ground boundary struck off the bat."
    },
    {
        "column_name": "is_six",
        "category": "Ball Outcome",
        "data_type": "bool / int",
        "description": "Flag indicating if the delivery resulted in an over-the-rope six.",
        "representation": "Boolean (True / False) or 1 / 0",
        "formula": "runs == 6",
        "interpretation": "Aerial maximum boundary struck off the bat."
    },
    {
        "column_name": "is_wicket",
        "category": "Ball Outcome",
        "data_type": "bool / int",
        "description": "Flag indicating if any dismissal occurred on the delivery.",
        "representation": "Boolean (True / False) or 1 / 0",
        "formula": "dismissal_type is not null",
        "interpretation": "Includes all dismissal types (bowler-credited and runouts)."
    },
    {
        "column_name": "dismissal_type_id",
        "category": "Ball Outcome",
        "data_type": "float64",
        "description": "Categorical code representing the mode of dismissal.",
        "representation": "Numeric code",
        "formula": "Database dismissal lookup ID",
        "interpretation": "Maps to dismissal_type strings."
    },
    {
        "column_name": "dismissal_type",
        "category": "Ball Outcome",
        "data_type": "object (str)",
        "description": "Text description of the mode of dismissal.",
        "representation": "String: 'Caught', 'Bowled', 'LBW', 'RunOut', 'Stumped', 'Caught and Bowled'",
        "formula": "Scorebook recorded dismissal mode",
        "interpretation": "Used to classify bowler wickets vs non-bowler dismissals."
    },
    {
        "column_name": "dismissed_player_id",
        "category": "Ball Outcome",
        "data_type": "int64",
        "description": "Player ID of the batsman dismissed on this delivery.",
        "representation": "Player ID integer",
        "formula": "ID of player who lost wicket",
        "interpretation": "Identifies if the dismissed batsman was the striker or non-striker."
    },
    {
        "column_name": "extras_type",
        "category": "Ball Outcome",
        "data_type": "object (str)",
        "description": "Classification of extra conceded on the delivery, if any.",
        "representation": "String: 'wide', 'Overstep' (no-ball), 'byes', 'legbyes', 'Penalty', or NaN",
        "formula": "Delivery extras classification",
        "interpretation": "Determines legality and bowler run debit."
    },
    {
        "column_name": "extras1_runs",
        "category": "Ball Outcome",
        "data_type": "int64",
        "description": "Primary penalty runs awarded for an extra (e.g., 1 for wide / no-ball).",
        "representation": "Integer: 0, 1 (cleaned from corrupt 6s in raw files)",
        "formula": "1 if wide/no-ball/byes/legbyes else 0",
        "interpretation": "Standard penalty for illegal or unassisted deliveries."
    },
    {
        "column_name": "extras_2_runs",
        "category": "Ball Outcome",
        "data_type": "float64",
        "description": "Additional runs taken on top of an extra (e.g. running 2 on a wide).",
        "representation": "Float / Integer: 0, 1, 2, 4",
        "formula": "Additional runs completed during an extra event",
        "interpretation": "Added to total team runs conceded."
    },
    {
        "column_name": "pace_or_spin",
        "category": "Player Profile",
        "data_type": "object (str)",
        "description": "Binary broad classification of bowling discipline.",
        "representation": "Categorical: 'Pace' or 'Spin'",
        "formula": "'Spin' if bowling_category contains 'Spin' or 'Slow' else 'Pace'",
        "interpretation": "Primary tactical split for batter and bowler effectiveness."
    },
    {
        "column_name": "bowl_speed",
        "category": "Optical Tracking (HawkEye)",
        "data_type": "float64",
        "description": "Delivery release speed measured at bowler's hand by HawkEye tracking.",
        "representation": "Continuous: km/h (e.g., 148.5, 92.4; NaN in historical Cricsheet)",
        "formula": "Radar/Optical tracking speed at release",
        "interpretation": "Evaluates speed thresholds (e.g., express pace > 145 km/h)."
    },
    {
        "column_name": "stroke",
        "category": "Optical Tracking (HawkEye)",
        "data_type": "object (str)",
        "description": "Biomechanical classification of the shot played by the batter.",
        "representation": "String: 'Cover Drive', 'Pull', 'Sweep', 'Defensive', 'Flick', etc.",
        "formula": "Optical tracking trajectory classification",
        "interpretation": "Pinpoints tactical vulnerabilities and strengths against specific lengths."
    },
    {
        "column_name": "delivery_style",
        "category": "Optical Tracking (HawkEye)",
        "data_type": "object (str)",
        "description": "Pitch trajectory variation executed by the bowler.",
        "representation": "String: 'Yorker', 'Bouncer', 'Slower Ball', 'Good Length', 'Full Toss'",
        "formula": "Tracking pitch coordinate and trajectory classification",
        "interpretation": "Critical for death bowling execution and tactical setup."
    },
    {
        "column_name": "over_or_around",
        "category": "Player Profile",
        "data_type": "object (str)",
        "description": "Angle of bowler's approach relative to the stumps.",
        "representation": "Categorical: 'Over the wicket' or 'Around the wicket'",
        "formula": "Bowler delivery side tracking",
        "interpretation": "Crucial angle tactic (e.g. left-arm pace angling into RHB)."
    },
    {
        "column_name": "on_or_off",
        "category": "Optical Tracking (HawkEye)",
        "data_type": "object (str)",
        "description": "Ground sector of ball travel off the bat (Wagon Wheel).",
        "representation": "Categorical: 'Offside', 'Onside', or 'Behind'",
        "formula": "Ground projection angle from pitch centre",
        "interpretation": "Evaluates scoring distribution and field setting efficiency."
    },
    {
        "column_name": "delivery_ist_time",
        "category": "Metadata & Identifiers",
        "data_type": "object (str)",
        "description": "Real-time timestamp when ball was bowled in Indian Standard Time (IST).",
        "representation": "Timestamp string: 'YYYY-MM-DD HH:MM:SS'",
        "formula": "Official match clock recording",
        "interpretation": "Chronological ordering and over-rate analysis."
    },
    {
        "column_name": "win_team_id",
        "category": "Metadata & Identifiers",
        "data_type": "float64 / int64",
        "description": "Team ID of the side that ultimately won the match.",
        "representation": "Team ID integer",
        "formula": "Result recorded in matches table",
        "interpretation": "Ground truth label for Win Probability model training."
    },
    {
        "column_name": "revised_target",
        "category": "Match State",
        "data_type": "float64",
        "description": "Target score revised via DLS (Duckworth-Lewis-Stern) or VJD method.",
        "representation": "Target score integer/float (e.g., 171.0; NaN if full match)",
        "formula": "Official match referee revised score",
        "interpretation": "Ensures accurate RRR calculation during rain-shortened fixtures."
    },
    {
        "column_name": "second_inn_revised_overs",
        "category": "Match State",
        "data_type": "float64",
        "description": "Total overs allocated to 2nd innings in curtailed matches.",
        "representation": "Overs float (e.g., 15.0, 12.0; NaN if standard 20 overs)",
        "formula": "Official revised over quota",
        "interpretation": "Sets total balls budget for innings 2 state calculation."
    },
    {
        "column_name": "knock_out",
        "category": "Tournament Context",
        "data_type": "int64",
        "description": "Binary flag indicating high-stakes playoff or knockout encounter.",
        "representation": "1 = Knockout / Playoff, 0 = Group / League match",
        "formula": "1 if stage in ['Final', 'Qualifier', 'Eliminator', 'Semi Final'] else 0",
        "interpretation": "Applies official 1.12x tournament multiplier to Pressure Index."
    },
    {
        "column_name": "stage",
        "category": "Tournament Context",
        "data_type": "object (str)",
        "description": "Tournament phase descriptor.",
        "representation": "String: 'League', 'Qualifier 1', 'Qualifier 2', 'Eliminator', 'Final'",
        "formula": "Tournament schedule descriptor",
        "interpretation": "Identifies title-deciding and knockout games."
    },
    {
        "column_name": "match_format",
        "category": "Tournament Context",
        "data_type": "object (str)",
        "description": "Format category of the fixture.",
        "representation": "Categorical: 'IPL', 'T20', or 'T20I'",
        "formula": "Competition metadata format",
        "interpretation": "Enables global format filtering in the intelligence platform."
    },
    {
        "column_name": "comp_name",
        "category": "Tournament Context",
        "data_type": "object (str)",
        "description": "Official title of the tournament.",
        "representation": "String: 'IPL 2024', 'IPL 2026', 'ICC Men's T20 World Cup 2024'",
        "formula": "Competition name lookup",
        "interpretation": "Delineates specific tournaments and seasons."
    },
    {
        "column_name": "match_date",
        "category": "Metadata & Identifiers",
        "data_type": "object (str)",
        "description": "Calendar date on which the match commenced.",
        "representation": "ISO-8601 Date string: 'YYYY-MM-DD'",
        "formula": "Match calendar date",
        "interpretation": "Temporal sorting and historical trajectory tracking."
    },
    {
        "column_name": "ball_runs",
        "category": "Engineered Match State",
        "data_type": "int64",
        "description": "Total runs credited to the batting team on this delivery.",
        "representation": "Integer: 0 to 7+ (bat runs + all extras)",
        "formula": "runs + extras_2_runs + (1 if wide/no-ball/byes/legbyes else 0)",
        "interpretation": "Accurately represents team scoreboard movement on the ball."
    },
    {
        "column_name": "is_legal",
        "category": "Engineered Match State",
        "data_type": "bool",
        "description": "Boolean flag indicating if the delivery counted toward the 6-ball over.",
        "representation": "True = Legal ball, False = Illegal extra (wide or no-ball)",
        "formula": "extras_type not in ['wide', 'Overstep']",
        "interpretation": "Drives balls_rem, bowler economy, and legal ball count."
    },
    {
        "column_name": "is_batter_ball",
        "category": "Engineered Match State",
        "data_type": "bool",
        "description": "Boolean flag indicating if the delivery is credited to batter balls faced.",
        "representation": "True = Batter faced ball, False = Wide delivery",
        "formula": "extras_type != 'wide'",
        "interpretation": "Includes no-balls (which batter faces) but excludes wides."
    },
    {
        "column_name": "is_bowler_wkt",
        "category": "Engineered Match State",
        "data_type": "bool",
        "description": "Boolean flag indicating if dismissal is debited to bowler's figures.",
        "representation": "True = Bowler wicket, False = RunOut / Retired Out / Obstructing",
        "formula": "is_wicket and dismissal_type not in ['RunOut', 'Retire Out', 'Obstructing']",
        "interpretation": "Core variable for bowler bowling average and strike rate."
    },
    {
        "column_name": "bowler_runs",
        "category": "Engineered Match State",
        "data_type": "int64",
        "description": "Runs debited against the bowler's individual bowling figures.",
        "representation": "Integer: 0 to 6+ (excludes byes and legbyes)",
        "formula": "0 if extras_type in ['byes', 'legbyes'] else ball_runs",
        "interpretation": "Ensures fielding byes/legbyes do not unfairly penalize bowler."
    },
    {
        "column_name": "is_striker_out",
        "category": "Engineered Match State",
        "data_type": "bool",
        "description": "Boolean flag indicating if the facing striker lost their wicket.",
        "representation": "True = Striker dismissed, False = Striker survived",
        "formula": "is_wicket and (dismissed_player_id == striker_id)",
        "interpretation": "Core variable for batter batting average and survival under pressure."
    },
    {
        "column_name": "inn1_total",
        "category": "Engineered Match State",
        "data_type": "float64",
        "description": "Total runs scored by Team 1 in the completed first innings.",
        "representation": "Score integer (e.g., 185.0, 224.0)",
        "formula": "sum(ball_runs) for innings == 1 in match",
        "interpretation": "Baseline score defining the second innings target."
    },
    {
        "column_name": "target",
        "category": "Engineered Match State",
        "data_type": "float64",
        "description": "Target runs required by chasing side to win the match.",
        "representation": "Score integer (e.g., 186.0)",
        "formula": "revised_target if not null else (inn1_total + 1)",
        "interpretation": "Goalpost for all Innings 2 chase equations."
    },
    {
        "column_name": "cum_runs",
        "category": "Engineered Match State",
        "data_type": "int64",
        "description": "Cumulative team runs scored prior to the release of this delivery.",
        "representation": "Score integer (0 to 280+)",
        "formula": "cumsum(ball_runs) - ball_runs within match & innings",
        "interpretation": "Pre-delivery match state before event outcome."
    },
    {
        "column_name": "cum_wkts",
        "category": "Engineered Match State",
        "data_type": "int64",
        "description": "Cumulative wickets lost by batting team prior to this delivery.",
        "representation": "Integer 0 to 9",
        "formula": "cumsum(is_wicket) - is_wicket within match & innings",
        "interpretation": "Measures wicket depletion and collapse state."
    },
    {
        "column_name": "legal_balls",
        "category": "Engineered Match State",
        "data_type": "int64",
        "description": "Cumulative legal deliveries bowled in innings prior to this ball.",
        "representation": "Integer 0 to 119",
        "formula": "cumsum(is_legal) - is_legal within match & innings",
        "interpretation": "Denominator for Current Run Rate (CRR)."
    },
    {
        "column_name": "balls_rem",
        "category": "Engineered Match State",
        "data_type": "int64",
        "description": "Number of legal deliveries remaining in the innings before this ball.",
        "representation": "Integer: 1 to 120 (clamped to min 1 to prevent division by zero)",
        "formula": "max(1, total_balls - legal_balls)",
        "interpretation": "Resource constraint for Required Run Rate (RRR)."
    },
    {
        "column_name": "wkts_in_hand",
        "category": "Engineered Match State",
        "data_type": "int64",
        "description": "Batting resources remaining before this delivery.",
        "representation": "Integer: 1 to 10",
        "formula": "max(0, 10 - cum_wkts)",
        "interpretation": "Remaining wickets buffer for the batting team."
    },
    {
        "column_name": "runs_req",
        "category": "Engineered Match State",
        "data_type": "float64",
        "description": "Runs required by chasing team to win prior to this delivery.",
        "representation": "Integer / float: 0 to 280+",
        "formula": "max(0, target - cum_runs)",
        "interpretation": "Remaining deficit in Innings 2 chase."
    },
    {
        "column_name": "rrr",
        "category": "Engineered Match State",
        "data_type": "float64",
        "description": "Required Run Rate per 6 legal balls prior to this delivery.",
        "representation": "Runs/over float (e.g. 9.45, 14.20)",
        "formula": "(runs_req / balls_rem) * 6.0",
        "interpretation": "Measures scoring urgency; RRR > 10.0 exerts severe pressure."
    },
    {
        "column_name": "crr",
        "category": "Engineered Match State",
        "data_type": "float64",
        "description": "Current Run Rate scored by batting side so far in innings.",
        "representation": "Runs/over float (e.g., 8.25)",
        "formula": "(cum_runs / max(1, legal_balls)) * 6.0",
        "interpretation": "Pace of scoring achieved to date."
    },
    {
        "column_name": "chase_win",
        "category": "Engineered Match State",
        "data_type": "int64",
        "description": "Binary ground-truth result: 1 if chasing team won, 0 otherwise.",
        "representation": "1 = Chasing team won, 0 = Defending team won",
        "formula": "1 if batting_team == win_team else 0",
        "interpretation": "Target label used to fit the Logistic Win Probability model."
    },
    {
        "column_name": "wp",
        "category": "Engineered Pressure Metric",
        "data_type": "float64",
        "description": "Chasing team Win Probability estimated prior to this delivery.",
        "representation": "Probability float in [0.0, 1.0]",
        "formula": "LogisticRegression(runs_req, balls_rem, wkts_in_hand, rrr)",
        "interpretation": "0.50 = Dead-even match; 0.95 = Near-certain victory; 0.05 = Imminent defeat."
    },
    {
        "column_name": "pressure_index",
        "category": "Engineered Pressure Metric",
        "data_type": "float64",
        "description": "Continuous ball-by-ball Pressure Index synthesizing LI, RRR, wickets, phase, and stage.",
        "representation": "Continuous index in [0.0, 1.0]",
        "formula": "Composite formula based on innings, LI, RRR stress, collapse, & KO multiplier",
        "interpretation": "PI >= 0.60 denotes High Pressure; isolates the top 24.3% highest-stress moments."
    },
    {
        "column_name": "is_high_pressure",
        "category": "Engineered Pressure Metric",
        "data_type": "bool",
        "description": "Indicator flag for deliveries meeting the high-pressure threshold.",
        "representation": "True if pressure_index >= 0.60 else False",
        "formula": "pressure_index >= 0.60",
        "interpretation": "Core filter used to isolate pressure metrics for rankings."
    },
    {
        "column_name": "is_moderate_pressure",
        "category": "Engineered Pressure Metric",
        "data_type": "bool",
        "description": "Indicator flag for deliveries in moderate stress conditions.",
        "representation": "True if 0.40 <= pressure_index < 0.60 else False",
        "formula": "0.40 <= pressure_index < 0.60",
        "interpretation": "Standard match rhythm with moderate consequences."
    },
    {
        "column_name": "is_low_pressure",
        "category": "Engineered Pressure Metric",
        "data_type": "bool",
        "description": "Indicator flag for low-stress or blowout deliveries.",
        "representation": "True if pressure_index < 0.40 else False",
        "formula": "pressure_index < 0.40",
        "interpretation": "Low leverage (e.g. 5 runs needed off 40 balls with 9 wickets in hand)."
    },
    {
        "column_name": "exp_bowl_runs",
        "category": "Phase Expected Runs",
        "data_type": "float64",
        "description": "Historical expected runs conceded by a bowler in this exact innings and over.",
        "representation": "Runs float (e.g., 1.15 in over 19, 0.72 in over 3)",
        "formula": "mean(bowler_runs) grouped by (innings, overid) across dataset",
        "interpretation": "Phase par baseline for bowler evaluation."
    },
    {
        "column_name": "exp_bat_runs",
        "category": "Phase Expected Runs",
        "data_type": "float64",
        "description": "Historical expected runs scored by a batter in this exact innings and over.",
        "representation": "Runs float (e.g., 1.58 in over 20, 1.05 in over 5)",
        "formula": "mean(runs) grouped by (innings, overid) across dataset",
        "interpretation": "Phase par baseline for batter evaluation."
    },
    {
        "column_name": "runs_saved",
        "category": "Phase Expected Runs",
        "data_type": "float64",
        "description": "Runs saved by the bowler relative to phase par on this delivery.",
        "representation": "Runs float: Positive = Good bowling; Negative = Expensive ball",
        "formula": "exp_bowl_runs - bowler_runs (for legal balls)",
        "interpretation": "A dot in the 20th over (exp=1.80) yields +1.80 runs saved."
    },
    {
        "column_name": "runs_added",
        "category": "Phase Expected Runs",
        "data_type": "float64",
        "description": "Net runs generated by the batter above phase par on this delivery.",
        "representation": "Runs float: Positive = Value added; Negative = Below par",
        "formula": "runs - exp_bat_runs (for batter-faced balls)",
        "interpretation": "A six in the 19th over (exp=1.65) yields +4.35 runs added."
    },
    {
        "column_name": "phase",
        "category": "Tactical Phase",
        "data_type": "object (str)",
        "description": "Match phase categorization based on over sequence.",
        "representation": "Categorical: 'Powerplay (1-6)', 'Middle (7-15)', or 'Death (16-20)'",
        "formula": "Powerplay if overid <= 6 else (Middle if overid <= 15 else Death)",
        "interpretation": "Field restrictions and strategic intent differ across these 3 phases."
    },
    {
        "column_name": "bowling_category",
        "category": "Player Profile",
        "data_type": "object (str)",
        "description": "Synthesized tactical bowling archetype.",
        "representation": "Categorical: 'Right-Arm Pace', 'Left-Arm Pace', 'Right-Arm Leg-Spin', 'Right-Arm Off-Spin', 'Slow Left-Arm Orthodox', 'Left-Arm Wrist-Spin'",
        "formula": "Rule-based synthesis from bowling_type string",
        "interpretation": "Used to generate the Bowling Archetypes Matrix and simulate matchups."
    },
    {
        "column_name": "pressure_tier",
        "category": "Engineered Pressure Metric",
        "data_type": "object (str)",
        "description": "Categorical label of stress level for user display.",
        "representation": "String: 'High Pressure', 'Moderate Pressure', 'Low Pressure'",
        "formula": "High if PI >= 0.60 else (Moderate if PI >= 0.40 else Low)",
        "interpretation": "Used for quick visual filtering and report generation."
    }
]


# ==============================================================================
# 2. BATTING METRICS GLOSSARY (37 COLUMNS)
# ==============================================================================
BATTING_COLUMNS_INFO = [
    {
        "column_name": "striker_id",
        "display_name": "Striker ID",
        "category": "Identifiers",
        "data_type": "int64",
        "formula": "Primary key from player registry",
        "interpretation": "Unique numeric player identifier."
    },
    {
        "column_name": "striker_name",
        "display_name": "Player Name",
        "category": "Identifiers",
        "data_type": "object (str)",
        "formula": "Standardized clean player name",
        "interpretation": "Batter's full official display name."
    },
    {
        "column_name": "balls_base",
        "display_name": "Base Balls Faced",
        "category": "Baseline Volume",
        "data_type": "int64",
        "formula": "count(runs) for all balls faced",
        "interpretation": "Total volume of balls faced across all match situations."
    },
    {
        "column_name": "runs_base",
        "display_name": "Base Runs",
        "category": "Baseline Volume",
        "data_type": "int64",
        "formula": "sum(runs) across all balls faced",
        "interpretation": "Total career runs scored off the bat."
    },
    {
        "column_name": "dismissals_base",
        "display_name": "Base Outs",
        "category": "Baseline Volume",
        "data_type": "int64",
        "formula": "sum(is_striker_out) across all deliveries",
        "interpretation": "Total times the batsman was dismissed."
    },
    {
        "column_name": "dots_base",
        "display_name": "Base Dot Balls",
        "category": "Baseline Volume",
        "data_type": "int64",
        "formula": "sum(runs == 0) across all balls faced",
        "interpretation": "Total deliveries faced scoring zero runs."
    },
    {
        "column_name": "fours_base",
        "display_name": "Base Fours",
        "category": "Baseline Volume",
        "data_type": "int64",
        "formula": "sum(is_four) across all balls faced",
        "interpretation": "Total boundary fours hit in baseline sample."
    },
    {
        "column_name": "sixes_base",
        "display_name": "Base Sixes",
        "category": "Baseline Volume",
        "data_type": "int64",
        "formula": "sum(is_six) across all balls faced",
        "interpretation": "Total over-the-rope sixes hit in baseline sample."
    },
    {
        "column_name": "matches_base",
        "display_name": "Base Matches",
        "category": "Baseline Volume",
        "data_type": "int64",
        "formula": "nunique(match_id) where batter faced >= 1 ball",
        "interpretation": "Total games batted in."
    },
    {
        "column_name": "balls_hp",
        "display_name": "HP Balls Faced",
        "category": "High Pressure Volume",
        "data_type": "int64",
        "formula": "count(runs) where PI >= 0.60",
        "interpretation": "Deliveries faced in high-stress crisis/clutch situations. Qualification requires >= 120 (2022-26) or >= 150 (IPL all-time)."
    },
    {
        "column_name": "runs_hp",
        "display_name": "HP Runs",
        "category": "High Pressure Volume",
        "data_type": "int64",
        "formula": "sum(runs) where PI >= 0.60",
        "interpretation": "Total runs scored under high pressure."
    },
    {
        "column_name": "runs_added_hp",
        "display_name": "HP Runs Added (Total)",
        "category": "Phase-Adjusted Impact",
        "data_type": "float64",
        "formula": "sum(runs_added) where PI >= 0.60",
        "interpretation": "Cumulative runs contributed strictly above phase-expected par."
    },
    {
        "column_name": "dismissals_hp",
        "display_name": "HP Dismissals",
        "category": "High Pressure Volume",
        "data_type": "int64",
        "formula": "sum(is_striker_out) where PI >= 0.60",
        "interpretation": "Times dismissed in high pressure situations."
    },
    {
        "column_name": "dots_hp",
        "display_name": "HP Dot Balls",
        "category": "High Pressure Volume",
        "data_type": "int64",
        "formula": "sum(runs == 0) where PI >= 0.60",
        "interpretation": "Unproductive deliveries faced under pressure."
    },
    {
        "column_name": "fours_hp",
        "display_name": "HP Fours",
        "category": "High Pressure Volume",
        "data_type": "int64",
        "formula": "sum(is_four) where PI >= 0.60",
        "interpretation": "Fours hit when pressure index >= 0.60."
    },
    {
        "column_name": "sixes_hp",
        "display_name": "HP Sixes",
        "category": "High Pressure Volume",
        "data_type": "int64",
        "formula": "sum(is_six) where PI >= 0.60",
        "interpretation": "Maximums struck under high pressure."
    },
    {
        "column_name": "matches_hp",
        "display_name": "HP Matches",
        "category": "High Pressure Volume",
        "data_type": "int64",
        "formula": "nunique(match_id) where batter faced PI >= 0.60 balls",
        "interpretation": "Breadth of matches with high-pressure exposure."
    },
    {
        "column_name": "sr_base",
        "display_name": "Base Strike Rate",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "(runs_base / balls_base) * 100.0",
        "interpretation": "Overall scoring rate under all match conditions (T20 par ~ 135-140)."
    },
    {
        "column_name": "sr_hp",
        "display_name": "High-Pressure Strike Rate",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "(runs_hp / balls_hp) * 100.0",
        "interpretation": "Scoring velocity strictly during clutch moments (e.g. Klaasen 187.3, Surya 172.5)."
    },
    {
        "column_name": "avg_base",
        "display_name": "Base Batting Average",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "runs_base / max(1, dismissals_base)",
        "interpretation": "Career runs per dismissal across all situations."
    },
    {
        "column_name": "avg_hp",
        "display_name": "High-Pressure Batting Average",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "runs_hp / max(1, dismissals_hp)",
        "interpretation": "Runs per dismissal under clutch conditions (e.g. Tim David 41.5, Surya 41.9)."
    },
    {
        "column_name": "bnd_pct_base",
        "display_name": "Base Boundary %",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "((fours_base + sixes_base) / balls_base) * 100.0",
        "interpretation": "Percentage of deliveries converted into boundaries."
    },
    {
        "column_name": "bnd_pct_hp",
        "display_name": "HP Boundary %",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "((fours_hp + sixes_hp) / balls_hp) * 100.0",
        "interpretation": "Boundary percentage under pressure (Elite finishers exceed 22%)."
    },
    {
        "column_name": "dot_pct_base",
        "display_name": "Base Dot Ball %",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "(dots_base / balls_base) * 100.0",
        "interpretation": "Baseline proportion of balls where 0 runs were scored."
    },
    {
        "column_name": "dot_pct_hp",
        "display_name": "HP Dot Ball %",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "(dots_hp / balls_hp) * 100.0",
        "interpretation": "Dot ball percentage under high pressure. Lower is better."
    },
    {
        "column_name": "delta_sr",
        "display_name": "Clutch Strike Rate Elevation (Δ SR)",
        "category": "Clutch Differentials",
        "data_type": "float64",
        "formula": "sr_hp - sr_base",
        "interpretation": "Key metric: positive values demonstrate batter accelerates when the game is on the line."
    },
    {
        "column_name": "delta_avg",
        "display_name": "Clutch Average Differential (Δ Avg)",
        "category": "Clutch Differentials",
        "data_type": "float64",
        "formula": "avg_hp - avg_base",
        "interpretation": "Positive indicates player prices their wicket higher in pressure situations."
    },
    {
        "column_name": "delta_dot_pct",
        "display_name": "Dot Ball Reduction under Pressure",
        "category": "Clutch Differentials",
        "data_type": "float64",
        "formula": "dot_pct_base - dot_pct_hp",
        "interpretation": "Positive indicates the batter cuts out dot balls in high-stress situations."
    },
    {
        "column_name": "delta_bnd_pct",
        "display_name": "Boundary Rate Elevation",
        "category": "Clutch Differentials",
        "data_type": "float64",
        "formula": "bnd_pct_hp - bnd_pct_base",
        "interpretation": "Elevation in boundary finding ability under pressure."
    },
    {
        "column_name": "runs_added_per_100",
        "display_name": "Phase-Adjusted Runs Added / 100 Balls",
        "category": "Phase-Adjusted Impact",
        "data_type": "float64",
        "formula": "(runs_added_hp / balls_hp) * 100.0",
        "interpretation": "Expected runs contributed above phase-par per 100 balls. Directly normalizes death vs middle phase."
    },
    {
        "column_name": "sr_bayes",
        "display_name": "Bayesian Shrunk Strike Rate",
        "category": "Empirical Bayes",
        "data_type": "float64",
        "formula": "(balls_hp * sr_hp + M * mu_sr) / (balls_hp + M) [M=60, mu=142.42]",
        "interpretation": "Shrinks small samples toward population mean; prevents noisy outliers from topping rankings."
    },
    {
        "column_name": "avg_bayes",
        "display_name": "Bayesian Shrunk Average",
        "category": "Empirical Bayes",
        "data_type": "float64",
        "formula": "(dismissals_hp * avg_hp + K * mu_avg) / (dismissals_hp + K) [K=4, mu=21.52]",
        "interpretation": "Stabilizes batting average against extreme small-dismissal spikes."
    },
    {
        "column_name": "cons_rate",
        "display_name": "Match Consistency Rate (CR)",
        "category": "Reliability & Consistency",
        "data_type": "float64",
        "formula": "mean(positive_impact) across innings with >= 5 HP balls faced",
        "interpretation": "Percentage of high-pressure games where batter achieved positive runs added or SR >= 135 (0.0 to 1.0)."
    },
    {
        "column_name": "meaningful_hp_innings",
        "display_name": "Meaningful HP Innings",
        "category": "Reliability & Consistency",
        "data_type": "int64",
        "formula": "count of matches where player faced >= 5 HP balls",
        "interpretation": "Sample size of match-deciding innings analyzed for consistency."
    },
    {
        "column_name": "sample_conf",
        "display_name": "Sample Confidence Weight",
        "category": "Composite Weighting",
        "data_type": "float64",
        "formula": "1.0 - exp(-balls_hp / 150.0)",
        "interpretation": "Asymptotic penalty factor in [0, 1]. Smoothly penalizes fringe samples."
    },
    {
        "column_name": "pressure_rating",
        "display_name": "SupeRR Pressure Reliability Rating (PRR)",
        "category": "Composite Rating",
        "data_type": "float64",
        "formula": "50.0 + 22.0 * RawScore * sample_conf",
        "interpretation": "Final master score (0 to 100+). 50 = Average; > 70 = World-Class; > 80 = Elite Match-Winner."
    },
    {
        "column_name": "rank",
        "display_name": "Official Tournament Rank",
        "category": "Composite Rating",
        "data_type": "int64",
        "formula": "Order by pressure_rating descending",
        "interpretation": "Official leaderboard rank among all qualified batters."
    }
]


# ==============================================================================
# 3. BOWLING METRICS GLOSSARY (35 COLUMNS)
# ==============================================================================
BOWLING_COLUMNS_INFO = [
    {
        "column_name": "bowler_id",
        "display_name": "Bowler ID",
        "category": "Identifiers",
        "data_type": "int64",
        "formula": "Primary key from player registry",
        "interpretation": "Unique numeric bowler identifier."
    },
    {
        "column_name": "bowler_name",
        "display_name": "Bowler Name",
        "category": "Identifiers",
        "data_type": "object (str)",
        "formula": "Standardized clean player name",
        "interpretation": "Bowler's full official display name."
    },
    {
        "column_name": "balls_base",
        "display_name": "Base Legal Balls",
        "category": "Baseline Volume",
        "data_type": "int64",
        "formula": "sum(is_legal) across all deliveries",
        "interpretation": "Total career legal balls delivered."
    },
    {
        "column_name": "runs_base",
        "display_name": "Base Runs Conceded",
        "category": "Baseline Volume",
        "data_type": "int64",
        "formula": "sum(bowler_runs) across all deliveries",
        "interpretation": "Total career runs charged to the bowler."
    },
    {
        "column_name": "wkts_base",
        "display_name": "Base Wickets",
        "category": "Baseline Volume",
        "data_type": "int64",
        "formula": "sum(is_bowler_wkt) across all deliveries",
        "interpretation": "Total career wickets credited to the bowler."
    },
    {
        "column_name": "dots_base",
        "display_name": "Base Dot Balls",
        "category": "Baseline Volume",
        "data_type": "int64",
        "formula": "sum(ball_runs == 0) across all deliveries",
        "interpretation": "Total dot deliveries bowled across all situations."
    },
    {
        "column_name": "boundaries_base",
        "display_name": "Base Boundaries Conceded",
        "category": "Baseline Volume",
        "data_type": "int64",
        "formula": "sum(ball_runs >= 4) across all deliveries",
        "interpretation": "Total fours and sixes conceded in baseline sample."
    },
    {
        "column_name": "matches_base",
        "display_name": "Base Matches",
        "category": "Baseline Volume",
        "data_type": "int64",
        "formula": "nunique(match_id) where bowler bowled >= 1 ball",
        "interpretation": "Total career matches bowled in."
    },
    {
        "column_name": "balls_hp",
        "display_name": "HP Legal Balls",
        "category": "High Pressure Volume",
        "data_type": "int64",
        "formula": "sum(is_legal) where PI >= 0.60",
        "interpretation": "Legal deliveries bowled under high pressure. Minimum 150 required to qualify."
    },
    {
        "column_name": "runs_hp",
        "display_name": "HP Runs Conceded",
        "category": "High Pressure Volume",
        "data_type": "int64",
        "formula": "sum(bowler_runs) where PI >= 0.60",
        "interpretation": "Total runs conceded under high pressure."
    },
    {
        "column_name": "runs_saved_hp",
        "display_name": "HP Runs Saved (Total)",
        "category": "Phase-Adjusted Impact",
        "data_type": "float64",
        "formula": "sum(runs_saved) where PI >= 0.60",
        "interpretation": "Cumulative runs choked off relative to phase par under pressure."
    },
    {
        "column_name": "wkts_hp",
        "display_name": "HP Wickets",
        "category": "High Pressure Volume",
        "data_type": "int64",
        "formula": "sum(is_bowler_wkt) where PI >= 0.60",
        "interpretation": "Critical breakthrough wickets taken under pressure."
    },
    {
        "column_name": "dots_hp",
        "display_name": "HP Dot Balls",
        "category": "High Pressure Volume",
        "data_type": "int64",
        "formula": "sum(ball_runs == 0) where PI >= 0.60",
        "interpretation": "Pressure-building dot balls delivered in clutch situations."
    },
    {
        "column_name": "boundaries_hp",
        "display_name": "HP Boundaries Conceded",
        "category": "High Pressure Volume",
        "data_type": "int64",
        "formula": "sum(ball_runs >= 4) where PI >= 0.60",
        "interpretation": "Fours and sixes conceded when PI >= 0.60."
    },
    {
        "column_name": "matches_hp",
        "display_name": "HP Matches",
        "category": "High Pressure Volume",
        "data_type": "int64",
        "formula": "nunique(match_id) where bowler delivered PI >= 0.60 balls",
        "interpretation": "Number of high-pressure games bowled in."
    },
    {
        "column_name": "econ_base",
        "display_name": "Base Economy Rate",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "(runs_base / balls_base) * 6.0",
        "interpretation": "Career economy across all match situations."
    },
    {
        "column_name": "econ_hp",
        "display_name": "High-Pressure Economy Rate",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "(runs_hp / balls_hp) * 6.0",
        "interpretation": "Economy rate strictly during high pressure. Elite anchors keep this under 8.0."
    },
    {
        "column_name": "sr_base",
        "display_name": "Base Bowling Strike Rate",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "balls_base / max(1, wkts_base)",
        "interpretation": "Balls required to take a wicket across all match situations."
    },
    {
        "column_name": "sr_hp",
        "display_name": "High-Pressure Bowling Strike Rate",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "balls_hp / max(1, wkts_hp)",
        "interpretation": "Balls required per wicket in high-pressure situations."
    },
    {
        "column_name": "dot_pct_base",
        "display_name": "Base Dot Ball %",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "(dots_base / balls_base) * 100.0",
        "interpretation": "Percentage of deliveries resulting in zero runs across all situations."
    },
    {
        "column_name": "dot_pct_hp",
        "display_name": "HP Dot Ball %",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "(dots_hp / balls_hp) * 100.0",
        "interpretation": "Dot ball percentage under high pressure (Elite bowlers exceed 40%)."
    },
    {
        "column_name": "bnd_pct_base",
        "display_name": "Base Boundary % Conceded",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "(boundaries_base / balls_base) * 100.0",
        "interpretation": "Percentage of balls conceded for boundary fours or sixes."
    },
    {
        "column_name": "bnd_pct_hp",
        "display_name": "HP Boundary % Conceded",
        "category": "Rate Metrics",
        "data_type": "float64",
        "formula": "(boundaries_hp / balls_hp) * 100.0",
        "interpretation": "Boundary percentage conceded under pressure. Lower is better."
    },
    {
        "column_name": "delta_econ",
        "display_name": "Clutch Economy Suppression (Δ Econ)",
        "category": "Clutch Differentials",
        "data_type": "float64",
        "formula": "econ_base - econ_hp",
        "interpretation": "Key metric: positive values indicate bowler becomes STINGIER when the match is on the line."
    },
    {
        "column_name": "delta_sr",
        "display_name": "Clutch Strike Rate Acceleration (Δ SR)",
        "category": "Clutch Differentials",
        "data_type": "float64",
        "formula": "sr_base - sr_hp",
        "interpretation": "Positive indicates the bowler takes wickets FASTER in high-pressure situations."
    },
    {
        "column_name": "delta_dot_pct",
        "display_name": "Dot Ball Elevation under Pressure",
        "category": "Clutch Differentials",
        "data_type": "float64",
        "formula": "dot_pct_hp - dot_pct_base",
        "interpretation": "Positive shows bowler increases dot-ball frequency in clutch moments."
    },
    {
        "column_name": "delta_bnd_pct",
        "display_name": "Boundary Suppression under Pressure",
        "category": "Clutch Differentials",
        "data_type": "float64",
        "formula": "bnd_pct_base - bnd_pct_hp",
        "interpretation": "Positive shows bowler restricts boundaries better in clutch situations."
    },
    {
        "column_name": "runs_saved_per_over",
        "display_name": "Phase-Adjusted Runs Saved / Over",
        "category": "Phase-Adjusted Impact",
        "data_type": "float64",
        "formula": "runs_saved_hp / (balls_hp / 6.0)",
        "interpretation": "Expected runs saved per 6 balls relative to phase par (e.g. Sunil Narine +2.47)."
    },
    {
        "column_name": "econ_bayes",
        "display_name": "Bayesian Shrunk Economy Rate",
        "category": "Empirical Bayes",
        "data_type": "float64",
        "formula": "(balls_hp * econ_hp + M * mu_econ) / (balls_hp + M) [M=60, mu=8.89]",
        "interpretation": "Regularizes high-pressure economy rate toward population prior (8.89)."
    },
    {
        "column_name": "sr_bayes",
        "display_name": "Bayesian Shrunk Bowling SR",
        "category": "Empirical Bayes",
        "data_type": "float64",
        "formula": "(wkts_hp * sr_hp + K * mu_sr_bowl) / (wkts_hp + K) [K=4, mu=15.94]",
        "interpretation": "Regularizes bowling strike rate toward population prior (15.94)."
    },
    {
        "column_name": "cons_rate",
        "display_name": "Spell Consistency Rate (CR)",
        "category": "Reliability & Consistency",
        "data_type": "float64",
        "formula": "mean(positive_impact) across spells with >= 5 HP balls bowled",
        "interpretation": "Percentage of high-pressure spells where bowler saved positive runs or took >= 1 wkt at econ <= 8.5."
    },
    {
        "column_name": "meaningful_hp_spells",
        "display_name": "Meaningful HP Spells",
        "category": "Reliability & Consistency",
        "data_type": "int64",
        "formula": "count of matches where bowler delivered >= 5 HP balls",
        "interpretation": "Sample size of high-pressure match spells evaluated."
    },
    {
        "column_name": "sample_conf",
        "display_name": "Sample Confidence Weight",
        "category": "Composite Weighting",
        "data_type": "float64",
        "formula": "1.0 - exp(-balls_hp / 180.0)",
        "interpretation": "Asymptotic penalty factor in [0, 1]. Smoothly penalizes fringe samples."
    },
    {
        "column_name": "pressure_rating",
        "display_name": "SupeRR Pressure Reliability Rating (PRR)",
        "category": "Composite Rating",
        "data_type": "float64",
        "formula": "50.0 + 22.0 * RawScore * sample_conf",
        "interpretation": "Final master score (0 to 100). 50 = Average; > 70 = World-Class; > 80 = Legendary Finisher."
    },
    {
        "column_name": "rank",
        "display_name": "Official Tournament Rank",
        "category": "Composite Rating",
        "data_type": "int64",
        "formula": "Order by pressure_rating descending",
        "interpretation": "Official leaderboard rank among all qualified bowlers."
    }
]


def get_delivery_schema_df() -> pd.DataFrame:
    return pd.DataFrame(DELIVERY_COLUMNS_INFO)

def get_batting_metrics_df() -> pd.DataFrame:
    return pd.DataFrame(BATTING_COLUMNS_INFO)

def get_bowling_metrics_df() -> pd.DataFrame:
    return pd.DataFrame(BOWLING_COLUMNS_INFO)
