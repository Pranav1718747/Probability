# BMAT202 DA3: Scientific Academic Poster Content (Editable Source)
**Title:** Can a Chi-Square Test Catch Fake Numbers?  
**Subtitle:** Detecting Data Fabrication Using Benford's Law and Pearson's Goodness-of-Fit Analysis  
**Course:** BMAT202 – Probability and Statistics (Module 6: Hypothesis Testing-II)  
**Institution:** Vellore Institute of Technology (VIT), Chennai  
**Date:** 22 October 2026  
**Format:** A1 Landscape ($841\text{ mm} \times 594\text{ mm}$)  
**Deliverables:** `poster/BMAT202_DA3_Poster.pdf` and `poster/BMAT202_DA3_Poster.png`

---

### Panel 1: Real-Life Problem & Significance
- **The Challenge:** Millions of journal entries and tax returns make comprehensive manual auditing impossible. Fraudsters routinely fabricate numbers to cover shortfalls or pad expenses.
- **The Psychological Conflict:** Natural growth processes follow logarithmic scales, whereas humans inventing numbers instinctively distribute digits uniformly (~11.1% each) and avoid repeating digit 1.
- **Project Goal:** Leverage an undergraduate hypothesis test ($\chi^2$ goodness-of-fit) to establish an automated, non-invasive triage tool for detecting fabricated numerical records.

---

### Panel 2: Theoretical Concepts & Hypotheses
- **Benford's Law:** In naturally occurring unconstrained data spanning multiple orders of magnitude, the probability of leading digit $d \in \{1, \dots, 9\}$ is:
  $$P(d) = \log_{10}\left(1 + \frac{1}{d}\right)$$
  (Digit 1: 30.1% | Digit 2: 17.6% | Digit 3: 12.5% ... Digit 9: 4.6%)
- **Hypotheses:**
  - $H_0$: First-digit distribution follows Benford's Law.
  - $H_1$: First-digit distribution departs from Benford's Law.
- **Test Statistic:**
  $$\chi^2 = \sum_{i=1}^9 \frac{(O_i - E_i)^2}{E_i}, \quad E_i = n \cdot P(i)$$
- **Degrees of Freedom:** $df = 9 - 1 - 0 = 8$ (no parameters estimated from sample).
- **Critical Value ($\alpha = 0.05, df = 8$):** $\chi^2_{\text{crit}} = 15.507$.
- **Cochran's Condition:** $E_i \ge 5$ for all bins $\implies n \ge 110$. World Bank $n = 217$ yields $E_9 = 9.93 > 5.0$ (Passed).

---

### Panel 3: Methodology & Audit Screening Workflow
1. **Suitability & Boundary Check:** Verify positive, ratio scale, $\ge 3$ orders of magnitude (no exam scores / IDs).
2. **Digit Extraction:** Standardized `formatC(abs(x), "e")` isolates leading digit $d \in \{1, \dots, 9\}$ without error.
3. **Dual Goodness-of-Fit Evaluation:** Calculate $\chi^2$ ($df = 8$, $p$-value) and scale-free Mean Absolute Deviation (MAD).
4. **Automated Risk Triage:** Green Queue ($\chi^2 \le 15.5$) $\to$ Yellow Queue (boundary review) $\to$ Red Queue ($\chi^2 > 15.5$, high audit risk).
5. **Residual-Driven Audit Sampling:** Focus substantive manual audit on digit bins with residuals $R_i > +2.0$.

---

### Panel 4: Empirical Data Provenance
- **Dataset A (Genuine Demographic Data):**
  - Source: World Bank 2023 World Development Indicators (`SP.POP.TOTL`).
  - Sample: $n = 217$ sovereign nations (266 entities minus 1 null and 48 regional aggregates).
  - Span: 9,816 (Tuvalu) to 1.44B (India) — spans 5 orders of magnitude without artificial caps.
- **Dataset B (Simulated Fabricated Example):**
  - Sample: $n = 217$, fixed seed = 2026.
  - Cognitive Model: Discrete uniform digit bias model modeling human fabricator psychology.
  - *Disclaimer: Synthetic demonstration example; not actual fraud allegations.*

---

### Panel 5: Empirical Results & Visualizations
- **Figure 1:** Authentic World Bank Populations ($n = 217$) — Conforms closely to Benford curve.
- **Figure 2:** Simulated Fabricated Data ($n = 217$) — Massive deficit in digit 1 and surpluses in digits 5–9.
- **Results Table:**

| Dataset | Valid $n$ | $\chi^2$ | $p$-value | MAD | Decision ($\alpha=0.05$) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **World Bank (Genuine)** | 217 | 7.608 | 0.4726 | 0.0152 | **Fail to Reject $H_0$ (Conforms)** |
| **Simulated Fabrication** | 217 | 79.982 | $4.93 \times 10^{-14}$ | 0.0621 | **Reject $H_0$ (Flagged / Anomalous)** |
| **R Rivers Benchmark** | 141 | 44.177 | $5.27 \times 10^{-7}$ | 0.0525 | **Reject $H_0$ (Truncated Boundary)** |

---

### Panel 6: The River Lengths Paradox
- **Finding:** North American rivers ($n = 141$) failed Benford's test ($\chi^2 = 44.18, p < 0.001$).
- **Explanation:** The USGS World Almanac recorded only "major" rivers (>135 miles). Omitting small streams broke scale invariance, clustering values between 200–400 miles (digit 3 count: 36 vs exp 17.6).
- **Audit Rule:** Rejection does NOT prove fraud! Bounded or truncated authentic datasets naturally depart from Benford.

---

### Panel 7: Conclusions & Limitations
- **Clear Contrast:** Genuine data conformed ($\chi^2 = 7.608, p = 0.473$), whereas uniform fabrication failed overwhelmingly ($\chi^2 = 79.982, p < 10^{-13}$).
- **Effect Size is Mandatory:** With large samples, $\chi^2$ rejects tiny deviations. Mean Absolute Deviation (MAD) provides scale-free practical significance.
- **Audit Ethics:** Rejection flags anomalies for manual review; failure to reject does not guarantee innocence.

---

### Panel 8: Verified References
- Benford, F. (1938). Law of Anomalous Numbers. *Proc. Amer. Phil. Soc.*, 78(4).
- Nigrini, M. J. (2012). *Benford's Law: Forensic Accounting & Fraud Detection*. Wiley.
- Cochran, W. G. (1954). Strengthening Common $\chi^2$ Tests. *Biometrics*, 10(4).
- Hill, T. P. (1995). Statistical Derivation of Significant-Digit Law. *Stat. Sci.*, 10(4).
- World Bank (2024). World Development Indicators: Total Population (`SP.POP.TOTL`).
