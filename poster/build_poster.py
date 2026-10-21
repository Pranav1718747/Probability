#!/usr/bin/env python3
"""
Scientific Poster Generator for BMAT202 DA3
Creates an A1 Landscape Academic Digital Poster in HTML/CSS
and compiles it to both PDF and high-resolution PNG using Headless Chrome and PIL.
"""

import os
import base64
import subprocess
from PIL import Image
import pypdf

PROJECT_ROOT = "/Users/pranav1718/Probability"
POSTER_DIR = os.path.join(PROJECT_ROOT, "poster")
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")
FIGURES_DIR = os.path.join(OUTPUTS_DIR, "figures")

# Read figures as base64
def get_b64_img(filename):
    path = os.path.join(FIGURES_DIR, filename)
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

img_genuine_b64 = get_b64_img("genuine_benford_plot.png")
img_fake_b64 = get_b64_img("fabricated_benford_plot.png")

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>BMAT202 DA3 Academic Poster: Can a Chi-Square Test Catch Fake Numbers?</title>
<style>
  @page {
    size: 841mm 594mm landscape;
    margin: 0;
  }
  * {
    box-sizing: border-box;
  }
  body {
    margin: 0;
    padding: 0;
    width: 841mm;
    height: 594mm;
    background-color: #0F172A;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1E293B;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  /* Header Banner */
  header {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 60%, #0369A1 100%);
    color: #FFFFFF;
    padding: 16mm 24mm 14mm 24mm;
    border-bottom: 4mm solid #38BDF8;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .header-main {
    flex: 1;
  }
  .inst-pill {
    display: inline-block;
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 6mm;
    padding: 2.5mm 8mm;
    font-size: 11pt;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #E0F2FE;
    margin-bottom: 3mm;
  }
  h1 {
    margin: 0;
    font-size: 34pt;
    font-weight: 900;
    letter-spacing: -0.5px;
    line-height: 1.15;
    color: #FFFFFF;
  }
  .subtitle {
    margin: 2mm 0 0 0;
    font-size: 17pt;
    font-weight: 500;
    color: #BAE6FD;
  }
  .header-meta {
    background: rgba(15, 23, 42, 0.55);
    border: 1.5px solid rgba(56, 189, 248, 0.4);
    border-radius: 4mm;
    padding: 5mm 9mm;
    text-align: right;
    font-size: 12pt;
    line-height: 1.45;
    color: #F8FAFC;
  }
  .header-meta strong {
    color: #38BDF8;
  }

  /* Main Grid: 4 Columns */
  main {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr 1.18fr 1fr;
    gap: 10mm;
    padding: 10mm 16mm 8mm 16mm;
    background-color: #F1F5F9;
  }

  .col {
    display: flex;
    flex-direction: column;
    gap: 8mm;
  }

  /* Card Containers */
  .card {
    background: #FFFFFF;
    border-radius: 4mm;
    padding: 7mm 8mm;
    border: 1px solid #CBD5E1;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
  }
  .card.highlight {
    border-top: 4mm solid #2563EB;
  }
  .card.warning {
    border-top: 4mm solid #D97706;
  }
  .card.accent {
    border-top: 4mm solid #0284C7;
  }
  .card.success {
    border-top: 4mm solid #16A34A;
  }

  .card-title {
    font-size: 14pt;
    font-weight: 800;
    color: #0F172A;
    margin: 0 0 4mm 0;
    display: flex;
    align-items: center;
    gap: 3mm;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .card-title span.badge {
    background: #0F172A;
    color: #FFFFFF;
    font-size: 10pt;
    font-weight: 800;
    padding: 1mm 3mm;
    border-radius: 2mm;
  }

  p, li {
    font-size: 10.5pt;
    line-height: 1.45;
    color: #334155;
    margin: 0 0 3mm 0;
  }
  ul {
    margin: 0;
    padding-left: 5mm;
  }

  /* Formula Callout Box */
  .formula-box {
    background: #F8FAFC;
    border: 1.5px solid #E2E8F0;
    border-left: 3mm solid #2563EB;
    border-radius: 2mm;
    padding: 3mm 4mm;
    margin: 2mm 0 3mm 0;
    text-align: center;
    font-family: "Times New Roman", Times, serif;
    font-size: 13pt;
    font-weight: 600;
    color: #1E293B;
  }

  /* Flow Diagram */
  .flow-container {
    display: flex;
    flex-direction: column;
    gap: 2.5mm;
    margin: 2mm 0;
  }
  .flow-step {
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 2.5mm;
    padding: 2.5mm 4mm;
    display: flex;
    align-items: center;
    gap: 3mm;
  }
  .flow-step .num {
    background: #1E3A8A;
    color: #FFFFFF;
    font-size: 10pt;
    font-weight: 800;
    width: 6mm;
    height: 6mm;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .flow-step .text {
    font-size: 9.5pt;
    font-weight: 600;
    color: #1E293B;
    line-height: 1.25;
  }
  .flow-step .text small {
    display: block;
    font-size: 8pt;
    font-weight: 400;
    color: #64748B;
  }

  /* Chart Containers */
  .chart-box {
    text-align: center;
    margin-bottom: 3mm;
    border: 1px solid #E2E8F0;
    border-radius: 3mm;
    padding: 2mm;
    background: #FFFFFF;
  }
  .chart-box img {
    width: 100%;
    height: auto;
    border-radius: 2mm;
    display: block;
  }
  .chart-label {
    font-size: 9pt;
    font-weight: 700;
    color: #475569;
    margin-top: 1.5mm;
  }

  /* Data Table */
  table.poster-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 9pt;
    margin: 2mm 0;
  }
  table.poster-table th, table.poster-table td {
    padding: 2mm 2.5mm;
    text-align: right;
    border-bottom: 1px solid #E2E8F0;
  }
  table.poster-table th {
    background: #0F172A;
    color: #FFFFFF;
    font-weight: 700;
    text-align: right;
  }
  table.poster-table th:first-child, table.poster-table td:first-child {
    text-align: left;
  }
  table.poster-table tr:nth-child(even) {
    background: #F8FAFC;
  }
  .status-pass {
    color: #16A34A;
    font-weight: 800;
  }
  .status-fail {
    color: #DC2626;
    font-weight: 800;
  }

  /* Callout Pill */
  .pill-highlight {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 2mm;
    padding: 2mm 3mm;
    font-size: 9pt;
    color: #1E40AF;
    margin: 2mm 0;
  }
  .pill-warning {
    background: #FEF3C7;
    border: 1px solid #FDE68A;
    border-radius: 2mm;
    padding: 2mm 3mm;
    font-size: 9pt;
    color: #92400E;
    margin: 2mm 0;
  }

  /* Footer Banner */
  footer {
    background: #0F172A;
    color: #94A3B8;
    padding: 4mm 24mm;
    font-size: 9pt;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1.5mm solid #38BDF8;
  }
  footer strong {
    color: #E2E8F0;
  }
</style>
</head>
<body>

<!-- HEADER -->
<header>
  <div class="header-main">
    <div class="inst-pill">Vellore Institute of Technology (VIT), Chennai &bull; School of Advanced Sciences</div>
    <h1>Can a Chi-Square Test Catch Fake Numbers?</h1>
    <div class="subtitle">Detecting Data Fabrication Using Benford's Law and Pearson's Goodness-of-Fit Analysis</div>
  </div>
  <div class="header-meta">
    <strong>Course:</strong> BMAT202 &ndash; Probability and Statistics (DA3)<br>
    <strong>Syllabus Module:</strong> Module 6 &ndash; Hypothesis Testing-II (Chi-Square &amp; Goodness-of-Fit)<br>
    <strong>Investigative Team 14:</strong> Pranav S. (24BCE1166) &amp; Team Members<br>
    <strong>Submission Date:</strong> 22 October 2026
  </div>
</header>

<!-- MAIN 4-COLUMN CONTENT -->
<main>

  <!-- COLUMN 1: PROBLEM & THEORY -->
  <div class="col">
    <!-- Problem Statement -->
    <div class="card highlight">
      <div class="card-title"><span class="badge">01</span> Real-Life Problem &amp; Significance</div>
      <p>
        In modern forensic accounting, tax audit compliance, and research verification, manual review of millions of financial or experimental transactions is impossible. Fraudsters routinely fabricate numbers to cover shortfalls or pad expenses.
      </p>
      <div class="pill-highlight">
        <strong>Core Psychological Conflict:</strong> Natural growth processes follow logarithmic scales, whereas humans inventing numbers instinctively distribute digits uniformly (~11.1% each) and avoid repeating digit 1.
      </div>
      <p>
        <strong>Objective:</strong> Leverage an undergraduate statistical hypothesis test (&chi;&sup2; goodness-of-fit) to establish an automated, non-invasive triage tool for detecting fabricated numerical records.
      </p>
    </div>

    <!-- Syllabus Theory -->
    <div class="card accent">
      <div class="card-title"><span class="badge">02</span> Concepts &amp; Hypothesis Testing</div>
      <p><strong>Benford's First-Digit Law:</strong> In naturally occurring unconstrained data spanning multiple orders of magnitude, the probability of leading digit d &isin; {1, &hellip;, 9} is:</p>
      <div class="formula-box">
        P(d) = log<sub>10</sub>(1 + 1/d)
      </div>
      <p style="font-size: 8.5pt; text-align: center; color: #64748B;">
        Digit 1: 30.1% | Digit 2: 17.6% | Digit 3: 12.5% &hellip; Digit 9: 4.6%
      </p>

      <p><strong>Statistical Hypotheses (Module 6):</strong></p>
      <ul>
        <li><strong>H<sub>0</sub>:</strong> First-digit distribution follows Benford's Law.</li>
        <li><strong>H<sub>1</sub>:</strong> First-digit distribution departs from Benford's Law.</li>
      </ul>

      <p><strong>Pearson's Chi-Square Test Statistic:</strong></p>
      <div class="formula-box">
        &chi;&sup2; = &sum;<sub>i=1</sub><sup>9</sup> (O<sub>i</sub> - E<sub>i</sub>)&sup2; / E<sub>i</sub>, &nbsp;&nbsp; E<sub>i</sub> = n &middot; P(i)
      </div>
      <p>
        <strong>Degrees of Freedom:</strong> df = k - 1 - m = 9 - 1 - 0 = <strong>8</strong> (no parameters estimated from sample).<br>
        <strong>Critical Value (&alpha; = 0.05, df = 8):</strong> <strong>&chi;&sup2;<sub>crit</sub> = 15.507</strong>.
      </p>
      <div class="pill-highlight">
        <strong>Cochran's Condition:</strong> E<sub>i</sub> &ge; 5 for all bins &implies; n &ge; 110. World Bank n = 217 yields E<sub>9</sub> = 9.93 &gt; 5.0 (Passed).
      </div>
    </div>
  </div>

  <!-- COLUMN 2: METHODOLOGY & DATA PROVENANCE -->
  <div class="col">
    <!-- Methodology Flow -->
    <div class="card highlight">
      <div class="card-title"><span class="badge">03</span> Audit Screening Workflow</div>
      <div class="flow-container">
        <div class="flow-step">
          <div class="num">1</div>
          <div class="text">
            Suitability &amp; Boundary Check
            <small>Verify positive, ratio scale, &ge;3 orders of magnitude (no exam scores / IDs).</small>
          </div>
        </div>
        <div class="flow-step">
          <div class="num">2</div>
          <div class="text">
            Digit Extraction Algorithm
            <small>Standardized formatC(x, "e") isolates leading digit d &isin; {1..9} without error.</small>
          </div>
        </div>
        <div class="flow-step">
          <div class="num">3</div>
          <div class="text">
            Dual Goodness-of-Fit Evaluation
            <small>Calculate &chi;&sup2; (df=8, p-val) + scale-free Mean Absolute Deviation (MAD).</small>
          </div>
        </div>
        <div class="flow-step">
          <div class="num">4</div>
          <div class="text">
            Automated Risk Triage
            <small>Green (&chi;&sup2; &le; 15.5) &bull; Yellow (boundary review) &bull; Red (&chi;&sup2; &gt; 15.5, high risk).</small>
          </div>
        </div>
        <div class="flow-step">
          <div class="num">5</div>
          <div class="text">
            Residual-Driven Audit Sampling
            <small>Focus substantive manual audit on digit bins with residuals R<sub>i</sub> &gt; +2.0.</small>
          </div>
        </div>
      </div>
    </div>

    <!-- Data Provenance -->
    <div class="card accent">
      <div class="card-title"><span class="badge">04</span> Empirical Data Provenance</div>
      <p><strong>Dataset A: Genuine Demographic Data</strong></p>
      <ul>
        <li><strong>Source:</strong> World Bank 2023 World Development Indicators (`SP.POP.TOTL`).</li>
        <li><strong>Cleaning:</strong> 266 entities &rarr; excluded 1 null &amp; 48 regional aggregates &rarr; <strong>n = 217 sovereign nations</strong>.</li>
        <li><strong>Span:</strong> 9,816 (Tuvalu) to 1.44B (India) &mdash; spans 5 orders of magnitude without artificial caps.</li>
      </ul>

      <p style="margin-top: 3mm;"><strong>Dataset B: Simulated Fabricated Example</strong></p>
      <ul>
        <li><strong>Sample:</strong> n = 217, fixed seed = 2026.</li>
        <li><strong>Cognitive Mechanism:</strong> Models the <em>equal-likelihood fallacy</em> where humans invent numbers choosing digits 1&ndash;9 roughly uniformly (~11.1% each) across commercial invoice scales.</li>
        <li><em>Disclaimer: Demonstration example; not actual fraud allegations.</em></li>
      </ul>
    </div>
  </div>

  <!-- COLUMN 3: EMPIRICAL RESULTS & CHARTS -->
  <div class="col">
    <div class="card success">
      <div class="card-title"><span class="badge">05</span> Empirical Findings &amp; Visualizations</div>
      
      <!-- Genuine Plot -->
      <div class="chart-box">
        <img src="__IMG_GENUINE_PLACEHOLDER__" alt="Genuine World Bank Populations vs Benford">
        <div class="chart-label">Figure 1: Authentic World Bank Populations (n = 217) &mdash; Conforms Closely</div>
      </div>

      <!-- Fabricated Plot -->
      <div class="chart-box">
        <img src="__IMG_FAKE_PLACEHOLDER__" alt="Fabricated Data vs Benford">
        <div class="chart-label">Figure 2: Simulated Fabricated Data (n = 217) &mdash; Massive Deviation in 1, 5, 7, 8, 9</div>
      </div>

      <!-- Master Results Table -->
      <table class="poster-table">
        <thead>
          <tr>
            <th>Dataset</th>
            <th>n</th>
            <th>&chi;&sup2;</th>
            <th>p-value</th>
            <th>MAD</th>
            <th>Decision (&alpha;=0.05)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>World Bank (Genuine)</strong></td>
            <td>217</td>
            <td>7.608</td>
            <td>0.4726</td>
            <td>0.0152</td>
            <td class="status-pass">Fail to Reject H<sub>0</sub></td>
          </tr>
          <tr>
            <td><strong>Simulated Fabrication</strong></td>
            <td>217</td>
            <td>79.982</td>
            <td>4.93e-14</td>
            <td>0.0621</td>
            <td class="status-fail">Reject H<sub>0</sub> (Flagged)</td>
          </tr>
          <tr>
            <td><strong>R Rivers Benchmark</strong></td>
            <td>141</td>
            <td>44.177</td>
            <td>5.27e-07</td>
            <td>0.0525</td>
            <td class="status-fail">Reject H<sub>0</sub> (Truncated)</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- COLUMN 4: DISCUSSION, PARADOX & CONCLUSION -->
  <div class="col">
    <!-- River Paradox -->
    <div class="card warning">
      <div class="card-title"><span class="badge">06</span> The River Lengths Paradox</div>
      <p>
        The historical North American rivers dataset (n = 141) failed Benford's test (&chi;&sup2; = 44.18, p &lt; 0.001). Why?
      </p>
      <div class="pill-warning">
        <strong>Selection Truncation Effect:</strong> The USGS World Almanac recorded only "major" rivers (&gt;135 miles). Omitting small streams broke scale invariance, clustering values between 200&ndash;400 miles (digit 3 count: 36 vs exp 17.6).
      </div>
      <p>
        <strong>Vital Lesson:</strong> A rejection is NOT proof of fraud! Bounded or truncated authentic datasets naturally depart from Benford.
      </p>
    </div>

    <!-- Conclusions & Limitations -->
    <div class="card highlight">
      <div class="card-title"><span class="badge">07</span> Conclusions &amp; Audit Limits</div>
      <ul>
        <li><strong>Clear Contrast:</strong> Genuine data conformed (&chi;&sup2; = 7.608, p = 0.473), whereas uniform fabrication failed overwhelmingly (&chi;&sup2; = 79.982, p = 4.93&times;10<sup>-14</sup>).</li>
        <li><strong>Effect Size is Mandatory:</strong> With large samples, &chi;&sup2; rejects tiny deviations. Mean Absolute Deviation (MAD) provides scale-free practical significance.</li>
        <li><strong>Audit Ethics:</strong> Rejection flags anomalies for manual review; failure to reject does not guarantee innocence.</li>
      </ul>
    </div>

    <!-- References -->
    <div class="card accent">
      <div class="card-title"><span class="badge">08</span> Verified References</div>
      <p style="font-size: 8pt; line-height: 1.3; margin: 0; color: #475569;">
        &bull; <strong>Benford, F. (1938).</strong> Law of Anomalous Numbers. <em>Proc. Amer. Phil. Soc.</em>, 78(4).<br>
        &bull; <strong>Nigrini, M. J. (2012).</strong> <em>Benford's Law: Forensic Accounting &amp; Fraud Detection</em>. Wiley.<br>
        &bull; <strong>Cochran, W. G. (1954).</strong> Strengthening Common &chi;&sup2; Tests. <em>Biometrics</em>, 10(4).<br>
        &bull; <strong>Hill, T. P. (1995).</strong> Statistical Derivation of Significant-Digit Law. <em>Stat. Sci.</em>, 10(4).<br>
        &bull; <strong>World Bank (2024).</strong> World Development Indicators: Total Population (SP.POP.TOTL).
      </p>
    </div>
  </div>

</main>

<!-- FOOTER -->
<footer>
  <div>
    <strong>BMAT202 Probability and Statistics DA3</strong> &bull; School of Advanced Sciences (SAS), Department of Mathematics, VIT Chennai
  </div>
  <div>
    Generated via R / Headless Chrome Pipeline &bull; Print Standard: A1 Landscape (841 &times; 594 mm) &bull; Verified 22 October 2026
  </div>
</footer>

</body>
</html>
"""

# Inject images
html_content = html_template.replace("__IMG_GENUINE_PLACEHOLDER__", img_genuine_b64)
html_content = html_content.replace("__IMG_FAKE_PLACEHOLDER__", img_fake_b64)

# Write HTML file
html_path = os.path.join(POSTER_DIR, "BMAT202_DA3_Poster.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"[POSTER] Wrote HTML poster source to: {html_path}")

# Compile high-res 150 DPI PNG using Headless Chrome (4967 x 3508 pixels for exact A1 841 x 594 mm)
png_path = os.path.join(POSTER_DIR, "BMAT202_DA3_Poster.png")
chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

cmd_png = [
    chrome_bin,
    "--headless=new",
    "--disable-gpu",
    "--window-size=4967,3508",
    f"--screenshot={png_path}",
    html_path
]

print(f"[POSTER] Compiling 150 DPI A1 PNG via Chrome: {' '.join(cmd_png)}")
res_png = subprocess.run(cmd_png, capture_output=True, text=True)
if res_png.returncode == 0 and os.path.exists(png_path):
    size_kb = os.path.getsize(png_path) / 1024
    print(f"[POSTER] Successfully generated PNG: {png_path} ({size_kb:.1f} KB)")
else:
    print(f"[POSTER ERROR] PNG generation failed: {res_png.stderr}")

# Convert directly to exact A1 Landscape single-page PDF via PIL
pdf_path = os.path.join(POSTER_DIR, "BMAT202_DA3_Poster.pdf")
img = Image.open(png_path).convert("RGB")
img.save(pdf_path, "PDF", resolution=150.0)

reader = pypdf.PdfReader(pdf_path)
page = reader.pages[0]
width_mm = float(page.mediabox.width) * 25.4 / 72.0
height_mm = float(page.mediabox.height) * 25.4 / 72.0
print(f"[POSTER] Generated exact A1 Landscape PDF: {pdf_path}")
print(f"         Pages: {len(reader.pages)}, Dimensions: {width_mm:.1f} x {height_mm:.1f} mm")
