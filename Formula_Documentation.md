# 📐 SupeRR Selector Season 2: Comprehensive Mathematical & Methodological Architecture

> **Author:** Harsh Panchal  
> **Platform:** Rajasthan Royals SupeRR Selector Season 2 (Round 1 Submission)  
> **Scope:** Official Challenge Dataset (IPL 2022–2026 + T20I 2022–2026) & Historical IPL (2008–2026)  
> **Status:** Fully Audited, Verified, and Reproducible  

---

## 1. Executive Summary of Methodology

The **SupeRR Pressure Reliability Rating (PRR)** framework is an end-to-end analytical architecture designed to evaluate cricketer performance under match-defining stress. Traditional cricket statistics (raw batting averages, raw strike rates, raw economies) fail fundamentally in high-pressure evaluation because they treat all deliveries as equal. Scoring 15 runs in a dead rubber where 50 runs are needed off 6 balls is rewarded identically to scoring 15 runs when 16 are needed off the final over of a tournament final.

Our framework solves this through a four-stage analytical pipeline:
1. **Dynamic Match-State Reconstruction:** State variables ($R_{req}, B_{rem}, W_{in\_hand}, CRR, RRR$) are reconstructed ball-by-ball strictly *prior* to delivery execution.
2. **Pressure Index Synthesis ($PI \in [0, 1]$):** Synthesizes Win Probability Leverage, exponential Required Run Rate stress, top-order collapse penalties, and tournament knockout multipliers. Deliveries with $PI \ge 0.60$ define the **High-Pressure Domain**.
3. **Phase-Adjusted Value Attribution ($xRuns$):** Evaluates every high-pressure delivery against the historical par run expectation for that specific over and innings, computing **Runs Added Above Par** for batters and **Runs Saved Below Par** for bowlers.
4. **Bayesian Shrinkage & Consistency Normalization:** Small-sample outliers are regressed toward empirical population priors using Empirical Bayes shrinkage, weighted by game-to-game positive impact consistency and sample confidence.

---

## 2. Chronological Match-State Reconstruction

For every delivery event $t$, match state is calculated prior to the ball outcome:

### State Variables:
- **Cumulative Team Runs:** 
  $$R_{cum, t} = \sum_{i=1}^{t-1} runs_{total, i}$$
- **Cumulative Wickets Lost:** 
  $$W_{cum, t} = \sum_{i=1}^{t-1} \mathbb{I}(wicket_i)$$
- **Cumulative Legal Balls Bowled:** 
  $$B_{legal, t} = \sum_{i=1}^{t-1} \mathbb{I}(is\_legal_i)$$
- **Balls Remaining in Innings:** 
  $$B_{rem, t} = \max(1, B_{total} - B_{legal, t})$$
  *(where $B_{total} = revised\_overs 	imes 6$ for curtailed matches, else $120$)*
- **Wickets in Hand:** 
  $$W_{in\_hand, t} = \max(0, 10 - W_{cum, t})$$
- **Target Score (Innings 2):** 
  $$	ext{Target} = egin{cases} revised\_target, & 	ext{if rain-curtailed} \ 	ext{Innings 1 Total} + 1, & 	ext{standard} \end{cases}$$
- **Runs Required (Innings 2):** 
  $$R_{req, t} = \max(0, 	ext{Target} - R_{cum, t})$$
- **Required Run Rate ($RRR_t$):** 
  $$RRR_t = rac{R_{req, t}}{B_{rem, t}} 	imes 6.0$$
- **Current Run Rate ($CRR_t$):** 
  $$CRR_t = rac{R_{cum, t}}{\max(1, B_{legal, t})} 	imes 6.0$$

---

## 3. Dynamic Pressure Index ($PI$) Formulation

### A. Innings 2 (The Run Chase)

Pressure in a chase is driven by win-probability volatility, required scoring velocity, and resource scarcity:

1. **Win Probability Model ($WP$):**
   A calibrated multivariate Logistic Regression model predicts the batting team's win probability from pre-ball state features:
   $$z_t = eta_0 + eta_1 \cdot R_{req, t} + eta_2 \cdot B_{rem, t} + eta_3 \cdot W_{in\_hand, t} + eta_4 \cdot RRR_t$$
   $$WP_t = rac{1}{1 + e^{-z_t}}$$

