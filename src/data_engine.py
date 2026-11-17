"""
src/data_engine.py
==================
Central analytical and data retrieval engine for the Cricket Matchup & Profile Intelligence System.
Loads, enriches, caches, and provides high-speed queries for player profiles, splits,
stroke tracking, delivery styles, head-to-head batter vs bowler matchups, and tactical simulations.
"""

import os
import pandas as pd
import numpy as np
from src.pressure_engine import load_and_enrich_match_data, load_and_enrich_ipl_history

PARQUET_2022_2026_PATH = "data/cricket_master_2022_2026.parquet"
PARQUET_IPL_ALL_PATH = "data/cricket_master_ipl_2008_2026.parquet"
PARQUET_CACHE_PATH = "data/cricket_master.parquet"


def categorize_bowling_type(btype: str) -> str:
    """Categorizes detailed bowling types into standard tactical archetypes."""
    if pd.isna(btype):
        return "Unknown"
    btype_lower = str(btype).lower()
    if "left-arm" in btype_lower and ("fast" in btype_lower or "medium" in btype_lower or "pace" in btype_lower):
        return "Left-Arm Pace"
    if "right-arm" in btype_lower and ("fast" in btype_lower or "medium" in btype_lower or "pace" in btype_lower):
        return "Right-Arm Pace"
    if "slow left-arm orthodox" in btype_lower:
        return "Slow Left-Arm Orthodox"
    if "left-arm" in btype_lower and ("wrist" in btype_lower or "unorthodox" in btype_lower or "chinaman" in btype_lower):
        return "Left-Arm Wrist-Spin"
    if "offbreak" in btype_lower or "off-break" in btype_lower or "off break" in btype_lower or "off-spin" in btype_lower:
        return "Right-Arm Off-Spin"
    if "leg-break" in btype_lower or "legbreak" in btype_lower or "leg break" in btype_lower or "leg-spin" in btype_lower or "googly" in btype_lower:
        return "Right-Arm Leg-Spin"
    if "spin" in btype_lower:
        return "Spin (Other)"
    return "Pace (Other)"


def build_and_cache_master_dataset(workspace_dir: str = ".", scope: str = "2022-2026") -> pd.DataFrame:
    """
    Enriches and caches the complete delivery-level dataset into an optimized Parquet file.
    Supports either '2022-2026' (official challenge dataset) or 'ipl_2008_2026' (Whole IPL history).
    """
    if "ipl" in scope.lower():
        print("Reconstructing and caching Whole IPL (2008-2026) master dataset...")
        bbb, wp_model = load_and_enrich_ipl_history(workspace_dir)
        target_path = PARQUET_IPL_ALL_PATH
    else:
        print("Reconstructing and caching 2022-2026 master cricket dataset...")
        bbb, wp_model = load_and_enrich_match_data(workspace_dir)
        # Apply official challenge filter: exclude non-IPL developmental tournaments (comp_id 2670 and 3289)
        if 'comp_id' in bbb.columns:
            bbb = bbb[~bbb['comp_id'].isin([2670, 3289])].copy()
        target_path = PARQUET_2022_2026_PATH

    # 1. Match phase categorization
    if 'phase' not in bbb.columns:
        bbb['phase'] = np.where(
            bbb['overid'] <= 6, 'Powerplay (1-6)',
            np.where(bbb['overid'] <= 15, 'Middle (7-15)', 'Death (16-20)')
        )

    # 2. Bowling archetype categorization
    if 'bowling_category' not in bbb.columns:
        bbb['bowling_category'] = bbb['bowling_type'].apply(categorize_bowling_type)

    # 3. Pressure tier
    if 'pressure_tier' not in bbb.columns:
        bbb['pressure_tier'] = np.where(
            bbb['pressure_index'] >= 0.60, 'High Pressure',
            np.where(bbb['pressure_index'] >= 0.40, 'Moderate Pressure', 'Low Pressure')
        )

    # 4. Fill stroke & delivery style missing values
    if 'stroke' not in bbb.columns:
        bbb['stroke'] = 'Unclassified'
    else:
        bbb['stroke'] = bbb['stroke'].fillna('Unclassified')

    if 'delivery_style' not in bbb.columns:
        bbb['delivery_style'] = 'Standard'
    else:
        bbb['delivery_style'] = bbb['delivery_style'].fillna('Standard')

    if 'on_or_off' not in bbb.columns:
        bbb['on_or_off'] = 'Unclassified'
    else:
        bbb['on_or_off'] = bbb['on_or_off'].fillna('Unclassified')

    # Save to Parquet
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    bbb.to_parquet(target_path, index=False, engine='pyarrow')
    if scope == "2022-2026":
        bbb.to_parquet(PARQUET_CACHE_PATH, index=False, engine='pyarrow')
    print(f"Master dataset successfully cached at: {target_path} ({len(bbb):,} rows)")
    return bbb


