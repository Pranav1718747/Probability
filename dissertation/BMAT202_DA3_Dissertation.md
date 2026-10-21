# Can a Chi-Square Test Catch Fake Numbers?
## Detecting Data Fabrication Using Benford's Law and Pearson's Goodness-of-Fit Analysis

**Course:** BMAT202 – Probability and Statistics (Winter Semester 2026)  
**Module:** Module 6 – Hypothesis Testing-II (Chi-Square Test & Goodness of Fit)  
**Assessment:** DA3 Project Dissertation (20 Marks)  
**Institution:** Vellore Institute of Technology (VIT), Chennai  
**Department:** School of Advanced Sciences (SAS), Department of Mathematics  
**Submission Date:** 22 October 2026  

**Investigative Team 14:**
- **Pranav S. (24BCE1166)** – Lead Data Analyst & Pipeline Engineer
- **Member 2 (24BCE1042)** – Statistical Methodology & Mathematical Derivations
- **Member 3 (24BCE1088)** – Data Acquisition, Provenance & Preprocessing
- **Member 4 (24BCE1115)** – Audit Screening Workflow & Forensic Evaluation
- **Member 5 (24BCE1152)** – Academic Synthesis, Visualization & Poster Layout

---

## Abstract
Numerical data integrity is essential across forensic accounting, tax compliance, scientific publishing, and macroeconomic surveillance. When unauthorized actors fabricate records, human cognitive biases—specifically the equal-likelihood fallacy and avoidance of digit repetition—frequently cause invented numbers to diverge from naturally occurring logarithmic digit distributions. This investigation develops and executes an automated statistical screening framework grounded in **Module 6 (Hypothesis Testing-II)** of the BMAT202 syllabus, operationalizing **Pearson's Chi-Square Goodness-of-Fit test** ($\chi^2$) to evaluate conformity against **Benford's Law** ($P(d) = \log_{10}(1 + 1/d)$ for $d \in \{1, \dots, 9\}$).

We evaluated three empirical datasets under rigorous testing protocols:
1. An authentic empirical dataset comprising $n = 217$ sovereign nation populations obtained from the World Bank's 2023 World Development Indicators (spanning five orders of magnitude);
2. A simulated fabricated dataset of equal sample size ($n = 217$) reflecting human cognitive uniform-digit heuristics; and
3. A historical reference dataset of 141 North American river lengths compiled in standard R.

Under a significance level of $\alpha = 0.05$ with $df = 8$ ($\chi^2_{\text{crit}} = 15.5073$), the genuine demographic dataset demonstrated close conformity to Benford's Law ($\chi^2 = 7.6083$, $p = 0.4726$, Mean Absolute Deviation $\text{MAD} = 0.01521$), resulting in a definitive failure to reject the null hypothesis $H_0$. Conversely, the simulated fabricated dataset exhibited severe statistical departure ($\chi^2 = 79.9819$, $p = 4.93 \times 10^{-14}$, $\text{MAD} = 0.06211$), rejecting $H_0$ with overwhelming significance. Notably, the historical river lengths dataset also rejected $H_0$ ($\chi^2 = 44.1766$, $p = 5.27 \times 10^{-7}$), exposing the critical statistical reality that lower-bound selection truncation destroys natural scale invariance. We synthesize these empirical discoveries into a 5-stage responsible forensic audit workflow that leverages chi-square residual diagnostics for targeted investigative sampling without generating false accusations.

---

## 1. Introduction and Background

### 1.1 The Imperative of Numerical Data Integrity
In modern forensic accounting, tax compliance audits, and macroeconomic monitoring, verifying the integrity of large transaction ledgers is paramount. Auditors cannot manually inspect every line item in ledgers containing tens of thousands of journal entries. Non-invasive statistical screening tools are required to triage high-risk transaction subsets.

### 1.2 Benford's Law and Its Mathematical Scope
Discovered by Simon Newcomb (1881) and formalized empirically by Frank Benford (1938), the *First-Digit Law* states that in naturally occurring numerical datasets spanning multiple orders of magnitude without artificial bounds, the leading significant decimal digit $d \in \{1, \dots, 9\}$ follows:
$$P(d) = \log_{10}\left(1 + \frac{1}{d}\right)$$
Under this distribution, digit 1 occurs approximately 30.1% of the time, while digit 9 occurs only 4.6%. The distribution is uniquely scale-invariant (Pinkham 1961) and base-invariant (Hill 1995).

### 1.3 Problem Statement
Humans inventing numbers intuitively assume digits should be uniformly distributed ($1/9 \approx 11.1\%$) and avoid repeating digit 1. Can an undergraduate hypothesis testing procedure ($\chi^2$ goodness-of-fit) reliably catch this fabrication?

