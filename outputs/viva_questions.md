# BMAT202 DA3: Presentation & Viva Voce Preparation Guide
**Course:** BMAT202 – Probability and Statistics (Module 6: Hypothesis Testing-II)  
**Project Title:** *Can a Chi-Square Test Catch Fake Numbers? Detecting Data Fabrication Using Benford's Law*  
**Institution:** Vellore Institute of Technology (VIT), Chennai  
**Date:** October 2026

---

## Part 1: Comprehensive Viva Voce Questions & Model Answers

### Category A: R Implementation & Pipeline Mechanics (5 Questions)

#### Q1. How does your R function extract the first significant digit reliably without formatting errors?
**Answer:**  
In R, simply converting numbers to characters can fail due to leading decimal zeros (e.g., `0.0045`) or default scientific printing. Our function `extract_first_digit(x)` uses:
```r
formatC(abs(x[x != 0]), format = "e", digits = 10)
```
In scientific notation, any non-zero real number is represented as `d.dddddddddd e±xx` where the very first character is guaranteed to be the leading non-zero digit $d \in \{1, 2, \dots, 9\}$. We then extract `as.integer(substr(..., 1, 1))`. This handles integers, decimals, and extreme scales seamlessly while explicitly dropping zeros and non-finite values.

#### Q2. Why did you calculate theoretical Benford probabilities using formula rather than hardcoding rounded percentages?
**Answer:**  
Hardcoding rounded probabilities (e.g., 30.1%, 17.6%) introduces truncation bias that violates probability axioms (their sum might deviate slightly from 1.0) and distorts expected counts $E_i = n \cdot P(i)$. In R, we evaluate `benford_p <- log10(1 + 1 / (1:9))` directly to 64-bit double precision, guaranteeing $\sum_{i=1}^9 P(i) = \log_{10}(10/1) \equiv 1.0000000000$.

#### Q3. How did you parameterize `chisq.test()` in R to test against Benford's distribution?
**Answer:**  
By default, R's `chisq.test(x)` tests a discrete uniform null hypothesis ($P(i) = 1/k$). To test goodness-of-fit against Benford's law, we explicitly pass the custom theoretical probability vector via the `p` argument:
```r
chisq.test(obs_counts, p = benford_p, rescale.p = TRUE)
```
We also independently compute the manual statistic $\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$ to verify that the R output matches mathematical theory within machine precision.

#### Q4. How does your R script handle relative file paths across different working directories?
**Answer:**  
The script includes an autodetection function `get_project_root()` that examines `commandArgs(trailingOnly = FALSE)` when executed via `Rscript`, extracting the true script directory and navigating up to the root. If run interactively, it checks `getwd()` and parent directories for the `data/` folder, ensuring seamless execution without manual path editing.

#### Q5. How are the publication figures constructed in base R without external graphics libraries?
**Answer:**  
We use base R's `barplot()` to plot observed proportions, capture the bar midpoints returned by `bp <- barplot(...)`, and overlay the continuous theoretical Benford expectation curve using `lines(bp, exp_props, type = "b", pch = 18, col = "red", lwd = 2.5)`. Text labels are placed above bars using `text()`, and metadata (sample size, $\chi^2$, $p$-value) is dynamically inscribed via `mtext()`.

---

### Category B: Statistical Theory, Assumptions & Hypotheses (5 Questions)

#### Q6. What are the null and alternative hypotheses for this goodness-of-fit test?
**Answer:**  
- **Null Hypothesis ($H_0$):** The first significant-digit distribution of the underlying population follows Benford's Law, i.e., $P(d) = \log_{10}(1 + 1/d)$ for all $d \in \{1, 2, \dots, 9\}$.
- **Alternative Hypothesis ($H_1$):** The first significant-digit distribution departs from Benford's Law for at least one digit category.

#### Q7. Why are the degrees of freedom exactly 8 for this test?
**Answer:**  
In a Pearson chi-square goodness-of-fit test, degrees of freedom are given by:
$$df = k - 1 - m$$
where $k = 9$ is the number of digit categories (1 through 9), and $m$ is the number of population parameters estimated from sample data. Because Benford's Law is a fully specified theoretical distribution with zero estimated parameters ($m = 0$), the single linear constraint that total observed counts sum to sample size ($\sum O_i = n$) reduces the free categories by 1:
$$df = 9 - 1 - 0 = 8$$
The critical value at $\alpha = 0.05$ with $df = 8$ is $\chi^2_{0.05, 8} = 15.5073$.

