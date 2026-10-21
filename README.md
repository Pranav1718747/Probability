# BMAT202 DA3: Probability and Statistics Project
# "Can a Chi-Square Test Catch Fake Numbers? Detecting Data Fabrication Using Benford's Law"

**Course:** BMAT202 &ndash; Probability and Statistics  
**Assessment:** Digital Assignment 3 (DA3) &ndash; Poster Presentation (10 Marks) + Project Dissertation &amp; R Implementation (20 Marks)  
**Curriculum Module:** Module 6 &ndash; Hypothesis Testing-II (Small Samples, Chi-Square &amp; Goodness-of-Fit Tests)  
**Institution:** Vellore Institute of Technology (VIT), Chennai  
**Department:** School of Advanced Sciences (SAS), Department of Mathematics  
**Submission Date:** 22 October 2026  

---

## 1. Project Overview

In corporate auditing, forensic accounting, tax compliance, and scientific publishing, evaluating the authenticity of high-volume numerical records is a critical challenge. Unauthorized actors inventing numbers tend to suffer from cognitive biases—specifically the equal-likelihood fallacy and an aversion to repeating digit 1. Consequently, fabricated numbers typically follow an approximate uniform first-digit distribution (~11.1% each) rather than naturally occurring logarithmic decay.

This project implements an automated statistical screening framework using **Pearson's Chi-Square Goodness-of-Fit test** ($\chi^2$) to test conformity against **Benford's Law** ($P(d) = \log_{10}(1 + 1/d)$). Using an empirical dataset of $n = 217$ sovereign nation populations from the World Bank (2023) and a simulated fabricated dataset of equal sample size ($n = 217$), the project demonstrates how an undergraduate hypothesis testing procedure reliably distinguishes authentic multiplicative growth records from cognitive human fabrication.

---

## 2. Syllabus Mapping (BMAT202)

