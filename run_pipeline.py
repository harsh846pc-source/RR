"""
run_pipeline.py
===============
Master pipeline execution script for Rajasthan Royals SupeRR Selector Season 2.
Executes dual-dataset ingestion, pressure index computation, metrics evaluation,
Bayesian shrinkage, ranking generation, visualizations, and report production.

Datasets Processed:
1. 2022–2026 Official Challenge Dataset (IPL + T20Is, 867 matches, 200,999 deliveries)
2. Whole IPL History (2008–2026, 1,243 matches, 295,732 deliveries)
"""

import os
import sys
import pandas as pd
import numpy as np

from src.pressure_engine import load_and_enrich_match_data, load_and_enrich_ipl_history
from src.data_engine import build_and_cache_master_dataset
from src.metrics_engine import compute_batter_metrics, compute_bowler_metrics
from src.ranking_engine import rank_batters, rank_bowlers
from src.visualization import generate_all_visualizations
from src.report_generator import build_pdf_report, build_docx_report
from build_presentation import create_presentation


def run_pipeline_2022_2026():
    print("\n" + "=" * 80)
    print("  [PIPELINE 1/2] 2022-2026 OFFICIAL CHALLENGE DATASET (IPL + T20I)")
    print("=" * 80)

    # 1. State Reconstruction & Pressure Engine
    print("\n[Step 1/5] Loading datasets and reconstructing match states (2022-2026)...")
    bbb = build_and_cache_master_dataset(".", scope="2022-2026")
    print(f"  Processed {len(bbb):,} deliveries across {bbb['match_id'].nunique()} matches.")
    print(f"  High Pressure deliveries (PI >= 0.60): {(bbb['pressure_index'] >= 0.60).sum():,} ({(bbb['pressure_index'] >= 0.60).mean()*100:.1f}%)")

    # 2. Metrics Engine
    print("\n[Step 2/5] Computing player metrics, phase-adjusted xRuns, and consistency scores...")
    bat_metrics = compute_batter_metrics(bbb, min_hp_balls=120)
    bowl_metrics = compute_bowler_metrics(bbb, min_hp_balls=150)
    print(f"  Qualified Batters (>= 120 HP balls): {len(bat_metrics[bat_metrics['balls_hp'] >= 120])}")
    print(f"  Qualified Bowlers (>= 150 HP balls): {len(bowl_metrics[bowl_metrics['balls_hp'] >= 150])}")

    # 3. Ranking Engine
    print("\n[Step 3/5] Calculating composite Pressure Reliability Ratings (PRR) & ranking players...")
    qual_bat = rank_batters(bat_metrics, min_hp_balls=120)
    qual_bowl = rank_bowlers(bowl_metrics, min_hp_balls=150)

    top_10_bat = qual_bat.head(10).copy()
    top_10_bowl = qual_bowl.head(10).copy()

    # Save CSV outputs (both versioned and default)
    top_10_bat.to_csv("top_10_batters_under_pressure.csv", index=False)
    top_10_bowl.to_csv("top_10_bowlers_under_pressure.csv", index=False)
    qual_bat.to_csv("all_qualified_batters_rankings.csv", index=False)
    qual_bowl.to_csv("all_qualified_bowlers_rankings.csv", index=False)

    top_10_bat.to_csv("top_10_batters_under_pressure_2022_2026.csv", index=False)
    top_10_bowl.to_csv("top_10_bowlers_under_pressure_2022_2026.csv", index=False)
    qual_bat.to_csv("all_qualified_batters_rankings_2022_2026.csv", index=False)
    qual_bowl.to_csv("all_qualified_bowlers_rankings_2022_2026.csv", index=False)
    print("  Exported 2022-2026 rankings to CSV files successfully.")

    # 4. Visualizations
    print("\n[Step 4/5] Generating publication-grade visualizations...")
    os.makedirs("figures", exist_ok=True)
    generate_all_visualizations(bbb, qual_bat, qual_bowl, top_10_bat, top_10_bowl)

    # 5. Report & Presentation Production
    print("\n[Step 5/5] Building submission PDF, Word, and PowerPoint reports...")
    build_pdf_report(top_10_bat, top_10_bowl, "SupeRR_Selector_Methodology_Report.pdf")
    build_docx_report(top_10_bat, top_10_bowl, "SupeRR_Selector_Methodology_Report.docx")
    create_presentation()

    return top_10_bat, top_10_bowl