2. **Win Probability Leverage Index ($WPLI$):**
   Measuring swing potential between optimal and adverse delivery outcomes:
   $$LI_{WP, t} = 4.0 \cdot WP_t \cdot (1.0 - WP_t)$$
   *(Note: $LI_{WP} = 1.0$ when $WP = 0.50$ [maximum balance]; $LI_{WP} 	o 0$ when match is decided).*

3. **Required Run Rate Stress ($S_{RRR}$):**
   Linear-ramp transformation above baseline par rate ($6.0$ rpo):
   $$S_{RRR, t} = 	ext{clip}\left(rac{RRR_t - 6.0}{8.0}, 0.0, 1.0ight)$$

4. **Resource Scarcity Stress ($S_{wkt}$):**
   Penalizes resource depletion as wickets in hand drop below 6:
   $$S_{wkt, t} = 	ext{clip}\left(rac{6.0 - W_{in\_hand, t}}{5.0}, 0.0, 1.0ight)$$

5. **Innings Phase Weight ($S_{phase}$):**
   Power-law progression reflecting dwindling recovery windows as overs elapse:
   $$S_{phase, t} = \left(	ext{clip}\left(rac{overid_t - 1}{19.0}, 0.0, 1.0ight)ight)^{1.2}$$

6. **Tournament Knockout Multiplier ($KO_{mult}$):**
   $$KO_{mult} = egin{cases} 1.12, & 	ext{if Playoff, Qualifier, Eliminator, Semi-Final, or Final} \ 1.00, & 	ext{standard group-stage fixture} \end{cases}$$

7. **Composite Innings 2 Pressure Index ($PI_{inn2}$):**
   $$PI_{inn2, t} = \left(0.40 \cdot LI_{WP, t} + 0.30 \cdot S_{RRR, t} \cdot S_{phase, t} + 0.20 \cdot S_{wkt, t} \cdot S_{RRR, t} + 0.10 \cdot S_{phase, t}ight) 	imes KO_{mult}$$

---

### B. Innings 1 (Setting the Target)

In the first innings, pressure arises from target-setting velocity, death-over acceleration, and batting collapses:

1. **Phase Base Expectation:**
   $$	ext{phase\_base}_t = egin{cases} 0.70 + (over_t - 16) \cdot 0.05, & 	ext{if } over_t \ge 16 	ext{ (Death Overs)} \ 0.45, & 	ext{if } 7 \le over_t \le 15 	ext{ (Middle Overs)} \ 0.35, & 	ext{if } over_t \le 6 	ext{ (Powerplay)} \end{cases}$$

2. **Top-Order Collapse Penalty:**
   $$	ext{collapse\_bonus}_t = egin{cases} 0.25 + (W_{cum, t} - 2) \cdot 0.10, & 	ext{if } over_t \le 6 	ext{ and } W_{cum, t} \ge 2 \ 0.20 + (W_{cum, t} - 3) \cdot 0.08, & 	ext{if } over_t \le 10 	ext{ and } W_{cum, t} \ge 3 \ 0.20, & 	ext{if } over_t \le 15 	ext{ and } W_{cum, t} \ge 5 \ 0.00, & 	ext{otherwise} \end{cases}$$

3. **Tailender Resource Stress:**
   $$	ext{wkt\_pressure}_t = egin{cases} 0.15, & 	ext{if } W_{in\_hand, t} \le 3 \ 0.00, & 	ext{otherwise} \end{cases}$$

4. **Composite Innings 1 Pressure Index ($PI_{inn1}$):**
   $$PI_{inn1, t} = \left(	ext{phase\_base}_t + 	ext{collapse\_bonus}_t + 	ext{wkt\_pressure}_tight) 	imes KO_{mult}$$

### C. Super Overs
For all super overs ($innings \ge 3$), terminal maximum pressure is assigned:
$$PI_{super, t} = 1.00$$

### D. Final Boundary & Cutoff
$$PI_t = 	ext{clip}(PI_t, 0.0, 1.0)$$
$$	ext{High-Pressure Delivery} \iff PI_t \ge 0.60$$

Empirical validation shows that $PI \ge 0.60$ isolates **47,102 deliveries (24.3%)** of the official dataset.

---

## 4. Phase-Adjusted Expected Runs ($xRuns$)

Raw runs scored or conceded are inherently confounded by match phase (Powerplay historical par is $7.8$ rpo; Death over par is $10.4$ rpo). We baseline every delivery against phase-specific empirical expected values:

- **Expected Batting Runs ($E[R_{bat} \mid inn, over]$):**
  $$E[R_{bat}] = rac{1}{N_{inn, over}} \sum_{i \in \{inn, over\}} runs_{batter, i}$$
