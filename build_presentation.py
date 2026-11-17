"""
build_presentation.py
=====================
Generates the executive PowerPoint presentation (SupeRR_Selector_Methodology_Presentation.pptx)
for the Rajasthan Royals SupeRR Selector Season 2 Case Study submission by Harsh Panchal.
"""

import os
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Brand Colors (Rajasthan Royals Palette)
COLOR_BG_DARK = RGBColor(10, 20, 40)        # #0A1428 Deep Navy
COLOR_CARD = RGBColor(18, 32, 60)           # #12203C Card Navy
COLOR_CARD_BORDER = RGBColor(30, 50, 90)    # Border Navy
COLOR_RR_PINK = RGBColor(228, 0, 124)       # #E4007C RR Royal Pink
COLOR_GOLD = RGBColor(234, 179, 8)          # #EAB308 Gold
COLOR_WHITE = RGBColor(255, 255, 255)       # Pure White
COLOR_TEXT_MUTED = RGBColor(148, 163, 184)  # Slate Muted
COLOR_TEXT_LIGHT = RGBColor(226, 232, 240)  # Slate Light
COLOR_ROW_ALT = RGBColor(24, 42, 75)        # Table alternating row
COLOR_ACCENT_CYAN = RGBColor(56, 189, 248)  # Cyan accent


def set_slide_background(slide, color=COLOR_BG_DARK):
    """Sets slide solid dark background."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header(slide, title_text, category_text="RAJASTHAN ROYALS • SUPERR SELECTOR SEASON 2"):
    """Adds standard branded header to slide."""
    # Category / Super-title
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_RR_PINK

    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(24)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_WHITE


def add_card(slide, left, top, width, height, bg_color=COLOR_CARD, border_color=COLOR_CARD_BORDER):
    """Adds a stylish card container shape."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    return shape