- **Module 6: Hypothesis Testing-II**
  - **Concept:** Pearson's Chi-Square Goodness-of-Fit Test.
  - **Hypotheses:**
    - $H_0: P(X = d) = \log_{10}(1 + 1/d)$ for all $d \in \{1, 2, \dots, 9\}$ (First digits conform to Benford's Law).
    - $H_1: P(X = d) \ne \log_{10}(1 + 1/d)$ for at least one $d$ (First digits depart from Benford's Law).
  - **Degrees of Freedom:** $df = k - 1 - m = 9 - 1 - 0 = 8$ (no population parameters estimated from sample).
  - **Significance Level &amp; Critical Value:** $\alpha = 0.05 \implies \chi^2_{0.05, 8} = 15.5073$.
  - **Decision Rule:** Reject $H_0$ if $\chi^2 > 15.5073$ ($p < 0.05$).
  - **Sample Size Assumption (Cochran's Rule):** Minimum expected count $E_9 = n \cdot P(9) \ge 5.0 \implies n \ge 110$. Both primary datasets ($n = 217$) yield $E_9 = 9.93 > 5.0$, perfectly satisfying Cochran's rule.

---

## 3. Directory Structure

```text
BMAT202_DA3/
├── README.md                                  # Master project guide and reproduction instructions
├── BMAT202_DA3_project_context.md             # Foundational project brief and syllabus context
├── data/
│   ├── raw/
│   │   └── world_bank_population_2023_raw.json # Official downloaded World Bank JSON (266 entities)
│   ├── processed/
│   │   ├── world_bank_population_2023_clean.csv # Cleaned sovereign country populations (n = 217)
│   │   ├── simulated_fabricated_data.csv       # Reproducible simulated fabricated numbers (n = 217, seed = 2026)
│   │   └── rivers.csv                          # North American river lengths benchmark (n = 141)
│   └── DATA_SOURCES.md                        # Complete provenance, data hygiene, and citation records
├── R/
│   ├── benford_analysis.R                     # Complete, self-contained R analysis script
│   └── run_statistical_engine.py             # High-precision statistical validation & execution engine
├── outputs/
│   ├── tables/
│   │   ├── genuine_frequency_table.csv        # Detailed observed vs expected digit frequencies (World Bank)
│   │   ├── fabricated_frequency_table.csv     # Detailed observed vs expected digit frequencies (Fabricated)
│   │   ├── rivers_frequency_table.csv         # Detailed observed vs expected digit frequencies (Rivers)
│   │   └── model_comparison_summary.csv      # Cross-dataset statistical comparison table
│   ├── figures/
│   │   ├── genuine_benford_plot.png           # Publication-quality chart: World Bank vs Benford
│   │   ├── fabricated_benford_plot.png        # Publication-quality chart: Fabricated Data vs Benford
│   │   └── comparison_benford_plot.png        # Side-by-side comparative distribution chart
│   ├── logs/
│   │   └── statistical_engine_run.log         # Complete execution log
│   ├── results_summary.txt                    # Plain-text executive statistical summary
│   └── viva_questions.md                      # 15 viva questions with answers + team presentation script
├── dissertation/
│   ├── BMAT202_DA3_Dissertation.pdf           # Formal 20-page print-ready dissertation PDF
│   ├── BMAT202_DA3_Dissertation.html          # Self-contained academic HTML source with embedded figures
│   ├── BMAT202_DA3_Dissertation.md            # Editable Markdown source of dissertation
│   └── build_dissertation.py                  # Automated dissertation builder & PDF compiler
├── poster/
│   ├── BMAT202_DA3_Poster.pdf                 # Single-page A1 Landscape print-ready poster PDF (841 x 594 mm)
│   ├── BMAT202_DA3_Poster.png                 # Ultra-high-resolution 150 DPI poster PNG (4967 x 3508 px)
│   ├── BMAT202_DA3_Poster.html                # Editable CSS/HTML A1 landscape layout source
│   ├── BMAT202_DA3_Poster.md                  # Concise editable Markdown poster content
│   └── build_poster.py                        # Automated poster builder & PDF/PNG compiler
└── references/
    └── REFERENCES.md                          # Academic bibliography and verified peer-reviewed citations
```

---

## 4. Key Empirical Findings

| Dataset Under Evaluation | Valid $n$ | Chi-Square ($\chi^2$) | $df$ | Critical Val ($\alpha=0.05$) | $p$-value | MAD | Statistical Decision |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Genuine Country Populations (World Bank 2023)** | **217** | **7.6083** | **8** | **15.5073** | **0.4726** | **0.01521** | **Fail to Reject $H_0$ (Conforms to Benford)** |
| **Simulated Fabricated Data (Uniform Bias)** | **217** | **79.9819** | **8** | **15.5073** | **$4.93 \times 10^{-14}$** | **0.06211** | **Reject $H_0$ (Severe Departure / Flagged)** |
| **North American River Lengths (`rivers`)** | **141** | **44.1766** | **8** | **15.5073** | **$5.27 \times 10^{-7}$** | **0.05246** | **Reject $H_0$ (Selection Truncation Paradox)** |

### Core Insights:
1. **Multiplicative Growth Conforms:** Sovereign nation populations grow geometrically, producing scale-invariant logarithmic digit frequencies ($\chi^2 = 7.608 < 15.507, p = 0.4726$).
2. **Cognitive Fabrication Fails Dramatically:** Fabricators under-produce digit 1 (observed: 30 vs expected: 65.3) and over-produce digits 5, 7, 8, and 9, triggering overwhelming rejection ($\chi^2 = 79.982 \gg 15.507, p = 4.93 \times 10^{-14}$).
3. **The River Lengths Paradox:** The USGS `rivers` dataset fails Benford's Law because only "major" rivers ($>135$ miles) were compiled in the World Almanac. Artificial lower-bound truncation destroys scale invariance, clustering lengths between 200–400 miles. This proves that **rejection does not prove fraud**—dataset suitability must always be audited first.

---

## 5. Software Requirements & Reproduction Instructions

### Environment Audit:
- **Operating System:** macOS Darwin (Apple Silicon ARM64).
- **Execution Engine:** Python 3.14 (NumPy, SciPy, Matplotlib, Pillow, PyPDF) & R v4.4+.
- **Rendering Engine:** Google Chrome 155 (Headless Paged PDF & High-Res Screenshot Engine).

### To Execute the Analysis Pipeline:
```bash
# 1. Run the statistical analysis engine (generates tables, plots, and summary):
python3 R/run_statistical_engine.py

# 2. If R is installed on your workstation, run the pure R script:
Rscript R/benford_analysis.R

# 3. Rebuild the 20-page dissertation PDF:
python3 dissertation/build_dissertation.py

# 4. Rebuild the print-ready A1 Landscape poster (PDF and PNG):
python3 poster/build_poster.py
```

---

## 6. Proposed Audit Screening Workflow

1. **Stage 1 (Suitability Assessment):** Verify unconstrained positive ratio metrics spanning $\ge 3$ orders of magnitude.
2. **Stage 2 (Digit Extraction):** Extract first significant digit via standardized scientific notation (`formatC(abs(x), "e")`).
3. **Stage 3 (Dual Evaluation):** Compute sample-dependent $\chi^2$ ($df = 8$, $p$-value) and scale-free Mean Absolute Deviation (MAD).
4. **Stage 4 (Automated Triage):** Green Queue (Compliant) vs Yellow Queue (Boundary review) vs Red Queue (High audit risk).
5. **Stage 5 (Residual Substantive Sampling):** Substantively audit transactions originating in digit bins with standardized residuals $R_i > +2.0$.

---

## 7. Submission Checklist & Deliverable Paths

- [x] **R Source Code:** `R/benford_analysis.R`
- [x] **Raw & Processed Data:** `data/raw/` & `data/processed/`
- [x] **Data Provenance:** `data/DATA_SOURCES.md`
- [x] **Results Summary & Tables:** `outputs/tables/` & `outputs/results_summary.txt`
- [x] **Publication Figures:** `outputs/figures/` (PNGs at 300 DPI)
- [x] **Dissertation PDF:** `dissertation/BMAT202_DA3_Dissertation.pdf` (20 pages, print-ready)
- [x] **Dissertation Source:** `dissertation/BMAT202_DA3_Dissertation.html` & `.md`
- [x] **Poster PDF:** `poster/BMAT202_DA3_Poster.pdf` (Single page, exact A1 landscape $841 \times 594$ mm)
- [x] **Poster PNG:** `poster/BMAT202_DA3_Poster.png` (4967 $\times$ 3508 px, 150 DPI)
- [x] **Poster Source:** `poster/BMAT202_DA3_Poster.html` & `.md`
- [x] **Viva Questions & Presentation Script:** `outputs/viva_questions.md` (15 Q&As + 2.5 min script)
- [x] **Verified Bibliography:** `references/REFERENCES.md`
