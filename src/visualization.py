"""
src/visualization.py
====================
Generates publication-quality charts and visualizations for the
methodology report and submission artifact.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def set_plotting_style():
    """Sets publication aesthetic for matplotlib/seaborn."""
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({
        'font.sans-serif': 'DejaVu Sans',
        'font.family': 'sans-serif',
        'axes.edgecolor': '#cccccc',
        'axes.linewidth': 1.0,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.labelsize': 11,
        'axes.labelweight': 'bold',
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'figure.titlesize': 16,
        'figure.titleweight': 'bold'
    })


def plot_pressure_index_distribution(bbb: pd.DataFrame, output_path: str = "figures/pressure_index_distribution.png"):
    """
    Plots the distribution of the Pressure Index across match phases and innings.
    """
    set_plotting_style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 1. By Match Phase
    bbb_sample = bbb.copy()
    bbb_sample['phase'] = np.where(
        bbb_sample['overid'] <= 6, 'Powerplay (Overs 1-6)',
        np.where(bbb_sample['overid'] <= 15, 'Middle (Overs 7-15)', 'Death (Overs 16-20)')
    )
    phase_order = ['Powerplay (Overs 1-6)', 'Middle (Overs 7-15)', 'Death (Overs 16-20)']

    sns.kdeplot(
        data=bbb_sample, x='pressure_index', hue='phase', hue_order=phase_order,
        common_norm=False, fill=True, alpha=0.35, linewidth=2, ax=axes[0], palette=['#2b5c8f', '#d97724', '#c92a2a']
    )
    axes[0].axvline(0.60, color='black', linestyle='--', linewidth=1.5, label='High-Pressure Cutoff (0.60)')
    axes[0].set_title("Pressure Index Density by Match Phase", pad=12)
    axes[0].set_xlabel("Pressure Index (PI)")
    axes[0].set_ylabel("Density")
    axes[0].legend(loc='upper right', frameon=True)

    # 2. Innings 1 vs Innings 2 Boxplot
    inn_data = bbb_sample[bbb_sample['innings'].isin([1, 2])]
    sns.boxplot(
        data=inn_data, x='innings', y='pressure_index',
        palette=['#3b82f6', '#10b981'], ax=axes[1], width=0.45, fliersize=1.5
    )
    axes[1].axhline(0.60, color='black', linestyle='--', linewidth=1.5, label='High-Pressure Cutoff (0.60)')
    axes[1].set_xticklabels(['Innings 1 (Setting)', 'Innings 2 (Chasing)'])
    axes[1].set_title("Pressure Index Distribution by Innings", pad=12)
    axes[1].set_xlabel("Innings")
    axes[1].set_ylabel("Pressure Index (PI)")
    axes[1].legend(loc='upper right', frameon=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_batter_pressure_vs_baseline(bat_df: pd.DataFrame, top_10_bat: pd.DataFrame, output_path: str = "figures/batter_pressure_vs_baseline.png"):
    """
    Plots Strike Rate under High Pressure vs Baseline Strike Rate.
    Highlights the Top 10 Batters.
    """
    set_plotting_style()
    fig, ax = plt.subplots(figsize=(10, 7))

    # All qualified batters
    sns.scatterplot(
        data=bat_df, x='sr_base', y='sr_hp', size='balls_hp',
        sizes=(40, 260), color='#94a3b8', alpha=0.6, ax=ax, legend=False
    )

    # Top 10 Batters highlighted
    sns.scatterplot(
        data=top_10_bat, x='sr_base', y='sr_hp', size='balls_hp',
        sizes=(100, 300), color='#dc2626', edgecolor='black', linewidth=1.2, ax=ax, legend=False
    )

    # Diagonal equality line (x = y)
    lims = [110, 205]
    ax.plot(lims, lims, color='#475569', linestyle='--', linewidth=1.5, label='Parity (SR HP = SR Base)')
    ax.set_xlim(lims)
    ax.set_ylim(lims)

    # Annotate Top 10
    for _, row in top_10_bat.iterrows():
        ax.annotate(
            f"{row['rank']}. {row['striker_name']}",
            (row['sr_base'], row['sr_hp']),
            textcoords="offset points", xytext=(6, 6),
            fontsize=8.5, weight='bold', color='#1e293b'
        )

    ax.set_title("Batters: High-Pressure Strike Rate vs Baseline Strike Rate", pad=12)
    ax.set_xlabel("Baseline Strike Rate (All Match Situations)")
    ax.set_ylabel("High-Pressure Strike Rate (PI >= 0.60)")
    ax.legend(loc='lower right', frameon=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_bowler_pressure_vs_baseline(bowl_df: pd.DataFrame, top_10_bowl: pd.DataFrame, output_path: str = "figures/bowler_pressure_vs_baseline.png"):
    """
    Plots Economy Rate under High Pressure vs Baseline Economy Rate.
    Highlights the Top 10 Bowlers.
    """
    set_plotting_style()
    fig, ax = plt.subplots(figsize=(10, 7))

    # All qualified bowlers
    sns.scatterplot(
        data=bowl_df, x='econ_base', y='econ_hp', size='balls_hp',
        sizes=(40, 260), color='#94a3b8', alpha=0.6, ax=ax, legend=False
    )

    # Top 10 Bowlers highlighted
    sns.scatterplot(
        data=top_10_bowl, x='econ_base', y='econ_hp', size='balls_hp',
        sizes=(100, 300), color='#0284c7', edgecolor='black', linewidth=1.2, ax=ax, legend=False
    )

    # Diagonal equality line (x = y)
    lims = [4.5, 11.5]
    ax.plot(lims, lims, color='#475569', linestyle='--', linewidth=1.5, label='Parity (Econ HP = Econ Base)')
    ax.set_xlim(lims)
    ax.set_ylim(lims)

    # Annotate Top 10
    for _, row in top_10_bowl.iterrows():
        ax.annotate(
            f"{row['rank']}. {row['bowler_name']}",
            (row['econ_base'], row['econ_hp']),
            textcoords="offset points", xytext=(6, 6),
            fontsize=8.5, weight='bold', color='#0f172a'
        )

    ax.set_title("Bowlers: High-Pressure Economy vs Baseline Economy", pad=12)
    ax.set_xlabel("Baseline Economy Rate (All Match Situations)")
    ax.set_ylabel("High-Pressure Economy Rate (PI >= 0.60)")
    ax.legend(loc='upper left', frameon=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_top_10_rankings(top_10_bat: pd.DataFrame, top_10_bowl: pd.DataFrame, output_path: str = "figures/top_10_rankings_combined.png"):
    """
    Horizontal bar charts showing Top 10 Batters and Top 10 Bowlers by Pressure Rating.
    """
    set_plotting_style()
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Batters
    bat_sorted = top_10_bat.sort_values('pressure_rating', ascending=True)
    y_pos = np.arange(len(bat_sorted))
    axes[0].barh(y_pos, bat_sorted['pressure_rating'], color='#e11d48', alpha=0.85, edgecolor='black', linewidth=0.8)
    axes[0].set_yticks(y_pos)
    axes[0].set_yticklabels([f"#{r} {n}" for r, n in zip(bat_sorted['rank'], bat_sorted['striker_name'])], weight='bold')
    axes[0].set_xlabel("Batter Pressure Reliability Rating (0-100)")
    axes[0].set_title("Top 10 Batters Under Pressure", pad=12)
    axes[0].set_xlim([60, 90])
    for i, v in enumerate(bat_sorted['pressure_rating']):
        axes[0].text(v + 0.4, i, f"{v:.1f} (SR {bat_sorted['sr_hp'].iloc[i]:.1f})", va='center', fontsize=9, weight='bold')

    # Bowlers
    bowl_sorted = top_10_bowl.sort_values('pressure_rating', ascending=True)
    y_pos_b = np.arange(len(bowl_sorted))
    axes[1].barh(y_pos_b, bowl_sorted['pressure_rating'], color='#0284c7', alpha=0.85, edgecolor='black', linewidth=0.8)
    axes[1].set_yticks(y_pos_b)
    axes[1].set_yticklabels([f"#{r} {n}" for r, n in zip(bowl_sorted['rank'], bowl_sorted['bowler_name'])], weight='bold')
    axes[1].set_xlabel("Bowler Pressure Reliability Rating (0-100)")
    axes[1].set_title("Top 10 Bowlers Under Pressure", pad=12)
    axes[1].set_xlim([60, 90])
    for i, v in enumerate(bowl_sorted['pressure_rating']):
        axes[1].text(v + 0.4, i, f"{v:.1f} (Econ {bowl_sorted['econ_hp'].iloc[i]:.2f})", va='center', fontsize=9, weight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def generate_all_visualizations(bbb, qual_bat, qual_bowl, top_10_bat, top_10_bowl):
    """Executes all figure generation functions."""
    print("Generating Figure 1: Pressure Index Distribution...")
    plot_pressure_index_distribution(bbb)

    print("Generating Figure 2: Batter Pressure vs Baseline...")
    plot_batter_pressure_vs_baseline(qual_bat, top_10_bat)

    print("Generating Figure 3: Bowler Pressure vs Baseline...")
    plot_bowler_pressure_vs_baseline(qual_bowl, top_10_bowl)

    print("Generating Figure 4: Top 10 Combined Rankings...")
    plot_top_10_rankings(top_10_bat, top_10_bowl)
    print("All figures successfully generated in figures/ directory!")