def _optimize_memory(df: pd.DataFrame) -> pd.DataFrame:
    """Downcasts low-cardinality string columns to category for 50% RAM reduction."""
    cat_cols = [
        'phase', 'bowling_category', 'pressure_tier', 'stroke', 'delivery_style',
        'on_or_off', 'over_or_around', 'batting_type', 'bowling_type', 'stage',
        'knock_out', 'match_format', 'extras_type', 'dismissal_type', 'comp_name'
    ]
    for c in cat_cols:
        if c in df.columns:
            df[c] = df[c].astype('category')
    return df


def get_master_data(workspace_dir: str = ".", scope: str = "2022-2026") -> pd.DataFrame:
    """Loads master dataset from cache, or builds it if missing."""
    if "ipl" in scope.lower():
        if os.path.exists(PARQUET_IPL_ALL_PATH):
            df = pd.read_parquet(PARQUET_IPL_ALL_PATH, engine='pyarrow')
        else:
            df = build_and_cache_master_dataset(workspace_dir, scope="ipl_2008_2026")
    else:
        if os.path.exists(PARQUET_2022_2026_PATH):
            df = pd.read_parquet(PARQUET_2022_2026_PATH, engine='pyarrow')
        elif os.path.exists(PARQUET_CACHE_PATH):
            df = pd.read_parquet(PARQUET_CACHE_PATH, engine='pyarrow')
        else:
            df = build_and_cache_master_dataset(workspace_dir, scope="2022-2026")
    return _optimize_memory(df)