def run_pipeline_ipl_2008_2026():
    print("\n" + "=" * 80)
    print("  [PIPELINE 2/2] WHOLE IPL (2008-2026) ALL-TIME HISTORY (19 SEASONS)")
    print("=" * 80)

    # 1. State Reconstruction & Pressure Engine
    print("\n[Step 1/3] Loading full IPL history and reconstructing match states (2008-2026)...")
    bbb = build_and_cache_master_dataset(".", scope="ipl_2008_2026")
    print(f"  Processed {len(bbb):,} deliveries across {bbb['match_id'].nunique()} IPL matches.")
    print(f"  High Pressure deliveries (PI >= 0.60): {(bbb['pressure_index'] >= 0.60).sum():,} ({(bbb['pressure_index'] >= 0.60).mean()*100:.1f}%)")

    # 2. Metrics Engine
    print("\n[Step 2/3] Computing IPL all-time metrics, phase-adjusted xRuns, and consistency scores...")
    # Using 150 HP balls for Batters, 150 HP balls for Bowlers across 19 seasons
    bat_metrics = compute_batter_metrics(bbb, min_hp_balls=150)
    bowl_metrics = compute_bowler_metrics(bbb, min_hp_balls=150)
    print(f"  Qualified IPL Batters (>= 150 HP balls): {len(bat_metrics[bat_metrics['balls_hp'] >= 150])}")
    print(f"  Qualified IPL Bowlers (>= 150 HP balls): {len(bowl_metrics[bowl_metrics['balls_hp'] >= 150])}")

    # 3. Ranking Engine
    print("\n[Step 3/3] Calculating composite Pressure Reliability Ratings (PRR) & ranking IPL players...")
    qual_bat = rank_batters(bat_metrics, min_hp_balls=150)
    qual_bowl = rank_bowlers(bowl_metrics, min_hp_balls=150)

    top_10_bat = qual_bat.head(10).copy()
    top_10_bowl = qual_bowl.head(10).copy()

    # Save CSV outputs
    top_10_bat.to_csv("top_10_batters_under_pressure_ipl_2008_2026.csv", index=False)
    top_10_bowl.to_csv("top_10_bowlers_under_pressure_ipl_2008_2026.csv", index=False)
    qual_bat.to_csv("all_qualified_batters_rankings_ipl_2008_2026.csv", index=False)
    qual_bowl.to_csv("all_qualified_bowlers_rankings_ipl_2008_2026.csv", index=False)
    print("  Exported Whole IPL (2008-2026) rankings to CSV files successfully.")

    return top_10_bat, top_10_bowl


def main():
    print("=" * 80)
    print("  Rajasthan Royals SupeRR Selector Season 2: Player Reliability Under Pressure")
    print("  Dual-Scope Pipeline Execution (Whole IPL 2008-2026 & Official 2022-2026)")
    print("=" * 80)

    # Run Pipeline 1: 2022-2026 Official Dataset
    top_10_bat_22, top_10_bowl_22 = run_pipeline_2022_2026()

    # Run Pipeline 2: Whole IPL 2008-2026
    top_10_bat_ipl, top_10_bowl_ipl = run_pipeline_ipl_2008_2026()

    # Summary Outputs
    print("\n" + "=" * 80)
    print("  OFFICIAL UNSTOP SUBMISSION (2022-2026): TOP 10 BATTERS UNDER PRESSURE")
    print("=" * 80)
    bat_summary_22 = top_10_bat_22[['rank', 'striker_name', 'balls_hp', 'runs_hp', 'sr_hp', 'avg_hp', 'delta_sr', 'runs_added_per_100', 'cons_rate', 'pressure_rating']]
    print(bat_summary_22.to_string(index=False))

    print("\n" + "=" * 80)
    print("  OFFICIAL UNSTOP SUBMISSION (2022-2026): TOP 10 BOWLERS UNDER PRESSURE")
    print("=" * 80)
    bowl_summary_22 = top_10_bowl_22[['rank', 'bowler_name', 'balls_hp', 'wkts_hp', 'econ_hp', 'sr_hp', 'delta_econ', 'runs_saved_per_over', 'cons_rate', 'pressure_rating']]
    print(bowl_summary_22.to_string(index=False))

    print("\n" + "=" * 80)
    print("  WHOLE IPL (2008-2026) ALL-TIME HISTORY: TOP 10 BATTERS UNDER PRESSURE")
    print("=" * 80)
    bat_summary_ipl = top_10_bat_ipl[['rank', 'striker_name', 'balls_hp', 'runs_hp', 'sr_hp', 'avg_hp', 'delta_sr', 'runs_added_per_100', 'cons_rate', 'pressure_rating']]
    print(bat_summary_ipl.to_string(index=False))

    print("\n" + "=" * 80)
    print("  WHOLE IPL (2008-2026) ALL-TIME HISTORY: TOP 10 BOWLERS UNDER PRESSURE")
    print("=" * 80)
    bowl_summary_ipl = top_10_bowl_ipl[['rank', 'bowler_name', 'balls_hp', 'wkts_hp', 'econ_hp', 'sr_hp', 'delta_econ', 'runs_saved_per_over', 'cons_rate', 'pressure_rating']]
    print(bowl_summary_ipl.to_string(index=False))

    print("\nDual pipeline execution complete! All artifacts and reports are ready.")


if __name__ == "__main__":
    main()
