# Data Sources and Provenance Documentation
**BMAT202 Probability and Statistics – DA3 Project**  
*Title: Can a Chi-Square Test Catch Fake Numbers? Detecting Data Fabrication Using Benford's Law*

This document provides complete transparency, provenance, and data-cleaning records for all datasets utilized in the analysis.

---

## 1. Dataset A: Genuine Numerical Data (World Bank Country Populations)

- **Dataset Name:** World Development Indicators: Population, Total
- **Indicator Code:** `SP.POP.TOTL`
- **Publishing Organization:** The World Bank Group (Development Data Group)
- **Official Source Portal:** [https://data.worldbank.org/indicator/SP.POP.TOTL](https://data.worldbank.org/indicator/SP.POP.TOTL)
- **API Endpoint:** `https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?date=2023:2023&format=json&per_page=300`
- **Retrieval Date:** 20 October 2026
- **Data Year:** 2023 (most recent complete annual release available)
- **Storage Locations:**
  - Raw archive: `data/raw/world_bank_population_2023_raw.json`
  - Processed CSV: `data/processed/world_bank_population_2023_clean.csv`

### Provenance and Observations:
- **Raw Entity Count:** 266 downloaded reporting entities.
- **Data Hygiene and Cleaning Steps:**
  1. *Null / Missing Values:* 1 record (`XY` - "Not classified") had a null value and was excluded.
  2. *Regional & Income Aggregates:* 48 multi-national and regional groups (e.g., `WLD` World, `EUU` European Union, `ARB` Arab World, `EAS` East Asia & Pacific, etc.) were separated to avoid double-counting sovereign populations.
  3. *Valid Sovereign Nations & Autonomous Territories:* Exactly **217** positive numeric observations were retained.
  4. *Scale & Span:* Minimum value is 9,816 (Tuvalu); maximum value is 1,438,069,596 (India). The data spans over 5 orders of magnitude (base-10 log scale spans from 3.99 to 9.16), making it structurally ideal for Benford analysis.
  5. *Expected Count Verification:* At $n = 217$, the minimum expected digit frequency (for digit 9) is $E_9 = 217 \times \log_{10}(1 + 1/9) \approx 9.93 > 5$, completely satisfying Cochran's rule for the asymptotic chi-square goodness-of-fit test without bin-collapsing.

---

## 2. Dataset B: Simulated Fabricated Data Example

- **Dataset Label:** `simulated fabricated-data example`
- **File Location:** `data/processed/simulated_fabricated_data.csv`
- **Generation Environment:** Reproducible Python 3 / R simulation script
- **Random Number Seed:** `2026`
- **Sample Size:** $n = 217$ (matched exactly to Dataset A for controlled comparative power)
- **Cognitive Model Simulated:** Uniform First-Digit Cognitive Bias (Equal Likelihood Fallacy).
  - When humans attempt to fabricate plausible expense amounts, invoice records, or demographic metrics without statistical guidance, they intuitively assume that each leading digit $d \in \{1, 2, \dots, 9\}$ should occur with approximately equal likelihood ($\approx 1/9 \approx 11.1\%$).
  - In reality, natural multiplicative growth processes obey Benford's logarithmic decay ($30.1\%$ for 1 versus $4.6\%$ for 9).
- **Generation Method:**
  - Fixed seed: `2026`
  - First digits sampled from discrete uniform distribution: $d \sim \text{DiscreteUniform}(1, 9)$
  - Mantissas and scales: Values distributed across typical commercial invoice and accounting magnitudes (hundreds, thousands, tens of thousands): $\text{Value} = (d + U[0, 1)) \times 10^k$, where $k \in \{2, 3, 4\}$.
- **Integrity Statement & Disclaimer:**
  - This dataset is a **synthetic demonstration example** designed to illustrate how deliberate or psychological departures from logarithmic digit behavior appear in a forensic hypothesis test.
  - It does **not** represent real financial accounts, actual audit investigations, or real-world wrongdoing by any individual or institution.

---

## 3. Dataset C: Pipeline Test Reference (R Built-in `rivers`)

- **Dataset Name:** North American River Lengths (`rivers`)
- **Source:** Built-in R standard package `datasets` (originally compiled by Landwehr, 1972; McNeil, 1977).
- **Sample Size:** 141 observations (lengths in miles of 141 major North American rivers).
- **Role in Study:** Used to independently verify and unit-test the R first-digit extraction function and goodness-of-fit test pipeline against published benchmark literature.
- **Evaluation & Limitations:** At $n = 141$, $E_9 = 141 \times 0.045757 \approx 6.45 > 5$. While valid for testing, 141 observations represents a modest sample size where statistical power against minor anomalies is lower than the primary World Bank dataset ($n = 217$).