class CricketIntelligenceEngine:
    """High-speed query interface for profiles, splits, and head-to-head matchups."""

    def __init__(self, workspace_dir: str = ".", scope: str = "2022-2026"):
        self.workspace_dir = workspace_dir
        self.scope = "ipl_2008_2026" if "ipl" in str(scope).lower() else "2022-2026"
        self.df = get_master_data(workspace_dir, scope=self.scope)
        self._init_player_registry()

    def _apply_format_filter(self, sub: pd.DataFrame, format_filter: str) -> pd.DataFrame:
        """Applies format filter flexibly across tournament designations."""
        if format_filter == "All" or len(sub) == 0:
            return sub
        if format_filter in ["IPL", "T20"]:
            return sub[sub['match_format'].isin(['IPL', 'T20']) | sub['comp_name'].str.contains('IPL', case=False, na=False)]
        return sub[sub['match_format'] == format_filter]

    def get_leaderboard_data(self) -> dict:
        """Loads the top 10 and qualified rankings for the active dataset scope."""
        if self.scope == "ipl_2008_2026":
            top_bat_p = "top_10_batters_under_pressure_ipl_2008_2026.csv"
            top_bowl_p = "top_10_bowlers_under_pressure_ipl_2008_2026.csv"
            all_bat_p = "all_qualified_batters_rankings_ipl_2008_2026.csv"
            all_bowl_p = "all_qualified_bowlers_rankings_ipl_2008_2026.csv"
        else:
            top_bat_p = "top_10_batters_under_pressure_2022_2026.csv" if os.path.exists("top_10_batters_under_pressure_2022_2026.csv") else "top_10_batters_under_pressure.csv"
            top_bowl_p = "top_10_bowlers_under_pressure_2022_2026.csv" if os.path.exists("top_10_bowlers_under_pressure_2022_2026.csv") else "top_10_bowlers_under_pressure.csv"
            all_bat_p = "all_qualified_batters_rankings_2022_2026.csv" if os.path.exists("all_qualified_batters_rankings_2022_2026.csv") else "all_qualified_batters_rankings.csv"
            all_bowl_p = "all_qualified_bowlers_rankings_2022_2026.csv" if os.path.exists("all_qualified_bowlers_rankings_2022_2026.csv") else "all_qualified_bowlers_rankings.csv"

        return {
            'top_bat': pd.read_csv(top_bat_p) if os.path.exists(top_bat_p) else pd.DataFrame(),
            'top_bowl': pd.read_csv(top_bowl_p) if os.path.exists(top_bowl_p) else pd.DataFrame(),
            'all_bat': pd.read_csv(all_bat_p) if os.path.exists(all_bat_p) else pd.DataFrame(),
            'all_bowl': pd.read_csv(all_bowl_p) if os.path.exists(all_bowl_p) else pd.DataFrame(),
            'paths': {
                'top_bat': top_bat_p,
                'top_bowl': top_bowl_p,
                'all_bat': all_bat_p,
                'all_bowl': all_bowl_p
            }
        }

    def _init_player_registry(self):
        """Initializes fast lookups of all active batters and bowlers."""
        # Batters
        bat_summary = self.df[self.df['is_batter_ball']].groupby(['striker_id', 'striker_name']).agg(
            balls_faced=('runs', 'count'),
            total_runs=('runs', 'sum'),
            hand=('batting_type', lambda s: s.dropna().iloc[0] if len(s.dropna()) > 0 else 'RHB')
        ).reset_index()

        # Bowlers
        bowl_summary = self.df.groupby(['bowler_id', 'bowler_name']).agg(
            balls_bowled=('is_legal', 'sum'),
            total_wkts=('is_bowler_wkt', 'sum'),
            style=('bowling_type', lambda s: s.dropna().iloc[0] if len(s.dropna()) > 0 else 'Unknown'),
            pace_or_spin=('pace_or_spin', lambda s: s.dropna().iloc[0] if len(s.dropna()) > 0 else 'Pace')
        ).reset_index()

        self.batters_dict = {
            row['striker_name']: {
                'id': row['striker_id'],
                'balls': row['balls_faced'],
                'runs': row['total_runs'],
                'hand': row['hand']
            }
            for _, row in bat_summary.iterrows()
        }

        self.bowlers_dict = {
            row['bowler_name']: {
                'id': row['bowler_id'],
                'balls': row['balls_bowled'],
                'wickets': row['total_wkts'],
                'style': row['style'],
                'pace_or_spin': row['pace_or_spin']
            }
            for _, row in bowl_summary.iterrows()
        }

        # Sorted player lists
        self.batter_names = sorted(list(self.batters_dict.keys()), key=lambda x: self.batters_dict[x]['runs'], reverse=True)
        self.bowler_names = sorted(list(self.bowlers_dict.keys()), key=lambda x: self.bowlers_dict[x]['wickets'], reverse=True)
        self.all_player_names = sorted(list(set(self.batter_names).union(set(self.bowler_names))))

    def get_batter_career(self, batter_name: str, format_filter: str = "All") -> dict:
        """Returns comprehensive career overview and KPI statistics for a batter."""
        sub = self.df[self.df['striker_name'] == batter_name]
        sub = self._apply_format_filter(sub, format_filter)

        sub_faced = sub[sub['is_batter_ball']]
        balls = len(sub_faced)
        runs = int(sub_faced['runs'].sum()) if balls > 0 else 0
        outs = int((sub_faced['is_wicket'] & (sub_faced['dismissed_player_id'] == sub_faced['striker_id'])).sum())
        dots = int((sub_faced['runs'] == 0).sum())
        fours = int(sub_faced['is_four'].sum())
        sixes = int(sub_faced['is_six'].sum())
        matches = int(sub['match_id'].nunique())
        innings = int(sub.groupby(['match_id', 'innings'])['runs'].count().count())

        inn_runs = sub.groupby(['match_id', 'innings'])['runs'].sum()
        fifties = int(((inn_runs >= 50) & (inn_runs < 100)).sum())
        hundreds = int((inn_runs >= 100).sum())
        highest = int(inn_runs.max()) if len(inn_runs) > 0 else 0

        sr = (runs / balls * 100.0) if balls > 0 else 0.0
        avg = (runs / outs) if outs > 0 else float(runs)
        dot_pct = (dots / balls * 100.0) if balls > 0 else 0.0
        bnd_pct = ((fours + sixes) / balls * 100.0) if balls > 0 else 0.0

        hand = sub['batting_type'].dropna().iloc[0] if len(sub['batting_type'].dropna()) > 0 else 'RHB'

        return {
            'player_name': batter_name,
            'hand': hand,
            'matches': matches,
            'innings': innings,
            'runs': runs,
            'balls': balls,
            'dismissals': outs,
            'highest_score': highest,
            'fifties': fifties,
            'hundreds': hundreds,
            'sr': round(sr, 1),
            'avg': round(avg, 1) if outs > 0 else f"{runs}*",
            'dots': dots,
            'dot_pct': round(dot_pct, 1),
            'fours': fours,
            'sixes': sixes,
            'bnd_pct': round(bnd_pct, 1)
        }

    def get_bowler_career(self, bowler_name: str, format_filter: str = "All") -> dict:
        """Returns comprehensive career overview and KPI statistics for a bowler."""
        sub = self.df[self.df['bowler_name'] == bowler_name]
        sub = self._apply_format_filter(sub, format_filter)

        legal_balls = int(sub['is_legal'].sum())
        runs_conceded = int(sub['bowler_runs'].sum())
        wkts = int(sub['is_bowler_wkt'].sum())
        dots = int((sub['ball_runs'] == 0).sum())
        boundaries = int((sub['ball_runs'] >= 4).sum())
        matches = int(sub['match_id'].nunique())
        spells = int(sub.groupby(['match_id', 'innings'])['is_legal'].count().count())

        econ = (runs_conceded / legal_balls * 6.0) if legal_balls > 0 else 0.0
        sr = (legal_balls / wkts) if wkts > 0 else 0.0
        avg = (runs_conceded / wkts) if wkts > 0 else 0.0
        dot_pct = (dots / len(sub) * 100.0) if len(sub) > 0 else 0.0
        bnd_pct = (boundaries / len(sub) * 100.0) if len(sub) > 0 else 0.0

        match_wkts = sub.groupby('match_id').agg(w=('is_bowler_wkt', 'sum'), r=('bowler_runs', 'sum'))
        best_str = "—"
        if len(match_wkts) > 0:
            best_row = match_wkts.sort_values(by=['w', 'r'], ascending=[False, True]).iloc[0]
            best_str = f"{int(best_row['w'])}/{int(best_row['r'])}"

        style = sub['bowling_type'].dropna().iloc[0] if len(sub['bowling_type'].dropna()) > 0 else 'Unknown'
        pace_or_spin = sub['pace_or_spin'].dropna().iloc[0] if len(sub['pace_or_spin'].dropna()) > 0 else 'Pace'

        return {
            'player_name': bowler_name,
            'style': style,
            'pace_or_spin': pace_or_spin,
            'matches': matches,
            'spells': spells,
            'overs': f"{legal_balls // 6}.{legal_balls % 6}",
            'legal_balls': legal_balls,
            'runs_conceded': runs_conceded,
            'wickets': wkts,
            'best_bowling': best_str,
            'econ': round(econ, 2),
            'sr': round(sr, 1) if wkts > 0 else '—',
            'avg': round(avg, 1) if wkts > 0 else '—',
            'dots': dots,
            'dot_pct': round(dot_pct, 1),
            'boundaries': boundaries,
            'bnd_pct': round(bnd_pct, 1)
        }

    def get_batter_splits(self, batter_name: str, split_by: str = "pace_or_spin", format_filter: str = "All") -> pd.DataFrame:
        """Computes split statistics for a batter."""
        sub = self.df[(self.df['striker_name'] == batter_name) & (self.df['is_batter_ball'])]
        sub = self._apply_format_filter(sub, format_filter)

        if len(sub) == 0:
            return pd.DataFrame()

        grp = sub.groupby(split_by).agg(
            balls=('runs', 'count'),
            runs=('runs', 'sum'),
            dismissals=('is_striker_out', 'sum'),
            dots=('runs', lambda s: (s == 0).sum()),
            fours=('is_four', 'sum'),
            sixes=('is_six', 'sum')
        ).reset_index()

        grp['sr'] = np.round((grp['runs'] / np.maximum(1, grp['balls'])) * 100.0, 1)
        grp['avg'] = np.where(grp['dismissals'] > 0, np.round(grp['runs'] / grp['dismissals'], 1), np.round(grp['runs'], 1))
        grp['dot_pct'] = np.round((grp['dots'] / np.maximum(1, grp['balls'])) * 100.0, 1)
        grp['bnd_pct'] = np.round(((grp['fours'] + grp['sixes']) / np.maximum(1, grp['balls'])) * 100.0, 1)
        return grp.sort_values('balls', ascending=False)

    def get_bowler_splits(self, bowler_name: str, split_by: str = "batting_type", format_filter: str = "All") -> pd.DataFrame:
        """Computes split statistics for a bowler."""
        sub = self.df[self.df['bowler_name'] == bowler_name]
        sub = self._apply_format_filter(sub, format_filter)

        if len(sub) == 0:
            return pd.DataFrame()

        grp = sub.groupby(split_by).agg(
            legal_balls=('is_legal', 'sum'),
            runs_conceded=('bowler_runs', 'sum'),
            wickets=('is_bowler_wkt', 'sum'),
            dots=('ball_runs', lambda s: (s == 0).sum()),
            boundaries=('ball_runs', lambda s: (s >= 4).sum())
        ).reset_index()

        grp['econ'] = np.round((grp['runs_conceded'] / np.maximum(1, grp['legal_balls'])) * 6.0, 2)
        grp['sr'] = np.where(grp['wickets'] > 0, np.round(grp['legal_balls'] / grp['wickets'], 1), np.nan)
        grp['dot_pct'] = np.round((grp['dots'] / np.maximum(1, grp['legal_balls'])) * 100.0, 1)
        grp['bnd_pct'] = np.round((grp['boundaries'] / np.maximum(1, grp['legal_balls'])) * 100.0, 1)
        return grp.sort_values('legal_balls', ascending=False)

    def get_batter_shots(self, batter_name: str, min_balls: int = 3, format_filter: str = "All") -> pd.DataFrame:
        """Returns stroke/shot breakdown."""
        sub = self.df[(self.df['striker_name'] == batter_name) & (self.df['is_batter_ball'])]
        sub = self._apply_format_filter(sub, format_filter)

        if len(sub) == 0:
            return pd.DataFrame()

        grp = sub.groupby('stroke').agg(
            balls=('runs', 'count'),
            runs=('runs', 'sum'),
            dismissals=('is_striker_out', 'sum'),
            dots=('runs', lambda s: (s == 0).sum()),
            fours=('is_four', 'sum'),
            sixes=('is_six', 'sum')
        ).reset_index()

        grp = grp[grp['balls'] >= min_balls].copy()
        grp['sr'] = np.round((grp['runs'] / np.maximum(1, grp['balls'])) * 100.0, 1)
        grp['dot_pct'] = np.round((grp['dots'] / np.maximum(1, grp['balls'])) * 100.0, 1)
        grp['bnd_pct'] = np.round(((grp['fours'] + grp['sixes']) / np.maximum(1, grp['balls'])) * 100.0, 1)
        return grp.sort_values('runs', ascending=False)

    def get_batter_wagon_wheel_zone(self, batter_name: str, format_filter: str = "All") -> pd.DataFrame:
        """Returns on-side vs off-side breakdown."""
        sub = self.df[(self.df['striker_name'] == batter_name) & (self.df['is_batter_ball'])]
        sub = self._apply_format_filter(sub, format_filter)

        if len(sub) == 0:
            return pd.DataFrame()

        grp = sub.groupby('on_or_off').agg(
            balls=('runs', 'count'),
            runs=('runs', 'sum'),
            fours=('is_four', 'sum'),
            sixes=('is_six', 'sum'),
            dismissals=('is_striker_out', 'sum')
        ).reset_index()
        grp['sr'] = np.round((grp['runs'] / np.maximum(1, grp['balls'])) * 100.0, 1)
        return grp

    def get_batter_vs_delivery_styles(self, batter_name: str, min_balls: int = 3, format_filter: str = "All") -> pd.DataFrame:
        """Returns performance vs delivery styles."""
        sub = self.df[(self.df['striker_name'] == batter_name) & (self.df['is_batter_ball'])]
        sub = self._apply_format_filter(sub, format_filter)

        if len(sub) == 0:
            return pd.DataFrame()

        grp = sub.groupby('delivery_style').agg(
            balls=('runs', 'count'),
            runs=('runs', 'sum'),
            dismissals=('is_striker_out', 'sum'),
            dots=('runs', lambda s: (s == 0).sum()),
            fours=('is_four', 'sum'),
            sixes=('is_six', 'sum')
        ).reset_index()
        grp = grp[grp['balls'] >= min_balls].copy()
        grp['sr'] = np.round((grp['runs'] / np.maximum(1, grp['balls'])) * 100.0, 1)
        return grp.sort_values('balls', ascending=False)

    def get_bowler_delivery_styles(self, bowler_name: str, min_balls: int = 3, format_filter: str = "All") -> pd.DataFrame:
        """Returns bowler delivery styles."""
        sub = self.df[self.df['bowler_name'] == bowler_name]
        sub = self._apply_format_filter(sub, format_filter)

        if len(sub) == 0:
            return pd.DataFrame()

        grp = sub.groupby('delivery_style').agg(
            balls=('is_legal', 'sum'),
            runs=('bowler_runs', 'sum'),
            wickets=('is_bowler_wkt', 'sum'),
            dots=('ball_runs', lambda s: (s == 0).sum())
        ).reset_index()
        grp = grp[grp['balls'] >= min_balls].copy()
        grp['econ'] = np.round((grp['runs'] / np.maximum(1, grp['balls'])) * 6.0, 2)
        grp['dot_pct'] = np.round((grp['dots'] / np.maximum(1, grp['balls'])) * 100.0, 1)
        return grp.sort_values('balls', ascending=False)

    def simulate_matchup(self, batter_name: str, bowler_name: str) -> dict:
        """
        Simulates tactical matchup projection between a batter and bowler based on
        bowling archetype and batter hand metrics when direct H2H sample is low or zero.
        """
        bowler_info = self.bowlers_dict.get(bowler_name, {})
        bowler_style = bowler_info.get('style', 'Unknown')
        bowler_cat = categorize_bowling_type(bowler_style)

        batter_info = self.batters_dict.get(batter_name, {})
        batter_hand = batter_info.get('hand', 'RHB')

        # 1. Batter vs this specific bowling archetype
        sub_bat = self.df[(self.df['striker_name'] == batter_name) & (self.df['bowling_category'] == bowler_cat) & (self.df['is_batter_ball'])]
        bat_balls = len(sub_bat)
        bat_runs = sub_bat['runs'].sum()
        bat_outs = (sub_bat['is_wicket'] & (sub_bat['dismissed_player_id'] == sub_bat['striker_id'])).sum()
        bat_sr = round((bat_runs / bat_balls * 100.0), 1) if bat_balls > 0 else 135.0
        bat_avg = round((bat_runs / bat_outs), 1) if bat_outs > 0 else (float(bat_runs) if bat_runs > 0 else 30.0)

        # 2. Bowler vs this batter hand
        sub_bowl = self.df[(self.df['bowler_name'] == bowler_name) & (self.df['batting_type'] == batter_hand)]
        bowl_balls = sub_bowl['is_legal'].sum()
        bowl_runs = sub_bowl['bowler_runs'].sum()
        bowl_wkts = sub_bowl['is_bowler_wkt'].sum()
        bowl_econ = round((bowl_runs / bowl_balls * 6.0), 2) if bowl_balls > 0 else 8.5
        bowl_sr = round((bowl_balls / bowl_wkts), 1) if bowl_wkts > 0 else 20.0

        # Projected composite expected strike rate and dismissal probability
        proj_sr = round((bat_sr * 0.6) + ((bowl_econ / 6.0 * 100.0) * 0.4), 1)
        wkt_threat = "High Risk" if (bowl_sr < 16.0 or bat_avg < 25.0) else ("Moderate" if bowl_sr < 22.0 else "Low Risk")

        return {
            'bowler_category': bowler_cat,
            'batter_hand': batter_hand,
            'bat_vs_archetype_balls': int(bat_balls),
            'bat_vs_archetype_sr': bat_sr,
            'bat_vs_archetype_avg': bat_avg,
            'bat_vs_archetype_outs': int(bat_outs),
            'bowl_vs_hand_balls': int(bowl_balls),
            'bowl_vs_hand_econ': bowl_econ,
            'bowl_vs_hand_sr': bowl_sr,
            'bowl_vs_hand_wkts': int(bowl_wkts),
            'projected_sr': proj_sr,
            'wicket_threat': wkt_threat
        }

    def get_head_to_head_matchup(self, batter_name: str, bowler_name: str, format_filter: str = "All") -> dict:
        """
        Computes head-to-head confrontation metrics and chronological ball-by-ball history
        between any batter and any bowler.
        """
        sub = self.df[(self.df['striker_name'] == batter_name) & (self.df['bowler_name'] == bowler_name)].copy()

        sub = self._apply_format_filter(sub, format_filter)

        sim = self.simulate_matchup(batter_name, bowler_name)

        if len(sub) == 0:
            fmt_desc = f" in {format_filter}" if format_filter != "All" else ""
            return {
                'has_data': False,
                'batter': batter_name,
                'bowler': bowler_name,
                'message': f"No direct historical deliveries recorded between {batter_name} and {bowler_name}{fmt_desc} (2022–2026).",
                'simulation': sim
            }

        sub_faced = sub[sub['is_batter_ball']]
        balls = len(sub_faced)
        runs = int(sub_faced['runs'].sum()) if balls > 0 else 0
        outs = int((sub_faced['is_wicket'] & (sub_faced['dismissed_player_id'] == sub_faced['striker_id'])).sum())
        dots = int((sub_faced['runs'] == 0).sum())
        fours = int(sub_faced['is_four'].sum())
        sixes = int(sub_faced['is_six'].sum())
        legal_balls = int(sub['is_legal'].sum())
        bowler_conceded = int(sub['bowler_runs'].sum())

        sr = (runs / balls * 100.0) if balls > 0 else 0.0
        avg = (runs / outs) if outs > 0 else float(runs)
        econ = (bowler_conceded / legal_balls * 6.0) if legal_balls > 0 else 0.0
        dot_pct = (dots / balls * 100.0) if balls > 0 else 0.0
        bnd_pct = ((fours + sixes) / balls * 100.0) if balls > 0 else 0.0

        # Tactical Verdict
        if outs >= 3 or (outs >= 2 and sr < 115):
            verdict = f"{bowler_name} Dominates (Bowler Edge)"
            badge_color = "#dc2626"
            verdict_desc = f"Bowler has dismissed the batter {outs} times with extreme containment."
        elif sr >= 170 and outs <= 1:
            verdict = f"{batter_name} Dominates (High Batting Edge)"
            badge_color = "#16a34a"
            verdict_desc = f"Batter scores freely at SR {sr:.1f} with minimal dismissal danger."
        elif sr >= 140 and outs == 0:
            verdict = f"{batter_name} on Top (Never Out)"
            badge_color = "#2563eb"
            verdict_desc = f"Batter strikes at {sr:.1f} and has never been dismissed in this sample."
        elif outs >= 1:
            verdict = "Even Contest (Wicket Danger)"
            badge_color = "#d97706"
            verdict_desc = f"Healthy contest with {outs} dismissal(s) and SR of {sr:.1f}."
        else:
            verdict = "Evenly Contested Rivalry"
            badge_color = "#64748b"
            verdict_desc = f"Balanced battle across {balls} deliveries."

        # Match Phase breakdown in this matchup
        phase_df = sub_faced.groupby('phase').agg(
            balls=('runs', 'count'),
            runs=('runs', 'sum'),
            dismissals=('is_striker_out', 'sum'),
            dots=('runs', lambda s: (s == 0).sum())
        ).reset_index()
        phase_df['sr'] = np.round((phase_df['runs'] / np.maximum(1, phase_df['balls'])) * 100.0, 1)

        # Ground Sector breakdown in this matchup
        wagon_df = sub_faced.groupby('on_or_off').agg(
            balls=('runs', 'count'),
            runs=('runs', 'sum'),
            fours=('is_four', 'sum'),
            sixes=('is_six', 'sum')
        ).reset_index()

        # Shots breakdown
        shots_df = sub_faced.groupby('stroke').agg(
            balls=('runs', 'count'),
            runs=('runs', 'sum'),
            dismissals=('is_striker_out', 'sum')
        ).reset_index().sort_values('balls', ascending=False)
        shots_df['sr'] = np.round((shots_df['runs'] / np.maximum(1, shots_df['balls'])) * 100.0, 1)

        # Delivery styles breakdown
        styles_df = sub.groupby('delivery_style').agg(
            balls=('is_legal', 'sum'),
            runs=('bowler_runs', 'sum'),
            wickets=('is_bowler_wkt', 'sum')
        ).reset_index().sort_values('balls', ascending=False)
        styles_df['econ'] = np.round((styles_df['runs'] / np.maximum(1, styles_df['balls'])) * 6.0, 2)

        # Chronological battle log
        cols_log = [
            'match_date', 'comp_name', 'innings', 'overid', 'over_ball_num',
            'stroke', 'delivery_style', 'on_or_off', 'runs', 'extras_type',
            'is_wicket', 'dismissal_type', 'pressure_index'
        ]
        log_df = sub[cols_log].copy().sort_values(['match_date', 'overid', 'over_ball_num'], ascending=False)
        log_df['over_display'] = log_df['overid'].astype(str) + "." + log_df['over_ball_num'].astype(str)
        log_df['pressure_index'] = np.round(log_df['pressure_index'], 2)
        log_df['extras_type'] = log_df['extras_type'].fillna('—')
        log_df['dismissal_type'] = log_df['dismissal_type'].fillna('—')
        log_df['is_wicket_label'] = log_df['is_wicket'].map({True: '🔴 WICKET', False: '—'})

        return {
            'has_data': True,
            'batter': batter_name,
            'bowler': bowler_name,
            'balls': balls,
            'runs': runs,
            'dismissals': outs,
            'sr': round(sr, 1),
            'avg': round(avg, 1) if outs > 0 else f"{runs}*",
            'econ': round(econ, 2),
            'dots': dots,
            'dot_pct': round(dot_pct, 1),
            'fours': fours,
            'sixes': sixes,
            'bnd_pct': round(bnd_pct, 1),
            'verdict': verdict,
            'verdict_desc': verdict_desc,
            'badge_color': badge_color,
            'phase_df': phase_df,
            'wagon_df': wagon_df,
            'shots_df': shots_df,
            'styles_df': styles_df,
            'log_df': log_df,
            'simulation': sim
        }