def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Load ranking datasets
    bat_csv = "final_submission/Official_Top10_Batters_2022_2026.csv" if os.path.exists("final_submission/Official_Top10_Batters_2022_2026.csv") else "top_10_batters_under_pressure.csv"
    bowl_csv = "final_submission/Official_Top10_Bowlers_2022_2026.csv" if os.path.exists("final_submission/Official_Top10_Bowlers_2022_2026.csv") else "top_10_bowlers_under_pressure.csv"
    bat_ipl_csv = "final_submission/Historical_IPL_Top10_Batters_2008_2026.csv" if os.path.exists("final_submission/Historical_IPL_Top10_Batters_2008_2026.csv") else "top_10_batters_under_pressure_ipl_2008_2026.csv"
    bowl_ipl_csv = "final_submission/Historical_IPL_Top10_Bowlers_2008_2026.csv" if os.path.exists("final_submission/Historical_IPL_Top10_Bowlers_2008_2026.csv") else "top_10_bowlers_under_pressure_ipl_2008_2026.csv"

    bat_22 = pd.read_csv(bat_csv)
    bowl_22 = pd.read_csv(bowl_csv)
    bat_ipl = pd.read_csv(bat_ipl_csv)
    bowl_ipl = pd.read_csv(bowl_ipl_csv)

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, COLOR_BG_DARK)

    # Decorative background card
    add_card(slide1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg_color=COLOR_CARD, border_color=COLOR_RR_PINK)

    # Badge
    badge_box = slide1.shapes.add_textbox(Inches(1.3), Inches(1.2), Inches(10.7), Inches(0.4))
    tf_b = badge_box.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "RAJASTHAN ROYALS  |  SUPERR SELECTOR SEASON 2  |  ROUND 1 SUBMISSION"
    p_b.font.size = Pt(13)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_GOLD

    # Main Title
    title_box = slide1.shapes.add_textbox(Inches(1.3), Inches(1.7), Inches(10.7), Inches(1.8))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_t1 = tf_title.paragraphs[0]
    p_t1.text = "DECISION-MAKING UNDER FIRE"
    p_t1.font.size = Pt(40)
    p_t1.font.bold = True
    p_t1.font.color.rgb = COLOR_WHITE

    p_t2 = tf_title.add_paragraph()
    p_t2.text = "Quantifying Player Performance Under High Pressure in T20 Cricket"
    p_t2.font.size = Pt(22)
    p_t2.font.bold = True
    p_t2.font.color.rgb = COLOR_RR_PINK

    # Subtitle / Pillars
    desc_box = slide1.shapes.add_textbox(Inches(1.3), Inches(3.6), Inches(10.7), Inches(1.5))
    tf_desc = desc_box.text_frame
    tf_desc.word_wrap = True
    
    p_d1 = tf_desc.paragraphs[0]
    p_d1.text = "A Unified Bayesian Leverage Model (PI >= 0.60) evaluating Phase Par Values, Clutch Elevation, and Match Consistency across 19 IPL Seasons & Official Tracking Data."
    p_d1.font.size = Pt(15)
    p_d1.font.color.rgb = COLOR_TEXT_LIGHT

    # Metadata & Author Box
    meta_box = slide1.shapes.add_textbox(Inches(1.3), Inches(5.3), Inches(10.7), Inches(1.1))
    tf_meta = meta_box.text_frame
    p_m1 = tf_meta.paragraphs[0]
    p_m1.text = "Candidate: Harsh Panchal   |   Status: Completed Case Study   |   Platform: Unstop & Rajasthan Royals"
    p_m1.font.size = Pt(13)
    p_m1.font.bold = True
    p_m1.font.color.rgb = COLOR_ACCENT_CYAN

    p_m2 = tf_meta.add_paragraph()
    p_m2.text = "Deliverables: PowerPoint Deck (.pptx)  •  Formal Report (.pdf)  •  Interactive Web Dashboard (Streamlit localhost:8501)"
    p_m2.font.size = Pt(12)
    p_m2.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & KEY CLARIFICATIONS
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "Problem Statement & Strategic Framing")

    # Card 1: The Core Mandate
    add_card(slide2, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2))
    b1 = slide2.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(5.1), Inches(4.8))
    tf1 = b1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "Round 1 Core Mandate"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_RR_PINK

    points1 = [
        ("Identify Top 10 Batters", "Rank batters who objectively perform best when match leverage and stress are at their peak."),
        ("Identify Top 10 Bowlers", "Rank bowlers who excel at wicket-taking and boundary suppression under critical game pressure."),
        ("No Auction/Retention Constraint", "The goal is NOT team composition or auction value, but pure analytical valuation of clutch reliability."),
        ("Methodology-First Evaluation", "Success is judged on how we define pressure, how we reconstruct match state, and how we eliminate sample noise.")
    ]
    for title, desc in points1:
        p_sub = tf1.add_paragraph()
        p_sub.text = f"• {title}:"
        p_sub.font.size = Pt(13)
        p_sub.font.bold = True
        p_sub.font.color.rgb = COLOR_WHITE
        p_desc = tf1.add_paragraph()
        p_desc.text = f"  {desc}"
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = COLOR_TEXT_MUTED

    # Card 2: Datasets & Dual-Scope Architecture
    add_card(slide2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    b2 = slide2.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.1), Inches(4.8))
    tf2 = b2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "Dataset Architecture & Scope"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD

    points2 = [
        ("Scope A: Official Challenge Dataset (2022–2026)", "867 matches, 138 tournaments, 200,999 deliveries. Contains rich optical HawkEye tracking, speeds, delivery styles, and wagon wheels."),
        ("Scope B: Complete Whole IPL History (2008–2026)", "1,243 matches, 19 seasons, 295,732 deliveries. Complete all-time IPL dataset benchmarking modern stars against legends."),
        ("State Reconstruction", "Every delivery chronologically tracks cumulative score, wickets down, required run rate, balls remaining, and tournament context."),
        ("Multi-Modal Deliverables", "Executive PPT presentation, 4-page formal PDF report, and an interactive Streamlit scouting dashboard.")
    ]
    for title, desc in points2:
        p_sub = tf2.add_paragraph()
        p_sub.text = f"• {title}:"
        p_sub.font.size = Pt(13)
        p_sub.font.bold = True
        p_sub.font.color.rgb = COLOR_WHITE
        p_desc = tf2.add_paragraph()
        p_desc.text = f"  {desc}"
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 3: DEFINING PRESSURE — THE MATHEMATICAL MODEL
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "Defining Pressure: The Unified Pressure Index (PI)")

    # 3 Horizontal Cards
    card_w = Inches(3.7)
    card_h = Inches(4.5)
    
    # Pillar 1
    add_card(slide3, Inches(0.8), Inches(1.6), card_w, card_h)
    tb1 = slide3.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(3.3), Inches(4.1))
    t1 = tb1.text_frame
    t1.word_wrap = True
    p = t1.paragraphs[0]
    p.text = "1. Win Probability Leverage (WPLI)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_CYAN
    
    p = t1.add_paragraph()
    p.text = "\n• Dynamic State Tracking:\nEvaluates match state (balls left, runs needed, wickets lost) using a calibrated Logistic Win Probability Model."
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_LIGHT

    p = t1.add_paragraph()
    p.text = "\n• Swing Potential:\nWPLI measures the absolute delta between the best-case outcome (boundary/wicket) and worst-case outcome."
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_MUTED

    # Pillar 2
    add_card(slide3, Inches(4.8), Inches(1.6), card_w, card_h)
    tb2 = slide3.shapes.add_textbox(Inches(5.0), Inches(1.8), Inches(3.3), Inches(4.1))
    t2 = tb2.text_frame
    t2.word_wrap = True
    p = t2.paragraphs[0]
    p.text = "2. Contextual Stressors"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_RR_PINK
    
    p = t2.add_paragraph()
    p.text = "\n• RRR Exponential Surge:\nRequired Run Rate stress escalates non-linearly: RRR_stress = exp((RRR - 8.0) / 4.0)."
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_LIGHT

    p = t2.add_paragraph()
    p.text = "\n• Collapse & Resource Depletion:\nWickets fallen early create extreme pressure in overs 1-10 even if the required rate is modest."
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_MUTED

    # Pillar 3
    add_card(slide3, Inches(8.8), Inches(1.6), card_w, card_h)
    tb3 = slide3.shapes.add_textbox(Inches(9.0), Inches(1.8), Inches(3.3), Inches(4.1))
    t3 = tb3.text_frame
    t3.word_wrap = True
    p = t3.paragraphs[0]
    p.text = "3. Threshold & Synthesis"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    
    p = t3.add_paragraph()
    p.text = "\n• Composite Formula:\nPI = 0.50 * WPLI + 0.30 * RRR_stress + 0.20 * Collapse_stress (bounded [0, 1])."
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_LIGHT

    p = t3.add_paragraph()
    p.text = "\n• High Pressure Cutoff (PI >= 0.60):\nIsolates the top ~24% highest-stress deliveries in the match, eliminating low-stakes stat padding."
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_MUTED

    # Bottom Banner
    add_card(slide3, Inches(0.8), Inches(6.3), Inches(11.7), Inches(0.8), bg_color=COLOR_ROW_ALT)
    tbb = slide3.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.3), Inches(0.7))
    tbp = tbb.text_frame.paragraphs[0]
    tbp.text = "Empirical Finding: 48,788 out of 200,999 deliveries (24.3%) qualify as High Pressure (PI >= 0.60). Chases account for 61% of all high-pressure events."
    tbp.font.size = Pt(12)
    tbp.font.bold = True
    tbp.font.color.rgb = COLOR_WHITE

    # =========================================================================
    # SLIDE 4: PERFORMANCE EVALUATION FRAMEWORK
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Performance Evaluation: Beyond Basic Averages")

    # 4 Quadrants
    w_q = Inches(5.7)
    h_q = Inches(2.5)

    # Q1: Phase-Adjusted Par (xRuns)
    add_card(slide4, Inches(0.8), Inches(1.6), w_q, h_q)
    tb = slide4.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(2.3))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Pillar 1: Phase-Adjusted Par (xRuns)"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_ACCENT_CYAN
    p2 = tf.add_paragraph()
    p2.text = "Raw strike rates and economies are inherently biased by match phase (Powerplay 7.8 rpo vs Death 10.4 rpo). We baseline every single ball against its historical phase expected value (xRuns). Batters earn Runs Added above par; Bowlers earn Runs Saved below par."
    p2.font.size = Pt(11); p2.font.color.rgb = COLOR_TEXT_LIGHT

    # Q2: Relative Elevation (Delta Metrics)
    add_card(slide4, Inches(6.8), Inches(1.6), w_q, h_q)
    tb = slide4.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(2.3))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Pillar 2: Relative Elevation (Δ Metrics)"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_RR_PINK
    p2 = tf.add_paragraph()
    p2.text = "Does a player elevate or collapse under pressure? We compute Delta SR (SR_HP - SR_Normal) for batters and Delta Economy (Econ_Normal - Econ_HP) for bowlers. Elite performers (e.g. Kohli +37.9 SR, Narine +1.49 Econ) dramatically increase their output when pressure peaks."
    p2.font.size = Pt(11); p2.font.color.rgb = COLOR_TEXT_LIGHT

    # Q3: Empirical Bayes Shrinkage
    add_card(slide4, Inches(0.8), Inches(4.4), w_q, h_q)
    tb = slide4.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(5.3), Inches(2.3))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Pillar 3: Empirical Bayes Shrinkage"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_GOLD
    p2 = tf.add_paragraph()
    p2.text = "Small sample sizes create extreme outliers (e.g., a batter facing 20 balls with a 250 SR). We apply empirical Bayesian shrinkage: Shrunk_Metric = (N * Metric + M * Prior) / (N + M). This penalizes volatile flukes and ensures ratings reflect durable, repeatable talent."
    p2.font.size = Pt(11); p2.font.color.rgb = COLOR_TEXT_LIGHT

    # Q4: Match Impact Consistency Rate
    add_card(slide4, Inches(6.8), Inches(4.4), w_q, h_q)
    tb = slide4.shapes.add_textbox(Inches(7.0), Inches(4.5), Inches(5.3), Inches(2.3))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Pillar 4: Game-by-Game Consistency Rate"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_WHITE
    p2 = tf.add_paragraph()
    p2.text = "A clutch player cannot be a one-hit wonder. We calculate the percentage of high-pressure match appearances where the player generated positive net run value or took critical wickets. The composite Pressure Reliability Rating (PRR) integrates volume, efficiency, and consistency."
    p2.font.size = Pt(11); p2.font.color.rgb = COLOR_TEXT_LIGHT

    # =========================================================================
    # SLIDE 5: TOP 10 BATTERS UNDER PRESSURE (2022-2026)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "Official Rankings: Top 10 Batters Under Pressure (2022–2026)")

    # Left: Table (width 7.6)
    table_shape = slide5.shapes.add_table(11, 7, Inches(0.8), Inches(1.5), Inches(7.5), Inches(5.4))
    tbl = table_shape.table
    col_widths = [Inches(0.6), Inches(2.2), Inches(0.9), Inches(0.9), Inches(1.0), Inches(1.0), Inches(0.9)]
    for i, w in enumerate(col_widths):
        tbl.columns[i].width = w

    headers = ["Rank", "Batter", "HP Balls", "HP Runs", "HP SR", "Δ SR", "Rating"]
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_RR_PINK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    for i, row in bat_22.head(10).iterrows():
        cells = [
            f"#{int(row['rank'])}",
            str(row['striker_name']),
            f"{int(row['balls_hp'])}",
            f"{int(row['runs_hp'])}",
            f"{row['sr_hp']:.1f}",
            f"{row['delta_sr']:+.1f}",
            f"{row['pressure_rating']:.1f}"
        ]
        row_idx = i + 1
        for j, val in enumerate(cells):
            cell = tbl.cell(row_idx, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD if (i % 2 == 0) else COLOR_ROW_ALT
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_GOLD if j == 6 else COLOR_WHITE
            p.alignment = PP_ALIGN.LEFT if j == 1 else PP_ALIGN.CENTER

    # Right: Analytical Insights Box (width 4.0)
    add_card(slide5, Inches(8.6), Inches(1.5), Inches(3.9), Inches(5.4))
    tb = slide5.shapes.add_textbox(Inches(8.8), Inches(1.7), Inches(3.5), Inches(5.0))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Key Analytical Takeaways"
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_GOLD

    notes = [
        ("#1 Suryakumar Yadav (83.4)", "Supreme 360° geometry; scores at 177.5 SR in HP with a +11.1 elevation over baseline."),
        ("#2 Tim David (81.7)", "Death-over specialist with 1,052 HP runs; 81.5% match consistency under pressure."),
        ("#3 Heinrich Klaasen (79.1)", "Devastating spin destroyer; 175.5 HP SR and 36.7 average in critical middle/death overs."),
        ("#4 Virat Kohli (77.8)", "Master of chases; elevates strike rate by +37.9 in high pressure with a 43.5 average."),
        ("#5 Jos Buttler (77.6)", "Proven match-winner with +23.0 SR elevation and 544 HP runs in high leverage.")
    ]
    for name, desc in notes:
        p_n = tf.add_paragraph()
        p_n.text = f"\n• {name}:"
        p_n.font.size = Pt(11); p_n.font.bold = True; p_n.font.color.rgb = COLOR_WHITE
        p_d = tf.add_paragraph()
        p_d.text = f"  {desc}"
        p_d.font.size = Pt(10); p_d.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 6: TOP 10 BOWLERS UNDER PRESSURE (2022-2026)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "Official Rankings: Top 10 Bowlers Under Pressure (2022–2026)")

    # Left: Table (width 7.6)
    table_shape = slide6.shapes.add_table(11, 7, Inches(0.8), Inches(1.5), Inches(7.5), Inches(5.4))
    tbl = table_shape.table
    for i, w in enumerate(col_widths):
        tbl.columns[i].width = w

    headers_b = ["Rank", "Bowler", "HP Balls", "HP Wkts", "HP Econ", "Δ Econ", "Rating"]
    for j, h in enumerate(headers_b):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_ACCENT_CYAN
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_BG_DARK
        p.alignment = PP_ALIGN.CENTER

    for i, row in bowl_22.head(10).iterrows():
        cells = [
            f"#{int(row['rank'])}",
            str(row['bowler_name']),
            f"{int(row['balls_hp'])}",
            f"{int(row['wkts_hp'])}",
            f"{row['econ_hp']:.2f}",
            f"{row['delta_econ']:+.2f}",
            f"{row['pressure_rating']:.1f}"
        ]
        row_idx = i + 1
        for j, val in enumerate(cells):
            cell = tbl.cell(row_idx, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD if (i % 2 == 0) else COLOR_ROW_ALT
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_GOLD if j == 6 else COLOR_WHITE
            p.alignment = PP_ALIGN.LEFT if j == 1 else PP_ALIGN.CENTER

    # Right: Analytical Insights Box (width 4.0)
    add_card(slide6, Inches(8.6), Inches(1.5), Inches(3.9), Inches(5.4))
    tb = slide6.shapes.add_textbox(Inches(8.8), Inches(1.7), Inches(3.5), Inches(5.0))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Key Analytical Takeaways"
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_ACCENT_CYAN

    notes_b = [
        ("#1 Sunil Narine (84.3)", "Phenomenal 5.36 economy in HP (+1.49 better than baseline); 3.26 runs saved per over."),
        ("#2 Varun Chakravarthy (75.1)", "Elite mystery spin; 6.47 HP economy and +1.53 economy suppression under fire."),
        ("#3 Wanindu Hasaranga (73.3)", "Highest wicket taker in high pressure (43 wickets, 10.3 strike rate)."),
        ("#4 Kuldeep Yadav (72.1)", "Aggressive middle-over game changer; 37 HP wickets with 75% positive impact consistency."),
        ("#5 Jasprit Bumrah (70.1)", "Death over master; 7.32 HP economy across 553 balls; 2.36 runs saved per over.")
    ]
    for name, desc in notes_b:
        p_n = tf.add_paragraph()
        p_n.text = f"\n• {name}:"
        p_n.font.size = Pt(11); p_n.font.bold = True; p_n.font.color.rgb = COLOR_WHITE
        p_d = tf.add_paragraph()
        p_d.text = f"  {desc}"
        p_d.font.size = Pt(10); p_d.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 7: ALL-TIME IPL PERSPECTIVE (2008-2026, 19 SEASONS)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "Validation: All-Time IPL History (2008–2026, 19 Seasons)")

    # Left Card: Batters All-Time
    add_card(slide7, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.4))
    tb = slide7.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.3), Inches(5.2))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "All-Time IPL Batters (1,243 Matches)"
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_RR_PINK

    p_sub = tf.add_paragraph()
    p_sub.text = "Top 5 All-Time Legends Under Pressure:"
    p_sub.font.size = Pt(12); p_sub.font.bold = True; p_sub.font.color.rgb = COLOR_GOLD

    all_time_bats = [
        ("#1 AB de Villiers", "Rating 110.4 | 1,740 HP Runs | 201.4 SR | 48.3 Avg | +49.5 ΔSR"),
        ("#2 Andre Russell", "Rating 82.8 | 1,270 HP Runs | 184.9 SR | 31.8 Avg | +10.8 ΔSR"),
        ("#3 Rishabh Pant", "Rating 80.9 | 1,047 HP Runs | 173.1 SR | 36.1 Avg | +26.3 ΔSR"),
        ("#4 Heinrich Klaasen", "Rating 79.9 | 875 HP Runs | 173.6 SR | 36.5 Avg | +6.9 ΔSR"),
        ("#5 Tim David", "Rating 79.6 | 692 HP Runs | 182.6 SR | 34.6 Avg | +5.5 ΔSR")
    ]
    for name, stat in all_time_bats:
        p1 = tf.add_paragraph()
        p1.text = f"• {name}:"
        p1.font.size = Pt(11); p1.font.bold = True; p1.font.color.rgb = COLOR_WHITE
        p2 = tf.add_paragraph()
        p2.text = f"   {stat}"
        p2.font.size = Pt(10); p2.font.color.rgb = COLOR_TEXT_MUTED

    p_val = tf.add_paragraph()
    p_val.text = "\nValidation Insight: ABD's historic #1 standing confirms model validity—his ability to strike at 201.4 in pressure chases remains unmatched in T20 history."
    p_val.font.size = Pt(11); p_val.font.color.rgb = COLOR_TEXT_LIGHT

    # Right Card: Bowlers All-Time
    add_card(slide7, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    tb = slide7.shapes.add_textbox(Inches(7.0), Inches(1.6), Inches(5.3), Inches(5.2))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "All-Time IPL Bowlers (295,732 Balls)"
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_ACCENT_CYAN

    p_sub = tf.add_paragraph()
    p_sub.text = "Top 5 All-Time Legends Under Pressure:"
    p_sub.font.size = Pt(12); p_sub.font.bold = True; p_sub.font.color.rgb = COLOR_GOLD

    all_time_bowls = [
        ("#1 Lasith Malinga", "Rating 73.6 | 814 HP Balls | 69 Wkts | 11.8 SR | 7.64 Econ"),
        ("#2 Mitchell Starc", "Rating 72.4 | 321 HP Balls | 36 Wkts | 8.9 SR | 8.39 Econ"),
        ("#3 Sunil Narine", "Rating 70.3 | 1,108 HP Balls | 68 Wkts | 16.3 SR | 6.96 Econ"),
        ("#4 Piyush Chawla", "Rating 70.2 | 619 HP Balls | 43 Wkts | 14.4 SR | 7.09 Econ"),
        ("#5 Deepak Chahar", "Rating 69.8 | 285 HP Balls | 24 Wkts | 11.9 SR | 7.62 Econ")
    ]
    for name, stat in all_time_bowls:
        p1 = tf.add_paragraph()
        p1.text = f"• {name}:"
        p1.font.size = Pt(11); p1.font.bold = True; p1.font.color.rgb = COLOR_WHITE
        p2 = tf.add_paragraph()
        p2.text = f"   {stat}"
        p2.font.size = Pt(10); p2.font.color.rgb = COLOR_TEXT_MUTED

    p_val2 = tf.add_paragraph()
    p_val2.text = "\nValidation Insight: Lasith Malinga's #1 standing proves our model rewards strike power (11.8 balls/wicket) and yorker execution when matches hang in the balance."
    p_val2.font.size = Pt(11); p_val2.font.color.rgb = COLOR_TEXT_LIGHT

    # =========================================================================
    # SLIDE 8: EMPIRICAL EVIDENCE & VISUAL DIAGNOSTICS
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "Empirical Validation: Diagnostics & Charts")

    # Left: Embed Figure 1 (Pressure Index Distribution)
    add_card(slide8, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.4))
    tb = slide8.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.3), Inches(0.5))
    tb.text_frame.paragraphs[0].text = "Figure 1: Pressure Index (PI) Distribution"
    tb.text_frame.paragraphs[0].font.size = Pt(13)
    tb.text_frame.paragraphs[0].font.bold = True
    tb.text_frame.paragraphs[0].font.color.rgb = COLOR_WHITE
    if os.path.exists("figures/pressure_index_distribution.png"):
        slide8.shapes.add_picture("figures/pressure_index_distribution.png", Inches(1.0), Inches(2.2), Inches(5.3), Inches(2.3))

    tb_desc = slide8.shapes.add_textbox(Inches(1.0), Inches(4.7), Inches(5.3), Inches(2.0))
    tf_d = tb_desc.text_frame; tf_d.word_wrap = True
    p = tf_d.paragraphs[0]
    p.text = "Key Statistical Characteristics:\n• Bimodal distribution cleanly separates low-leverage cruise overs (PI 0.20-0.45) from high-stakes death/chase crisis overs (PI >= 0.60).\n• Innings 2 (Chasing) demonstrates significantly higher right-tail density."
    p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT_MUTED

    # Right: Embed Figure 4 (Top 10 Combined Rankings)
    add_card(slide8, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    tb = slide8.shapes.add_textbox(Inches(7.0), Inches(1.6), Inches(5.3), Inches(0.5))
    tb.text_frame.paragraphs[0].text = "Figure 4: Top 10 Batters & Bowlers Comparison"
    tb.text_frame.paragraphs[0].font.size = Pt(13)
    tb.text_frame.paragraphs[0].font.bold = True
    tb.text_frame.paragraphs[0].font.color.rgb = COLOR_WHITE
    if os.path.exists("figures/top_10_rankings_combined.png"):
        slide8.shapes.add_picture("figures/top_10_rankings_combined.png", Inches(7.0), Inches(2.2), Inches(5.3), Inches(2.3))

    tb_desc2 = slide8.shapes.add_textbox(Inches(7.0), Inches(4.7), Inches(5.3), Inches(2.0))
    tf_d2 = tb_desc2.text_frame; tf_d2.word_wrap = True
    p = tf_d2.paragraphs[0]
    p.text = "Key Statistical Characteristics:\n• Clear separation of tier-1 performers (Suryakumar & Narine > 80 rating) from steady performers.\n• Consistent performance across both volume of high-pressure deliveries and per-ball impact."
    p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 9: TACTICAL & STRATEGIC RECOMMENDATIONS FOR RR
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "Tactical Recommendations & In-Game Decision Support")

    # 3 Strategic Pillars
    w_p = Inches(3.7)
    h_p = Inches(5.2)

    # Pillar 1: Entry Point Optimization
    add_card(slide9, Inches(0.8), Inches(1.6), w_p, h_p)
    tb = slide9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(3.3), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "1. Entry Point Optimization"
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_RR_PINK
    points = [
        ("Deploy by Leverage, Not Overs", "Hold clutch anchors (Kohli, Buttler) for situations where PI >= 0.60 rather than fixed batting orders."),
        ("Shield Low-PI Vulnerabilities", "Players with negative ΔSR should be inserted during stable middle overs (PI < 0.40) to build momentum before pressure peaks."),
        ("Exploit Matchup Clusters", "Use optical wagon-wheel data to attack bowler quadrants during high-pressure death phases.")
    ]
    for t, d in points:
        p_t = tf.add_paragraph()
        p_t.text = f"\n• {t}:"
        p_t.font.size = Pt(11); p_t.font.bold = True; p_t.font.color.rgb = COLOR_WHITE
        p_d = tf.add_paragraph()
        p_d.text = f"  {d}"
        p_d.font.size = Pt(10); p_d.font.color.rgb = COLOR_TEXT_MUTED

    # Pillar 2: Dynamic Bowler Allocation
    add_card(slide9, Inches(4.8), Inches(1.6), w_p, h_p)
    tb = slide9.shapes.add_textbox(Inches(5.0), Inches(1.8), Inches(3.3), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "2. Dynamic Bowler Deployment"
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_ACCENT_CYAN
    points = [
        ("Break the Rigid 19th/20th Script", "Do not hold your best bowler (e.g. Bumrah, Narine) purely for the 19th over if a PI spike occurs in Over 13 or 14."),
        ("Attack with Mystery Spin in Crises", "Varun and Narine suppress boundaries in high pressure better than pure pace; deploy them when opponents chase > 10 rpo."),
        ("Wicket Aggression vs Economy", "Pair high-strike bowlers (Hasaranga, 10.3 SR) with economy suppressors (Axar, 6.8 Econ) in tandem.")
    ]
    for t, d in points:
        p_t = tf.add_paragraph()
        p_t.text = f"\n• {t}:"
        p_t.font.size = Pt(11); p_t.font.bold = True; p_t.font.color.rgb = COLOR_WHITE
        p_d = tf.add_paragraph()
        p_d.text = f"  {d}"
        p_d.font.size = Pt(10); p_d.font.color.rgb = COLOR_TEXT_MUTED

    # Pillar 3: Real-Time Dugout Simulation
    add_card(slide9, Inches(8.8), Inches(1.6), w_p, h_p)
    tb = slide9.shapes.add_textbox(Inches(9.0), Inches(1.8), Inches(3.3), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "3. Real-Time Dugout Analytics"
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_GOLD
    points = [
        ("Live Streamlit Dashboard", "Interactive web tool allows coaches to simulate batter vs bowler matchups live during match pauses."),
        ("Tactical Risk Profiling", "Simulate win-probability outcomes for alternative bowling choices when game leverage crosses 0.75."),
        ("Continuous Bayesian Updating", "Model adapts dynamically with every delivery bowled, maintaining live reliability indices.")
    ]
    for t, d in points:
        p_t = tf.add_paragraph()
        p_t.text = f"\n• {t}:"
        p_t.font.size = Pt(11); p_t.font.bold = True; p_t.font.color.rgb = COLOR_WHITE
        p_d = tf.add_paragraph()
        p_d.text = f"  {d}"
        p_d.font.size = Pt(10); p_d.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 10: DELIVERABLES & CONCLUSION
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, "Summary of Deliverables & Halla Bol!")

    # Left: Deliverables Checklist Card
    add_card(slide10, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.4))
    tb = slide10.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(5.1), Inches(5.0))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Complete Submission Package"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_GOLD

    delivs = [
        ("PowerPoint Deck (.pptx)", "SupeRR_Selector_Methodology_Presentation.pptx — 10 widescreen executive slides ready for presentation."),
        ("Formal PDF Report (.pdf)", "SupeRR_Selector_Methodology_Report.pdf — 4-page publication-grade whitepaper with mathematical formulations."),
        ("Interactive Dashboard (Streamlit)", "app.py — Complete scouting application with dual-scope switcher, HawkEye tracking, and simulations."),
        ("Clean CSV Datasets", "top_10_batters_under_pressure.csv & top_10_bowlers_under_pressure.csv exported for both scopes."),
        ("Share Your Journey Post & Reel", "Structured script and social copy crafted for #SuperSelector tagging Rajasthan Royals & Unstop.")
    ]
    for title, desc in delivs:
        p1 = tf.add_paragraph()
        p1.text = f"✓ {title}:"
        p1.font.size = Pt(12); p1.font.bold = True; p1.font.color.rgb = COLOR_WHITE
        p2 = tf.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(11); p2.font.color.rgb = COLOR_TEXT_MUTED

    # Right: Closing Philosophy Card
    add_card(slide10, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), bg_color=COLOR_CARD, border_color=COLOR_RR_PINK)
    tb = slide10.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.1), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Analytics Philosophy"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_RR_PINK

    quote = tf.add_paragraph()
    quote.text = '\n"Pressure is not a feeling to fear—it is an informational advantage to quantify."'
    quote.font.size = Pt(15); quote.font.bold = True; quote.font.color.rgb = COLOR_WHITE

    body = tf.add_paragraph()
    body.text = "\nBy decomposing match situations into dynamic leverage, phase-adjusted run value, and Bayesian reliability, we transform clutch performance from subjective folklore into objective competitive edge."
    body.font.size = Pt(12); body.font.color.rgb = COLOR_TEXT_LIGHT

    footer = tf.add_paragraph()
    footer.text = "\n\nSubmitted by Harsh Panchal\nRajasthan Royals SupeRR Selector Season 2 | Halla Bol! 👑🏏"
    footer.font.size = Pt(13); footer.font.bold = True; footer.font.color.rgb = COLOR_GOLD

    # Save presentation
    output_pptx = "SupeRR_Selector_Methodology_Presentation.pptx"
    prs.save(output_pptx)
    prs.save("final_submission/SupeRR_Selector_Methodology_Presentation.pptx")
    print(f"PowerPoint presentation generated successfully at: {output_pptx} and final_submission/{output_pptx}")


if __name__ == "__main__":
    create_presentation()