#### Q8. What is Cochran's rule for chi-square tests, and how did your sample size satisfy it?
**Answer:**  
Cochran (1952, 1954) established that the continuous chi-square distribution accurately approximates the discrete multinomial distribution only if no expected cell count is less than 1, and no more than 20% of expected counts are below 5. For Benford's Law, the lowest expected probability is for digit 9 ($P(9) \approx 0.045757$). Therefore:
$$E_9 = n \cdot P(9) \ge 5 \implies n \ge \frac{5}{0.045757} \approx 109.3$$
Our World Bank dataset has $n = 217$, giving $E_9 = 217 \times 0.045757 = 9.93 > 5.0$. All 9 expected frequencies exceed 9.9, satisfying Cochran's rule with 100% compliance without needing category collapsing.

#### Q9. Explain Type I and Type II errors in the context of fraud detection with Benford's Law.
**Answer:**  
- **Type I Error ($\alpha = 0.05$):** Rejecting $H_0$ when the dataset is actually authentic (False Alarm). In auditing, this causes unnecessary investigations of innocent organizations, wasting audit time and resources.
- **Type II Error ($\beta$):** Failing to reject $H_0$ when the dataset is actually fabricated (Missed Detection). In forensic accounting, this allows fraudulent transactions or manipulated accounting books to go undetected.

#### Q10. What is Mean Absolute Deviation (MAD), and why is relying solely on the $p$-value insufficient for large sample sizes?
**Answer:**  
The chi-square test statistic $\chi^2 = n \sum \frac{(p_{\text{obs}} - p_{\text{exp}})^2}{p_{\text{exp}}}$ is directly proportional to sample size $n$. In very large datasets ($n > 10,000$), even minuscule, economically trivial departures from Benford's Law produce enormous $\chi^2$ values and tiny $p$-values ($p < 0.001$).  
To assess **practical significance** independent of sample size, Nigrini (2012) introduced MAD:
$$\text{MAD} = \frac{1}{9} \sum_{i=1}^9 \left| \frac{O_i}{n} - P(i) \right|$$
In our study, World Bank data yielded $\text{MAD} = 0.0152$ (close conformity), whereas fabricated data yielded $\text{MAD} = 0.0621$ (over $4\times$ larger, indicating non-conformity).

---

### Category C: Forensic Interpretation, Anomaly Detection & Scope (5 Questions)

#### Q11. If a dataset rejects $H_0$, does that prove fraud or illegal activity?
**Answer:**  
**No, absolutely not.** A rejection of $H_0$ proves only that the empirical digit distribution deviates from logarithmic decay beyond random sampling variation. Legitimate datasets naturally violate Benford's Law if they are bounded (e.g., student exam marks 0–100, adult heights), subject to psychological pricing (e.g., \$9.99 or \$4.95), or constrained by minimum thresholds. A statistical rejection is an indicator for **manual audit review**, not proof of wrongdoing.

#### Q12. If a dataset fails to reject $H_0$, does that guarantee the data is clean and genuine?
**Answer:**  
**No.** Sophisticated fraudsters who understand Benford's Law can generate fake numbers that mimic logarithmic probabilities. Additionally, small-scale embezzlement (e.g., skimming a few thousand dollars amidst millions of transactions) will not alter the overall macro-distribution of leading digits. Benford analysis is a broad screening sieve, not an exhaustive forensic guarantee.

#### Q13. Why did the standard North American river lengths (`rivers`) dataset fail Benford's test in your analysis?
**Answer:**  
The `rivers` dataset ($n = 141$) yielded $\chi^2 = 44.177$ ($p = 5.27 \times 10^{-7}$). This occurred because the USGS compilation in the *World Almanac* was subject to a lower truncation threshold: only "major" rivers exceeding approximately 135 miles were recorded, with heavy clustering between 200 and 400 miles (digit 3 count was 36 vs expected 17.6). Because the dataset was artificially truncated at the lower boundary, it lost scale invariance across lower orders of magnitude, causing it to deviate from Benford's distribution. This highlights why data selection criteria must be scrutinized before screening.

#### Q14. What psychological cognitive bias causes human fabricators to fail Benford's Law?
**Answer:**  
Untrained humans intuitively believe that "random" or "plausible" numbers should have an equal chance of starting with any digit from 1 to 9 (uniform distribution hypothesis, $\approx 11.1\%$ each). Furthermore, humans suffer from an aversion to repeating digit 1 (which naturally occurs 30.1% of the time) and over-select middle/higher digits (such as 5, 7, and 8). When tested against Benford's Law, this uniform bias results in a severe deficit in digit 1 and massive surpluses in digits 4–9, driving $\chi^2$ past critical thresholds.

