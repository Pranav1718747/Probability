# BMAT202 DA3 – Project Context for the AI Coding Assistant

> Read this whole file first. It contains everything decided so far: the assignment brief, the chosen topic, the method, a starter R script, and the outlines for the dissertation and poster. Your job is to help the student finish this project (R analysis, dissertation report, poster content) before the deadline.

## 1. Situation

- **Student course:** BMAT202 – Probability and Statistics.
- **Assessment:** DA3 – poster presentation (theory, 10 marks) + project dissertation with R implementation (laboratory, 20 marks).
- **Team:** up to 5 members. One hard copy of the poster and one of the dissertation per team.
- **Deadline / presentation:** **22 October 2026**, during the scheduled laboratory class. Today (when this file was written) is 20 October 2026, so about 2 days remain. Prioritise getting a complete, working version first, then polish.
- **Hard copies** of both the digital poster and the dissertation must be brought on that day.

## 2. Assignment brief (from the instructor, condensed but complete)

Each team selects **one topic from the syllabus** and applies the probability/statistics concept to solve a **real-life problem**.

**Project must include:**
1. Selection of a topic from the syllabus.
2. Real-life application: a practical problem and why it matters.
3. Proposed solution: how the concept addresses the problem.
4. Implementation and analysis: apply the concept to suitable **real-life data** and analyse results.
5. **Use of R programming**: include the relevant code and outputs in the dissertation.
6. Conclusion: interpret results and explain how they help solve or give insight into the problem.

**Poster (digital, printed) must explain:**
- the selected topic and its real-life application
- the problem statement and significance
- the concepts used
- the methodology and application
- the results, their interpretation, and the proposed solution
- the conclusion and key findings
- **Do NOT include R code on the poster.** Focus on theory, application and results.

**Dissertation report must include:**
- Introduction and background of the topic
- Real-life problem statement and objectives
- Relevant theoretical concepts from the syllabus
- Data source and methodology
- Detailed statistical analysis and its application
- **Complete R code with the corresponding outputs**
- Interpretation and discussion of results
- Proposed solution, conclusion, and references

The dissertation must show clearly how the R results support the proposed solution, and there must be a clear link between syllabus theory, R implementation and the real-life problem. All team members should be able to explain the work.

## 3. Syllabus (revised) – for reference

- Module 1: Introduction to Statistics – central tendency, dispersion, moments, skewness, kurtosis (concepts)
- Module 2: Random Variables – PMF, distribution and density functions, joint/marginal/conditional distributions, expectation, covariance, MGF
- Module 3: Correlation and Regression – rank, partial, multiple correlation, multiple regression
- Module 4: Probability Distributions – binomial, Poisson, normal, gamma, exponential, Weibull
- Module 5: Hypothesis Testing I – types of errors, critical region, procedure, large-sample tests, Z test for proportions and means
- Module 6: Hypothesis Testing II – small sample tests, Student's t-test, F-test, **chi-square test, goodness of fit**, (list may continue; the student's paste was cut off)

(Reliability was considered earlier but is NOT in the revised syllabus, so it was dropped.)

## 4. Chosen topic (decision made)

**Module 6 – Chi-square test for goodness of fit**, applied to **Benford's law for fraud / fabricated-data detection**.

**Working title:** *Can a chi-square test catch fake numbers? Detecting data fabrication using Benford's law.*

### Why this topic
- Clear real-life problem: auditors, tax authorities and election/statistics watchdogs need a quick screening method for fabricated or manipulated numbers.
- Very presentable: observed vs expected first-digit bar chart shows match/mismatch at a glance.
- Simple to implement in R (`chisq.test`) on real data.
- Ties together several syllabus ideas: hypothesis testing procedure, types of errors, critical region, chi-square test, goodness of fit.

### Background (theory to include)
- **Benford's law:** in many naturally occurring datasets spanning several orders of magnitude, the probability that the first significant digit is d is
  `P(d) = log10(1 + 1/d)`, d = 1..9
  (about 30.1% for 1, 17.6% for 2, 12.5% for 3, 9.7% for 4, 7.9% for 5, 6.7% for 6, 5.8% for 7, 5.1% for 8, 4.6% for 9).