- **Runs Added Above Par (Batting):**
  $$RunsAdded_t = egin{cases} runs_{batter, t} - E[R_{bat} \mid inn_t, over_t], & 	ext{if legal batter ball} \ 0.0, & 	ext{wide delivery} \end{cases}$$
- **Runs Added per 100 Balls:**
  $$RunsAdded_{100} = \left(rac{\sum RunsAdded_{HP}}{Balls_{HP}}ight) 	imes 100.0$$

- **Expected Bowling Runs Conceded ($E[R_{bowl} \mid inn, over]$):**
  $$E[R_{bowl}] = rac{1}{N_{legal, inn, over}} \sum_{i \in \{legal, inn, over\}} runs_{bowler, i}$$
- **Runs Saved Below Par (Bowling):**
  $$RunsSaved_t = egin{cases} E[R_{bowl} \mid inn_t, over_t] - runs_{bowler, t}, & 	ext{if legal delivery} \ 0.0, & 	ext{illegal delivery} \end{cases}$$
- **Runs Saved per Over:**
  $$RunsSaved_{over} = rac{\sum RunsSaved_{HP}}{Balls_{HP} / 6.0}$$

---

## 5. Empirical Bayes Shrinkage

To prevent small sample sizes from dominating rankings (e.g., a batter scoring 28 off 10 balls with a 280 strike rate), we apply Empirical Bayes shrinkage toward population priors:

$$	heta_{bayes} = rac{N \cdot 	heta_{observed} + M \cdot \mu_{prior}}{N + M}$$

### Hyperparameters:
| Metric | Population Prior ($\mu$) | Shrinkage Weight ($M$ or $K$) | Unit |
| :--- | :---: | :---: | :---: |
| **Batting Strike Rate ($SR_{bayes}$)** | $142.42$ | $M = 60.0$ | Balls |
| **Batting Average ($Avg_{bayes}$)** | $21.52$ | $K = 4.0$ | Dismissals |
| **Bowling Economy ($Econ_{bayes}$)** | $8.89$ | $M = 60.0$ | Balls |
| **Bowling Strike Rate ($SR_{bowl, bayes}$)** | $15.94$ | $K = 4.0$ | Wickets |

---

## 6. Game-by-Game Consistency Rate ($ConsRate$)

A clutch performer must demonstrate repeatable game-to-game positive impact, not merely one or two massive statistical outliers.

- **Batting Consistency:**
  For all innings where the batter faced at least $5$ high-pressure deliveries:
  $$PositiveImpact_{bat, m} = \mathbb{I}\left(RunsAdded_m > 0 \;\lor\; SR_m \ge 135.0ight)$$
  $$ConsRate_{bat} = rac{1}{M_{innings}} \sum_{m=1}^{M_{innings}} PositiveImpact_{bat, m}$$

- **Bowling Consistency:**
  For all bowling spells where the bowler delivered at least $5$ high-pressure legal balls:
  $$PositiveImpact_{bowl, m} = \mathbb{I}\left(RunsSaved_m > 0 \;\lor\; (Wkts_m \ge 1 \;\land\; Econ_m \le 8.5)ight)$$
  $$ConsRate_{bowl} = rac{1}{M_{spells}} \sum_{m=1}^{M_{spells}} PositiveImpact_{bowl, m}$$

---

## 7. Sample Confidence Saturation ($SampleConf$)

To weight volume appropriately without establishing an arbitrary hard cliff:
$$SampleConf = 1.0 - \exp\left(-rac{Balls_{HP}}{150.0}ight)$$

- At $150$ HP balls: $SampleConf = 63.2\%$
- At $300$ HP balls: $SampleConf = 86.5\%$
- At $500$ HP balls: $SampleConf = 96.4\%$
- At $600+$ HP balls: $SampleConf > 98.0\%$

---

## 8. Final Composite SuperRR Pressure Reliability Rating (PRR)

### A. Batting Formula
1. **Standardized Sub-Indices:**
   - Scoring Velocity: $z_{scoring} = 0.60 \cdot \left(rac{RunsAdded_{100}}{15.0}ight) + 0.40 \cdot \left(rac{SR_{bayes} - 142.42}{18.0}ight)$
   - Wicket Preservation: $z_{avg} = rac{Avg_{bayes} - 21.52}{10.0}$
   - Relative Elevation: $z_{\Delta SR} = rac{\Delta SR}{15.0} = rac{SR_{HP} - SR_{base}}{15.0}$
   - Boundary-to-Dot Efficiency: $z_{bnd\_dot} = rac{BndPct_{HP} - 0.5 \cdot DotPct_{HP} - 5.0}{6.0}$
   - Consistency: $z_{cons} = rac{ConsRate - 0.50}{0.12}$

