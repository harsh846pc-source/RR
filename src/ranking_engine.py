"""
src/ranking_engine.py
=====================
Ranks players based on composite Pressure Reliability Ratings (PRR),
applies eligibility cutoffs, and exports top-10 and full tables.
"""

import pandas as pd
import numpy as np


def rank_batters(bat_df: pd.DataFrame, min_hp_balls: int = 120) -> pd.DataFrame:
    """
    Computes composite Batter Pressure Reliability Rating (BPRR)
    and ranks eligible batters.
    """
    qual = bat_df[bat_df['balls_hp'] >= min_hp_balls].copy()

    # Standardized components
    z_runs_added = qual['runs_added_per_100'] / 15.0
    z_sr = (qual['sr_bayes'] - 142.42) / 18.0
    z_scoring = 0.60 * z_runs_added + 0.40 * z_sr
    
    z_avg = (qual['avg_bayes'] - 21.52) / 10.0
    z_delta_sr = qual['delta_sr'] / 15.0
    z_bnd_dot = (qual['bnd_pct_hp'] - 0.5 * qual['dot_pct_hp'] - 5.0) / 6.0
    z_cons = (qual['cons_rate'] - 0.50) / 0.12

    # Weighted Composite Raw Score scaled by Sample Confidence
    raw_score = (
        0.35 * z_scoring +
        0.25 * z_avg +
        0.15 * z_delta_sr +
        0.10 * z_bnd_dot +
        0.15 * z_cons
    ) * qual['sample_conf']

    # Rescaled to 0-100 index (50 = average pressure performer)
    qual['pressure_rating'] = 50.0 + raw_score * 22.0
    qual = qual.sort_values('pressure_rating', ascending=False).reset_index(drop=True)
    qual['rank'] = qual.index + 1

    return qual


def rank_bowlers(bowl_df: pd.DataFrame, min_hp_balls: int = 150) -> pd.DataFrame:
    """
    Computes composite Bowler Pressure Reliability Rating (BPRR)
    and ranks eligible bowlers.
    """
    qual = bowl_df[bowl_df['balls_hp'] >= min_hp_balls].copy()

    # Standardized components
    z_runs_saved = qual['runs_saved_per_over'] / 1.20
    z_econ = (8.89 - qual['econ_bayes']) / 1.20
    z_suppression = 0.60 * z_runs_saved + 0.40 * z_econ
    
    z_wkt = (15.94 - qual['sr_bayes']) / 4.0
    z_delta_econ = np.clip(qual['delta_econ'], -0.75, 2.0) / 1.0
    z_dot_bnd = (qual['dot_pct_hp'] - qual['bnd_pct_hp'] - 15.0) / 8.0
    z_cons = (qual['cons_rate'] - 0.50) / 0.12

    # Weighted Composite Raw Score scaled by Sample Confidence
    raw_score = (
        0.35 * z_suppression +
        0.25 * z_wkt +
        0.15 * z_delta_econ +
        0.10 * z_dot_bnd +
        0.15 * z_cons
    ) * qual['sample_conf']

    # Rescaled to 0-100 index (50 = average pressure performer)
    qual['pressure_rating'] = 50.0 + raw_score * 22.0
    qual = qual.sort_values('pressure_rating', ascending=False).reset_index(drop=True)
    qual['rank'] = qual.index + 1

    return qual