- **Chi-square goodness-of-fit statistic:** `χ² = Σ (O_i − E_i)² / E_i`, with `E_i = n · P(i)`.
- **Hypotheses:** H0: first digits follow Benford's law. H1: they do not.
- **Degrees of freedom:** 9 − 1 = 8 (no parameters estimated). **Critical value at α = 0.05:** 15.507. Reject H0 if χ² > 15.507 (equivalently p < 0.05).
- **Types of errors:** Type I = flagging genuine data as suspicious (false alarm); Type II = failing to catch fabricated data. Discuss in the interpretation.
- **Assumptions / caveats to state honestly:**
  - Expected count per digit should be at least 5 (so n should be roughly 110+ for the rarest digit, 9, since 0.046 × n ≥ 5).
  - Benford's law works for data spanning several orders of magnitude (populations, financial amounts, river lengths); it does not apply to bounded data such as heights or exam marks.
  - With very large n, chi-square rejects even tiny deviations, so report effect size too (e.g. mean absolute deviation or the deviation per digit) and interpret practically, not only by p-value.
  - A rejection means "suspicious, investigate", not proof of fraud.

## 5. Data plan

Use **real** data. Options (pick at least one genuine dataset plus one "fabricated" dataset for contrast):

1. **Genuine data (should conform):** country populations (World Bank data, all countries and a recent year; about 200+ values, which meets the expected-count rule). Alternatives: river lengths (`rivers` built into R, 141 values), areas of countries, city populations, company revenues.
2. **Fabricated data (should be flagged):** collect about 100+ "made-up" numbers (for example ask team members and classmates to invent plausible expense amounts or populations without any rule). Humans tend to over-use middle digits and under-use 1. If collecting is not possible, simulate the fabrication transparently and label it clearly as simulated in the report (e.g. first digits drawn roughly uniformly).
3. Optional extra: a real dataset known for manipulation or a financial dataset (invoice or transaction amounts) if one can be sourced legitimately and cited.

Always cite the data source in the references (organisation, dataset name, year, URL, access date).

## 6. Methodology (steps)

1. Load the dataset and keep positive numeric values.
2. Extract the first significant digit of each value.
3. Tabulate observed counts O_1..O_9.
4. Compute expected counts E_i = n · log10(1 + 1/i).
5. Run the chi-square goodness-of-fit test; record χ², df = 8, p-value, and compare with the critical value 15.507.
6. Plot observed vs expected proportions.
7. Repeat for the fabricated dataset; compare.
8. Interpret: which dataset conforms, which is flagged, what it means for fraud screening, and discuss Type I/II errors and the limitations.
9. Proposed solution: a screening procedure that auditors can run (first-digit test → flag → manual investigation).

## 7. Starter R script (not yet run by the assistant; please run, fix, and extend)

```r
# BMAT202 DA3 – Benford's law with chi-square goodness of fit
# ---------------------------------------------------------------

benford_p <- log10(1 + 1 / (1:9))          # expected probabilities
names(benford_p) <- 1:9

first_digit <- function(x) {
  x <- abs(x)
  x <- x[!is.na(x) & x > 0]
  as.integer(substr(formatC(x, format = "e", digits = 10), 1, 1))
}

benford_test <- function(x, label = "Dataset") {
  d   <- first_digit(x)
  obs <- tabulate(d, nbins = 9)
  n   <- sum(obs)
  exp_counts <- n * benford_p

  test <- chisq.test(obs, p = benford_p, rescale.p = TRUE)

  res <- data.frame(
    digit        = 1:9,
    observed     = obs,
    expected     = round(exp_counts, 2),
    obs_prop     = round(obs / n, 4),
    exp_prop     = round(benford_p, 4)
  )

  cat("\n====", label, "====\n")
  cat("n =", n, "\n")
  print(res, row.names = FALSE)
  cat(sprintf("Chi-square = %.3f, df = %d, p-value = %.5f\n",
              test$statistic, test$parameter, test$p.value))
  cat(sprintf("Critical value (alpha = 0.05, df = 8) = %.3f\n", qchisq(0.95, 8)))
  cat("Decision:", ifelse(test$statistic > qchisq(0.95, 8),
                          "Reject H0 (does NOT follow Benford's law)",
                          "Fail to reject H0 (consistent with Benford's law)"), "\n")

  invisible(list(table = res, test = test, n = n))
}

benford_plot <- function(result, title) {
  props <- rbind(result$table$obs_prop, result$table$exp_prop)
  bp <- barplot(props[1, ], names.arg = 1:9, col = "steelblue",
                ylim = c(0, max(props) * 1.2),
                xlab = "First digit", ylab = "Proportion", main = title)
  lines(bp, props[2, ], type = "b", pch = 19, col = "red", lwd = 2)
  legend("topright", legend = c("Observed", "Benford expected"),
         fill = c("steelblue", NA), border = c("black", NA),
         pch = c(NA, 19), col = c("steelblue", "red"), lty = c(NA, 1), bty = "n")
}

# ---- 1. Genuine data -------------------------------------------
# Option A: World Bank population CSV (download, adjust the path/column)
# pop <- read.csv("data/world_population.csv")
# genuine <- pop$Population
# Option B (no download needed, for testing the pipeline): built-in river lengths
genuine <- rivers

res_genuine <- benford_test(genuine, "Genuine data")
benford_plot(res_genuine, "Genuine data vs Benford's law")

# ---- 2. Fabricated data ----------------------------------------
# Replace with real invented numbers collected from people (one value per row):
# fake <- read.csv("data/fabricated_numbers.csv")$value
# Placeholder simulation (label it as simulated in the report!):
set.seed(2026)
fake <- sample(100:9999, 150, replace = TRUE)   # first digits roughly uniform

res_fake <- benford_test(fake, "Fabricated data")
benford_plot(res_fake, "Fabricated data vs Benford's law")
```