#### Q15. Summarize your proposed practical fraud-screening workflow for an internal audit team.
**Answer:**  
Our proposed workflow consists of five structured stages:
1. **Suitability Assessment:** Verify that the data is positive, continuous, unconstrained by artificial caps, and spans at least 3 orders of magnitude (e.g., accounts payable, inventory totals).
2. **First-Digit Extraction:** Programmatically clean data and isolate the first significant digit using standardized scripts.
3. **Goodness-of-Fit Testing:** Compute $\chi^2$, $df = 8$, $p$-value, and MAD.
4. **Triage & Classification:** If $\chi^2 > 15.507$ and $\text{MAD} > 0.015$, flag the dataset as anomalous.
5. **Targeted Substantive Audit:** Rather than auditing all transactions randomly, forensic auditors focus substantive sampling on the specific digit buckets displaying the largest chi-square contributions $(O_i - E_i)^2 / E_i$.

---

## Part 2: Concise 2.5-Minute Team Presentation Script

### [Slide / Poster Section 1 & 2] Speaker 1: Introduction, Problem Statement & Motivation (30 seconds)
> "Good morning, respected Professor and classmates. In corporate auditing, forensic accounting, and tax compliance, scrutinizing millions of financial transactions line-by-line is virtually impossible. Fraudsters often invent plausible-looking amounts. Our project investigates a vital question: *Can a chi-square goodness-of-fit test catch fake numbers using Benford's Law?* We bridge Module 6 hypothesis testing with forensic data analytics to establish an automated, non-invasive screening protocol for detecting anomalous numerical records."

### [Poster Section 3] Speaker 2: Mathematical Theory & Syllabus Mapping (35 seconds)
> "In naturally occurring growth processes spanning multiple orders of magnitude, the leading digit $d \in \{1, \dots, 9\}$ is not uniformly distributed. It follows Benford's Law: $P(d) = \log_{10}(1 + 1/d)$. Digit 1 appears about 30.1% of the time, while digit 9 appears only 4.6%. Under Module 6, we formulate our null hypothesis $H_0$: the observed first digits follow Benford's Law, against $H_1$: they do not. Because there are 9 categories and zero estimated parameters, our degrees of freedom are $df = 9 - 1 = 8$. At significance level $\alpha = 0.05$, the critical value is $\chi^2_{0.05, 8} = 15.507$."

### [Poster Section 4] Speaker 3: Data Provenance & R Implementation Pipeline (35 seconds)
> "We acquired genuine demographic data from the World Bank's 2023 World Development Indicators: 217 sovereign nation populations spanning 5 orders of magnitude, from 9,816 in Tuvalu to 1.44 billion in India. To contrast, we simulated a fabricated dataset of equal size ($n = 217$) reflecting human cognitive bias, where leading digits are chosen roughly uniformly. In our R pipeline, we implemented a robust extraction algorithm utilizing scientific notation formatting, dynamically computed exact Benford expectations, evaluated the Pearson test statistic $\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$, and quantified practical effect size using Mean Absolute Deviation."

### [Poster Section 5 & Table] Speaker 4: Empirical Findings & Statistical Decisions (35 seconds)
> "Our empirical results provide a stark statistical contrast:
> 1. For the genuine World Bank data, our test yielded $\chi^2 = 7.608$, well below the critical value of 15.507, with a $p$-value of $0.4726$ and a low $\text{MAD} = 0.0152$. We fail to reject $H_0$, confirming excellent conformity.
> 2. For the fabricated dataset, $\chi^2$ surged to $79.982$, far exceeding the critical cutoff, with an infinitesimal $p$-value of $4.93 \times 10^{-14}$ and $\text{MAD} = 0.0621$. We reject $H_0$ with overwhelming significance.
> 3. Furthermore, every single expected cell count in our primary test exceeded 9.9, flawlessly satisfying Cochran's rule of thumb ($E_i \ge 5$)."

### [Poster Section 6 & 7] Speaker 5: Audit Screening Workflow, Limitations & Conclusion (25 seconds)
> "We emphasize that a statistical rejection is not legal proof of fraud—it identifies statistical anomalies requiring targeted audit review. Likewise, natural datasets with artificial cutoffs (like North American river lengths) can fail due to truncation. We propose an end-to-end 5-stage screening workflow that allows audit teams to triage high-risk ledgers and direct investigative resources where chi-square residuals are greatest. Thank you, and we welcome your questions!"
