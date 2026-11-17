# SupeRR Cricket Matchup & Player Intelligence Platform
### Rajasthan Royals Matchup Scouting & Analytics System (Dual-Scope: Whole IPL 2008–2026 & Official 2022–2026)

An advanced sports analytics platform powered by a Unified Bayesian Leverage Model ($PI \ge 0.60$), offering seamless switching between two extensive data scopes:
1. **Whole IPL History (2008–2026):** All **1,243 matches, 19 seasons, and 295,732 deliveries** covering the complete history of the Indian Premier League from inaugural match in 2008 to season 2026.
2. **2022–2026 Official Challenge Dataset:** Delivery-level records across **867 matches, 138 competitions, and 200,999 deliveries** in IPL and T20 Internationals with full optical HawkEye tracking (strokes, speeds, and wagon wheel ground directions).

---

## 🚀 Quick Start: Launch the Interactive Web Dashboard

The web app is powered by Streamlit and runs locally at:
👉 **[http://localhost:8501](http://localhost:8501)**

To launch or relaunch the web dashboard anytime:
```powershell
# Option 1: Double-click start_app.bat
.\start_app.bat

# Option 2: Run via PowerShell
.\start_app.ps1

# Option 3: Direct Streamlit command
streamlit run app.py
```

---

## 🎛️ Dual-Scope Data Selection in Web Dashboard

In the Streamlit sidebar, users can toggle between datasets with zero latency:
- **🏏 Whole IPL (2008–2026):**
  - **1,243 Matches | 19 Seasons | 295,732 Deliveries**
  - Full historical careers and splits for all-time IPL legends (AB de Villiers, Chris Gayle, Lasith Malinga, Shane Warne, Sachin Tendulkar, Suresh Raina) and modern stars (Virat Kohli, Rohit Sharma, MS Dhoni, Jasprit Bumrah).
  - All-time head-to-head encounters (e.g. Virat Kohli vs Lasith Malinga, MS Dhoni vs Sunil Narine).
  - All-time IPL Pressure Reliability Leaderboards.
- **⚡ 2022–2026 (Official Challenge Dataset):**
  - **867 Matches | 138 Competitions | 200,999 Deliveries**
  - Official Round 1 challenge submission baseline.
  - Full optical HawkEye ball tracking: Stroke Breakdown, Delivery Styles (Yorkers, Bouncers, Cutters), Bowling Speeds, and Wagon Wheel On-side vs Off-side sectors.
  - Official Top 10 Batters and Bowlers dropdown selections for the Unstop platform.

---

## 🌟 Key Platform Features

### 1. 👤 Comprehensive Player Profiles (Batting & Bowling)
- **Role Detection:** Automatically identifies whether a player is a pure Batter, Bowler, or All-Rounder.
- **Career KPIs:** Matches, Innings, Runs, Wickets, Average, Strike Rate, Economy, 50s, 100s, Dot %, Boundary %, Best Bowling.
- **Situational Splits:**
  - **Pace vs Spin:** Detailed table and comparison bar chart.
  - **Match Phases:** Powerplay (Overs 1–6), Middle (Overs 7–15), Death (Overs 16–20).
  - **Match Conditions:** 1st Innings (Setting) vs 2nd Innings (Chasing); High Pressure ($PI \ge 0.60$) vs Normal.
- **Optical HawkEye Metrics (2022–2026):**
  - Shot & Stroke Productivity (Cover Drive, Pull shot, Flick, Square Cut, Sweep, Slog, etc.).
  - Wagon Wheel Ground Sector (On-side vs Off-side donut distribution).
  - Specific Delivery Styles Faced/Bowled (Yorkers, Bouncers, Inswing, Outswing, Cutters, Googlies).

### 2. ⚔️ Head-to-Head Matchup Tool (ANY Batter vs ANY Bowler)
- Select **ANY batter** and **ANY bowler** from the active player registry (over 1,120+ players).
- **Matchup Scorecard:** Balls faced, runs scored, dismissals, strike rate, average, dot balls, fours, sixes.
- **Tactical Dominance Verdict:** Algorithmic verdict assessing matchup dominance.
- **Shot & Delivery Breakdown:** Specific strokes played and delivery variations bowled.
- **Complete Chronological Ball-by-Ball Encounter Log:** Full delivery table with date, tournament, over/ball, stroke, delivery style, runs, and dismissal events.

### 3. 🎯 Tactical Bowling Archetypes Matrix
- Evaluate any batter's productivity against:
  - Right-Arm Pace
  - Left-Arm Pace
  - Right-Arm Off-Spin
  - Right-Arm Leg-Spin / Wrist-Spin
  - Slow Left-Arm Orthodox
  - Left-Arm Wrist-Spin
- Evaluate any bowler's containment against **Right-Hand Batters (RHB)** vs **Left-Hand Batters (LHB)**.

### 4. 🏆 SupeRR Pressure Reliability Rankings
- **Official 2022–2026 Challenge Baseline (For Unstop Dropdowns):**
  - **Top 10 Batters:** Suryakumar Yadav, Tim David, Heinrich Klaasen, Virat Kohli, Jos Buttler, Naman Dhir, Andre Russell, Rishabh Pant, Cameron Green, David Miller.
  - **Top 10 Bowlers:** Sunil Narine, Varun Chakravarthy, Wanindu Hasaranga, Kuldeep Yadav, Jasprit Bumrah, Axar Patel, Haris Rauf, Abrar Ahmed, Rashid Khan, Umran Malik.
- **Whole IPL (2008–2026) All-Time Baseline:**
  - **Top 10 Batters:** AB de Villiers, Andre Russell, Rishabh Pant, Heinrich Klaasen, Tim David, Chris Gayle, JP Duminy, Virat Kohli, Sam Curran, Faf du Plessis.
  - **Top 10 Bowlers:** Lasith Malinga, Mitchell Starc, Sunil Narine, Piyush Chawla, Deepak Chahar, Nathan Coulter-Nile, Umran Malik, Rahul Chahar, Harbhajan Singh, Jasprit Bumrah.

### 5. 🎬 Share Your Journey (Reel Script & Social Media Posts)
- Official submission asset fulfilling Item 5 of the Rajasthan Royals & Unstop challenge requirements:
  - **60-Second Video Reel Script:** Timecoded visual cues, speaking lines, and b-roll instructions for Instagram Reels, LinkedIn Video, or YouTube Shorts.
  - **LinkedIn Post Copy:** Thought-leadership article text with one-click copy.
  - **Instagram Caption & X Thread:** Punchy, viral-ready captions with official tags (`@rajasthanroyals`, `@unstop`) and `#SuperSelector`.
  - **Submission Readiness Checklist:** Step-by-step verification of all Round 1 assets.

### 6. 📖 Interactive Data Dictionary & Formula Reference
- A dedicated, fully searchable reference interface in the web dashboard covering:
  - **All 70 Delivery-Level Columns:** Full definitions, data types, allowed ranges, units, and derivation sources.
  - **All 37 Batting Metrics:** Formulas, volume baselines, clutch differentials, Bayesian shrinkage, consistency, and composite PRR.
  - **All 35 Bowling Metrics:** Formulas, economy/SR suppression, phase-par expected runs saved, Bayesian shrinkage, consistency, and composite PRR.
  - **Mathematical Formulations & Architecture:** LaTeX equations and worked proofs for Win Probability, Leverage Index, and Pressure Index.
  - **Live Dataset Sample Inspector:** Real-time column selection and preview of active deliveries.
  - **CSV Export:** 1-click download of all three complete schema dictionaries.

---

## 📐 Mathematical Framework & Analytical Logic

### 1. Chronological Match State Reconstruction
For every delivery $t$, state variables are reconstructed strictly prior to delivery outcome:
- **Cumulative Team Runs:** $R_{cum, t} = \sum_{i=1}^{t-1} runs_{total, i}$
- **Cumulative Team Wickets:** $W_{cum, t} = \sum_{i=1}^{t-1} \mathbb{I}(wicket_i)$
- **Cumulative Legal Balls:** $B_{legal, t} = \sum_{i=1}^{t-1} \mathbb{I}(is\_legal_i)$
- **Balls Remaining:** $B_{rem, t} = \max(1, B_{total} - B_{legal, t})$
- **Wickets in Hand:** $W_{in\_hand, t} = \max(0, 10 - W_{cum, t})$
- **Runs Required (Innings 2):** $R_{req, t} = \max(0, Target - R_{cum, t})$
- **Required Run Rate:** $RRR_t = \frac{R_{req, t}}{B_{rem, t}} \times 6.0$
- **Current Run Rate:** $CRR_t = \frac{R_{cum, t}}{\max(1, B_{legal, t})} \times 6.0$

### 2. Dynamic Chase Win Probability ($WP$) & Leverage Index ($LI$)
- **Logistic Win Probability Model (Innings 2):**
  $$z_t = \beta_0 + \beta_1 \cdot R_{req, t} + \beta_2 \cdot B_{rem, t} + \beta_3 \cdot W_{in\_hand, t} + \beta_4 \cdot RRR_t$$
  $$WP_t = \frac{1}{1 + e^{-z_t}} \quad (AUC = 0.889)$$
- **Leverage Index ($LI$):**
  $$LI_t = 4.0 \cdot WP_t \cdot (1.0 - WP_t)$$
  *Peak leverage $LI = 1.0$ occurs at $WP = 0.50$ (50-50 tossup match in the balance).*

### 3. Continuous Pressure Index ($PI \in [0.0, 1.0]$)
- **Innings 2 (Chasing Pressure):**
  $$S_{RRR} = \text{clip}\left(\frac{RRR - 6.0}{8.0}, 0.0, 1.0\right), \quad S_{Wkt} = \text{clip}\left(\frac{6.0 - W_{in\_hand}}{5.0}, 0.0, 1.0\right), \quad S_{Phase} = \left(\frac{\text{overid} - 1}{19.0}\right)^{1.2}$$
  $$PI_{inn2} = \left[ 0.40 \cdot LI + 0.30 \cdot (S_{RRR} \cdot S_{Phase}) + 0.20 \cdot (S_{Wkt} \cdot S_{RRR}) + 0.10 \cdot S_{Phase} \right] \times \Gamma_{stage}$$
- **Innings 1 (Collapse Crisis & Phase Par):**
  $$PI_{inn1} = \left(S_{Phase\_inn1} + \Theta_{collapse} + S_{Wkt\_inn1}\right) \times \Gamma_{stage}$$
  where $\Theta_{collapse}$ captures early top-order collapses (e.g. 2+ wickets down in overs 1–6).
- **Super Overs:** $PI_{super} = 1.00$
- **Tournament Knockout Multiplier:** $\Gamma_{stage} = 1.12$ for Playoffs / Knockouts.
- **High Pressure Threshold:** $PI \ge 0.60$ (top 24.3% highest-stress moments).

### 4. Phase-Adjusted Context Par: Expected Runs, Runs Added & Saved
- **Expected Runs Par Matrix:**
  $$\bar{x}_{inn, over}^{bowl} = \mathbb{E}[bowler\_runs \mid innings, overid], \quad \bar{x}_{inn, over}^{bat} = \mathbb{E}[runs_{bat} \mid innings, overid]$$
- **Runs Added per 100 Balls ($RA/100$):**
  $$RA/100 = \frac{\sum_{t \in HP} (runs_{bat, t} - \bar{x}_{inn, over}^{bat})}{N_{balls\_hp}} \times 100.0$$
- **Runs Saved per Over ($RS/Over$):**
  $$RS/Over = \frac{\sum_{t \in HP} (\bar{x}_{inn, over}^{bowl} - bowler\_runs_t)}{N_{balls\_hp} / 6.0}$$

### 5. Empirical Bayes Shrinkage
- **Batting Strike Rate ($M=60, \mu_{SR}=142.42$):** $SR_{Bayes} = \frac{N_{HP} \cdot SR_{HP} + M \cdot \mu_{SR}}{N_{HP} + M}$
- **Batting Average ($K=4, \mu_{Avg}=21.52$):** $Avg_{Bayes} = \frac{Outs_{HP} \cdot Avg_{HP} + K \cdot \mu_{Avg}}{Outs_{HP} + K}$
- **Bowling Economy ($M=60, \mu_{Econ}=8.89$):** $Econ_{Bayes} = \frac{N_{HP} \cdot Econ_{HP} + M \cdot \mu_{Econ}}{N_{HP} + M}$
- **Bowling Strike Rate ($K=4, \mu_{SR\_bowl}=15.94$):** $SR_{Bayes}^{bowl} = \frac{Wkts_{HP} \cdot SR_{HP} + K \cdot \mu_{SR\_bowl}}{Wkts_{HP} + K}$

### 6. Composite Pressure Reliability Rating ($PRR$)
- **Batting PRR ($BPRR$):**
  $$RawScore_{bat} = \left[ 0.35 \cdot Z_{scoring} + 0.25 \cdot Z_{avg} + 0.15 \cdot Z_{\Delta SR} + 0.10 \cdot Z_{bnd\_dot} + 0.15 \cdot Z_{cons} \right] \times W_{sample}^{bat}$$
  $$BPRR = 50.0 + 22.0 \cdot RawScore_{bat}$$
- **Bowling PRR ($BowlerPRR$):**
  $$RawScore_{bowl} = \left[ 0.35 \cdot Z_{suppression} + 0.25 \cdot Z_{wkt} + 0.15 \cdot Z_{\Delta Econ} + 0.10 \cdot Z_{dot\_bnd} + 0.15 \cdot Z_{cons} \right] \times W_{sample}^{bowl}$$
  $$BowlerPRR = 50.0 + 22.0 \cdot RawScore_{bowl}$$

---

## 📊 Summary Data Dictionaries

### Delivery-Level Schema (70 Columns)
| Column Name | Category | Type | Description |
|---|---|---|---|
| `match_id` | Metadata | `int64` | Unique match identifier |
| `innings` | Metadata | `int64` | Innings index (1=Setting, 2=Chase, 3/4=Super Over) |
| `overid` | Match State | `int64` | 1-based over sequence number (1 to 20) |
| `over_ball_num` | Match State | `int64` | Sequential ball count in over |
| `innings_ball_num` | Match State | `int64` | Cumulative delivery number in innings |
| `batting_team_id` / `bowling_team_id` | Metadata | `int64` | Unique team IDs |
| `striker_id` / `bowler_id` | Metadata | `int64` | Unique player IDs |
| `striker_name` / `bowler_name` | Metadata | `object` | Standardized display names |
| `batting_type` / `bowling_type` | Profile | `object` | RHB/LHB, official bowling style |
| `runs`, `ball_runs`, `bowler_runs` | Outcomes | `int64` | Bat runs, total team runs, bowler-charged runs |
| `is_legal`, `is_batter_ball`, `is_bowler_wkt`| State | `bool` | Legality, batter faced, bowler-credited wicket |
| `bowl_speed`, `stroke`, `delivery_style` | HawkEye | `float`/`str` | Speed in km/h, shot type, delivery style variation |
| `on_or_off`, `over_or_around` | HawkEye | `object` | Wagon wheel sector (Offside/Onside), bowler angle |
| `cum_runs`, `cum_wkts`, `legal_balls` | State | `int64` | Running score & wickets prior to ball |
| `balls_rem`, `wkts_in_hand`, `runs_req` | State | `int64` | Chasing resources remaining before ball |
| `rrr`, `crr` | State | `float64` | Required Run Rate & Current Run Rate |
| `wp`, `pressure_index` | Pressure | `float64` | Logistic Win Probability & Pressure Index $\in [0, 1]$ |
| `is_high_pressure` | Pressure | `bool` | High Pressure indicator ($PI \ge 0.60$) |
| `exp_bowl_runs`, `exp_bat_runs` | Par | `float64` | Phase par baseline expectation for over |
| `runs_saved`, `runs_added` | Par | `float64` | Value added above/below phase par |
| `phase`, `bowling_category`, `pressure_tier` | Context | `object` | Match phase, bowling archetype, pressure tier |

### Batting Metrics Glossary (37 Columns)
Includes: `striker_id`, `striker_name`, `balls_base`, `runs_base`, `dismissals_base`, `dots_base`, `fours_base`, `sixes_base`, `matches_base`, `balls_hp`, `runs_hp`, `runs_added_hp`, `dismissals_hp`, `dots_hp`, `fours_hp`, `sixes_hp`, `matches_hp`, `sr_base`, `sr_hp`, `avg_base`, `avg_hp`, `bnd_pct_base`, `bnd_pct_hp`, `dot_pct_base`, `dot_pct_hp`, `delta_sr`, `delta_avg`, `delta_dot_pct`, `delta_bnd_pct`, `runs_added_per_100`, `sr_bayes`, `avg_bayes`, `cons_rate`, `meaningful_hp_innings`, `sample_conf`, `pressure_rating`, `rank`.

### Bowling Metrics Glossary (35 Columns)
Includes: `bowler_id`, `bowler_name`, `balls_base`, `runs_base`, `wkts_base`, `dots_base`, `boundaries_base`, `matches_base`, `balls_hp`, `runs_hp`, `runs_saved_hp`, `wkts_hp`, `dots_hp`, `boundaries_hp`, `matches_hp`, `econ_base`, `econ_hp`, `sr_base`, `sr_hp`, `dot_pct_base`, `dot_pct_hp`, `bnd_pct_base`, `bnd_pct_hp`, `delta_econ`, `delta_sr`, `delta_dot_pct`, `delta_bnd_pct`, `runs_saved_per_over`, `econ_bayes`, `sr_bayes`, `cons_rate`, `meaningful_hp_spells`, `sample_conf`, `pressure_rating`, `rank`.

---

---

## 📁 Repository Structure

```
RR/
├── app.py                                              # Master Streamlit web dashboard
├── start_app.bat                                       # 1-click batch launcher
├── start_app.ps1                                       # 1-click PowerShell launcher
├── run_pipeline.py                                     # Dual-scope end-to-end pipeline script
├── build_presentation.py                               # PowerPoint deck builder (python-pptx)
├── SupeRR_Selector_Methodology_Presentation.pptx       # Executive PowerPoint submission deck (10 widescreen slides)
├── SupeRR_Selector_Methodology_Report.pdf              # Formal PDF submission report (4-page mathematical paper)
├── SupeRR_Selector_Methodology_Report.docx             # Word document submission report
├── SHARE_YOUR_JOURNEY_SCRIPT_AND_POSTS.md             # Reel script, LinkedIn post, Instagram & X copy (#SuperSelector)
├── top_10_batters_under_pressure.csv                   # Official 2022-2026 Top 10 Batters
├── top_10_bowlers_under_pressure.csv                   # Official 2022-2026 Top 10 Bowlers
├── all_qualified_batters_rankings.csv                  # Official 2022-2026 Qualified Batters
├── all_qualified_bowlers_rankings.csv                  # Official 2022-2026 Qualified Bowlers
├── top_10_batters_under_pressure_ipl_2008_2026.csv     # Whole IPL (2008-2026) Top 10 Batters
├── top_10_bowlers_under_pressure_ipl_2008_2026.csv     # Whole IPL (2008-2026) Top 10 Bowlers
├── all_qualified_batters_rankings_ipl_2008_2026.csv    # Whole IPL (2008-2026) Qualified Batters
├── all_qualified_bowlers_rankings_ipl_2008_2026.csv    # Whole IPL (2008-2026) Qualified Bowlers
├── data/
│   ├── cricket_master_2022_2026.parquet               # High-speed precomputed 2022-2026 dataset
│   ├── cricket_master_ipl_2008_2026.parquet           # High-speed precomputed Whole IPL dataset
│   └── cricket_master.parquet                         # Master Parquet database cache
├── src/
│   ├── data_engine.py                                  # Query & retrieval engine for dual scopes
│   ├── pressure_engine.py                              # State reconstruction & Pressure Index synthesis
│   ├── metrics_engine.py                               # Expected runs, Bayesian shrinkage & consistency
│   ├── ranking_engine.py                               # Composite pressure rating formulas
│   ├── visualization.py                                # Publication chart generator
│   └── report_generator.py                             # Automated PDF & DOCX report compiler
└── figures/                                            # Generated publication charts (PNG)
```