Notes for the assistant: `rivers` has 141 values, so the expected count for digit 9 is about 6.5 (acceptable). Check the console output for warnings about small expected counts. Export the plots as PNG (e.g. `png("genuine.png", 900, 600)` … `dev.off()`) so they can go on the poster and in the report. Save the console output as text for the dissertation (`sink("output.txt")` or copy from the console).

## 8. Dissertation outline (maps to the brief)

1. Title page (course, topic, team members, date)
2. Abstract (short)
3. Introduction and background (statistics in fraud detection, Benford's law history)
4. Real-life problem statement and objectives
5. Theoretical concepts: Benford's law, hypothesis testing procedure, types of errors, critical region, chi-square statistic, goodness of fit, degrees of freedom, assumptions
6. Data source and methodology (datasets, how fabricated data was obtained, steps)
7. Statistical analysis and application (tables of observed vs expected, χ², p-values)
8. Complete R code with outputs and plots
9. Interpretation and discussion (conformity vs flagged, Type I/II errors, limitations such as large-n sensitivity and bounded data)
10. Proposed solution (a first-digit screening workflow for auditors)
11. Conclusion
12. References (data sources, Benford's original and Nigrini's work on forensic accounting, R documentation; verify every citation before including it)

## 9. Poster outline (digital, printed, NO R code)

1. **Title + team names**
2. **Real-life problem:** fabricated numbers in accounts and statistics, and why catching them matters
3. **Concept box:** Benford's law formula and the expected-digit bar chart; hypothesis test and chi-square formula
4. **Method:** flow diagram (data → first digit → observed vs expected → χ² test → decision)
5. **Results:** side-by-side charts for genuine vs fabricated data, with a small table of χ², df, p-value, decision
6. **Interpretation + proposed solution:** the audit screening workflow; Type I/II errors in plain language
7. **Conclusion and key findings** (3 to 4 bullets) + references
- Design: large readable fonts, 2 charts maximum, minimal text, consistent colours.

## 10. Suggested work plan (about 2 days)

- **Today:** get the data (World Bank populations + collect fabricated numbers), run the script, fix any errors, save plots and outputs.
- **Tomorrow:** write the dissertation sections (use sections 4 to 6 of this file as raw material), build the poster from the plots.
- **22 Oct (morning):** print the poster and the dissertation, rehearse the explanation so every member can explain the work.

## 11. How the assistant should help

- Run and debug the R script; do not invent results. All numbers in the report must come from real R output.
- Be honest about the limitations (large-n sensitivity, applicability range, "suspicious is not proof").
- Keep explanations at an undergraduate level and tied to the syllabus topics above.
- Verify any reference before adding it; do not fabricate citations.
- The student's language is English; keep the writing clear and simple.
