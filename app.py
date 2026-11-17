"""
app.py
======
SupeRR Cricket Matchup & Player Intelligence Platform
Interactive Streamlit Application for 2022–2026 T20 & IPL Data.
Official Round 1 Challenge Submission — Rajasthan Royals

Features:
- Individual Player Profiles (Batting & Bowling)
- Pace vs Spin, Bowling Type, and Match Phase Splits
- Stroke/Shot Breakdown & On/Off-side Scoring Zones
- Head-to-Head Matchup Tool (ANY Batter vs ANY Bowler) with Tactical Simulation
- Quick Rivalry Selector & Filterable Chronological Delivery Logs
- Bowling Archetypes Tactical Matrix (Pace vs Spin subtypes, RHB vs LHB)
- SupeRR Pressure Reliability Leaderboards (Top 10 & Full Qualified Database)
- One-Click Report & CSV Downloads (PDF, DOCX, CSV)
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.data_engine import CricketIntelligenceEngine
from src.data_dictionary import (
    get_delivery_schema_df,
    get_batting_metrics_df,
    get_bowling_metrics_df
)

# Page configuration
st.set_page_config(
    page_title="SupeRR Intelligence Platform | Rajasthan Royals",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Modern Styling (Rajasthan Royals Pink, Deep Navy & Obsidian)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Global Background Cleanliness */
    .stApp {
        background-color: #0B1120;
        color: #F8FAFC;
    }

    /* Main Headers */
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFFFFF 0%, #F472B6 60%, #D91680 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
        margin-bottom: 2px;
    }
    .sub-header {
        font-size: 1.0rem;
        font-weight: 500;
        color: #94A3B8;
        margin-bottom: 20px;
    }

    /* Glassmorphic Metric Cards */
    .metric-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 18px;
        border-left: 4px solid #D91680;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(8px);
        margin-bottom: 12px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(217, 22, 128, 0.4);
    }
    .metric-card-gold {
        border-left: 4px solid #F59E0B !important;
    }
    .metric-card-blue {
        border-left: 4px solid #38BDF8 !important;
    }
    .metric-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 4px;
    }

    /* Matchup Hero Banner */
    .matchup-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #2E0854 100%);
        border: 1px solid rgba(217, 22, 128, 0.35);
        border-radius: 16px;
        padding: 24px 28px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 10px 25px -5px rgba(217, 22, 128, 0.15);
    }
    .badge-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.3px;
    }

    /* Podium Card for Top 3 */
    .podium-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 18px 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Custom Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        background-color: rgba(15, 23, 42, 0.6);
        border-radius: 8px 8px 0px 0px;
        font-weight: 600;
        font-size: 0.92rem;
        color: #94A3B8;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-bottom: none;
        padding: 0 18px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #D91680 !important;
        color: #FFFFFF !important;
        border-color: #D91680 !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def load_engine(scope: str = "2022-2026"):
    return CricketIntelligenceEngine(".", scope=scope)

# Sidebar Setup
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/6/60/Rajasthan_Royals_Logo.svg/1200px-Rajasthan_Royals_Logo.svg.png", width=105)
    st.markdown("### **SupeRR Intelligence**")
    st.caption("Rajasthan Royals War Room Analytics Platform")
    
    st.markdown("---")
    st.markdown("#### **📊 Dataset Selection**")
    dataset_scope = st.radio(
        "Choose Active Dataset:",
        [
            "🏏 Whole IPL (2008–2026)",
            "⚡ 2022–2026 (Official Challenge Dataset)"
        ],
        index=0,
        help="Select between the entire 19-season history of IPL (2008-2026, 1,243 matches) or the official 2022-2026 tournament dataset."
    )
    active_scope = "ipl_2008_2026" if "Whole IPL" in dataset_scope else "2022-2026"
    engine = load_engine(active_scope)

    st.markdown("---")
    nav = st.radio(
        "Navigation",
        [
            "👤 Player Profile Explorer",
            "⚔️ Head-to-Head Matchup Tool",
            "🎯 Bowling Archetypes Matrix",
            "🏆 Pressure Rankings & Leaderboards",
            "🎬 Share Your Journey (Reel & Post)",
            "📖 Data Dictionary & Formula Reference"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("#### **Global Filters**")
    if active_scope == "2022-2026":
        format_filter = st.selectbox(
            "Tournament Format",
            ["All Formats", "IPL", "T20I"],
            index=0
        )
        format_query = "All" if format_filter == "All Formats" else ("T20" if format_filter == "IPL" else "T20I")
    else:
        format_filter = "IPL (All Seasons)"
        format_query = "All"
        st.markdown(
            "<div style='background:rgba(217,22,128,0.15); border:1px solid #D91680; border-radius:8px; padding:8px 12px; font-size:0.85rem; color:#F472B6;'>"
            "<b>Format:</b> Indian Premier League (2008–2026)</div>",
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    if active_scope == "ipl_2008_2026":
        st.markdown("""
        **Active Dataset Scope:**
        - 🗓️ Seasons: **2008 to 2026** (19 Seasons)
        - ⚡ **295,732** Deliveries
        - 🏟️ **1,243** Matches (All-Time IPL)
        - 👑 Complete IPL Legends & Active Stars
        - 📊 Comprehensive Matchup History
        """)
    else:
        st.markdown("""
        **Active Dataset Scope:**
        - 🗓️ Seasons: **2022 to 2026**
        - ⚡ **200,999** Deliveries
        - 🏟️ **867** Matches (IPL & T20I)
        - 🎯 Full Optical Stroke & Speed Tracking
        - 🏆 Official Challenge Submission Baseline
        """)
    
    st.markdown("---")
    st.markdown("#### **📥 Submission Assets**")
    pdf_rep_path = "final_submission/SuperRR_Final_Methodology_Report.pdf" if os.path.exists("final_submission/SuperRR_Final_Methodology_Report.pdf") else "SupeRR_Selector_Methodology_Report.pdf"
    if os.path.exists(pdf_rep_path):
        with open(pdf_rep_path, "rb") as f_pdf:
            st.download_button(
                label="📄 Download Methodology Report (PDF)",
                data=f_pdf.read(),
                file_name="SuperRR_Final_Methodology_Report.pdf",
                mime="application/pdf"
            )
    if os.path.exists("final_submission/Dataset_Audit_Report.pdf"):
        with open("final_submission/Dataset_Audit_Report.pdf", "rb") as f_audit:
            st.download_button(
                label="📋 Download Dataset Audit Report (PDF)",
                data=f_audit.read(),
                file_name="Dataset_Audit_Report.pdf",
                mime="application/pdf"
            )
    if os.path.exists("final_submission/Old_vs_Updated_Rankings_Comparison.xlsx"):
        with open("final_submission/Old_vs_Updated_Rankings_Comparison.xlsx", "rb") as f_xl:
            st.download_button(
                label="📊 Download Rankings Comparison (Excel)",
                data=f_xl.read(),
                file_name="Old_vs_Updated_Rankings_Comparison.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    if os.path.exists("SupeRR_Selector_Methodology_Presentation.pptx"):
        with open("SupeRR_Selector_Methodology_Presentation.pptx", "rb") as f_pptx:
            st.download_button(
                label="📑 Download Presentation Deck (PPTX)",
                data=f_pptx.read(),
                file_name="SupeRR_Selector_Methodology_Presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )


# Top Banner
st.markdown('<div class="main-header">🏏 SupeRR Cricket Intelligence Platform</div>', unsafe_allow_html=True)
if active_scope == "ipl_2008_2026":
    st.markdown('<div class="sub-header">Data-Driven Pressure Reliability & Tactical Matchup Engine | <span style="color:#D91680; font-weight:700;">Whole IPL All-Time History (2008–2026, 1,243 Matches)</span></div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="sub-header">Data-Driven Pressure Reliability & Tactical Matchup Engine | Filter: <span style="color:#D91680; font-weight:700;">{format_filter}</span> (2022–2026 Challenge Dataset)</div>', unsafe_allow_html=True)


# ==============================================================================
# TAB 1: PLAYER PROFILE EXPLORER
# ==============================================================================
if nav == "👤 Player Profile Explorer":
    st.markdown("### 👤 Player Profile & Tactical Breakdown")
    st.caption("Deep-dive into any player's career KPIs, pace vs spin splits, match phases, shot selection, ground direction, and pressure performance.")

    col_sel1, col_sel2 = st.columns([3, 1])
    with col_sel1:
        default_name = "Virat Kohli" if "Virat Kohli" in engine.all_player_names else engine.all_player_names[0]
        selected_player = st.selectbox(
            "Select or Search Player:",
            engine.all_player_names,
            index=engine.all_player_names.index(default_name)
        )
    
    is_batter = selected_player in engine.batters_dict
    is_bowler = selected_player in engine.bowlers_dict
    role = "All-Rounder" if (is_batter and is_bowler) else ("Batter" if is_batter else "Bowler")
    
    with col_sel2:
        badge_bg = "#831843" if role == "All-Rounder" else ("#1e3a8a" if role == "Bowler" else "#065f46")
        st.markdown(f"<div style='margin-top: 26px;'><span class='badge-tag' style='background:{badge_bg}; color:#F8FAFC;'>Role: {role}</span></div>", unsafe_allow_html=True)

    profile_mode = "Batting"
    if is_batter and is_bowler:
        profile_mode = st.radio("Active Discipline View:", ["Batting", "Bowling"], horizontal=True)
    elif is_bowler:
        profile_mode = "Bowling"

    st.markdown("---")

    # ------------------- BATTING PROFILE -------------------
    if profile_mode == "Batting" and is_batter:
        bat_stats = engine.get_batter_career(selected_player, format_query)
        
        kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
        with kpi1:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Runs (Innings)</div><div class='metric-value'>{bat_stats['runs']:,} <span style='font-size:0.9rem;color:#94A3B8;'>({bat_stats['innings']})</span></div></div>", unsafe_allow_html=True)
        with kpi2:
            st.markdown(f"<div class='metric-card metric-card-gold'><div class='metric-label'>Strike Rate</div><div class='metric-value'>{bat_stats['sr']}</div></div>", unsafe_allow_html=True)
        with kpi3:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Average</div><div class='metric-value'>{bat_stats['avg']}</div></div>", unsafe_allow_html=True)
        with kpi4:
            st.markdown(f"<div class='metric-card metric-card-blue'><div class='metric-label'>Highest (50s/100s)</div><div class='metric-value'>{bat_stats['highest_score']} <span style='font-size:0.85rem;color:#94A3B8;'>({bat_stats['fifties']}/{bat_stats['hundreds']})</span></div></div>", unsafe_allow_html=True)
        with kpi5:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Boundary %</div><div class='metric-value'>{bat_stats['bnd_pct']}%</div></div>", unsafe_allow_html=True)
        with kpi6:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Dot Ball %</div><div class='metric-value'>{bat_stats['dot_pct']}%</div></div>", unsafe_allow_html=True)

        tab_splits, tab_shots, tab_wagon, tab_styles = st.tabs([
            "📊 Situational Splits (Pace/Spin, Phases, Pressure)",
            "🏏 Shot & Stroke Analysis",
            "🧭 Ground Scoring Direction (Wagon Wheel)",
            "🎯 Delivery Styles (Yorkers, Bouncers, Cutters)"
        ])

        with tab_splits:
            col_s1, col_s2 = st.columns(2)
            
            with col_s1:
                st.markdown("#### **Pace vs Spin Breakdown**")
                df_pace_spin = engine.get_batter_splits(selected_player, "pace_or_spin", format_query)
                if not df_pace_spin.empty:
                    st.dataframe(df_pace_spin[['pace_or_spin', 'runs', 'balls', 'dismissals', 'sr', 'avg', 'dot_pct', 'bnd_pct']].rename(columns={
                        'pace_or_spin': 'Bowling Type', 'runs': 'Runs', 'balls': 'Balls', 'dismissals': 'Outs',
                        'sr': 'SR', 'avg': 'Avg', 'dot_pct': 'Dot %', 'bnd_pct': 'Bnd %'
                    }), width="stretch", hide_index=True)
                    
                    fig_ps = px.bar(
                        df_pace_spin, x='pace_or_spin', y=['sr', 'avg'], barmode='group',
                        title=f"{selected_player}: Strike Rate & Average vs Pace / Spin",
                        color_discrete_sequence=['#D91680', '#38BDF8'],
                        labels={'value': 'Metric Value', 'pace_or_spin': 'Bowling Type'}
                    )
                    fig_ps.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig_ps, width="stretch")
                else:
                    st.info("No pace vs spin split data available for the active filter.")

            with col_s2:
                st.markdown("#### **Match Phase Breakdown (Powerplay vs Middle vs Death)**")
                df_phase = engine.get_batter_splits(selected_player, "phase", format_query)
                if not df_phase.empty:
                    st.dataframe(df_phase[['phase', 'runs', 'balls', 'dismissals', 'sr', 'avg', 'bnd_pct', 'dot_pct']].rename(columns={
                        'phase': 'Phase', 'runs': 'Runs', 'balls': 'Balls', 'dismissals': 'Outs',
                        'sr': 'SR', 'avg': 'Avg', 'bnd_pct': 'Bnd %', 'dot_pct': 'Dot %'
                    }), width="stretch", hide_index=True)
                    
                    fig_phase = px.bar(
                        df_phase, x='phase', y='sr', color='runs',
                        title=f"{selected_player}: Strike Rate by Match Phase",
                        color_continuous_scale='Magma',
                        labels={'sr': 'Strike Rate', 'phase': 'Phase', 'runs': 'Runs Scored'}
                    )
                    fig_phase.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig_phase, width="stretch")
                else:
                    st.info("No phase split data available for the active filter.")

            st.markdown("---")
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.markdown("#### **Innings Context (1st Setting vs 2nd Chasing)**")
                df_inn = engine.get_batter_splits(selected_player, "innings", format_query)
                if not df_inn.empty:
                    df_inn['innings_name'] = df_inn['innings'].map({1: '1st Innings (Setting)', 2: '2nd Innings (Chasing)', 3: 'Super Over 1', 4: 'Super Over 2'}).fillna('Other')
                    st.dataframe(df_inn[['innings_name', 'runs', 'balls', 'dismissals', 'sr', 'avg', 'bnd_pct']].rename(columns={
                        'innings_name': 'Innings Context', 'runs': 'Runs', 'balls': 'Balls', 'dismissals': 'Outs',
                        'sr': 'SR', 'avg': 'Avg', 'bnd_pct': 'Bnd %'
                    }), width="stretch", hide_index=True)
            with col_c2:
                st.markdown("#### **High Pressure vs Baseline Situations**")
                df_p = engine.get_batter_splits(selected_player, "pressure_tier", format_query)
                if not df_p.empty:
                    st.dataframe(df_p[['pressure_tier', 'runs', 'balls', 'dismissals', 'sr', 'avg', 'bnd_pct', 'dot_pct']].rename(columns={
                        'pressure_tier': 'Pressure Tier', 'runs': 'Runs', 'balls': 'Balls', 'dismissals': 'Outs',
                        'sr': 'SR', 'avg': 'Avg', 'bnd_pct': 'Bnd %', 'dot_pct': 'Dot %'
                    }), width="stretch", hide_index=True)

        with tab_shots:
            st.markdown("#### **Shot Selection & Run Productivity by Stroke**")
            df_shots = engine.get_batter_shots(selected_player, min_balls=3, format_filter=format_query)
            has_stroke_data = not df_shots.empty and not (len(df_shots) == 1 and df_shots['stroke'].iloc[0] == 'Unclassified')
            if has_stroke_data:
                col_sh1, col_sh2 = st.columns([3, 2])
                with col_sh1:
                    fig_shots = px.bar(
                        df_shots.head(10), x='runs', y='stroke', orientation='h',
                        color='sr', color_continuous_scale='Turbo',
                        title="Top 10 Scoring Strokes (Colored by Strike Rate)",
                        labels={'runs': 'Runs Scored', 'stroke': 'Stroke Played', 'sr': 'Strike Rate'}
                    )
                    fig_shots.update_layout(yaxis={'categoryorder': 'total ascending'}, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig_shots, width="stretch")
                with col_sh2:
                    st.dataframe(df_shots[['stroke', 'runs', 'balls', 'sr', 'dismissals', 'fours', 'sixes', 'bnd_pct']].rename(columns={
                        'stroke': 'Shot', 'runs': 'Runs', 'balls': 'Balls', 'sr': 'SR',
                        'dismissals': 'Outs', 'fours': '4s', 'sixes': '6s', 'bnd_pct': 'Bnd %'
                    }), width="stretch", hide_index=True)
            else:
                st.info("🎯 Optical HawkEye stroke tracking is featured for 2022–2026 matches. For all-time IPL careers, explore the Situational Splits tab above for full Phase, Pressure, and Pace vs Spin analytics.")

        with tab_wagon:
            st.markdown("#### **Scoring Direction: On-Side vs Off-Side Distribution**")
            df_wagon = engine.get_batter_wagon_wheel_zone(selected_player, format_filter=format_query)
            has_wagon_data = not df_wagon.empty and not (len(df_wagon) == 1 and df_wagon['on_or_off'].iloc[0] == 'Unclassified')
            if has_wagon_data:
                col_w1, col_w2 = st.columns(2)
                with col_w1:
                    fig_pie = px.pie(
                        df_wagon, names='on_or_off', values='runs',
                        title=f"{selected_player}: Runs Distribution by Ground Sector",
                        color='on_or_off',
                        color_discrete_map={'Off-side': '#38BDF8', 'On-side': '#D91680', 'Unclassified': '#64748B'},
                        hole=0.48
                    )
                    fig_pie.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig_pie, width="stretch")
                with col_w2:
                    st.dataframe(df_wagon[['on_or_off', 'runs', 'balls', 'sr', 'fours', 'sixes', 'dismissals']].rename(columns={
                        'on_or_off': 'Ground Side', 'runs': 'Runs', 'balls': 'Balls', 'sr': 'SR',
                        'fours': '4s', 'sixes': '6s', 'dismissals': 'Outs'
                    }), width="stretch", hide_index=True)
            else:
                st.info("🌐 Optical ground tracking (On-side vs Off-side) is featured for 2022–2026 matches. Full situational match condition splits are available in the Splits tab.")

        with tab_styles:
            st.markdown("#### **Performance vs Specific Delivery Styles**")
            df_styles = engine.get_batter_vs_delivery_styles(selected_player, min_balls=3, format_filter=format_query)
            has_style_data = not df_styles.empty and not (len(df_styles) == 1 and df_styles['delivery_style'].iloc[0] == 'Standard')
            if has_style_data:
                col_st1, col_st2 = st.columns([3, 2])
                with col_st1:
                    fig_styles = px.bar(
                        df_styles.head(10), x='delivery_style', y='sr', color='balls',
                        title="Strike Rate vs Delivery Variations (Yorkers, Bouncers, Cutters)",
                        color_continuous_scale='Blues',
                        labels={'sr': 'Strike Rate', 'delivery_style': 'Delivery Type', 'balls': 'Balls Faced'}
                    )
                    fig_styles.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig_styles, width="stretch")
                with col_st2:
                    st.dataframe(df_styles[['delivery_style', 'balls', 'runs', 'sr', 'dismissals', 'dots']].rename(columns={
                        'delivery_style': 'Delivery Style', 'balls': 'Balls', 'runs': 'Runs', 'sr': 'SR',
                        'dismissals': 'Outs', 'dots': 'Dots'
                    }), width="stretch", hide_index=True)
            else:
                st.info("No delivery style data available.")

    # ------------------- BOWLING PROFILE -------------------
    elif profile_mode == "Bowling" and is_bowler:
        bowl_stats = engine.get_bowler_career(selected_player, format_query)
        
        kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
        with kpi1:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Wickets (Spells)</div><div class='metric-value'>{bowl_stats['wickets']} <span style='font-size:0.9rem;color:#94A3B8;'>({bowl_stats['spells']})</span></div></div>", unsafe_allow_html=True)
        with kpi2:
            st.markdown(f"<div class='metric-card metric-card-gold'><div class='metric-label'>Economy Rate</div><div class='metric-value'>{bowl_stats['econ']}</div></div>", unsafe_allow_html=True)
        with kpi3:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Bowling SR</div><div class='metric-value'>{bowl_stats['sr']}</div></div>", unsafe_allow_html=True)
        with kpi4:
            st.markdown(f"<div class='metric-card metric-card-blue'><div class='metric-label'>Overs Bowled</div><div class='metric-value'>{bowl_stats['overs']}</div></div>", unsafe_allow_html=True)
        with kpi5:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Dot Ball %</div><div class='metric-value'>{bowl_stats['dot_pct']}%</div></div>", unsafe_allow_html=True)
        with kpi6:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Best Figures</div><div class='metric-value'>{bowl_stats['best_bowling']}</div></div>", unsafe_allow_html=True)

        tab_b_splits, tab_b_styles = st.tabs([
            "📊 Situational Splits (vs RHB/LHB, Phases, Pressure)",
            "🎯 Delivery Repertoire (Yorkers, Bouncers, Cutters, Variations)"
        ])

        with tab_b_splits:
            col_bs1, col_bs2 = st.columns(2)
            with col_bs1:
                st.markdown("#### **vs Right-Hand vs Left-Hand Batters**")
                df_hand = engine.get_bowler_splits(selected_player, "batting_type", format_query)
                if not df_hand.empty:
                    st.dataframe(df_hand[['batting_type', 'legal_balls', 'runs_conceded', 'wickets', 'econ', 'sr', 'dot_pct', 'bnd_pct']].rename(columns={
                        'batting_type': 'Batter Hand', 'legal_balls': 'Balls', 'runs_conceded': 'Runs',
                        'wickets': 'Wkts', 'econ': 'Econ', 'sr': 'SR', 'dot_pct': 'Dot %', 'bnd_pct': 'Bnd %'
                    }), width="stretch", hide_index=True)
                    
                    fig_hand = px.bar(
                        df_hand, x='batting_type', y=['econ', 'dot_pct'], barmode='group',
                        title=f"{selected_player}: Economy & Dot % vs RHB / LHB",
                        color_discrete_sequence=['#38BDF8', '#10B981'],
                        labels={'value': 'Rate / %', 'batting_type': 'Batter Hand'}
                    )
                    fig_hand.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig_hand, width="stretch")
            with col_bs2:
                st.markdown("#### **Match Phase Breakdown (Powerplay, Middle, Death)**")
                df_b_phase = engine.get_bowler_splits(selected_player, "phase", format_query)
                if not df_b_phase.empty:
                    st.dataframe(df_b_phase[['phase', 'legal_balls', 'runs_conceded', 'wickets', 'econ', 'sr', 'dot_pct']].rename(columns={
                        'phase': 'Phase', 'legal_balls': 'Balls', 'runs_conceded': 'Runs',
                        'wickets': 'Wkts', 'econ': 'Econ', 'sr': 'SR', 'dot_pct': 'Dot %'
                    }), width="stretch", hide_index=True)
                    
                    fig_bp = px.bar(
                        df_b_phase, x='phase', y='econ', color='wickets',
                        title=f"{selected_player}: Economy & Wickets by Match Phase",
                        color_continuous_scale='Purples',
                        labels={'econ': 'Economy Rate', 'phase': 'Phase', 'wickets': 'Wickets Taken'}
                    )
                    fig_bp.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig_bp, width="stretch")

            st.markdown("---")
            col_bc1, col_bc2 = st.columns(2)
            with col_bc1:
                st.markdown("#### **Pressure Situation Breakdown**")
                df_bp = engine.get_bowler_splits(selected_player, "pressure_tier", format_query)
                if not df_bp.empty:
                    st.dataframe(df_bp[['pressure_tier', 'legal_balls', 'runs_conceded', 'wickets', 'econ', 'sr', 'dot_pct']].rename(columns={
                        'pressure_tier': 'Pressure Tier', 'legal_balls': 'Balls', 'runs_conceded': 'Runs',
                        'wickets': 'Wkts', 'econ': 'Econ', 'sr': 'SR', 'dot_pct': 'Dot %'
                    }), width="stretch", hide_index=True)
            with col_bc2:
                st.markdown("#### **Over vs Around the Wicket Angle**")
                df_oa = engine.get_bowler_splits(selected_player, "over_or_around", format_query)
                if not df_oa.empty:
                    st.dataframe(df_oa[['over_or_around', 'legal_balls', 'runs_conceded', 'wickets', 'econ', 'sr']].rename(columns={
                        'over_or_around': 'Bowling Angle', 'legal_balls': 'Balls', 'runs_conceded': 'Runs',
                        'wickets': 'Wkts', 'econ': 'Econ', 'sr': 'SR'
                    }), width="stretch", hide_index=True)

        with tab_b_styles:
            st.markdown("#### **Delivery Style Repertoire & Containment Efficiency**")
            df_b_styles = engine.get_bowler_delivery_styles(selected_player, min_balls=3, format_filter=format_query)
            has_b_style = not df_b_styles.empty and not (len(df_b_styles) == 1 and df_b_styles['delivery_style'].iloc[0] == 'Standard')
            if has_b_style:
                col_bst1, col_bst2 = st.columns([3, 2])
                with col_bst1:
                    fig_bst = px.bar(
                        df_b_styles.head(10), x='delivery_style', y='econ', color='wickets',
                        title="Economy & Wickets by Delivery Variation",
                        color_continuous_scale='Teal',
                        labels={'econ': 'Economy Rate', 'delivery_style': 'Delivery Style', 'wickets': 'Wickets'}
                    )
                    fig_bst.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig_bst, width="stretch")
                with col_bst2:
                    st.dataframe(df_b_styles[['delivery_style', 'balls', 'runs', 'wickets', 'econ', 'dot_pct']].rename(columns={
                        'delivery_style': 'Delivery Style', 'balls': 'Balls', 'runs': 'Runs',
                        'wickets': 'Wkts', 'econ': 'Econ', 'dot_pct': 'Dot %'
                    }), width="stretch", hide_index=True)
            else:
                st.info("🎯 Optical delivery variation tracking (Yorkers, Bouncers, Cutters, Slower balls) is featured for 2022–2026 matches. Full RHB/LHB and Phase containment metrics are available in the Splits tab.")


# ==============================================================================
# TAB 2: HEAD-TO-HEAD MATCHUP TOOL
# ==============================================================================
elif nav == "⚔️ Head-to-Head Matchup Tool":
    st.markdown("### ⚔️ Head-to-Head Matchup Analyzer & Tactical Simulator")
    st.caption("Select ANY Batter and ANY Bowler to inspect their direct historical confrontation or project a tactical simulation when they haven't met.")
    
    # Quick Rivals Selector
    if active_scope == "ipl_2008_2026":
        notable_matchups = [
            "-- Select a Notable Rivalry --",
            "Virat Kohli vs Lasith Malinga",
            "MS Dhoni vs Sunil Narine",
            "Rohit Sharma vs Jasprit Bumrah",
            "AB de Villiers vs Jasprit Bumrah",
            "Chris Gayle vs Bhuvneshwar Kumar",
            "Virat Kohli vs Jasprit Bumrah",
            "Andre Russell vs Dwayne Bravo",
            "Heinrich Klaasen vs Varun Chakravarthy"
        ]
    else:
        notable_matchups = [
            "-- Select a Notable Rivalry --",
            "Virat Kohli vs Jasprit Bumrah",
            "Heinrich Klaasen vs Varun Chakravarthy",
            "Suryakumar Yadav vs Rashid Khan",
            "Jos Buttler vs Sunil Narine",
            "Rohit Sharma vs Trent Boult",
            "Rishabh Pant vs Kuldeep Yadav",
            "Andre Russell vs Haris Rauf"
        ]
    quick_sel = st.selectbox("⚡ Quick Matchup Presets:", notable_matchups, index=0)

    col_m1, col_m2 = st.columns(2)
    default_bat = "Virat Kohli"
    default_bowl = "Jasprit Bumrah"
    
    if quick_sel != "-- Select a Notable Rivalry --":
        parts = quick_sel.split(" vs ")
        if len(parts) == 2 and parts[0] in engine.batter_names and parts[1] in engine.bowler_names:
            default_bat = parts[0]
            default_bowl = parts[1]

    with col_m1:
        sel_batter = st.selectbox("Select Batter:", engine.batter_names, index=engine.batter_names.index(default_bat) if default_bat in engine.batter_names else 0)
    with col_m2:
        sel_bowler = st.selectbox("Select Bowler:", engine.bowler_names, index=engine.bowler_names.index(default_bowl) if default_bowl in engine.bowler_names else 0)
    
    st.markdown("---")
    
    matchup = engine.get_head_to_head_matchup(sel_batter, sel_bowler, format_query)
    
    if not matchup['has_data']:
        st.warning(f"⚠️ {matchup['message']}")
        
        sim = matchup.get('simulation', {})
        st.markdown(f"""
        <div class='matchup-banner'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <h3 style='color:white; margin:0 0 6px 0;'>🔮 Tactical Matchup Projection (Archetype Simulation)</h3>
                    <p style='color:#CBD5E1; margin:0;'>
                        No direct deliveries recorded between <b>{sel_batter}</b> and <b>{sel_bowler}</b>. Simulated projection based on <b>{sim.get('bowler_category', 'Pace')}</b> and <b>{sim.get('batter_hand', 'RHB')}</b>:
                    </p>
                </div>
                <div>
                    <span style='background:#7C3AED; color:white; padding:8px 18px; border-radius:20px; font-weight:800; font-size:0.95rem;'>
                        Projected SR: {sim.get('projected_sr', 135.0)} | {sim.get('wicket_threat', 'Moderate')}
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        sim_c1, sim_c2 = st.columns(2)
        with sim_c1:
            st.markdown(f"#### **{sel_batter} vs {sim.get('bowler_category', 'Pace')} Archetype**")
            st.markdown(f"""
            - **Deliveries Faced:** **{sim.get('bat_vs_archetype_balls', 0)}** balls
            - **Strike Rate vs Archetype:** **{sim.get('bat_vs_archetype_sr', 135.0)}**
            - **Batting Average vs Archetype:** **{sim.get('bat_vs_archetype_avg', 30.0)}**
            - **Times Dismissed by Archetype:** **{sim.get('bat_vs_archetype_outs', 0)}**
            """)
        with sim_c2:
            st.markdown(f"#### **{sel_bowler} vs {sim.get('batter_hand', 'RHB')} Batters**")
            st.markdown(f"""
            - **Legal Balls Bowled vs Hand:** **{sim.get('bowl_vs_hand_balls', 0)}** balls
            - **Economy Rate vs Hand:** **{sim.get('bowl_vs_hand_econ', 8.5)}**
            - **Bowling Strike Rate vs Hand:** **{sim.get('bowl_vs_hand_sr', 20.0)}** balls/wkt
            - **Wickets Taken vs Hand:** **{sim.get('bowl_vs_hand_wkts', 0)}**
            """)

    else:
        # Matchup Hero Banner
        st.markdown(f"""
        <div class='matchup-banner'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <h2 style='color:white; margin:0;'>{sel_batter} <span style='color:#D91680;'>vs</span> {sel_bowler}</h2>
                    <p style='color:#94A3B8; margin:4px 0 0 0;'>Historical Head-to-Head Record | {matchup['verdict_desc']}</p>
                </div>
                <div>
                    <span style='background:{matchup['badge_color']}; color:white; padding:8px 18px; border-radius:24px; font-weight:800; font-size:1.0rem;'>
                        {matchup['verdict']}
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        m_kpi1, m_kpi2, m_kpi3, m_kpi4, m_kpi5, m_kpi6 = st.columns(6)
        with m_kpi1:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Balls Faced</div><div class='metric-value'>{matchup['balls']}</div></div>", unsafe_allow_html=True)
        with m_kpi2:
            st.markdown(f"<div class='metric-card metric-card-gold'><div class='metric-label'>Runs Scored</div><div class='metric-value'>{matchup['runs']}</div></div>", unsafe_allow_html=True)
        with m_kpi3:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Dismissals</div><div class='metric-value'>{matchup['dismissals']}</div></div>", unsafe_allow_html=True)
        with m_kpi4:
            st.markdown(f"<div class='metric-card metric-card-blue'><div class='metric-label'>Strike Rate</div><div class='metric-value'>{matchup['sr']}</div></div>", unsafe_allow_html=True)
        with m_kpi5:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Batting Average</div><div class='metric-value'>{matchup['avg']}</div></div>", unsafe_allow_html=True)
        with m_kpi6:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Dot Balls (Dot %)</div><div class='metric-value'>{matchup['dots']} <span style='font-size:0.85rem;color:#94A3B8;'>({matchup['dot_pct']}%)</span></div></div>", unsafe_allow_html=True)

        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.markdown(f"#### **Shots Played by {sel_batter} vs {sel_bowler}**")
            if not matchup['shots_df'].empty:
                fig_h_shots = px.bar(
                    matchup['shots_df'], x='stroke', y='runs', color='balls',
                    title=f"Runs & Balls by Stroke in this Rivalry",
                    color_continuous_scale='Reds',
                    labels={'runs': 'Runs', 'stroke': 'Stroke Played', 'balls': 'Balls Faced'}
                )
                fig_h_shots.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_h_shots, width="stretch")
            else:
                st.info("No shot breakdown details available.")

        with col_h2:
            st.markdown(f"#### **Delivery Styles Bowled by {sel_bowler} to {sel_batter}**")
            if not matchup['styles_df'].empty:
                fig_h_styles = px.bar(
                    matchup['styles_df'], x='delivery_style', y='balls', color='runs',
                    title=f"Deliveries & Runs Conceded by Delivery Variation",
                    color_continuous_scale='Blues',
                    labels={'balls': 'Deliveries', 'delivery_style': 'Delivery Style', 'runs': 'Runs Conceded'}
                )
                fig_h_styles.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_h_styles, width="stretch")
            else:
                st.info("No delivery variation details available.")

        # Phase breakdown in this matchup
        if not matchup['phase_df'].empty:
            st.markdown("#### **Match Phase Breakdown in this Rivalry**")
            st.dataframe(matchup['phase_df'].rename(columns={
                'phase': 'Phase', 'balls': 'Balls', 'runs': 'Runs', 'dismissals': 'Dismissals',
                'dots': 'Dots', 'sr': 'Strike Rate'
            }), width="stretch", hide_index=True)

        # Complete Delivery by Delivery History Log
        st.markdown("---")
        st.markdown(f"#### **📜 Complete Delivery-by-Delivery Encounter Log ({sel_batter} vs {sel_bowler})**")
        
        col_flt1, col_flt2 = st.columns([2, 2])
        with col_flt1:
            log_filter = st.selectbox(
                "Filter Deliveries In Log:",
                ["All Deliveries", "Boundaries Only (4s & 6s)", "Wickets Only", "High Pressure Only (PI >= 0.60)"],
                index=0
            )

        log_display = matchup['log_df'].copy()
        if log_filter == "Boundaries Only (4s & 6s)":
            log_display = log_display[log_display['runs'] >= 4]
        elif log_filter == "Wickets Only":
            log_display = log_display[log_display['is_wicket'] == True]
        elif log_filter == "High Pressure Only (PI >= 0.60)":
            log_display = log_display[log_display['pressure_index'] >= 0.60]

        log_table = log_display[['match_date', 'comp_name', 'innings', 'over_display', 'stroke', 'delivery_style', 'on_or_off', 'runs', 'extras_type', 'is_wicket_label', 'dismissal_type', 'pressure_index']].rename(columns={
            'match_date': 'Date',
            'comp_name': 'Tournament',
            'innings': 'Inn',
            'over_display': 'Over.Ball',
            'stroke': 'Shot Played',
            'delivery_style': 'Delivery Type',
            'on_or_off': 'Ground Side',
            'runs': 'Runs',
            'extras_type': 'Extras',
            'is_wicket_label': 'Wicket?',
            'dismissal_type': 'Dismissal Mode',
            'pressure_index': 'Pressure Index'
        })
        st.dataframe(log_table, width="stretch", hide_index=True)


# ==============================================================================
# TAB 3: ARCHETYPES MATRIX
# ==============================================================================
elif nav == "🎯 Bowling Archetypes Matrix":
    st.markdown("### 🎯 Tactical Archetypes & Matchup Matrix")
    st.caption("Analyze how any batter handles 6+ bowling categories, or how any bowler performs across batter hands (RHB vs LHB) and bowling angles.")

    sub_arch = st.radio("Choose Tactical Matrix View:", ["Batter vs All Bowling Types", "Bowler vs Batter Hands (RHB vs LHB)"], horizontal=True)
    st.markdown("---")
    
    if sub_arch == "Batter vs All Bowling Types":
        default_b = "Virat Kohli" if "Virat Kohli" in engine.batter_names else engine.batter_names[0]
        sel_bat_arch = st.selectbox("Select Batter:", engine.batter_names, index=engine.batter_names.index(default_b))
        df_arch = engine.get_batter_splits(sel_bat_arch, "bowling_category", format_query)
        
        st.markdown(f"#### **{sel_bat_arch} vs All Bowling Archetypes ({format_filter}, 2022–2026)**")
        if not df_arch.empty:
            col_a1, col_a2 = st.columns([3, 2])
            with col_a1:
                fig_arch = px.bar(
                    df_arch, x='bowling_category', y='sr', color='runs',
                    title=f"{sel_bat_arch}: Strike Rate vs Bowling Archetypes",
                    color_continuous_scale='Viridis',
                    labels={'sr': 'Strike Rate', 'bowling_category': 'Bowling Archetype', 'runs': 'Runs Scored'}
                )
                fig_arch.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_arch, width="stretch")
            with col_a2:
                st.dataframe(df_arch[['bowling_category', 'runs', 'balls', 'dismissals', 'sr', 'avg', 'bnd_pct', 'dot_pct']].rename(columns={
                    'bowling_category': 'Archetype', 'runs': 'Runs', 'balls': 'Balls', 'dismissals': 'Outs',
                    'sr': 'SR', 'avg': 'Avg', 'bnd_pct': 'Bnd %', 'dot_pct': 'Dot %'
                }), width="stretch", hide_index=True)
        else:
            st.info("No archetype split data available for the active filter.")

    else:
        default_bw = "Jasprit Bumrah" if "Jasprit Bumrah" in engine.bowler_names else engine.bowler_names[0]
        sel_bowl_arch = st.selectbox("Select Bowler:", engine.bowler_names, index=engine.bowler_names.index(default_bw))
        df_bowl_hand = engine.get_bowler_splits(sel_bowl_arch, "batting_type", format_query)
        
        st.markdown(f"#### **{sel_bowl_arch} vs Right-Hand vs Left-Hand Batters ({format_filter})**")
        if not df_bowl_hand.empty:
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                fig_bh = px.bar(
                    df_bowl_hand, x='batting_type', y='econ', color='wickets',
                    title=f"{sel_bowl_arch}: Economy Rate vs RHB and LHB",
                    color_continuous_scale='Teal',
                    labels={'econ': 'Economy Rate', 'batting_type': 'Batter Hand', 'wickets': 'Wickets'}
                )
                fig_bh.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_bh, width="stretch")
            with col_b2:
                st.dataframe(df_bowl_hand[['batting_type', 'legal_balls', 'runs_conceded', 'wickets', 'econ', 'sr', 'dot_pct']].rename(columns={
                    'batting_type': 'Batter Hand', 'legal_balls': 'Balls', 'runs_conceded': 'Runs',
                    'wickets': 'Wkts', 'econ': 'Econ', 'sr': 'SR', 'dot_pct': 'Dot %'
                }), width="stretch", hide_index=True)
        else:
            st.info("No hand split data available for the active filter.")


# ==============================================================================
# TAB 4: PRESSURE RANKINGS & LEADERBOARDS
# ==============================================================================
elif nav == "🏆 Pressure Rankings & Leaderboards":
    lb = engine.get_leaderboard_data()
    df_top_bat = lb['top_bat']
    df_top_bowl = lb['top_bowl']
    df_all_bat = lb['all_bat']
    df_all_bowl = lb['all_bowl']
    paths = lb['paths']

    if active_scope == "ipl_2008_2026":
        st.markdown("### 🏆 SupeRR Pressure Reliability Rankings — Whole IPL (2008–2026)")
        st.caption("All-Time IPL History Rankings covering 19 seasons (1,243 matches, 295,732 deliveries) under Unified Bayesian Leverage Model ($PI \\ge 0.60$).")
        st.markdown(
            "<div style='background:rgba(217,22,128,0.15); border:1px solid #D91680; border-radius:10px; padding:12px 16px; margin-bottom:16px; font-size:0.9rem;'>"
            "👑 <b>All-Time IPL Historical Mode Active:</b> Evaluating all 19 seasons from 2008 to 2026. "
            "To review or submit rankings for the <b>Unstop dropdown challenge</b>, switch to <i>⚡ 2022–2026 (Official Challenge Dataset)</i> in the sidebar."
            "</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown("### 🏆 SupeRR Pressure Reliability Rankings — Official 2022–2026 Challenge")
        st.caption("Official Round 1 Challenge rankings & full database leaderboards based on our Unified Bayesian Leverage Model ($PI \\ge 0.60$).")
        st.markdown(
            "<div style='background:rgba(34,197,94,0.15); border:1px solid #22C55E; border-radius:10px; padding:12px 16px; margin-bottom:16px; font-size:0.9rem;'>"
            "🎯 <b>Official Challenge Mode Active:</b> These rankings directly populate the official Top 10 Batters & Bowlers dropdowns on Unstop."
            "</div>",
            unsafe_allow_html=True
        )

    tab_r1, tab_r2, tab_r3, tab_meth = st.tabs([
        "Top 10 Batters Under Pressure",
        "Top 10 Bowlers Under Pressure",
        f"📋 Full Database Leaderboards ({len(df_all_bat)}+ Qualified)",
        "📐 Mathematical Methodology & Architecture"
    ])
    
    with tab_r1:
        if not df_top_bat.empty:
            # Podium Highlights for Top 3 Batters
            p_col1, p_col2, p_col3 = st.columns(3)
            with p_col1:
                b1 = df_top_bat.iloc[0]
                st.markdown(f"""
                <div class='podium-card' style='border-color: #F59E0B;'>
                    <div style='font-size:2rem;'>🥇</div>
                    <div style='font-size:1.25rem; font-weight:800; color:#F59E0B;'>{b1['striker_name']}</div>
                    <div style='font-size:0.85rem; color:#94A3B8;'>SupeRR Rating: <b>{b1['pressure_rating']}</b></div>
                    <div style='font-size:0.9rem; margin-top:8px;'>HP SR: <b>{b1['sr_hp']}</b> (Δ +{b1['delta_sr']}) | Avg: <b>{b1['avg_hp']}</b></div>
                </div>
                """, unsafe_allow_html=True)
            with p_col2:
                b2 = df_top_bat.iloc[1]
                st.markdown(f"""
                <div class='podium-card' style='border-color: #E2E8F0;'>
                    <div style='font-size:2rem;'>🥈</div>
                    <div style='font-size:1.25rem; font-weight:800; color:#E2E8F0;'>{b2['striker_name']}</div>
                    <div style='font-size:0.85rem; color:#94A3B8;'>SupeRR Rating: <b>{b2['pressure_rating']}</b></div>
                    <div style='font-size:0.9rem; margin-top:8px;'>HP SR: <b>{b2['sr_hp']}</b> (Δ +{b2['delta_sr']}) | Avg: <b>{b2['avg_hp']}</b></div>
                </div>
                """, unsafe_allow_html=True)
            with p_col3:
                b3 = df_top_bat.iloc[2]
                st.markdown(f"""
                <div class='podium-card' style='border-color: #CD7F32;'>
                    <div style='font-size:2rem;'>🥉</div>
                    <div style='font-size:1.25rem; font-weight:800; color:#CD7F32;'>{b3['striker_name']}</div>
                    <div style='font-size:0.85rem; color:#94A3B8;'>SupeRR Rating: <b>{b3['pressure_rating']}</b></div>
                    <div style='font-size:0.9rem; margin-top:8px;'>HP SR: <b>{b3['sr_hp']}</b> (Δ +{b3['delta_sr']}) | Avg: <b>{b3['avg_hp']}</b></div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            disp_top_bat = df_top_bat[['rank', 'striker_name', 'balls_hp', 'runs_hp', 'sr_hp', 'sr_base', 'delta_sr', 'avg_hp', 'runs_added_per_100', 'cons_rate', 'pressure_rating']].rename(columns={
                'rank': 'Rank',
                'striker_name': 'Batter Name',
                'balls_hp': 'HP Balls',
                'runs_hp': 'HP Runs',
                'sr_hp': 'HP Strike Rate',
                'sr_base': 'Base SR',
                'delta_sr': 'Clutch Δ SR',
                'avg_hp': 'HP Average',
                'runs_added_per_100': 'Phase xRuns / 100',
                'cons_rate': 'Consistency',
                'pressure_rating': 'SupeRR Rating'
            })
            st.dataframe(disp_top_bat, width="stretch", hide_index=True)
            
            fig_top_b = px.bar(
                df_top_bat.sort_values('pressure_rating', ascending=True),
                x='pressure_rating', y='striker_name', orientation='h',
                color='sr_hp', color_continuous_scale='Reds',
                title=f"Top 10 Batters by SupeRR Pressure Reliability Rating ({'Whole IPL 2008-2026' if active_scope == 'ipl_2008_2026' else '2022-2026'})",
                labels={'pressure_rating': 'Rating (0-100)', 'striker_name': 'Player Name', 'sr_hp': 'HP Strike Rate'}
            )
            fig_top_b.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_top_b, width="stretch")

            csv_bat = df_top_bat.to_csv(index=False).encode('utf-8')
            st.download_button(f"📥 Download Top 10 Batters CSV ({paths['top_bat']})", csv_bat, paths['top_bat'], "text/csv")
        else:
            st.info("Run `python run_pipeline.py` to generate the top 10 rankings.")

    with tab_r2:
        if not df_top_bowl.empty:
            # Podium Highlights for Top 3 Bowlers
            pb_col1, pb_col2, pb_col3 = st.columns(3)
            with pb_col1:
                bw1 = df_top_bowl.iloc[0]
                st.markdown(f"""
                <div class='podium-card' style='border-color: #F59E0B;'>
                    <div style='font-size:2rem;'>🥇</div>
                    <div style='font-size:1.25rem; font-weight:800; color:#F59E0B;'>{bw1['bowler_name']}</div>
                    <div style='font-size:0.85rem; color:#94A3B8;'>SupeRR Rating: <b>{bw1['pressure_rating']}</b></div>
                    <div style='font-size:0.9rem; margin-top:8px;'>HP Econ: <b>{bw1['econ_hp']}</b> (Δ +{bw1['delta_econ']}) | xRuns Saved/Ov: <b>+{bw1['runs_saved_per_over']}</b></div>
                </div>
                """, unsafe_allow_html=True)
            with pb_col2:
                bw2 = df_top_bowl.iloc[1]
                st.markdown(f"""
                <div class='podium-card' style='border-color: #E2E8F0;'>
                    <div style='font-size:2rem;'>🥈</div>
                    <div style='font-size:1.25rem; font-weight:800; color:#E2E8F0;'>{bw2['bowler_name']}</div>
                    <div style='font-size:0.85rem; color:#94A3B8;'>SupeRR Rating: <b>{bw2['pressure_rating']}</b></div>
                    <div style='font-size:0.9rem; margin-top:8px;'>HP Econ: <b>{bw2['econ_hp']}</b> (Δ +{bw2['delta_econ']}) | xRuns Saved/Ov: <b>+{bw2['runs_saved_per_over']}</b></div>
                </div>
                """, unsafe_allow_html=True)
            with pb_col3:
                bw3 = df_top_bowl.iloc[2]
                st.markdown(f"""
                <div class='podium-card' style='border-color: #CD7F32;'>
                    <div style='font-size:2rem;'>🥉</div>
                    <div style='font-size:1.25rem; font-weight:800; color:#CD7F32;'>{bw3['bowler_name']}</div>
                    <div style='font-size:0.85rem; color:#94A3B8;'>SupeRR Rating: <b>{bw3['pressure_rating']}</b></div>
                    <div style='font-size:0.9rem; margin-top:8px;'>HP Econ: <b>{bw3['econ_hp']}</b> (Δ +{bw3['delta_econ']}) | xRuns Saved/Ov: <b>+{bw3['runs_saved_per_over']}</b></div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            disp_top_bowl = df_top_bowl[['rank', 'bowler_name', 'balls_hp', 'wkts_hp', 'econ_hp', 'econ_base', 'delta_econ', 'sr_hp', 'runs_saved_per_over', 'cons_rate', 'pressure_rating']].rename(columns={
                'rank': 'Rank',
                'bowler_name': 'Bowler Name',
                'balls_hp': 'HP Balls',
                'wkts_hp': 'HP Wkts',
                'econ_hp': 'HP Economy',
                'econ_base': 'Base Econ',
                'delta_econ': 'Clutch Δ Econ',
                'sr_hp': 'HP Bowling SR',
                'runs_saved_per_over': 'Phase xRuns Saved / Over',
                'cons_rate': 'Consistency',
                'pressure_rating': 'SupeRR Rating'
            })
            st.dataframe(disp_top_bowl, width="stretch", hide_index=True)
            
            fig_top_bw = px.bar(
                df_top_bowl.sort_values('pressure_rating', ascending=True),
                x='pressure_rating', y='bowler_name', orientation='h',
                color='econ_hp', color_continuous_scale='Blues_r',
                title=f"Top 10 Bowlers by SupeRR Pressure Reliability Rating ({'Whole IPL 2008-2026' if active_scope == 'ipl_2008_2026' else '2022-2026'})",
                labels={'pressure_rating': 'Rating (0-100)', 'bowler_name': 'Bowler Name', 'econ_hp': 'HP Economy'}
            )
            fig_top_bw.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_top_bw, width="stretch")

            csv_bowl = df_top_bowl.to_csv(index=False).encode('utf-8')
            st.download_button(f"📥 Download Top 10 Bowlers CSV ({paths['top_bowl']})", csv_bowl, paths['top_bowl'], "text/csv")
        else:
            st.info("Run `python run_pipeline.py` to generate the top 10 rankings.")

    with tab_r3:
        st.markdown(f"#### **Complete Qualified Players Leaderboards ({'Whole IPL 2008–2026' if active_scope == 'ipl_2008_2026' else '2022–2026 Challenge'})**")
        min_b = 150 if active_scope == 'ipl_2008_2026' else 120
        min_bw = 150
        sub_lb = st.radio("Select Leaderboard Discipline:", [f"Batters Leaderboard (Min {min_b} HP Balls)", f"Bowlers Leaderboard (Min {min_bw} HP Balls)"], horizontal=True)
        
        if "Batters" in sub_lb and not df_all_bat.empty:
            search_b = st.text_input("Filter / Search Batter:", "")
            disp_all_b = df_all_bat.copy()
            if search_b:
                disp_all_b = disp_all_b[disp_all_b['striker_name'].str.contains(search_b, case=False, na=False)]
            st.dataframe(
                disp_all_b[['rank', 'striker_name', 'balls_hp', 'runs_hp', 'sr_hp', 'avg_hp', 'delta_sr', 'runs_added_per_100', 'cons_rate', 'pressure_rating']].rename(columns={
                    'rank': 'Rank', 'striker_name': 'Player', 'balls_hp': 'HP Balls', 'runs_hp': 'HP Runs',
                    'sr_hp': 'HP SR', 'avg_hp': 'HP Avg', 'delta_sr': 'Delta SR', 'runs_added_per_100': 'xRuns/100',
                    'cons_rate': 'Consistency', 'pressure_rating': 'Rating'
                }),
                width="stretch", hide_index=True
            )
            st.download_button(f"📥 Download All Batters Rankings CSV ({paths['all_bat']})", df_all_bat.to_csv(index=False).encode('utf-8'), paths['all_bat'], "text/csv")

        elif "Bowlers" in sub_lb and not df_all_bowl.empty:
            search_bw = st.text_input("Filter / Search Bowler:", "")
            disp_all_bw = df_all_bowl.copy()
            if search_bw:
                disp_all_bw = disp_all_bw[disp_all_bw['bowler_name'].str.contains(search_bw, case=False, na=False)]
            st.dataframe(
                disp_all_bw[['rank', 'bowler_name', 'balls_hp', 'wkts_hp', 'econ_hp', 'sr_hp', 'delta_econ', 'runs_saved_per_over', 'cons_rate', 'pressure_rating']].rename(columns={
                    'rank': 'Rank', 'bowler_name': 'Player', 'balls_hp': 'HP Balls', 'wkts_hp': 'HP Wkts',
                    'econ_hp': 'HP Econ', 'sr_hp': 'HP Bowling SR', 'delta_econ': 'Delta Econ', 'runs_saved_per_over': 'xRuns Saved/Ov',
                    'cons_rate': 'Consistency', 'pressure_rating': 'Rating'
                }),
                width="stretch", hide_index=True
            )
            st.download_button(f"📥 Download All Bowlers Rankings CSV ({paths['all_bowl']})", df_all_bowl.to_csv(index=False).encode('utf-8'), paths['all_bowl'], "text/csv")

    with tab_meth:
        st.markdown("#### 📐 SupeRR Pressure Reliability Index (PRI) Mathematical Framework")
        st.markdown(r"""
        Our framework defines pressure continuously at the ball-by-ball level rather than relying on arbitrary over cutoffs:
        
        1. **Chasing Leverage Index ($LI$)**:
           $$LI = 4 \cdot WP \cdot (1 - WP)$$
           Derived from an empirical chase Win Probability logistic model ($AUC = 0.889$). Peak swing occurs at $WP = 0.50$ ($LI = 1.0$).
           
        2. **Required Run Rate Stress ($\Psi$)**:
           $$\Psi = \frac{RRR}{10.0}$$
           
        3. **Innings 1 Collapse Crises ($\Theta$)**:
           Evaluates resource scarcity when top-order wickets fall rapidly (e.g. 3 wickets down in first 6 overs).
           
        4. **Knockout Stage Multiplier**:
           Playoff, semifinal, and final deliveries receive an official $1.12\times$ high-stakes tournament multiplier.
           
        5. **High Pressure Threshold ($PI \ge 0.60$)**:
           Isolates the top 24.3% highest-stress moments (47,102 deliveries across official IPL 2022–2026 + T20I).
           
        6. **Empirical Bayes Shrinkage**:
           Stabilizes extreme sample sizes toward population priors ($\mu_{SR} = 142.42$, $\mu_{Econ} = 8.89$).
        """)
        
        docx_path = "final_submission/SuperRR_Final_Methodology_Report.docx" if os.path.exists("final_submission/SuperRR_Final_Methodology_Report.docx") else ("SuperRR_Final_Methodology_Report.docx" if os.path.exists("SuperRR_Final_Methodology_Report.docx") else "SupeRR_Selector_Methodology_Report.docx")
        if os.path.exists(docx_path):
            with open(docx_path, "rb") as f_docx:
                st.download_button(
                    label="📥 Download Formal Methodology Report (Word .docx)",
                    data=f_docx.read(),
                    file_name="SuperRR_Final_Methodology_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

        st.markdown("---")
        st.info("💡 **Exhaustive Data Dictionary & Formulas**: For the complete interactive 70-column delivery schema, 37 batting metrics, 35 bowling metrics, and step-by-step mathematical proofs, switch to **📖 Data Dictionary & Formula Reference** in the sidebar navigation!")


# ==============================================================================
# TAB 5: SHARE YOUR JOURNEY (REEL & POST FOR UNSTOP & RAJASTHAN ROYALS)
# ==============================================================================
elif nav == "🎬 Share Your Journey (Reel & Post)":
    st.markdown("### 🎬 Share Your Journey — Video Reel Script & Social Posts")
    st.caption("Official submission asset fulfilling Item 5 of the Rajasthan Royals & Unstop challenge requirements: Share one reel/post capturing your journey with #SuperSelector.")

    st.markdown(
        "<div style='background:rgba(217,22,128,0.15); border:1px solid #D91680; border-radius:10px; padding:14px 18px; margin-bottom:20px; font-size:0.92rem;'>"
        "👑 <b>Rajasthan Royals Requirement (Item 5):</b> "
        "<i>'Tell us how you approached the challenge, what inspired your methodology, or how you arrived at your solution. Best if you’re visible as well :) Share your reel on social media, tag Rajasthan Royals and Unstop, and use #SuperSelector.'</i>"
        "</div>",
        unsafe_allow_html=True
    )

    j_tab1, j_tab2, j_tab3, j_tab4, j_tab5 = st.tabs([
        "📱 60-Second Video Reel Script & Storyboard",
        "💼 LinkedIn Post Copy",
        "📸 Instagram Reel Caption",
        "🐦 X (Twitter) 5-Tweet Thread",
        "✅ Submission Readiness Checklist"
    ])

    with j_tab1:
        st.markdown("#### 📱 60-Second High-Energy Video Reel Script")
        st.caption("Designed for Instagram Reels, LinkedIn Video, or YouTube Shorts (9:16 vertical format). Ensure you are visible on camera!")
        
        st.markdown("""
        <div class="table-card" style="margin-bottom:16px;">
            <div style="font-weight:700; color:#F472B6; margin-bottom:8px;">[0:00 – 0:08] SCENE 1: THE HOOK (Direct to Camera)</div>
            <p><b>Visual:</b> Harsh looking directly into the camera, holding a cricket ball or sitting in front of the laptop displaying this Streamlit dashboard.</p>
            <p><b>On-Screen Text:</b> <i>What if everything you knew about 'Pressure' in the IPL was WRONG? 🏏💥</i></p>
            <p style="background:rgba(255,255,255,0.05); padding:10px; border-left:3px solid #D91680; border-radius:4px;">
            <b>Harsh (Speaking):</b> "Ask any cricket fan who the best pressure player in the IPL is, and they’ll give you a gut feeling. But as an analyst competing in Rajasthan Royals’ SupeRR Selector Season 2, gut feeling wasn’t going to cut it. I needed pure mathematical truth."
            </p>
        </div>

        <div class="table-card" style="margin-bottom:16px;">
            <div style="font-weight:700; color:#38BDF8; margin-bottom:8px;">[0:08 – 0:22] SCENE 2: THE PROBLEM & METHODOLOGY BREAKTHROUGH</div>
            <p><b>Visual:</b> Screen recording zooming into the Pressure Index formula ($PI \ge 0.60$), Win Probability Leverage, and Phase Expected Runs ($xRuns$).</p>
            <p><b>On-Screen Text:</b> <i>Pressure ≠ Just the 20th Over! 🧠📉</i></p>
            <p style="background:rgba(255,255,255,0.05); padding:10px; border-left:3px solid #38BDF8; border-radius:4px;">
            <b>Harsh (Speaking):</b> "Here’s what everyone gets wrong: Pressure isn’t just bowling the 20th over when defending 30 runs. That’s low leverage! Real pressure is being 3 down for 20 in the Powerplay, or needing 12 an over against elite spin. So, I built a Unified Bayesian Leverage Model across 295,000+ deliveries and all 19 seasons of IPL history, isolating every single high-pressure ball with a Pressure Index of 0.60 or higher!"
            </p>
        </div>

        <div class="table-card" style="margin-bottom:16px;">
            <div style="font-weight:700; color:#F59E0B; margin-bottom:8px;">[0:22 – 0:38] SCENE 3: THE TOP RANKINGS (2022–2026 CHALLENGE)</div>
            <p><b>Visual:</b> Dynamic screen recording showing the Top 10 Batters and Bowlers leaderboards in this dashboard.</p>
            <p><b>On-Screen Text:</b> <i>Top 10 Batters & Bowlers Under Pressure 👑📊</i></p>
            <p style="background:rgba(255,255,255,0.05); padding:10px; border-left:3px solid #F59E0B; border-radius:4px;">
            <b>Harsh (Speaking):</b> "And the results blew my mind! In modern cricket, Suryakumar Yadav is unmatched—striking at 177.5 with an 11-point elevation under fire. And the bowlers? It’s not pace that chokes teams—it’s mystery spin. Sunil Narine concedes an unreal 5.36 runs per over under pressure, saving over 3 runs every single over!"
            </p>
        </div>

        <div class="table-card" style="margin-bottom:16px;">
            <div style="font-weight:700; color:#A855F7; margin-bottom:8px;">[0:38 – 0:50] SCENE 4: HISTORICAL VALIDATION (19 SEASONS)</div>
            <p><b>Visual:</b> Toggling the sidebar to 'Whole IPL (2008–2026)' showing AB de Villiers and Lasith Malinga at #1.</p>
            <p><b>On-Screen Text:</b> <i>All-Time IPL Legends Validated 🏆</i></p>
            <p style="background:rgba(255,255,255,0.05); padding:10px; border-left:3px solid #A855F7; border-radius:4px;">
            <b>Harsh (Speaking):</b> "To stress-test my framework, I backtested it across 19 years of IPL history. And guess what? The model crowned AB de Villiers as the all-time clutch king with a 201 strike rate, and Lasith Malinga as the all-time pressure bowler. The math doesn't lie."
            </p>
        </div>

        <div class="table-card" style="margin-bottom:16px;">
            <div style="font-weight:700; color:#22C55E; margin-bottom:8px;">[0:50 – 1:00] SCENE 5: CALL TO ACTION & HALLA BOL</div>
            <p><b>Visual:</b> Harsh back on camera smiling, holding up phone showing the interactive dashboard and presentation deck.</p>
            <p><b>On-Screen Text:</b> <i>Check out my submission! #SuperSelector @rajasthanroyals @unstop</i></p>
            <p style="background:rgba(255,255,255,0.05); padding:10px; border-left:3px solid #22C55E; border-radius:4px;">
            <b>Harsh (Speaking):</b> "I’ve submitted my interactive dashboard, 10-slide executive deck, and formal whitepaper for Round 1 of SupeRR Selector. Pressure is a privilege—analytics makes it predictable. Halla Bol! 👑🔥"
            </p>
        </div>
        """, unsafe_allow_html=True)

    with j_tab2:
        st.markdown("#### 💼 LinkedIn Submission Post")
        st.caption("Professional, structured, thought-leadership post ready to copy and publish:")
        linkedin_text = (
            "🏏 \"Pressure is a privilege — analytics makes it predictable.\" 📊🔥\n\n"
            "I am thrilled to submit my Round 1 case study for Rajasthan Royals' SupeRR Selector Season 2, hosted on Unstop!\n\n"
            "The challenge: Identify the Top 10 Batters and Top 10 Bowlers who perform best under high pressure.\n\n"
            "Most cricket discussions treat \"pressure\" as a subjective vibe or simply equate it to death overs. But in modern T20 cricket, context is everything:\n"
            "• Defending 30 runs in the 20th over is NOT high pressure.\n"
            "• Being 25/3 in the 5th over chasing 190 IS extreme crisis pressure.\n\n"
            "To solve this rigorously, I engineered an end-to-end analytics platform powered by a Unified Bayesian Leverage Model:\n\n"
            "📐 1. Dynamic Pressure Index (PI): Reconstructing chronological ball-by-ball states across 200,999 deliveries (2022–2026) and 295,732 deliveries (Whole IPL 2008–2026). PI combines Win Probability Leverage (WPLI), exponential Required Run Rate stress, and collapse penalties, isolating the top 24% most clutch deliveries (PI ≥ 0.60).\n\n"
            "⚖️ 2. Phase-Adjusted Par (xRuns): Raw averages lie. Every delivery is benchmarked against phase-specific run expectations (Powerplay 7.8 vs Death 10.4 rpo) to calculate Runs Added and Runs Saved.\n\n"
            "🔬 3. Empirical Bayes Shrinkage & Consistency: Regressing small sample sizes toward population priors to eliminate flukes, scaled by game-to-game positive impact frequency.\n\n"
            "🏆 The Key Findings (2022–2026 Official Baseline):\n"
            "👑 Batters: Suryakumar Yadav (Rating 83.4 | 177.5 SR), Tim David (81.7 | 1,052 HP runs), Heinrich Klaasen (79.1 | spin dominator), Virat Kohli (77.8 | +37.9 SR elevation!), and Jos Buttler (77.6).\n"
            "🎯 Bowlers: Sunil Narine (Rating 84.3 | unreal 5.36 HP economy, saving 3.26 RPO), Varun Chakravarthy (75.1 | 6.47 Econ), Wanindu Hasaranga (73.3 | 43 HP wickets, 10.3 SR), Kuldeep Yadav (72.1), and Jasprit Bumrah (70.1 | 7.32 Econ).\n\n"
            "🌟 Historic Validation (19 Seasons of IPL):\n"
            "Backtesting against 1,243 matches naturally crowned AB de Villiers (All-time #1 batter, 201.4 SR) and Lasith Malinga (All-time #1 bowler, 11.8 SR, 69 HP wickets), proving model stability across two decades.\n\n"
            "📁 Full Submission Deliverables:\n"
            "1. Executive Slide Deck (.pptx)\n"
            "2. Formal Mathematical Report (.pdf)\n"
            "3. Interactive Streamlit Scouting Dashboard (with optical HawkEye tracking and live H2H matchup simulations)\n\n"
            "Huge thanks to Rajasthan Royals and Unstop for designing this visionary challenge. Halla Bol! 👑\n\n"
            "#SuperSelector #RajasthanRoyals #Unstop #CricketAnalytics #DataScience #SportsAnalytics #IPL #HallaBol #Python #MachineLearning"
        )
        st.text_area("LinkedIn Post Copy (Click inside, Ctrl+A, Ctrl+C to copy)", linkedin_text, height=340)

    with j_tab3:
        st.markdown("#### 📸 Instagram Caption")
        st.caption("Engaging, punchy caption for your video reel:")
        insta_text = (
            "What does \"PRESSURE\" actually look like in data? 🏏🧠📊\n\n"
            "Submitted my Round 1 case study for @rajasthanroyals SupeRR Selector Season 2 on @unstop!\n\n"
            "Instead of guessing, I crunched 295,000+ IPL deliveries and engineered a Bayesian Leverage Model (PI ≥ 0.60) to find the TOP 10 BATTERS & BOWLERS who elevate when the stakes are highest.\n\n"
            "👑 Top Batters: Suryakumar Yadav, Tim David, Heinrich Klaasen, Virat Kohli, Jos Buttler\n"
            "🎯 Top Bowlers: Sunil Narine, Varun Chakravarthy, Wanindu Hasaranga, Kuldeep Yadav, Jasprit Bumrah\n\n"
            "And all-time across 19 years of IPL? AB de Villiers (201.4 SR under pressure!) and Lasith Malinga take the crown. 🐐\n\n"
            "Swipe through to see the methodology, the interactive dashboard, and the data breakdowns.\n\n"
            "Halla Bol! 👑🔥\n\n"
            "#SuperSelector #RajasthanRoyals #Unstop #HallaBol #CricketAnalytics #IPL #ViratKohli #SuryakumarYadav #SunilNarine #SportsData #DataStorytelling"
        )
        st.text_area("Instagram Caption (Ctrl+A, Ctrl+C to copy)", insta_text, height=260)

    with j_tab4:
        st.markdown("#### 🐦 X (Twitter) 5-Tweet Thread")
        st.caption("Structured 5-tweet thread breaking down the methodology:")
        x_text = (
            "1/5 🧵 How do you mathematically quantify \"PRESSURE\" in T20 cricket?\n\n"
            "For Round 1 of @rajasthanroyals SupeRR Selector Season 2 on @Unstop, I analyzed 295,000+ deliveries across 19 IPL seasons to uncover the Top 10 Batters & Bowlers under fire.\n\n"
            "Here is the breakdown 👇 #SuperSelector #HallaBol\n\n"
            "2/5 📐 The Myth: Pressure = The 20th Over.\n"
            "Reality: Pressure is dynamic. A collapse at 20/3 in Over 4 has higher win-probability leverage than hitting 6 runs off 12 balls in Over 20.\n\n"
            "We built a Unified Pressure Index (PI ≥ 0.60) measuring Win Probability Leverage, RRR stress, and collapse risk.\n\n"
            "3/5 👑 Top 5 Batters Under Pressure (2022–2026):\n"
            "1. Suryakumar Yadav (Rating 83.4 | 177.5 SR, +11.1 ΔSR)\n"
            "2. Tim David (81.7 | 1,052 HP runs)\n"
            "3. Heinrich Klaasen (79.1 | spin crusher)\n"
            "4. Virat Kohli (77.8 | +37.9 ΔSR in chases!)\n"
            "5. Jos Buttler (77.6)\n\n"
            "4/5 🎯 Top 5 Bowlers Under Pressure (2022–2026):\n"
            "1. Sunil Narine (84.3 | 5.36 economy under fire!)\n"
            "2. Varun Chakravarthy (75.1 | 6.47 economy)\n"
            "3. Wanindu Hasaranga (73.3 | 43 HP wickets, 10.3 SR)\n"
            "4. Kuldeep Yadav (72.1)\n"
            "5. Jasprit Bumrah (70.1 | 7.32 death economy)\n\n"
            "5/5 🏆 Validation: When run across all 19 seasons of IPL (2008–2026), the model crowns AB de Villiers (201.4 SR) & Lasith Malinga (11.8 SR) as the all-time clutch GOATs.\n\n"
            "Complete dashboard + report + deck ready! Halla Bol! 👑🔥"
        )
        st.text_area("X Thread (Ctrl+A, Ctrl+C to copy)", x_text, height=280)

    with j_tab5:
        st.markdown("#### ✅ Official Unstop Submission Checklist")
        st.markdown("""
        Review this checklist before submitting on the Unstop portal:
        
        - [x] **Official Top 10 Batters Selected:** Suryakumar Yadav, Tim David, Heinrich Klaasen, Virat Kohli, Jos Buttler, Naman Dhir, Andre Russell, Rishabh Pant, Cameron Green, David Miller.
        - [x] **Official Top 10 Bowlers Selected:** Sunil Narine, Varun Chakravarthy, Wanindu Hasaranga, Kuldeep Yadav, Jasprit Bumrah, Axar Patel, Haris Rauf, Abrar Ahmed, Rashid Khan, Umran Malik.
        - [x] **PowerPoint Presentation Deck:** `SupeRR_Selector_Methodology_Presentation.pptx` (10 widescreen slides).
        - [x] **PDF Methodology Report:** `SupeRR_Selector_Methodology_Report.pdf` (4-page mathematical paper).
        - [x] **Word Document Report:** `SupeRR_Selector_Methodology_Report.docx`.
        - [x] **Interactive Dashboard:** `streamlit run app.py` running locally on `http://localhost:8501`.
        - [x] **Latest RR Data Pack Extracted:** `6afc28b07d034_6af458274c1e8_data_pack_1.zip` verified & merged with `IPL.csv`.
        - [ ] **Record & Post Reel:** Record 60-second video following Tab 1 script and post on LinkedIn/Instagram tagging `@rajasthanroyals` & `@unstop` with `#SuperSelector`!
        """)


# ==============================================================================
# TAB 6: DATA DICTIONARY, COLUMN LOGIC & MATHEMATICAL FORMULAS
# ==============================================================================
elif nav == "📖 Data Dictionary & Formula Reference":
    st.markdown("### 📖 Complete Data Dictionary, Mathematical Formulas & Column Logic")
    st.caption("Comprehensive technical reference for Rajasthan Royals: Complete schemas, statistical formulas, and tactical representations across all 142 variables in the platform.")

    df_del_dict = get_delivery_schema_df()
    df_bat_dict = get_batting_metrics_df()
    df_bowl_dict = get_bowling_metrics_df()

    dict_tab1, dict_tab2, dict_tab3, dict_tab4 = st.tabs([
        "📐 Mathematical Formulations & Architecture",
        "🏏 Ball-by-Ball Delivery Schema (70 Columns)",
        "🏏 Batting Metrics Glossary (37 Columns)",
        "🎯 Bowling Metrics Glossary (35 Columns)"
    ])

    with dict_tab1:
        st.markdown("#### 📐 Mathematical Architecture & Core Engine Formulations")
        st.caption("Step-by-step mathematical specifications for state reconstruction, Win Probability, Leverage Index, Pressure Index, Empirical Bayes Shrinkage, and composite Pressure Reliability Ratings (PRR).")

        # Mathematical Modules in Expanders
        with st.expander("1. ⏱️ Match State Reconstruction & Cumulative Metrics", expanded=True):
            st.markdown(r"""
            Every ball in the dataset represents a discrete chronological event $t$. Before calculating probability or pressure, all pre-delivery state variables are reconstructed strictly from historical information up to delivery $t-1$:
            
            * **Cumulative Team Runs ($R_{cum}$):**
              $$R_{cum, t} = \sum_{i=1}^{t-1} runs_{total, i}$$
              *Represents the running score on the team scoreboard prior to ball $t$.*
              
            * **Cumulative Team Wickets ($W_{cum}$):**
              $$W_{cum, t} = \sum_{i=1}^{t-1} \mathbb{I}(wicket_i)$$
              *Integer between 0 and 9; 10 wickets ends the innings.*
              
            * **Cumulative Legal Deliveries ($B_{legal}$):**
              $$B_{legal, t} = \sum_{i=1}^{t-1} \mathbb{I}(extras\_type_i \notin \{\text{'wide'}, \text{'Overstep'}\})$$
              
            * **Deliveries Remaining ($B_{rem}$):**
              $$B_{rem, t} = \max\left(1, B_{total} - B_{legal, t}\right)$$
              *Where $B_{total} = 120$ in standard T20s, or $6 \times \text{revised\_overs}$ in rain-curtailed fixtures.*
              
            * **Wickets in Hand ($W_{in\_hand}$):**
              $$W_{in\_hand, t} = \max(0, 10 - W_{cum, t})$$
              
            * **Runs Required in Chase ($R_{req}$):**
              $$R_{req, t} = \max(0, Target - R_{cum, t})$$
              *Where $Target = Inn1Total + 1$ (or official DLS / VJD revised target).*
              
            * **Required Run Rate ($RRR$):**
              $$RRR_t = \frac{R_{req, t}}{B_{rem, t}} \times 6.0$$
              
            * **Current Run Rate ($CRR$):**
              $$CRR_t = \frac{R_{cum, t}}{\max(1, B_{legal, t})} \times 6.0$$
            """)

        with st.expander("2. 📊 Dynamic Chase Win Probability ($WP$) & Leverage Index ($LI$)", expanded=True):
            st.markdown(r"""
            In modern analytics, pressure is fundamentally tied to the swing in winning equity. A delivery where a single ball swings match outcome by 30% carries far higher stakes than a delivery in a blowout.
            
            * **Innings 2 Logistic Win Probability ($WP$):**
              We model the real-time probability of the chasing side winning using multi-variable logistic regression:
              $$z_t = \beta_0 + \beta_1 \cdot R_{req, t} + \beta_2 \cdot B_{rem, t} + \beta_3 \cdot W_{in\_hand, t} + \beta_4 \cdot RRR_t$$
              $$WP_t = \sigma(z_t) = \frac{1}{1 + e^{-z_t}}$$
              *Model Validation:* Achieves $AUC = 0.889$ on historical T20 chases, with well-calibrated Brier score.
              
            * **Leverage Index ($LI$):**
              Leverage measures the sensitivity of the win probability function to the outcome of the current event. Following Tom Tango's formulation adapted for cricket:
              $$LI_t = 4.0 \cdot WP_t \cdot (1.0 - WP_t)$$
              
              * **Mathematical Properties of $LI$:**
                * $\mathbf{LI = 1.00}$ (Maximum Leverage): Occurs when $WP = 0.50$ (50-50 tossup match in the balance).
                * $\mathbf{LI = 0.36}$ (Low Leverage): Occurs when $WP = 0.90$ or $0.10$ (game heavily tilted).
                * $\mathbf{LI \to 0.00}$ (No Leverage): Occurs in blowouts where $WP \to 1.0$ or $WP \to 0.0$.
            """)

        with st.expander("3. 🎯 Pressure Index ($PI$) Synthesis & Thresholds", expanded=True):
            st.markdown(r"""
            Pressure is computed ball-by-ball on a continuous scale $[0.0, 1.0]$ by synthesizing leverage, run-rate stress, resource scarcity, match phase urgency, and tournament context:
            
            * **Innings 2 (Chasing Pressure):**
              $$S_{RRR} = \text{clip}\left(\frac{RRR - 6.0}{8.0}, 0.0, 1.0\right)$$
              $$S_{Wkt} = \text{clip}\left(\frac{6.0 - W_{in\_hand}}{5.0}, 0.0, 1.0\right)$$
              $$S_{Phase} = \left(\frac{\text{overid} - 1}{19.0}\right)^{1.2}$$
              $$PI_{inn2} = \left[ 0.40 \cdot LI + 0.30 \cdot (S_{RRR} \cdot S_{Phase}) + 0.20 \cdot (S_{Wkt} \cdot S_{RRR}) + 0.10 \cdot S_{Phase} \right] \times \Gamma_{stage}$$
              
            * **Innings 1 (Target Setting & Collapse Crises):**
              In the first innings, there is no fixed target, but teams experience pressure through match phase progression and catastrophic batting collapses:
              $$S_{Phase\_inn1} = \begin{cases} 0.70 + 0.05 \cdot (\text{overid} - 16) & \text{if } \text{overid} \ge 16 \text{ (Death Overs 16-20)} \\ 0.45 & \text{if } 7 \le \text{overid} \le 15 \text{ (Middle Overs)} \\ 0.35 & \text{if } \text{overid} \le 6 \text{ (Powerplay)} \end{cases}$$
              
              $$\Theta_{collapse} = \begin{cases} 
              0.25 + 0.10 \cdot (W_{cum} - 2) & \text{if } \text{overid} \le 6 \text{ and } W_{cum} \ge 2 \\ 
              0.20 + 0.08 \cdot (W_{cum} - 3) & \text{if } \text{overid} \le 10 \text{ and } W_{cum} \ge 3 \\ 
              0.20 & \text{if } \text{overid} \le 15 \text{ and } W_{cum} \ge 5 \\ 
              0.0 & \text{otherwise} 
              \end{cases}$$
              
              $$S_{Wkt\_inn1} = 0.15 \text{ if } W_{in\_hand} \le 3 \text{ else } 0.0$$
              $$PI_{inn1} = \left(S_{Phase\_inn1} + \Theta_{collapse} + S_{Wkt\_inn1}\right) \times \Gamma_{stage}$$
              
            * **Super Overs (Terminal Maximum Stress):**
              $$PI_{super} = 1.00$$
              
            * **Knockout Stage Multiplier ($\Gamma_{stage}$):**
              $$\Gamma_{stage} = \begin{cases} 1.12 & \text{if Qualifier, Eliminator, Semi-Final, or Final} \\ 1.00 & \text{if League Stage} \end{cases}$$
              
            * **High Pressure Delivery Cutoff:**
              $$\mathbb{I}_{HP} = \mathbb{I}(PI \ge 0.60)$$
              *Filters strictly the top ~24.3% highest-stress moments in the tournament (48,843 balls in 2022-26, 71,863 balls in all-time IPL).*
            """)

        with st.expander("4. ⚖️ Phase-Adjusted Context Par: Expected Runs, Runs Added & Runs Saved", expanded=True):
            st.markdown(r"""
            Raw strike rates and economies are inherently biased by over distributions: a batter batting purely in the death overs naturally records higher strike rates, while a bowler bowling in the powerplay faces field restrictions. We eliminate phase bias through empirical baseline expectations:
            
            * **Phase Par Expectation Matrix:**
              $$\bar{x}_{inn, over}^{bowl} = \mathbb{E}[bowler\_runs \mid innings, overid]$$
              $$\bar{x}_{inn, over}^{bat} = \mathbb{E}[runs_{bat} \mid innings, overid]$$
              
            * **Delivery-Level Value Added:**
              $$RunsSaved_t = \bar{x}_{inn, over}^{bowl} - bowler\_runs_t \quad (\text{for legal deliveries})$$
              $$RunsAdded_t = runs_{bat, t} - \bar{x}_{inn, over}^{bat} \quad (\text{for balls faced})$$
              
            * **Standardized Rate Metrics:**
              * **Runs Added per 100 Balls ($RA/100$):**
                $$RunsAdded/100 = \frac{\sum_{t \in HP} RunsAdded_t}{N_{balls\_hp}} \times 100.0$$
                *(Measures batter's run contribution above replacement par normalized per 100 deliveries).*
              * **Runs Saved per Over ($RS/Over$):**
                $$RunsSaved/Over = \frac{\sum_{t \in HP} RunsSaved_t}{N_{balls\_hp} / 6.0}$$
                *(Measures bowler's run suppression below phase par per 6 legal balls).*
            """)

        with st.expander("5. 🔬 Empirical Bayes Shrinkage Regularization", expanded=True):
            st.markdown(r"""
            To prevent small sample sizes from producing noisy, spuriously high or low ratings, all player rates under pressure are regularized toward tournament-wide population priors using Empirical Bayes shrinkage:
            
            * **Batting Strike Rate Shrinkage ($M=60, \mu_{SR}=142.42$):**
              $$SR_{Bayes} = \frac{N_{balls\_hp} \cdot SR_{HP} + M \cdot \mu_{SR}}{N_{balls\_hp} + M}$$
              
            * **Batting Average Shrinkage ($K=4, \mu_{Avg}=21.52$):**
              $$Avg_{Bayes} = \frac{Outs_{HP} \cdot Avg_{HP} + K \cdot \mu_{Avg}}{Outs_{HP} + K}$$
              
            * **Bowling Economy Shrinkage ($M=60, \mu_{Econ}=8.89$):**
              $$Econ_{Bayes} = \frac{N_{balls\_hp} \cdot Econ_{HP} + M \cdot \mu_{Econ}}{N_{balls\_hp} + M}$$
              
            * **Bowling Strike Rate Shrinkage ($K=4, \mu_{SR\_bowl}=15.94$):**
              $$SR_{Bayes}^{bowl} = \frac{Wkts_{HP} \cdot SR_{HP} + K \cdot \mu_{SR\_bowl}}{Wkts_{HP} + K}$$
            """)

        with st.expander("6. 📈 Match Consistency Rate ($CR$) & Sample Confidence ($W_{sample}$)", expanded=True):
            st.markdown(r"""
            Reliability under pressure is not merely high average performance across multiple years; it requires match-to-match consistency so team leadership can depend on the player in knockout scenarios.
            
            * **Match-to-Match Consistency Rate ($CR \in [0.0, 1.0]$):**
              Evaluates individual innings and spells with at least 5 deliveries under high pressure ($N_{HP} \ge 5$):
              * **Batting Positive Impact:**
                $$\mathbb{I}_{impact}^{bat} = \mathbb{I}(MatchRunsAdded > 0) \;\lor\; \mathbb{I}(MatchSR \ge 135.0)$$
              * **Bowling Positive Impact:**
                $$\mathbb{I}_{impact}^{bowl} = \mathbb{I}(MatchRunsSaved > 0) \;\lor\; \left(\mathbb{I}(MatchWkts \ge 1) \;\land\; \mathbb{I}(MatchEcon \le 8.50)\right)$$
              * **Consistency Score:**
                $$CR = \frac{1}{K_{meaningful}} \sum_{m=1}^{K_{meaningful}} \mathbb{I}_{impact, m}$$
                
            * **Sample Confidence Weight ($W_{sample} \in [0.0, 1.0]$):**
              An asymptotic volume penalty ensures players with massive, proven sample sizes are appropriately rewarded over those right at the qualification threshold:
              $$W_{sample}^{bat} = 1.0 - \exp\left(-\frac{N_{balls\_hp}}{150.0}\right)$$
              $$W_{sample}^{bowl} = 1.0 - \exp\left(-\frac{N_{balls\_hp}}{180.0}\right)$$
            """)

        with st.expander("7. 👑 Composite Pressure Reliability Rating ($PRR$) Master Formulations", expanded=True):
            st.markdown(r"""
            The final Pressure Reliability Rating ($PRR$) integrates standardized $Z$-scores across scoring power, average, clutch differentials, boundary-dot balance, and consistency, scaled to a 50-centered master index:
            
            ### **Batting Pressure Reliability Rating ($BPRR$):**
            $$Z_{scoring} = 0.60 \cdot \left(\frac{RunsAdded/100}{15.0}\right) + 0.40 \cdot \left(\frac{SR_{Bayes} - 142.42}{18.0}\right)$$
            $$Z_{avg} = \frac{Avg_{Bayes} - 21.52}{10.0}$$
            $$Z_{\Delta SR} = \frac{\Delta SR}{15.0} \quad \text{where } \Delta SR = SR_{HP} - SR_{Base}$$
            $$Z_{bnd\_dot} = \frac{Bnd\%_{HP} - 0.50 \cdot Dot\%_{HP} - 5.0}{6.0}$$
            $$Z_{cons} = \frac{CR - 0.50}{0.12}$$
            $$RawScore_{bat} = \left(0.35 \cdot Z_{scoring} + 0.25 \cdot Z_{avg} + 0.15 \cdot Z_{\Delta SR} + 0.10 \cdot Z_{bnd\_dot} + 0.15 \cdot Z_{cons}\right) \times W_{sample}^{bat}$$
            $$\mathbf{BPRR = 50.0 + 22.0 \cdot RawScore_{bat}}$$
            
            ---
            
            ### **Bowling Pressure Reliability Rating ($BowlerPRR$):**
            $$Z_{suppression} = 0.60 \cdot \left(\frac{RunsSaved/Over}{1.20}\right) + 0.40 \cdot \left(\frac{8.89 - Econ_{Bayes}}{1.20}\right)$$
            $$Z_{wkt} = \frac{15.94 - SR_{Bayes}^{bowl}}{4.0}$$
            $$Z_{\Delta Econ} = \frac{\text{clip}(\Delta Econ, -0.75, 2.0)}{1.0} \quad \text{where } \Delta Econ = Econ_{Base} - Econ_{HP}$$
            $$Z_{dot\_bnd} = \frac{Dot\%_{HP} - Bnd\%_{HP} - 15.0}{8.0}$$
            $$Z_{cons} = \frac{CR - 0.50}{0.12}$$
            $$RawScore_{bowl} = \left(0.35 \cdot Z_{suppression} + 0.25 \cdot Z_{wkt} + 0.15 \cdot Z_{\Delta Econ} + 0.10 \cdot Z_{dot\_bnd} + 0.15 \cdot Z_{cons}\right) \times W_{sample}^{bowl}$$
            $$\mathbf{BowlerPRR = 50.0 + 22.0 \cdot RawScore_{bowl}}$$
            
            * **Interpretation Scale:**
              * **$PRR \ge 80.0$:** Elite Tournament Match-Winner (e.g. Suryakumar Yadav 83.38, Sunil Narine 84.26, AB de Villiers 110.44).
              * **$70.0 \le PRR < 80.0$:** World-Class Pressure Performer (e.g. Heinrich Klaasen 79.12, Varun Chakravarthy 75.05).
              * **$60.0 \le PRR < 70.0$:** Highly Reliable Specialist (e.g. Riyan Parag 68.74, Jasprit Bumrah 68.21).
              * **$50.0 \le PRR < 60.0$:** Solid Tournament Average.
              * **$PRR < 50.0$:** Vulnerable / Negative Clutch Elevation under High Pressure.
            """)

    with dict_tab2:
        st.markdown("#### 🏏 Ball-by-Ball Delivery Schema (70 Columns)")
        st.caption("Exhaustive dictionary for every column in the master reconstructed delivery dataset (`cricket_master_2022_2026.parquet` and `cricket_master_ipl_2008_2026.parquet`).")

        d_col1, d_col2, d_col3, d_col4 = st.columns(4)
        with d_col1:
            st.markdown("""
            <div class='metric-card metric-card-gold'>
                <div class='metric-label'>Total Columns</div>
                <div class='metric-value'>70</div>
                <div style='font-size:0.75rem; color:#94A3B8;'>Full Reconstructed Schema</div>
            </div>
            """, unsafe_allow_html=True)
        with d_col2:
            st.markdown("""
            <div class='metric-card metric-card-blue'>
                <div class='metric-label'>Engineered State Variables</div>
                <div class='metric-value'>18</div>
                <div style='font-size:0.75rem; color:#94A3B8;'>Runs, Wkts, RRR, WP, PI</div>
            </div>
            """, unsafe_allow_html=True)
        with d_col3:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-label'>HawkEye Optical Variables</div>
                <div class='metric-value'>5</div>
                <div style='font-size:0.75rem; color:#94A3B8;'>Speed, Stroke, Style, Zones</div>
            </div>
            """, unsafe_allow_html=True)
        with d_col4:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-label'>High Pressure Share</div>
                <div class='metric-value'>24.3%</div>
                <div style='font-size:0.75rem; color:#94A3B8;'>Deliveries with PI ≥ 0.60</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        s_col1, s_col2 = st.columns([2, 1])
        with s_col1:
            search_del = st.text_input("🔍 Search Delivery Columns (Name, Description, Formula, Interpretation):", "")
        with s_col2:
            cats_del = ["All Categories (70 Columns)"] + sorted(list(df_del_dict['category'].unique()))
            cat_del = st.selectbox("Filter by Category:", cats_del)

        disp_del = df_del_dict.copy()
        if cat_del != "All Categories (70 Columns)":
            disp_del = disp_del[disp_del['category'] == cat_del]
        if search_del:
            q = search_del.lower()
            disp_del = disp_del[
                disp_del['column_name'].str.lower().str.contains(q, na=False) |
                disp_del['description'].str.lower().str.contains(q, na=False) |
                disp_del['formula'].str.lower().str.contains(q, na=False) |
                disp_del['interpretation'].str.lower().str.contains(q, na=False)
            ]

        st.markdown(f"**Showing {len(disp_del)} of 70 Columns:**")
        st.dataframe(
            disp_del[['column_name', 'category', 'data_type', 'description', 'representation', 'formula', 'interpretation']].rename(columns={
                'column_name': 'Column Name',
                'category': 'Category',
                'data_type': 'Data Type',
                'description': 'Description & Business Meaning',
                'representation': 'Representation / Units / Allowed Values',
                'formula': 'Mathematical Formula / Derivation',
                'interpretation': 'Tactical Interpretation & Role'
            }),
            width="stretch",
            hide_index=True
        )

        csv_del = df_del_dict.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Complete Delivery Schema CSV (70 Columns)", csv_del, "rr_delivery_schema_70_columns.csv", "text/csv")

        with st.expander("🔍 Live Master Dataset Inspector (Inspect 5 Real Deliveries)", expanded=False):
            st.caption(f"Inspecting active master dataset: **{len(engine.df):,} rows** ({'Whole IPL 2008-2026' if active_scope == 'ipl_2008_2026' else '2022-2026 Challenge Dataset'}).")
            selected_inspect_cols = st.multiselect(
                "Choose columns to display:",
                options=list(engine.df.columns),
                default=['match_date', 'comp_name', 'innings', 'overid', 'over_ball_num', 'striker_name', 'bowler_name', 'ball_runs', 'is_wicket', 'rrr', 'wp', 'pressure_index', 'is_high_pressure', 'runs_saved', 'runs_added']
            )
            st.dataframe(engine.df[selected_inspect_cols].head(10), width="stretch", hide_index=True)

    with dict_tab3:
        st.markdown("#### 🏏 Batting Metrics Glossary (37 Columns)")
        st.caption("Complete reference for all 37 aggregated batting metrics computed by the metrics and ranking engines (`all_qualified_batters_rankings.csv` and `top_10_batters_under_pressure.csv`).")

        b_col1, b_col2, b_col3, b_col4 = st.columns(4)
        with b_col1:
            st.markdown("""
            <div class='metric-card metric-card-gold'>
                <div class='metric-label'>Total Batting Metrics</div>
                <div class='metric-value'>37</div>
                <div style='font-size:0.75rem; color:#94A3B8;'>Aggregated Evaluator Columns</div>
            </div>
            """, unsafe_allow_html=True)
        with b_col2:
            st.markdown("""
            <div class='metric-card metric-card-blue'>
                <div class='metric-label'>Clutch Differentials</div>
                <div class='metric-value'>4</div>
                <div style='font-size:0.75rem; color:#94A3B8;'>Δ SR, Δ Avg, Δ Dot%, Δ Bnd%</div>
            </div>
            """, unsafe_allow_html=True)
        with b_col3:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-label'>Phase-Adjusted Par</div>
                <div class='metric-value'>xRuns Added</div>
                <div style='font-size:0.75rem; color:#94A3B8;'>Normalized per 100 balls</div>
            </div>
            """, unsafe_allow_html=True)
        with b_col4:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-label'>Bayesian Priors</div>
                <div class='metric-value'>M=60, K=4</div>
                <div style='font-size:0.75rem; color:#94A3B8;'>μ_SR = 142.42, μ_Avg = 21.52</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        sb_col1, sb_col2 = st.columns([2, 1])
        with sb_col1:
            search_bat = st.text_input("🔍 Search Batting Metrics:", "")
        with sb_col2:
            cats_bat = ["All Categories (37 Metrics)"] + sorted(list(df_bat_dict['category'].unique()))
            cat_bat = st.selectbox("Filter by Batting Category:", cats_bat)

        disp_bat = df_bat_dict.copy()
        if cat_bat != "All Categories (37 Metrics)":
            disp_bat = disp_bat[disp_bat['category'] == cat_bat]
        if search_bat:
            qb = search_bat.lower()
            disp_bat = disp_bat[
                disp_bat['column_name'].str.lower().str.contains(qb, na=False) |
                disp_bat['display_name'].str.lower().str.contains(qb, na=False) |
                disp_bat['formula'].str.lower().str.contains(qb, na=False) |
                disp_bat['interpretation'].str.lower().str.contains(qb, na=False)
            ]

        st.markdown(f"**Showing {len(disp_bat)} of 37 Batting Metrics:**")
        st.dataframe(
            disp_bat[['column_name', 'display_name', 'category', 'data_type', 'formula', 'interpretation']].rename(columns={
                'column_name': 'Column Name',
                'display_name': 'Display Name',
                'category': 'Category',
                'data_type': 'Data Type',
                'formula': 'Exact Mathematical Formula',
                'interpretation': 'Tactical Interpretation & Role'
            }),
            width="stretch",
            hide_index=True
        )

        csv_bat_dict = df_bat_dict.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Batting Metrics Glossary CSV (37 Columns)", csv_bat_dict, "rr_batting_metrics_glossary_37_columns.csv", "text/csv")

        with st.expander("👀 View Top 10 Batters Live Metric Values", expanded=False):
            lb_data = engine.get_leaderboard_data()
            if not lb_data['top_bat'].empty:
                st.dataframe(lb_data['top_bat'], width="stretch", hide_index=True)

    with dict_tab4:
        st.markdown("#### 🎯 Bowling Metrics Glossary (35 Columns)")
        st.caption("Complete reference for all 35 aggregated bowling metrics computed by the metrics and ranking engines (`all_qualified_bowlers_rankings.csv` and `top_10_bowlers_under_pressure.csv`).")

        bw_col1, bw_col2, bw_col3, bw_col4 = st.columns(4)
        with bw_col1:
            st.markdown("""
            <div class='metric-card metric-card-gold'>
                <div class='metric-label'>Total Bowling Metrics</div>
                <div class='metric-value'>35</div>
                <div style='font-size:0.75rem; color:#94A3B8;'>Aggregated Evaluator Columns</div>
            </div>
            """, unsafe_allow_html=True)
        with bw_col2:
            st.markdown("""
            <div class='metric-card metric-card-blue'>
                <div class='metric-label'>Clutch Differentials</div>
                <div class='metric-value'>4</div>
                <div style='font-size:0.75rem; color:#94A3B8;'>Δ Econ, Δ SR, Δ Dot%, Δ Bnd%</div>
            </div>
            """, unsafe_allow_html=True)
        with bw_col3:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-label'>Phase-Adjusted Par</div>
                <div class='metric-value'>xRuns Saved</div>
                <div style='font-size:0.75rem; color:#94A3B8;'>Normalized per over (6 balls)</div>
            </div>
            """, unsafe_allow_html=True)
        with bw_col4:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-label'>Bayesian Priors</div>
                <div class='metric-value'>M=60, K=4</div>
                <div style='font-size:0.75rem; color:#94A3B8;'>μ_Econ = 8.89, μ_SR = 15.94</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        sbw_col1, sbw_col2 = st.columns([2, 1])
        with sbw_col1:
            search_bowl = st.text_input("🔍 Search Bowling Metrics:", "")
        with sbw_col2:
            cats_bowl = ["All Categories (35 Metrics)"] + sorted(list(df_bowl_dict['category'].unique()))
            cat_bowl = st.selectbox("Filter by Bowling Category:", cats_bowl)

        disp_bowl = df_bowl_dict.copy()
        if cat_bowl != "All Categories (35 Metrics)":
            disp_bowl = disp_bowl[disp_bowl['category'] == cat_bowl]
        if search_bowl:
            qbw = search_bowl.lower()
            disp_bowl = disp_bowl[
                disp_bowl['column_name'].str.lower().str.contains(qbw, na=False) |
                disp_bowl['display_name'].str.lower().str.contains(qbw, na=False) |
                disp_bowl['formula'].str.lower().str.contains(qbw, na=False) |
                disp_bowl['interpretation'].str.lower().str.contains(qbw, na=False)
            ]

        st.markdown(f"**Showing {len(disp_bowl)} of 35 Bowling Metrics:**")
        st.dataframe(
            disp_bowl[['column_name', 'display_name', 'category', 'data_type', 'formula', 'interpretation']].rename(columns={
                'column_name': 'Column Name',
                'display_name': 'Display Name',
                'category': 'Category',
                'data_type': 'Data Type',
                'formula': 'Exact Mathematical Formula',
                'interpretation': 'Tactical Interpretation & Role'
            }),
            width="stretch",
            hide_index=True
        )

        csv_bowl_dict = df_bowl_dict.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Bowling Metrics Glossary CSV (35 Columns)", csv_bowl_dict, "rr_bowling_metrics_glossary_35_columns.csv", "text/csv")

        with st.expander("👀 View Top 10 Bowlers Live Metric Values", expanded=False):
            lb_data = engine.get_leaderboard_data()
            if not lb_data['top_bowl'].empty:
                st.dataframe(lb_data['top_bowl'], width="stretch", hide_index=True)