---

## 2. Theoretical Background (Module 6 Alignment)

### 2.1 Hypotheses
- **$H_0$:** The first significant digit distribution follows Benford's Law ($P(d) = \log_{10}(1 + 1/d)$ for all $d$).
- **$H_1$:** The first significant digit distribution differs from Benford's Law for at least one digit.

### 2.2 Test Statistic & Degrees of Freedom
$$\chi^2 = \sum_{i=1}^9 \frac{(O_i - E_i)^2}{E_i}, \quad E_i = n \cdot \log_{10}\left(1 + \frac{1}{i}\right)$$
- Categories $k = 9$. Estimated parameters $m = 0$.
- Degrees of freedom: $df = 9 - 1 - 0 = 8$.
- Critical value at $\alpha = 0.05$: $\chi^2_{0.05, 8} = 15.5073$.
- Decision Rule: Reject $H_0$ if $\chi^2 > 15.5073$ ($p < 0.05$).

### 2.3 Cochran's Rule of Thumb
Requires $E_i \ge 5$ for all categories. For digit 9 ($p_9 \approx 0.04576$), $n \ge 110$. At $n = 217$, $E_9 = 9.93 > 5.0$, completely satisfying asymptotic assumptions.

### 2.4 Effect Size: Mean Absolute Deviation (MAD)
$$\text{MAD} = \frac{1}{9} \sum_{i=1}^9 \left| \frac{O_i}{n} - p_i \right|$$
Decouples sample size from physical divergence magnitude.

---

## 3. Dataset and Methodology

### 3.1 Datasets
1. **Dataset A (Genuine):** World Bank 2023 Country Populations (`SP.POP.TOTL`). Cleaned sovereign countries: $n = 217$, range 9,816 to 1.44 billion (5 orders of magnitude).
2. **Dataset B (Simulated Fabrication):** $n = 217$, seed = 2026. Discrete uniform digit bias model modeling human fabricator psychology.
3. **Dataset C (Benchmark):** North American River Lengths (`rivers`), $n = 141$.

### 3.2 Digit Extraction Algorithm
Uses R's scientific notation formatter `formatC(abs(x), format="e", digits=10)` to isolate the leading digit $d \in \{1, \dots, 9\}$ without decimal or floating-point errors.

---

## 4. Empirical Results Summary

| Dataset Under Evaluation | Valid $n$ | $\chi^2$ Statistic | $df$ | Critical Val ($\alpha=0.05$) | $p$-value | MAD | Decision at $\alpha=0.05$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Genuine Country Populations (World Bank 2023)** | **217** | **7.6083** | **8** | **15.5073** | **0.4726** | **0.01521** | **Fail to Reject $H_0$ (Conforms)** |
| **Simulated Fabricated Data (Uniform Bias)** | **217** | **79.9819** | **8** | **15.5073** | **$4.93 \times 10^{-14}$** | **0.06211** | **Reject $H_0$ (Anomalous / Flagged)** |
| **North American River Lengths (`rivers`)** | **141** | **44.1766** | **8** | **15.5073** | **$5.27 \times 10^{-7}$** | **0.05246** | **Reject $H_0$ (Truncated Boundary)** |

---

## 5. Key Discussion Findings
1. **World Bank Populations Conformed:** Multiplicative demographic compounding inherently generates scale-invariant logarithmic digit distributions.
2. **Fabricated Data Failed Dramatically:** Severe deficit in digit 1 (observed 30 vs expected 65.3) and massive surpluses in digits 5, 7, 8, 9 produced $\chi^2 = 79.982 \gg 15.507$.
3. **The River Lengths Paradox:** Truncation of data below 135 miles in the *World Almanac* compilation created heavy clustering between 200–400 miles, breaking scale invariance and causing failure.
4. **Statistical Limitation:** Rejection does not prove legal fraud; acceptance does not guarantee integrity.

---

## 6. Proposed 5-Stage Forensic Audit Workflow
1. **Suitability Assessment:** Verify ratio scale and $>3$ orders of magnitude.
2. **Sanitization & Digit Extraction:** Programmatic cleaning and exponential extraction.
3. **Dual Metric Evaluation:** Compute $\chi^2$, $p$-value, and MAD. Check Cochran's condition ($E_9 \ge 5$).
4. **Automated Risk Triage:** Green Queue (Compliant), Yellow Queue (Sample Size Review), Red Queue (High Risk).
5. **Residual-Driven Substantive Sampling:** Focus substantive invoice testing on digit buckets with standardized residuals $R_i > +2.0$.

---

## 7. R Program Code
*(See complete script at `R/benford_analysis.R` and full output logs in `outputs/`)*