2. **Raw Composite Score:**
   $$RawScore_{bat} = \left(0.35 \cdot z_{scoring} + 0.25 \cdot z_{avg} + 0.15 \cdot z_{\Delta SR} + 0.10 \cdot z_{bnd\_dot} + 0.15 \cdot z_{cons}ight) 	imes SampleConf$$

3. **Final Linear Rescaling:**
   $$Rating_{bat} = 50.0 + RawScore_{bat} 	imes 22.0$$

---

### B. Bowling Formula
1. **Standardized Sub-Indices:**
   - Run Containment: $z_{suppression} = 0.60 \cdot \left(rac{RunsSaved_{over}}{1.20}ight) + 0.40 \cdot \left(rac{8.89 - Econ_{bayes}}{1.20}ight)$
   - Strike Lethality: $z_{wkt} = rac{15.94 - SR_{bowl, bayes}}{4.0}$
   - Relative Elevation: $z_{\Delta Econ} = rac{	ext{clip}(\Delta Econ, -0.75, 2.0)}{1.0}$ *(where $\Delta Econ = Econ_{base} - Econ_{HP}$; positive means stingier under pressure)*
   - Dot-to-Boundary Containment: $z_{dot\_bnd} = rac{DotPct_{HP} - BndPct_{HP} - 15.0}{8.0}$
   - Consistency: $z_{cons} = rac{ConsRate - 0.50}{0.12}$

2. **Raw Composite Score:**
   $$RawScore_{bowl} = \left(0.35 \cdot z_{suppression} + 0.25 \cdot z_{wkt} + 0.15 \cdot z_{\Delta Econ} + 0.10 \cdot z_{dot\_bnd} + 0.15 \cdot z_{cons}ight) 	imes SampleConf$$

3. **Final Linear Rescaling:**
   $$Rating_{bowl} = 50.0 + RawScore_{bowl} 	imes 22.0$$

---

## 9. Resolution of the Rating Scale & The AB de Villiers Phenomenon

### A. Mathematical Explanation of AB de Villiers (110.439 Rating)
In the historical IPL analysis across 19 seasons (1,243 matches), **AB de Villiers** achieved a calculated SuperRR Rating of **110.439**.

This occurs because the SuperRR Rating is **formally an unbounded standardized rating centered at 50.0 with a scaling factor of 22.0 per unit standard deviation of raw score**:
$$Rating = 50.0 + RawScore 	imes 22.0$$

For a player's rating to exceed 100.0, their composite $RawScore$ must exceed:
$$RawScore > rac{100.0 - 50.0}{22.0} = 2.273 	ext{ standard deviations above population mean}$$

AB de Villiers' historical metrics:
- $Balls_{HP} = 864$ (Sample confidence $= 99.7\%$)
- $Runs_{HP} = 1,740$
- $SR_{HP} = 201.39$ (vs Population prior $142.42$, delta $= +58.97$)
- $Avg_{HP} = 48.33$ (vs Population prior $21.52$, delta $= +26.81$)
- $\Delta SR = +49.50$ (Elevates his strike rate by almost 50 runs per 100 balls under pressure!)
- $RunsAdded_{100} = +51.06$ runs added above par per 100 deliveries

These astronomical statistics generated a composite $RawScore = +2.747$.  
Plugging this into the linear rescaling formula:
$$Rating_{ABD} = 50.0 + (2.747 	imes 22.0) = 110.439$$

### B. Correct Interpretation & Documentation
1. **The scale is NOT a closed 0–100 percentage.** It is a standardized index where:
   - **$50.0$** represents a replacement-level / average high-pressure performer.
   - **$65.0$ – $75.0$** represents high-quality tournament performers.
   - **$75.0$ – $85.0$** represents world-class elite performers (Suryakumar Yadav 83.4, Sunil Narine 84.3).
   - **$> 100.0$** represents historic, generational outliers across multiple eras (AB de Villiers 110.4).
2. **Comparability:** Official-period ratings (2022–2026) and Historical-period ratings (2008–2026) are calculated using identical formula architectures but calibrated against their respective era population baselines. Therefore, they should be presented side-by-side as distinct analytical scopes.
