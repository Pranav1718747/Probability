#!/usr/bin/env python3
"""
Dissertation Generator for BMAT202 DA3
Generates an academic HTML document and compiles it to PDF via Headless Chrome.
"""

import os
import base64
import subprocess

PROJECT_ROOT = "/Users/pranav1718/Probability"
DISSERTATION_DIR = os.path.join(PROJECT_ROOT, "dissertation")
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")
FIGURES_DIR = os.path.join(OUTPUTS_DIR, "figures")

# Read figures as base64
def get_b64_img(filename):
    path = os.path.join(FIGURES_DIR, filename)
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

img_genuine_b64 = get_b64_img("genuine_benford_plot.png")
img_fake_b64 = get_b64_img("fabricated_benford_plot.png")
img_comp_b64 = get_b64_img("comparison_benford_plot.png")

# Load executed R script
with open(os.path.join(PROJECT_ROOT, "R", "benford_analysis.R"), "r", encoding="utf-8") as f:
    r_code_content = f.read()

# Load plain text results summary
with open(os.path.join(OUTPUTS_DIR, "results_summary.txt"), "r", encoding="utf-8") as f:
    results_summary_content = f.read()

# Load HTML template from separate file or assemble safely
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>BMAT202 DA3 Dissertation: Can a Chi-Square Test Catch Fake Numbers?</title>
<style>
  @page {
    size: A4;
    margin: 22mm 18mm 22mm 18mm;
    @bottom-right {
      content: counter(page);
      font-size: 9pt;
      font-family: 'Times New Roman', Times, serif;
      color: #555;
    }
  }
  
  body {
    font-family: 'Times New Roman', Times, Georgia, serif;
    font-size: 11pt;
    line-height: 1.55;
    color: #111827;
    margin: 0;
    padding: 0;
    text-align: justify;
  }

  /* Headings */
  h1, h2, h3, h4 {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    color: #0F172A;
    font-weight: 700;
    page-break-after: avoid;
  }
  h1 { font-size: 18pt; margin-top: 24pt; margin-bottom: 12pt; border-bottom: 2px solid #0284C7; padding-bottom: 4pt; }
  h2 { font-size: 14pt; margin-top: 18pt; margin-bottom: 8pt; color: #1E3A8A; border-bottom: 1px solid #E2E8F0; padding-bottom: 3pt; }
  h3 { font-size: 12pt; margin-top: 14pt; margin-bottom: 6pt; color: #334155; }
  
  p { margin-top: 0; margin-bottom: 8pt; }
  
  /* Title Page */
  .title-page {
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 90vh;
    text-align: center;
    padding: 30pt 20pt 20pt 20pt;
  }
  .inst-header {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 16pt;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #0F172A;
    text-transform: uppercase;
    margin-bottom: 6pt;
  }
  .dept-header {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 11.5pt;
    font-weight: 600;
    color: #475569;
    letter-spacing: 0.5px;
    margin-bottom: 30pt;
  }
  .course-badge {
    display: inline-block;
    background-color: #F1F5F9;
    border: 1px solid #CBD5E1;
    border-radius: 4px;
    padding: 6pt 16pt;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 11pt;
    font-weight: 700;
    color: #1E3A8A;
    margin-bottom: 35pt;
  }
  .project-title {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 23pt;
    font-weight: 800;
    line-height: 1.25;
    color: #0F172A;
    margin-bottom: 12pt;
  }
  .project-subtitle {
    font-family: 'Times New Roman', Times, serif;
    font-size: 14pt;
    font-style: italic;
    color: #334155;
    margin-bottom: 40pt;
  }
  .meta-box {
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #0284C7;
    border-radius: 4px;
    padding: 14pt 18pt;
    text-align: left;
    margin: 0 auto;
    width: 85%;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.6;
  }
  .meta-box table { width: 100%; border-collapse: collapse; }
  .meta-box td { padding: 3pt 6pt; }
  .meta-box td.label { font-weight: 700; color: #1E293B; width: 35%; }
  
  .submission-foot {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 10pt;
    font-weight: 600;
    color: #64748B;
    margin-top: 40pt;
  }

  /* Abstract Box */
  .abstract-box {
    background-color: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 16pt 20pt;
    margin: 18pt 0 24pt 0;
  }
  .abstract-title {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 13pt;
    font-weight: 700;
    color: #0F172A;
    text-align: center;
    margin-bottom: 10pt;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  .keywords {
    font-size: 10pt;
    font-style: italic;
    color: #334155;
    margin-top: 10pt;
  }

  /* Tables */
  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 12pt 0 16pt 0;
    font-size: 9.5pt;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  }
  table.data-table th, table.data-table td {
    padding: 6pt 8pt;
    text-align: right;
    border-bottom: 1px solid #E2E8F0;
  }
  table.data-table th {
    background-color: #0F172A;
    color: #FFFFFF;
    font-weight: 600;
    text-align: right;
  }
  table.data-table th:first-child, table.data-table td:first-child {
    text-align: center;
  }
  table.data-table th:nth-child(2), table.data-table td:nth-child(2) {
    text-align: left;
  }
  table.data-table tr:nth-child(even) {
    background-color: #F8FAFC;
  }
  table.data-table tr:hover {
    background-color: #F1F5F9;
  }
  .table-caption {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 9pt;
    font-weight: 700;
    color: #334155;
    margin-bottom: 4pt;
    text-align: left;
  }

  /* Figures */
  .figure-container {
    text-align: center;
    margin: 16pt 0 20pt 0;
    page-break-inside: avoid;
  }
  .figure-container img {
    max-width: 95%;
    height: auto;
    border: 1px solid #CBD5E1;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  }
  .figure-caption {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 9pt;
    font-weight: 600;
    color: #475569;
    margin-top: 6pt;
  }

  /* Code Blocks */
  pre.code-block {
    background-color: #0F172A;
    color: #F8FAFC;
    font-family: 'Courier New', Courier, monospace;
    font-size: 8.5pt;
    line-height: 1.45;
    padding: 12pt;
    border-radius: 4px;
    overflow-x: auto;
    margin: 12pt 0;
    page-break-inside: avoid;
  }
  pre.console-output {
    background-color: #1E293B;
    color: #38BDF8;
    font-family: 'Courier New', Courier, monospace;
    font-size: 8.5pt;
    line-height: 1.4;
    padding: 10pt;
    border-radius: 4px;
    border-left: 3px solid #38BDF8;
    margin: 10pt 0;
    page-break-inside: avoid;
  }

  /* Callout Boxes */
  .callout {
    background-color: #EFF6FF;
    border-left: 4px solid #2563EB;
    padding: 10pt 14pt;
    margin: 12pt 0;
    font-size: 10pt;
    border-radius: 0 4px 4px 0;
  }
  .callout-title {
    font-weight: 700;
    color: #1E3A8A;
    margin-bottom: 4pt;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  }

  /* Mathematical Equations */
  .equation-box {
    text-align: center;
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
    padding: 10pt 0;
    margin: 10pt 0;
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
  }

  /* Lists */
  ul, ol {
    margin-top: 0;
    margin-bottom: 8pt;
    padding-left: 20pt;
  }
  li { margin-bottom: 3pt; }

  .page-break {
    page-break-after: always;
  }
</style>
</head>
<body>

<!-- TITLE PAGE -->
<div class="title-page">
  <div>
    <div class="inst-header">Vellore Institute of Technology, Chennai</div>
    <div class="dept-header">School of Advanced Sciences &bull; Department of Mathematics</div>
    <div class="course-badge">BMAT202 &ndash; Probability and Statistics &bull; Winter Semester 2026</div>
  </div>

  <div>
    <div class="project-title">Can a Chi-Square Test Catch Fake Numbers?</div>
    <div class="project-subtitle">Detecting Numerical Data Fabrication Using Benford's Law and Pearson's Goodness-of-Fit Analysis</div>
  </div>

  <div>
    <div class="meta-box">
      <table>
        <tr>
          <td class="label">Course Code &amp; Title:</td>
          <td>BMAT202 &ndash; Probability and Statistics</td>
        </tr>
        <tr>
          <td class="label">Curriculum Module:</td>
          <td>Module 6: Hypothesis Testing-II (Small Samples, Chi-Square &amp; Goodness-of-Fit)</td>
        </tr>
        <tr>
          <td class="label">Assessment Component:</td>
          <td>Digital Assignment 3 (DA3) Project Dissertation (20 Marks)</td>
        </tr>
        <tr>
          <td class="label">Investigative Team:</td>
          <td>
            <strong>Student Team 14:</strong><br>
            &bull; Pranav S. (24BCE1166) &ndash; Lead Data Analyst &amp; Pipeline Engineer<br>
            &bull; Member 2 (24BCE1042) &ndash; Statistical Methodology &amp; Mathematical Derivations<br>
            &bull; Member 3 (24BCE1088) &ndash; Data Acquisition, Provenance &amp; Preprocessing<br>
            &bull; Member 4 (24BCE1115) &ndash; Audit Screening Workflow &amp; Forensic Evaluation<br>
            &bull; Member 5 (24BCE1152) &ndash; Academic Synthesis, Visualization &amp; Poster Layout
          </td>
        </tr>
        <tr>
          <td class="label">Evaluation Panel:</td>
          <td>Faculty of Mathematics, School of Advanced Sciences (SAS), VIT Chennai</td>
        </tr>
        <tr>
          <td class="label">Date of Submission:</td>
          <td>22 October 2026</td>
        </tr>
      </table>
    </div>

    <div class="submission-foot">
      A Formal Academic Project Dissertation Submitted in Partial Fulfillment of the Requirements for Course BMAT202
    </div>
  </div>
</div>

<!-- ABSTRACT -->
<div class="abstract-box">
  <div class="abstract-title">Academic Abstract</div>
  <p>
    Numerical data integrity is essential across forensic accounting, tax compliance, scientific publishing, and macroeconomic surveillance. When unauthorized actors fabricate records, human cognitive biases—specifically the equal-likelihood fallacy and avoidance of digit repetition—frequently cause invented numbers to diverge from naturally occurring logarithmic digit distributions. This investigation develops and executes an automated statistical screening framework grounded in <strong>Module 6 (Hypothesis Testing-II)</strong> of the BMAT202 syllabus, operationalizing <strong>Pearson's Chi-Square Goodness-of-Fit test</strong> (&#967;&sup2;) to evaluate conformity against <strong>Benford's Law</strong> (P(d) = log<sub>10</sub>(1 + 1/d) for d &isin; {1, &hellip;, 9}).
  </p>
  <p>
    We evaluated three empirical datasets under rigorous testing protocols: (1) an authentic empirical dataset comprising n = 217 sovereign nation populations obtained from the World Bank's 2023 World Development Indicators (spanning five orders of magnitude); (2) a simulated fabricated dataset of equal sample size (n = 217) reflecting human cognitive uniform-digit heuristics; and (3) a historical reference dataset of 141 North American river lengths compiled in standard R. Under a significance level of &alpha; = 0.05 with df = 8 (&chi;&sup2;<sub>crit</sub> = 15.5073), the genuine demographic dataset demonstrated close conformity to Benford's Law (&chi;&sup2; = 7.6083, p = 0.4726, Mean Absolute Deviation MAD = 0.01521), resulting in a definitive failure to reject the null hypothesis H<sub>0</sub>. Conversely, the simulated fabricated dataset exhibited severe statistical departure (&chi;&sup2; = 79.9819, p = 4.93 &times; 10<sup>-14</sup>, MAD = 0.06211), rejecting H<sub>0</sub> with overwhelming significance. Notably, the historical river lengths dataset also rejected H<sub>0</sub> (&chi;&sup2; = 44.1766, p = 5.27 &times; 10<sup>-7</sup>), exposing the critical statistical reality that lower-bound selection truncation destroys natural scale invariance. We synthesize these empirical discoveries into a 5-stage responsible forensic audit workflow that leverages chi-square residual diagnostics for targeted investigative sampling without generating false accusations.
  </p>
  <div class="keywords">
    <strong>Keywords:</strong> Benford's Law, Chi-Square Goodness-of-Fit Test, Hypothesis Testing, Forensic Accounting, Data Fabrication Detection, Cochran's Rule, Mean Absolute Deviation (MAD), World Bank Data, R Programming.
  </div>
</div>

<!-- 1. INTRODUCTION -->
<h1>1. Introduction and Background</h1>

<h2>1.1 The Imperative of Numerical Data Integrity</h2>
<p>
  In an increasingly data-driven global economy, decisions involving billions of dollars in capital allocation, governmental fiscal policy, corporate compliance, and peer-reviewed scientific discovery hinge upon the authenticity of underlying numerical records. However, modern auditing environments face a staggering volume of data: corporate general ledgers contain millions of journal entries, revenue authorities process hundreds of millions of tax filings, and research databases index thousands of empirical studies weekly. In such high-dimensional environments, line-by-line substantive manual auditing is mathematically and economically infeasible.
</p>
<p>
  Consequently, auditors, regulatory watchdogs, and forensic investigators require automated, computationally lightweight, non-invasive statistical screening procedures that can rapidly triage entire numerical populations, highlighting high-risk ledgers for targeted human inspection while certifying low-risk distributions as statistically unexceptional.
</p>

<h2>1.2 The Phenomenon of Benford's Law</h2>
<p>
  First observed by astronomer Simon Newcomb in 1881—who noticed that earlier pages of logarithm tables were systematically more soiled and worn than later pages—and systematically formalized empirically by physicist Frank Benford in 1938, the <em>First-Digit Law</em> (or <em>Law of Anomalous Numbers</em>) dictates that in naturally occurring numerical datasets spanning multiple orders of magnitude, the leading significant digit d &isin; {1, 2, &hellip;, 9} does not occur with uniform probability (1/9 &approx; 11.1%). Instead, it follows a strict logarithmic decay function:
</p>
<div class="equation-box">
  P(d) = log<sub>10</sub>(1 + 1/d) = log<sub>10</sub>(d + 1) - log<sub>10</sub>(d), &nbsp;&nbsp;&nbsp;&nbsp; d &isin; {1, 2, &hellip;, 9}
</div>
<p>
  Under this continuous logarithmic measure, numbers beginning with digit 1 appear approximately <strong>30.1%</strong> of the time, while numbers beginning with digit 9 occur only <strong>4.6%</strong> of the time. Mathematical foundations established by Pinkham (1961) and Hill (1995) proved that Benford's Law is the unique probability distribution on significant digits that exhibits both <em>scale invariance</em> (the distribution remains invariant under multiplication by any non-zero constant, such as currency conversion) and <em>base invariance</em>. Hill further proved that when numbers are sampled randomly from a mixture of diverse, independent probability distributions, the composite distribution asymptotically converges to Benford's Law.
</p>

<h2>1.3 Real-Life Problem Statement and Practical Significance</h2>
<p>
  When human agents invent numbers—whether deliberately committing procurement embezzlement, fabricating scientific laboratory trials, padding corporate travel expenses, or evading customs tariffs—they rarely consult mathematical distribution theory. Instead, humans are governed by a well-documented cognitive heuristic termed the <strong>equal-likelihood bias</strong> (or uniform digit fallacy). Humans intuitively believe that "random" numbers should look evenly dispersed across digits 1 through 9. Furthermore, fabricators suffer from psychological aversion to repeating digit 1, viewing repeated leading ones as "suspicious" or "cluttered."
</p>
<p>
  This fundamental cognitive discrepancy establishes a powerful diagnostic tension:
</p>
<ul>
  <li><strong>Natural Systems:</strong> Multiplicative growth, geometric compounding, and unconstrained physical metrics naturally satisfy logarithmic spacing (&sim; 30.1% ones).</li>
  <li><strong>Invented Systems:</strong> Human fabrication skews toward equal digit frequencies (&sim; 11.1% across all digits) or over-represents psychologically salient digits (such as 5, 7, and 8).</li>
</ul>
<p>
  The practical problem addressed in this study is: <em>Can an undergraduate-level hypothesis testing framework—specifically Pearson's Chi-Square Goodness-of-Fit test implemented in R—reliably distinguish authentic real-world data from cognitively fabricated numbers, while maintaining strict awareness of sample size constraints, selection boundaries, and inferential limitations?</em>
</p>

<h2>1.4 Project Objectives and Research Questions</h2>
<p>To resolve this problem systematically, our study pursues four formal academic objectives:</p>
<ol>
  <li><strong>Syllabus Integration:</strong> Directly bridge the theoretical principles of <strong>BMAT202 Module 6 (Hypothesis Testing-II)</strong>—including null/alternative hypothesis formulation, degrees of freedom calculation, critical region demarcation, and rejection decision rules—to forensic data screening.</li>
  <li><strong>Empirical Implementation:</strong> Develop a robust, end-to-end R programming pipeline that programmatically ingests raw data, sanitizes invalid observations, extracts significant leading digits without floating-point artifacts, and performs both manual and built-in goodness-of-fit testing.</li>
  <li><strong>Dual Dataset Comparison:</strong> Subject both a genuine macroeconomic population dataset (n = 217) and a reproducible simulated fabrication dataset (n = 217) to identical testing procedures, evaluating test statistics (&chi;&sup2;), exact p-values, and Mean Absolute Deviation (MAD) effect sizes.</li>
  <li><strong>Boundary &amp; Practical Workflow Formulation:</strong> Examine boundary cases where genuine data fails Benford's Law due to truncation (analyzing the historical `rivers` dataset), and construct an actionable 5-stage fraud screening workflow suitable for enterprise internal audit teams.</li>
</ol>

<!-- 2. THEORETICAL BACKGROUND -->
<div class="page-break"></div>
<h1>2. Theoretical Background &amp; Syllabus Alignment</h1>

<h2>2.1 Module 6 Syllabus Mapping</h2>
<p>
  This project directly implements the mathematical curriculum of <strong>BMAT202 (Probability and Statistics), Module 6: Hypothesis Testing-II</strong>. Specifically, it applies:
</p>
<ul>
  <li>The categorical goodness-of-fit testing framework.</li>
  <li>The derivation of degrees of freedom under linear constraints without parameter estimation.</li>
  <li>The statistical decision rule based on the upper tail of the Pearson &chi;&sup2; distribution.</li>
  <li>The rigorous evaluation of Type I and Type II error probabilities within real-world decision frameworks.</li>
</ul>

<h2>2.2 Formulation of Statistical Hypotheses</h2>
<p>
  Let X denote a discrete random variable representing the first significant decimal digit of an observation, where the support of X is S = {1, 2, 3, 4, 5, 6, 7, 8, 9}. The hypothesis testing problem is formally structured as:
</p>
<div class="equation-box">
  <strong>H<sub>0</sub>:</strong> P(X = d) = p<sub>d</sub> = log<sub>10</sub>(1 + 1/d), &nbsp;&nbsp;&nbsp;&nbsp; &forall; d &isin; {1, 2, &hellip;, 9}<br>
  <strong>H<sub>1</sub>:</strong> P(X = d) &ne; log<sub>10</sub>(1 + 1/d) &nbsp;&nbsp;&nbsp;&nbsp; for at least one d &isin; {1, 2, &hellip;, 9}
</div>
<p>
  The null hypothesis H<sub>0</sub> asserts complete conformity to Benford's Law. The alternative hypothesis H<sub>1</sub> is non-directional (omnibus), stating that the underlying generative process produces leading digits that depart from the theoretical logarithmic distribution.
</p>

<h2>2.3 The Chi-Square Goodness-of-Fit Test Statistic</h2>
<p>
  To test H<sub>0</sub> against H<sub>1</sub>, we partition a sample of n independent observations into k = 9 mutually exclusive and exhaustive digit bins. Let O<sub>i</sub> denote the observed frequency of digit i, and let E<sub>i</sub> denote the expected frequency under H<sub>0</sub>:
</p>
<div class="equation-box">
  E<sub>i</sub> = n &middot; p<sub>i</sub> = n &middot; log<sub>10</sub>(1 + 1/i), &nbsp;&nbsp;&nbsp;&nbsp; i &isin; {1, 2, &hellip;, 9}
</div>
<p>
  The discrepancy between observed counts and theoretical expectations is measured using Pearson's chi-square test statistic:
</p>
<div class="equation-box">
  &chi;&sup2; = &sum;<sub>i=1</sub><sup>9</sup> (O<sub>i</sub> - E<sub>i</sub>)&sup2; / E<sub>i</sub>
</div>
<p>
  Under H<sub>0</sub>, as n &to; &infin;, the distribution of &chi;&sup2; converges asymptotically to a continuous chi-square distribution with degrees of freedom df:
</p>
<div class="equation-box">
  df = k - 1 - m
</div>
<p>
  where k = 9 is the number of categorical bins, and m is the number of distribution parameters estimated from the sample data. Because Benford's Law is a completely specified mathematical distribution with fixed theoretical constants (p<sub>1</sub> &approx; 0.301, &hellip;, p<sub>9</sub> &approx; 0.046), <strong>no parameters are estimated from the sample (m = 0)</strong>. The loss of one degree of freedom arises solely from the linear constraint that observed counts must sum to the total sample size (&sum; O<sub>i</sub> = n). Thus:
</p>
<div class="equation-box">
  df = 9 - 1 - 0 = 8
</div>

<h2>2.4 Significance Level, Critical Region, and Decision Rule</h2>
<p>
  We establish an explicit significance level of &alpha; = 0.05. The critical value &chi;&sup2;<sub>&alpha;, df</sub> represents the (1 - &alpha;)-th quantile of the central &chi;&sup2; distribution with 8 degrees of freedom:
</p>
<div class="equation-box">
  &chi;&sup2;<sub>0.05, 8</sub> &approx; 15.5073
</div>
<p>
  The decision rule is formulated as follows:
</p>
<ul>
  <li>If &chi;&sup2; &gt; 15.5073 (or equivalently, if p-value &lt; 0.05), <strong>Reject H<sub>0</sub></strong> at &alpha; = 0.05. Conclude that the observed first-digit distribution departs significantly from Benford's Law.</li>
  <li>If &chi;&sup2; &le; 15.5073 (or equivalently, if p-value &ge; 0.05), <strong>Fail to Reject H<sub>0</sub></strong> at &alpha; = 0.05. Conclude that there is insufficient statistical evidence to reject conformity to Benford's Law.</li>
</ul>

<h2>2.5 Cochran's Expected-Count Condition</h2>
<p>
  The asymptotic convergence of Pearson's multinomial test statistic to the continuous &chi;&sup2; distribution relies on Cochran's classical sampling criteria (Cochran, 1952, 1954):
</p>
<blockquote>
  <strong>Cochran's Rule:</strong> The asymptotic chi-square approximation is valid provided that no expected cell frequency is less than 1 (E<sub>i</sub> &ge; 1 for all i), and no more than 20% of the cells have expected frequencies less than 5 (E<sub>i</sub> &ge; 5 for at least 80% of categories).
</blockquote>
<p>
  In a 9-cell Benford test, the least frequent digit is 9, with theoretical probability p<sub>9</sub> = log<sub>10</sub>(10/9) &approx; 0.045757. To satisfy the condition that <em>all</em> cells satisfy E<sub>i</sub> &ge; 5, the minimum sample size is:
</p>
<div class="equation-box">
  n &ge; 5 / p<sub>9</sub> &approx; 5 / 0.045757 &approx; 109.27 &implies; n &ge; 110
</div>
<p>
  In our study, the primary World Bank dataset contains n = 217 observations, yielding a minimum expected count of E<sub>9</sub> = 217 &times; 0.045757 = 9.93 &gt; 5.0. Therefore, 100% of the bins satisfy Cochran's rule with generous margin, completely eliminating any requirement to collapse digit categories.
</p>

<h2>2.6 Type I and Type II Error Dynamics</h2>
<ul>
  <li><strong>Type I Error (&alpha; = 0.05):</strong> False positive. An authentic dataset is flagged as anomalous. In a commercial audit, this triggers costly, disruptive forensic inquiries into compliant departments, squandering audit resources. We fix &alpha; = 0.05 to cap this error probability at 5%.</li>
  <li><strong>Type II Error (&beta;):</strong> False negative. A fabricated or fraudulent dataset is erroneously certified as compliant. This allows financial manipulation, tax fraud, or scientific falsification to escape detection. The power of the test (1 - &beta;) increases with sample size n and effect size.</li>
</ul>

<h2>2.7 Effect Size: Mean Absolute Deviation (MAD)</h2>
<p>
  A critical limitation of Pearson's chi-square test in large samples is its power sensitivity: because &chi;&sup2; is proportional to n, very large datasets produce massive &chi;&sup2; values even for trivial deviations. To decouple practical significance from sample size, Nigrini (2012) established the <strong>Mean Absolute Deviation (MAD)</strong> of digit proportions:
</p>
<div class="equation-box">
  MAD = (1/9) &sum;<sub>i=1</sub><sup>9</sup> |O<sub>i</sub>/n - p<sub>i</sub>| = (1/9) &sum;<sub>i=1</sub><sup>9</sup> |p<sub>obs, i</sub> - p<sub>exp, i</sub>|
</div>

<!-- 3. DATASET AND METHODOLOGY -->
<div class="page-break"></div>
<h1>3. Dataset Provenance and Methodology</h1>

<h2>3.1 Dataset A: Genuine Demographic Data (World Bank)</h2>
<ul>
  <li><strong>Indicator Code:</strong> SP.POP.TOTL (Population, Total).</li>
  <li><strong>Year:</strong> 2023 (latest finalized annual release).</li>
  <li><strong>Direct Source URL:</strong> https://data.worldbank.org/indicator/SP.POP.TOTL</li>
  <li><strong>Retrieval Date:</strong> 20 October 2026.</li>
  <li><strong>Raw Observations:</strong> 266 reporting entities.</li>
  <li><strong>Data Hygiene &amp; Sanitization:</strong> 1 null observation (XY) excluded; 48 regional aggregates separated; exactly <strong>n = 217 sovereign nations and autonomous territories</strong> retained.</li>
  <li><strong>Distribution Spread:</strong> Minimum population is 9,816 (Tuvalu); maximum population is 1,438,069,596 (India). The data spans over 5 orders of magnitude (log<sub>10</sub> range: 3.99 to 9.16).</li>
</ul>

<h2>3.2 Dataset B: Simulated Fabricated Numbers (Uniform Bias Heuristic)</h2>
<ul>
  <li><strong>Cognitive Mechanism:</strong> Untrained human fabricators assume that plausible ledger entries should exhibit equal leading digit probabilities (P(d) = 1/9 &approx; 11.11%). They systematically under-represent digit 1 and over-represent digits 4 through 9.</li>
  <li><strong>Sample Size &amp; Seed:</strong> n = 217 (matched exactly to Dataset A), random seed = 2026.</li>
  <li><strong>Integrity Disclaimer:</strong> This dataset is a controlled, reproducible methodological demonstration designed to quantify test sensitivity against human psychological heuristics. It does not represent actual fraudulent records from any commercial or governmental institution.</li>
</ul>

<h2>3.3 Significant Digit Extraction Algorithm</h2>
<p>
  We implemented an algorithm utilizing double-precision scientific representation: formatting positive real values into standardized exponential strings via R's `formatC(x, format="e", digits=10)`. The very first character of the resulting string is guaranteed to be the leading non-zero decimal digit d &isin; {1, &hellip;, 9}.
</p>

<!-- 4. R IMPLEMENTATION -->
<div class="page-break"></div>
<h1>4. R Programming Implementation &amp; Execution</h1>

<h2>4.1 Architecture of the R Script (`R/benford_analysis.R`)</h2>
<p>
  The complete statistical analysis was programmed in pure, idiomatic R, engineered to execute deterministically without external dependency bottlenecks. It includes project root autodetection, exact theoretical probability calculation, robust digit extraction with unit testing, comprehensive chi-square and MAD computation, and automated figure export.
</p>

<h2>4.2 Verbatim R Source Code</h2>
<pre class="code-block">
__R_CODE_PLACEHOLDER__
</pre>

<h2>4.3 Execution Audit and Console Output</h2>
<pre class="console-output">
__RESULTS_SUMMARY_PLACEHOLDER__
</pre>

<!-- 5. RESULTS -->
<div class="page-break"></div>
<h1>5. Empirical Results</h1>

<h2>5.1 Comparative Goodness-of-Fit Summary</h2>
<div class="table-caption">Table 1: Master Goodness-of-Fit and Effect Size Comparison Across Datasets</div>
<table class="data-table">
  <thead>
    <tr>
      <th style="text-align: left;">Dataset Under Evaluation</th>
      <th>Valid n</th>
      <th>Chi-Square (&chi;&sup2;)</th>
      <th>df</th>
      <th>Critical Val (&alpha;=0.05)</th>
      <th>p-value</th>
      <th>MAD</th>
      <th>Min E<sub>i</sub></th>
      <th style="text-align: left;">Statistical Decision</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: left;"><strong>Genuine Country Populations (World Bank 2023)</strong></td>
      <td>217</td>
      <td>7.6083</td>
      <td>8</td>
      <td>15.5073</td>
      <td>0.4726</td>
      <td>0.01521</td>
      <td>9.93</td>
      <td style="text-align: left; color: #16A34A; font-weight: 700;">Fail to Reject H<sub>0</sub> (Conforms)</td>
    </tr>
    <tr>
      <td style="text-align: left;"><strong>Simulated Fabricated Data (Uniform Bias)</strong></td>
      <td>217</td>
      <td>79.9819</td>
      <td>8</td>
      <td>15.5073</td>
      <td>4.93 &times; 10<sup>-14</sup></td>
      <td>0.06211</td>
      <td>9.93</td>
      <td style="text-align: left; color: #DC2626; font-weight: 700;">Reject H<sub>0</sub> (Flagged / Anomalous)</td>
    </tr>
    <tr>
      <td style="text-align: left;"><strong>North American River Lengths (`rivers`)</strong></td>
      <td>141</td>
      <td>44.1766</td>
      <td>8</td>
      <td>15.5073</td>
      <td>5.27 &times; 10<sup>-7</sup></td>
      <td>0.05246</td>
      <td>6.45</td>
      <td style="text-align: left; color: #DC2626; font-weight: 700;">Reject H<sub>0</sub> (Truncated Boundary)</td>
    </tr>
  </tbody>
</table>

<h2>5.2 Detailed Frequency Breakdown: Genuine World Bank Populations</h2>
<div class="table-caption">Table 2: Digit Distribution Analysis for World Bank 2023 Sovereign Populations (n = 217)</div>
<table class="data-table">
  <thead>
    <tr>
      <th>Digit (d)</th>
      <th>Observed (O<sub>i</sub>)</th>
      <th>Expected (E<sub>i</sub>)</th>
      <th>Obs Prop (p<sub>obs</sub>)</th>
      <th>Exp Prop (p<sub>exp</sub>)</th>
      <th>Residual (O<sub>i</sub> - E<sub>i</sub>)</th>
      <th>Contrib (O<sub>i</sub>-E<sub>i</sub>)&sup2;/E<sub>i</sub></th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>68</td><td>65.3235</td><td>0.31336</td><td>0.30103</td><td>+2.6765</td><td>0.10967</td></tr>
    <tr><td>2</td><td>36</td><td>38.2104</td><td>0.16590</td><td>0.17609</td><td>-2.2104</td><td>0.12787</td></tr>
    <tr><td>3</td><td>30</td><td>27.1122</td><td>0.13825</td><td>0.12494</td><td>+2.8878</td><td>0.30759</td></tr>
    <tr><td>4</td><td>16</td><td>21.0298</td><td>0.07373</td><td>0.09691</td><td>-5.0298</td><td>1.20300</td></tr>
    <tr><td>5</td><td>25</td><td>17.1824</td><td>0.11521</td><td>0.07918</td><td>+7.8176</td><td>3.55684</td></tr>
    <tr><td>6</td><td>16</td><td>14.5273</td><td>0.07373</td><td>0.06695</td><td>+1.4727</td><td>0.14929</td></tr>
    <tr><td>7</td><td>8</td><td>12.5843</td><td>0.03687</td><td>0.05799</td><td>-4.5843</td><td>1.67000</td></tr>
    <tr><td>8</td><td>10</td><td>11.1009</td><td>0.04608</td><td>0.05115</td><td>-1.1009</td><td>0.10917</td></tr>
    <tr><td>9</td><td>8</td><td>9.9292</td><td>0.03687</td><td>0.04576</td><td>-1.9292</td><td>0.37485</td></tr>
  </tbody>
  <tfoot>
    <tr style="font-weight: 700; background-color: #E2E8F0;">
      <td>Total</td><td>217</td><td>217.0000</td><td>1.00000</td><td>1.00000</td><td>0.0000</td><td>&chi;&sup2; = 7.6083</td>
    </tr>
  </tfoot>
</table>

<h2>5.3 Detailed Frequency Breakdown: Simulated Fabricated Data</h2>
<div class="table-caption">Table 3: Digit Distribution Analysis for Simulated Fabricated Numbers (n = 217)</div>
<table class="data-table">
  <thead>
    <tr>
      <th>Digit (d)</th>
      <th>Observed (O<sub>i</sub>)</th>
      <th>Expected (E<sub>i</sub>)</th>
      <th>Obs Prop (p<sub>obs</sub>)</th>
      <th>Exp Prop (p<sub>exp</sub>)</th>
      <th>Residual (O<sub>i</sub> - E<sub>i</sub>)</th>
      <th>Contrib (O<sub>i</sub>-E<sub>i</sub>)&sup2;/E<sub>i</sub></th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>30</td><td>65.3235</td><td>0.13825</td><td>0.30103</td><td>-35.3235</td><td>19.10111</td></tr>
    <tr><td>2</td><td>24</td><td>38.2104</td><td>0.11060</td><td>0.17609</td><td>-14.2104</td><td>5.28483</td></tr>
    <tr><td>3</td><td>16</td><td>27.1122</td><td>0.07373</td><td>0.12494</td><td>-11.1122</td><td>4.55410</td></tr>
    <tr><td>4</td><td>28</td><td>21.0298</td><td>0.12903</td><td>0.09691</td><td>+6.9702</td><td>2.31024</td></tr>
    <tr><td>5</td><td>31</td><td>17.1824</td><td>0.14286</td><td>0.07918</td><td>+13.8176</td><td>11.11169</td></tr>
    <tr><td>6</td><td>20</td><td>14.5273</td><td>0.09217</td><td>0.06695</td><td>+5.4727</td><td>2.06171</td></tr>
    <tr><td>7</td><td>27</td><td>12.5843</td><td>0.12442</td><td>0.05799</td><td>+14.4157</td><td>16.51368</td></tr>
    <tr><td>8</td><td>21</td><td>11.1009</td><td>0.09677</td><td>0.05115</td><td>+9.8991</td><td>8.82744</td></tr>
    <tr><td>9</td><td>20</td><td>9.9292</td><td>0.09217</td><td>0.04576</td><td>+10.0708</td><td>10.21443</td></tr>
  </tbody>
  <tfoot>
    <tr style="font-weight: 700; background-color: #E2E8F0;">
      <td>Total</td><td>217</td><td>217.0000</td><td>1.00000</td><td>1.00000</td><td>0.0000</td><td>&chi;&sup2; = 79.9819</td>
    </tr>
  </tfoot>
</table>

<h2>5.4 Graphical Visualizations</h2>
<div class="figure-container">
  <img src="__IMG_GENUINE_PLACEHOLDER__" alt="Figure 1: Genuine World Bank Populations vs Benford's Law">
  <div class="figure-caption">Figure 1: Observed First-Digit Proportions for World Bank 2023 Country Populations (n = 217) vs Theoretical Benford Distribution (&chi;&sup2; = 7.608, p = 0.4726, MAD = 0.0152).</div>
</div>

<div class="figure-container">
  <img src="__IMG_FAKE_PLACEHOLDER__" alt="Figure 2: Simulated Fabricated Data vs Benford's Law">
  <div class="figure-caption">Figure 2: Observed First-Digit Proportions for Simulated Fabricated Numbers (n = 217) vs Theoretical Benford Distribution (&chi;&sup2; = 79.982, p = 4.93 &times; 10<sup>-14</sup>, MAD = 0.0621). Notice the massive deficit in digit 1 and surpluses in digits 5&ndash;9.</div>
</div>

<div class="figure-container">
  <img src="__IMG_COMP_PLACEHOLDER__" alt="Figure 3: Comparative Benford Plot">
  <div class="figure-caption">Figure 3: Side-by-Side Comparative Visualization Contrasting Authentic Demographic Records (Blue) with Uniform Cognitive Fabrication (Gold) Against Benford's Law (Red Curve).</div>
</div>

<!-- 6. DISCUSSION -->
<div class="page-break"></div>
<h1>6. Discussion and Forensic Analysis</h1>

<h2>6.1 Interpretation of Genuine Data Results (World Bank Demographic Data)</h2>
<p>
  The analysis of the 2023 World Bank sovereign population dataset (n = 217) yielded a test statistic of &chi;&sup2; = 7.6083. With 8 degrees of freedom, the associated p-value is 0.4726 (47.26%). Because &chi;&sup2; = 7.6083 &lt; 15.5073 (and p = 0.4726 &gt; 0.05), we <strong>fail to reject the null hypothesis H<sub>0</sub></strong>.
</p>
<p>
  This finding confirms that the observed leading-digit distribution of national populations across the globe conforms closely to Benford's logarithmic decay. Observed relative frequencies mirror theoretical expectations across the distribution: digit 1 appeared in 31.34% of countries (expected: 30.10%), digit 2 in 16.59% (expected: 17.61%), and digit 9 in 3.69% (expected: 4.58%). The total Mean Absolute Deviation was MAD = 0.01521, which is well within normal random sampling variation for n &approx; 200.
</p>

<h2>6.2 Interpretation of Fabricated Data Results (Cognitive Bias Model)</h2>
<p>
  In stark contrast, the simulated fabricated dataset (n = 217) yielded &chi;&sup2; = 79.9819, more than <strong>five times</strong> the critical cutoff of 15.5073. The corresponding p-value is 4.93 &times; 10<sup>-14</sup>, leading to an unconditional, overwhelming <strong>rejection of H<sub>0</sub></strong>.
</p>
<ul>
  <li><strong>Digit 1 Deficit (&chi;&sup2; contribution = 19.10):</strong> Only 30 values began with digit 1 (13.82%), compared to the Benford expectation of 65.32 (30.10%). This single cell accounted for 23.9% of the total test statistic.</li>
  <li><strong>Digit 7 Surplus (&chi;&sup2; contribution = 16.51):</strong> 27 values began with digit 7 (12.44%), more than double the expected frequency of 12.58 (5.80%).</li>
  <li><strong>Digits 5, 8, and 9 Surpluses (&chi;&sup2; contributions = 11.11, 8.83, 10.21):</strong> Human fabricators systematically over-allocated numbers to higher digits.</li>
  <li><strong>Effect Size Surge:</strong> The MAD surged to 0.06211—over four times greater than that of the authentic dataset—placing it deep within Nigrini's "Severe Non-Conformity" diagnostic category.</li>
</ul>

<h2>6.3 The River Lengths Paradox: Selection Truncation vs. Scale Invariance</h2>
<p>
  The historical North American river lengths dataset (`rivers`, n = 141) provides a profoundly instructive academic lesson. The chi-square test yielded &chi;&sup2; = 44.1766 (p = 5.27 &times; 10<sup>-7</sup>), rejecting H<sub>0</sub>. Does this mean that the USGS fabricated river lengths in 1975?
</p>
<p>
  <strong>Certainly not.</strong> The rejection stems from a violation of Benford's fundamental requirement: <em>untruncated scale invariance spanning multiple orders of magnitude</em>. In the *World Almanac* compilation from which the dataset was extracted, only "major" rivers exceeding approximately 135 miles were recorded. Small streams and tributaries (which would naturally supply abundant lengths beginning with digit 1, such as 10–19 miles or 100–199 miles) were systematically omitted. Because of this artificial cutoff, observations cluster heavily between 200 and 400 miles (digit 3 occurred 36 times vs expected 17.62; digit 2 occurred 31 times vs expected 24.83). This lower truncation destroys base-10 scale invariance, causing the sample to fail Benford's test despite consisting of 100% genuine geographical measurements.
</p>

<!-- 7. PROPOSED SOLUTION -->
<div class="page-break"></div>
<h1>7. Proposed Practical Solution: Automated Forensic Audit Screening Workflow</h1>

<p>
  Based on our empirical findings, we propose a standardized, responsible <strong>5-Stage Forensic Screening Framework</strong> designed for integration into enterprise audit management systems, tax oversight platforms, and forensic accounting protocols.
</p>

<div class="callout">
  <div class="callout-title">Core Ethical &amp; Procedural Philosophy</div>
  A statistical flag from Benford's test is a <strong>diagnostic indicator for targeted manual inspection</strong>, NEVER an accusation of criminal fraud. The screening tool serves as a precision sieve to optimize scarce audit hours.
</div>

<h2>7.1 The 5-Stage Audit Screening Architecture</h2>
<ol>
  <li><strong>Stage 1: Pre-Screening Suitability &amp; Boundary Assessment:</strong> Validate that values represent unconstrained, positive continuous or discrete ratio-scale quantities spanning at least three orders of magnitude. Ensure data does not represent assigned identifiers, exam scores, or fixed retail price tiers.</li>
  <li><strong>Stage 2: Standardized Sanitization &amp; Digit Extraction:</strong> Process data using scientific notation extraction (`formatC(abs(x), format="e")`). Log and segregate zero/non-finite records.</li>
  <li><strong>Stage 3: Dual-Metric Statistical Evaluation:</strong> Compute both the sample-size-dependent test statistic (&chi;&sup2;, df = 8, p-value) and scale-free effect size (MAD). Check Cochran's rule (E<sub>9</sub> &ge; 5).</li>
  <li><strong>Stage 4: Automated Risk Triage &amp; Classification:</strong> Route ledgers into Green (Compliant: p &ge; 0.05, MAD &le; 0.015), Yellow (Marginal: review selection filters), or Red (Anomalous: p &lt; 0.01, MAD &gt; 0.015) queues.</li>
  <li><strong>Stage 5: Residual-Driven Substantive Forensic Sampling:</strong> Rather than inefficient random sampling, auditors inspect transactions originating in digit bins exhibiting the highest positive standardized residuals:
    <div class="equation-box">
      R<sub>i</sub> = (O<sub>i</sub> - E<sub>i</sub>) / &radic;(E<sub>i</sub>(1 - p<sub>i</sub>))
    </div>
    Targeting bins with R<sub>i</sub> &gt; +2.0 focuses audit resources precisely where fabrication occurs.
  </li>
</ol>

<!-- 8. CONCLUSION -->
<h1>8. Conclusion and Future Scope</h1>

<h2>8.1 Conclusion</h2>
<p>
  This study successfully designed, implemented, and validated a complete statistical and computational framework for detecting numerical data fabrication using Benford's Law and Pearson's Chi-Square Goodness-of-Fit test, directly fulfilling all requirements of <strong>BMAT202 Module 6</strong>. Authentic demographic growth processes conformed remarkably well (&chi;&sup2; = 7.6083, p = 0.4726, MAD = 0.01521), whereas human uniform cognitive heuristics produced dramatic statistical rejections (&chi;&sup2; = 79.9819, p = 4.93 &times; 10<sup>-14</sup>, MAD = 0.06211). Furthermore, the river lengths paradox demonstrated empirically why data selection criteria must always be audited before applying Benford's Law.
</p>

<h2>8.2 Future Scope</h2>
<p>
  Future research directions include: (1) Second-digit and first-two-digit joint testing to detect subtle threshold invoice padding; (2) Benford summation tests to detect high-dollar account skimming; and (3) Machine learning hybrid triage incorporating chi-square residuals into gradient-boosted decision trees.
</p>

<!-- 9. REFERENCES -->
<div class="page-break"></div>
<h1>9. Academic References &amp; Verified Bibliography</h1>
<ol>
  <li><strong>Benford, F. (1938).</strong> "The Law of Anomalous Numbers." <em>Proceedings of the American Philosophical Society</em>, 78(4), 551&ndash;572.</li>
  <li><strong>Carslaw, C. A. (1988).</strong> "Anomalies in Income Numbers: Evidence of Goal Oriented Behavior." <em>The Accounting Review</em>, 63(2), 321&ndash;327.</li>
  <li><strong>Cochran, W. G. (1952).</strong> "The &chi;&sup2; Test of Goodness of Fit." <em>The Annals of Mathematical Statistics</em>, 23(3), 315&ndash;345.</li>
  <li><strong>Cochran, W. G. (1954).</strong> "Some Methods for Strengthening the Common &chi;&sup2; Tests." <em>Biometrics</em>, 10(4), 417&ndash;451.</li>
  <li><strong>Hill, T. P. (1995).</strong> "A Statistical Derivation of the Significant-Digit Law." <em>Statistical Science</em>, 10(4), 354&ndash;363.</li>
  <li><strong>McNeil, D. R. (1977).</strong> <em>Interactive Data Analysis: A Practical Primer</em>. John Wiley &amp; Sons, New York. ISBN: 0-471-02631-5.</li>
  <li><strong>Newcomb, S. (1881).</strong> "Note on the Frequency of Use of the Different Digits in Natural Numbers." <em>American Journal of Mathematics</em>, 4(1/4), 39&ndash;40.</li>
  <li><strong>Nigrini, M. J. (1996).</strong> "A Taxpayer Compliance Application of Benford's Law." <em>The Journal of the American Taxation Association</em>, 18(1), 72&ndash;91.</li>
  <li><strong>Nigrini, M. J. (2012).</strong> <em>Benford's Law: Applications for Forensic Accounting, Auditing, and Fraud Detection</em>. John Wiley &amp; Sons, Inc., Hoboken, New Jersey. ISBN: 978-0-470-76808-2.</li>
  <li><strong>Pearson, K. (1900).</strong> "On the Criterion that a Given System of Deviations from the Probable in the Case of a Correlated System of Variables is Such that it Can be Reasonably Supposed to Have Arisen from Random Sampling." <em>Philosophical Magazine</em>, 50(302), 157&ndash;175.</li>
  <li><strong>Pinkham, R. S. (1961).</strong> "On the Distribution of First Significant Digits." <em>The Annals of Mathematical Statistics</em>, 32(4), 1223&ndash;1230.</li>
  <li><strong>R Core Team (2026).</strong> <em>R: A Language and Environment for Statistical Computing</em>. R Foundation for Statistical Computing, Vienna, Austria. URL: <a href="https://www.R-project.org/">https://www.R-project.org/</a></li>
  <li><strong>Virtanen, P., Gommers, R., Oliphant, T. E., et al. (2020).</strong> "SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python." <em>Nature Methods</em>, 17(3), 261&ndash;272.</li>
  <li><strong>World Bank Group (2024).</strong> <em>World Development Indicators: Population, total (SP.POP.TOTL)</em>. World Bank Open Data. Data released October 2024; retrieved October 20, 2026. URL: <a href="https://data.worldbank.org/indicator/SP.POP.TOTL">https://data.worldbank.org/indicator/SP.POP.TOTL</a></li>
</ol>

<!-- 10. APPENDIX -->
<div class="page-break"></div>
<h1>10. Appendix: Supplementary Materials &amp; Verification</h1>

<h2>10.1 Mathematical Verification of Chi-Square Residuals</h2>
<div class="table-caption">Table 4: Step-by-Step Chi-Square Arithmetic Verification</div>
<table class="data-table">
  <thead>
    <tr>
      <th>Digit (d)</th>
      <th>O<sub>i</sub></th>
      <th>E<sub>i</sub> = 217 &middot; log<sub>10</sub>(1 + 1/d)</th>
      <th>O<sub>i</sub> - E<sub>i</sub></th>
      <th>(O<sub>i</sub> - E<sub>i</sub>)&sup2;</th>
      <th>(O<sub>i</sub> - E<sub>i</sub>)&sup2; / E<sub>i</sub></th>
      <th>Cumulative &chi;&sup2;</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>68</td><td>65.3235</td><td>+2.6765</td><td>7.1636</td><td>0.10966</td><td>0.10966</td></tr>
    <tr><td>2</td><td>36</td><td>38.2104</td><td>-2.2104</td><td>4.8859</td><td>0.12787</td><td>0.23753</td></tr>
    <tr><td>3</td><td>30</td><td>27.1122</td><td>+2.8878</td><td>8.3394</td><td>0.30759</td><td>0.54512</td></tr>
    <tr><td>4</td><td>16</td><td>21.0298</td><td>-5.0298</td><td>25.2989</td><td>1.20300</td><td>1.74812</td></tr>
    <tr><td>5</td><td>25</td><td>17.1824</td><td>+7.8176</td><td>61.1149</td><td>3.55684</td><td>5.30496</td></tr>
    <tr><td>6</td><td>16</td><td>14.5273</td><td>+1.4727</td><td>2.1688</td><td>0.14929</td><td>5.45425</td></tr>
    <tr><td>7</td><td>8</td><td>12.5843</td><td>-4.5843</td><td>21.0158</td><td>1.67000</td><td>7.12425</td></tr>
    <tr><td>8</td><td>10</td><td>11.1009</td><td>-1.1009</td><td>1.2120</td><td>0.10918</td><td>7.23343</td></tr>
    <tr><td>9</td><td>8</td><td>9.9292</td><td>-1.9292</td><td>3.7218</td><td>0.37484</td><td><strong>7.60827</strong></td></tr>
  </tbody>
</table>
<p style="text-align: center; font-weight: 700; margin-top: 8pt;">
  Manual Total &chi;&sup2; = 7.60827 &equiv; R Output &chi;&sup2; = 7.6083 (Within Machine Tolerance &epsilon; &lt; 10<sup>-5</sup>)
</p>

<h2>10.2 Software and Computational Environment Audit</h2>
<ul>
  <li><strong>Statistical Computing Platform:</strong> R Language &amp; Environment (v4.4+) / SciPy Statistical Computing Engine (v1.14+).</li>
  <li><strong>Rendering &amp; Export Toolchain:</strong> Google Chrome 155 Headless Engine with PDF Paged Media Printing.</li>
  <li><strong>Hardware Architecture:</strong> Apple Silicon (ARM64), macOS Darwin Kernel.</li>
  <li><strong>Workspace Location:</strong> `/Users/pranav1718/Probability`.</li>
  <li><strong>Determinism &amp; Reproducibility:</strong> Random seed fixed at 2026; all data source artifacts archived under `data/raw/` and `data/processed/`.</li>
</ul>

</body>
</html>
"""

# Inject dynamic content safely
html_content = html_template.replace("__R_CODE_PLACEHOLDER__", r_code_content)
html_content = html_content.replace("__RESULTS_SUMMARY_PLACEHOLDER__", results_summary_content)
html_content = html_content.replace("__IMG_GENUINE_PLACEHOLDER__", img_genuine_b64)
html_content = html_content.replace("__IMG_FAKE_PLACEHOLDER__", img_fake_b64)
html_content = html_content.replace("__IMG_COMP_PLACEHOLDER__", img_comp_b64)

# Write HTML file
html_path = os.path.join(DISSERTATION_DIR, "BMAT202_DA3_Dissertation.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"[DISSERTATION] Wrote HTML source to: {html_path}")

# Compile to PDF using Headless Chrome
pdf_path = os.path.join(DISSERTATION_DIR, "BMAT202_DA3_Dissertation.pdf")
chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

cmd = [
    chrome_bin,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    html_path
]

print(f"[DISSERTATION] Compiling PDF via Chrome: {' '.join(cmd)}")
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0 and os.path.exists(pdf_path):
    size_kb = os.path.getsize(pdf_path) / 1024
    print(f"[DISSERTATION] Successfully generated PDF: {pdf_path} ({size_kb:.1f} KB)")
else:
    print(f"[DISSERTATION ERROR] Return code: {result.returncode}")
    print(f"Stderr: {result.stderr}")
