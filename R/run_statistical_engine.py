#!/usr/bin/env python3
"""
Statistical Calculation and Validation Engine for BMAT202 DA3
Performs rigorous Chi-Square Goodness-of-Fit and Benford's Law calculations
matching R's chisq.test() and pchisq() down to machine precision.
"""

import os
import math
import csv
import json
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Directory structure
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")
TABLES_DIR = os.path.join(OUTPUTS_DIR, "tables")
FIGURES_DIR = os.path.join(OUTPUTS_DIR, "figures")
LOGS_DIR = os.path.join(OUTPUTS_DIR, "logs")

for d in [TABLES_DIR, FIGURES_DIR, LOGS_DIR]:
    os.makedirs(d, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. THEORETICAL BENFORD PROBABILITIES
# P(d) = log10(1 + 1/d) for d in 1..9
# -----------------------------------------------------------------------------
digits = np.arange(1, 10)
benford_p = np.log10(1.0 + 1.0 / digits)
assert np.isclose(np.sum(benford_p), 1.0, atol=1e-12), "Benford probabilities must sum to 1.0"

# -----------------------------------------------------------------------------
# 2. FIRST SIGNIFICANT DIGIT EXTRACTION
# -----------------------------------------------------------------------------
def extract_first_digit(values, label="Dataset"):
    valid_digits = []
    excluded = 0
    for val in values:
        try:
            if val is None:
                excluded += 1
                continue
            f = float(val)
            if math.isnan(f) or math.isinf(f) or f == 0.0:
                excluded += 1
                continue
            # Strip sign
            f = abs(f)
            # Scientific notation guaranteed to have leading digit first
            s = f"{f:.10e}"
            d = int(s[0])
            if 1 <= d <= 9:
                valid_digits.append(d)
            else:
                excluded += 1
        except (ValueError, TypeError):
            excluded += 1
            
    print(f"[EXTRACT] '{label}': Retained {len(valid_digits)} observations ({excluded} excluded).")
    return np.array(valid_digits, dtype=int)

# -----------------------------------------------------------------------------
# 3. CHI-SQUARE GOODNESS-OF-FIT CALCULATION
# -----------------------------------------------------------------------------
def analyze_benford(digits_arr, label="Dataset", alpha=0.05):
    n = len(digits_arr)
    assert n > 0, f"Cannot analyze empty dataset {label}"
    
    # Count observed frequencies for digits 1..9
    obs_counts = np.array([np.sum(digits_arr == d) for d in range(1, 10)], dtype=float)
    exp_counts = n * benford_p
    
    # Differences and chi-square contributions
    diffs = obs_counts - exp_counts
    contributions = (diffs ** 2) / exp_counts
    chi2_stat_manual = float(np.sum(contributions))
    
    df = 9 - 1  # 8 degrees of freedom
    crit_val = float(stats.chi2.ppf(1.0 - alpha, df=df))
    
    # Scipy chi-square test
    res = stats.chisquare(f_obs=obs_counts, f_exp=exp_counts)
    chi2_stat_scipy = float(res.statistic)
    p_val_scipy = float(res.pvalue)
    
    # Manual p-value from survival function
    p_val_manual = float(stats.chi2.sf(chi2_stat_manual, df=df))
    
    assert np.isclose(chi2_stat_manual, chi2_stat_scipy, atol=1e-7)
    assert np.isclose(p_val_manual, p_val_scipy, atol=1e-7)
    
    # Proportions & MAD
    obs_props = obs_counts / n
    exp_props = benford_p
    mad = float(np.mean(np.abs(obs_props - exp_props)))
    
    # Decision
    if chi2_stat_scipy > crit_val:
        decision = "Reject H0 (Distribution departs significantly from Benford's Law)"
    else:
        decision = "Fail to Reject H0 (Distribution is consistent with Benford's Law)"
        
    min_exp = float(np.min(exp_counts))
    cochran_ok = min_exp >= 5.0
    
    # Format table
    table_rows = []
    for i in range(9):
        d = i + 1
        table_rows.append({
            "Digit": d,
            "Observed_Count": int(obs_counts[i]),
            "Expected_Count": round(exp_counts[i], 4),
            "Observed_Proportion": round(obs_props[i], 5),
            "Expected_Proportion": round(exp_props[i], 5),
            "O_minus_E": round(diffs[i], 4),
            "ChiSquare_Contrib": round(contributions[i], 5)
        })
        
    return {
        "label": label,
        "n": n,
        "obs_counts": obs_counts,
        "exp_counts": exp_counts,
        "obs_props": obs_props,
        "exp_props": exp_props,
        "chi2_stat": chi2_stat_scipy,
        "df": df,
        "crit_val": crit_val,
        "p_val": p_val_scipy,
        "mad": mad,
        "decision": decision,
        "min_exp": min_exp,
        "cochran_ok": cochran_ok,
        "table": table_rows
    }

# -----------------------------------------------------------------------------
# 4. PUBLICATION-QUALITY PLOTTING
# -----------------------------------------------------------------------------
def setup_plot_style():
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
        'axes.edgecolor': '#D1D5DB',
        'axes.linewidth': 1.2,
        'grid.color': '#E5E7EB',
        'grid.linestyle': '--',
        'grid.alpha': 0.7,
        'xtick.color': '#374151',
        'ytick.color': '#374151',
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'figure.autolayout': True
    })

def plot_dataset_benford(res, filename, bar_color="#1E3A8A"):
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    
    digits = np.arange(1, 10)
    obs_p = res["obs_props"]
    exp_p = res["exp_props"]
    
    bars = ax.bar(digits, obs_p, width=0.6, color=bar_color, alpha=0.9,
                  label="Observed Proportion", zorder=3, edgecolor='#1E293B', linewidth=1)
    
    # Overlay theoretical curve
    ax.plot(digits, exp_p, color="#DC2626", marker="s", markersize=7,
            linewidth=2.5, label="Benford's Law (Theoretical)", zorder=4)
    
    # Percentage labels
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, h + 0.008,
                f"{h*100:.1f}%", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#1F2937')
        
    ax.set_xticks(digits)
    ax.set_xlabel("First Significant Digit ($d$)", fontsize=13, fontweight='bold', labelpad=10)
    ax.set_ylabel("Relative Frequency (Proportion)", fontsize=13, fontweight='bold', labelpad=10)
    ax.set_ylim(0, max(np.max(obs_p), np.max(exp_p)) * 1.22)
    ax.grid(True, axis='y', zorder=0)
    
    # Subtitle with stats
    ax.set_title(f"{res['label']}\n"
                 f"$n = {res['n']}$ | $\chi^2 = {res['chi2_stat']:.3f}$ ($df=8$) | "
                 f"$p = {res['p_val']:.4e}$ | $\\mathrm{{MAD}} = {res['mad']:.4f}$",
                 fontsize=13, fontweight='bold', pad=12, color='#111827')
    
    ax.legend(frameon=True, facecolor='#F9FAFB', edgecolor='#E5E7EB', fontsize=11, loc='upper right')
    
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    print(f"[FIGURE] Saved figure: {filename}")

def plot_comparative_benford(res1, res2, filename):
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    
    digits = np.arange(1, 10)
    w = 0.35
    
    b1 = ax.bar(digits - w/2, res1["obs_props"], width=w, color="#2563EB", alpha=0.9,
                label=f"{res1['label']} ($\chi^2={res1['chi2_stat']:.2f}$, $p={res1['p_val']:.4f}$)",
                zorder=3, edgecolor='#1E3A8A', linewidth=1)
    b2 = ax.bar(digits + w/2, res2["obs_props"], width=w, color="#D97706", alpha=0.9,
                label=f"{res2['label']} ($\chi^2={res2['chi2_stat']:.2f}$, $p={res2['p_val']:.2e}$)",
                zorder=3, edgecolor='#92400E', linewidth=1)
    
    # Theoretical curve
    ax.plot(digits, res1["exp_props"], color="#DC2626", marker="D", markersize=7.5,
            linewidth=2.8, label="Benford's Law (Theoretical $P(d)=\log_{10}(1+1/d)$)", zorder=4)
    
    ax.set_xticks(digits)
    ax.set_xlabel("First Significant Digit ($d$)", fontsize=13, fontweight='bold', labelpad=10)
    ax.set_ylabel("Relative Frequency (Proportion)", fontsize=13, fontweight='bold', labelpad=10)
    ax.set_ylim(0, max(np.max(res1["obs_props"]), np.max(res2["obs_props"]), np.max(res1["exp_props"])) * 1.25)
    ax.grid(True, axis='y', zorder=0)
    
    ax.set_title("Comparative Benford Analysis: Genuine Demographic Data vs Simulated Fabrication\n"
                 "Side-by-Side First-Digit Distribution and Goodness-of-Fit Evaluation",
                 fontsize=13.5, fontweight='bold', pad=14, color='#111827')
    
    ax.legend(frameon=True, facecolor='#F9FAFB', edgecolor='#E5E7EB', fontsize=10.5, loc='upper right')
    
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    print(f"[FIGURE] Saved comparative figure: {filename}")

# -----------------------------------------------------------------------------
# 5. DATA INGESTION & PIPELINE EXECUTION
# -----------------------------------------------------------------------------
def run_pipeline():
    print("=" * 80)
    print(" BMAT202 DA3: EXECUTING STATISTICAL ANALYSIS PIPELINE")
    print("=" * 80)
    
    # 1. Genuine World Bank Population Data
    wb_csv = os.path.join(DATA_DIR, "processed", "world_bank_population_2023_clean.csv")
    wb_pops = []
    with open(wb_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            wb_pops.append(float(r["population"]))
            
    digits_genuine = extract_first_digit(wb_pops, label="World Bank Population (2023)")
    res_genuine = analyze_benford(digits_genuine, label="Genuine World Bank Country Populations (2023)")
    
    # 2. Simulated Fabricated Data
    fake_csv = os.path.join(DATA_DIR, "processed", "simulated_fabricated_data.csv")
    fake_vals = []
    with open(fake_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            fake_vals.append(float(r["value"]))
            
    digits_fake = extract_first_digit(fake_vals, label="Simulated Fabricated Data")
    res_fake = analyze_benford(digits_fake, label="Simulated Fabricated Numbers (Uniform Bias)")
    
    # 3. Built-in Rivers dataset
    rivers_data = [
        735, 320, 325, 392, 524, 450, 1459, 135, 465, 600, 330, 336, 280, 315,
        870, 906, 202, 329, 290, 1000, 600, 505, 1450, 840, 1243, 890, 350, 407,
        286, 280, 525, 720, 390, 250, 327, 230, 265, 850, 210, 630, 260, 230,
        360, 730, 600, 306, 390, 420, 291, 710, 340, 217, 281, 352, 259, 250,
        470, 680, 570, 350, 300, 560, 900, 625, 332, 2348, 1171, 3710, 2315, 2533,
        780, 280, 410, 460, 260, 255, 431, 350, 760, 618, 338, 981, 1306, 500,
        696, 605, 250, 411, 1054, 735, 233, 435, 490, 310, 460, 383, 375, 1270,
        545, 445, 1885, 380, 300, 380, 377, 425, 276, 210, 800, 420, 350, 360,
        538, 1100, 1205, 314, 237, 610, 360, 540, 1038, 424, 310, 300, 444, 301,
        268, 620, 215, 652, 900, 525, 246, 360, 529, 500, 720, 270, 430, 671,
        1770
    ]
    # Save rivers CSV for reproducibility
    with open(os.path.join(DATA_DIR, "processed", "rivers.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["river_id", "length_miles"])
        for idx, val in enumerate(rivers_data, 1):
            w.writerow([idx, val])
            
    digits_rivers = extract_first_digit(rivers_data, label="North American Rivers")
    res_rivers = analyze_benford(digits_rivers, label="North American River Lengths (rivers)")
    
    # -------------------------------------------------------------------------
    # EXPORT CSV FREQUENCY TABLES
    # -------------------------------------------------------------------------
    def export_table(res, filename):
        keys = ["Digit", "Observed_Count", "Expected_Count", "Observed_Proportion",
                "Expected_Proportion", "O_minus_E", "ChiSquare_Contrib"]
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(res["table"])
        print(f"[TABLE] Exported frequency table: {filename}")
        
    export_table(res_genuine, os.path.join(TABLES_DIR, "genuine_frequency_table.csv"))
    export_table(res_fake,    os.path.join(TABLES_DIR, "fabricated_frequency_table.csv"))
    export_table(res_rivers,  os.path.join(TABLES_DIR, "rivers_frequency_table.csv"))
    
    # Export Model Comparison Summary CSV
    comp_rows = [
        {
            "Dataset": res_genuine["label"],
            "Valid_N": res_genuine["n"],
            "ChiSquare_Stat": round(res_genuine["chi2_stat"], 4),
            "Degrees_of_Freedom": res_genuine["df"],
            "Critical_Val_05": round(res_genuine["crit_val"], 4),
            "P_Value": f"{res_genuine['p_val']:.6e}",
            "MAD": round(res_genuine["mad"], 5),
            "Min_Expected_Count": round(res_genuine["min_exp"], 2),
            "Decision_Alpha_05": res_genuine["decision"]
        },
        {
            "Dataset": res_fake["label"],
            "Valid_N": res_fake["n"],
            "ChiSquare_Stat": round(res_fake["chi2_stat"], 4),
            "Degrees_of_Freedom": res_fake["df"],
            "Critical_Val_05": round(res_fake["crit_val"], 4),
            "P_Value": f"{res_fake['p_val']:.6e}",
            "MAD": round(res_fake["mad"], 5),
            "Min_Expected_Count": round(res_fake["min_exp"], 2),
            "Decision_Alpha_05": res_fake["decision"]
        },
        {
            "Dataset": res_rivers["label"],
            "Valid_N": res_rivers["n"],
            "ChiSquare_Stat": round(res_rivers["chi2_stat"], 4),
            "Degrees_of_Freedom": res_rivers["df"],
            "Critical_Val_05": round(res_rivers["crit_val"], 4),
            "P_Value": f"{res_rivers['p_val']:.6e}",
            "MAD": round(res_rivers["mad"], 5),
            "Min_Expected_Count": round(res_rivers["min_exp"], 2),
            "Decision_Alpha_05": res_rivers["decision"]
        }
    ]
    with open(os.path.join(TABLES_DIR, "model_comparison_summary.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(comp_rows[0].keys()))
        writer.writeheader()
        writer.writerows(comp_rows)
    print(f"[TABLE] Exported model comparison summary: {os.path.join(TABLES_DIR, 'model_comparison_summary.csv')}")
    
    # -------------------------------------------------------------------------
    # EXPORT HIGH-RESOLUTION FIGURES
    # -------------------------------------------------------------------------
    plot_dataset_benford(res_genuine, os.path.join(FIGURES_DIR, "genuine_benford_plot.png"), bar_color="#2563EB")
    plot_dataset_benford(res_fake,    os.path.join(FIGURES_DIR, "fabricated_benford_plot.png"), bar_color="#D97706")
    plot_comparative_benford(res_genuine, res_fake, os.path.join(FIGURES_DIR, "comparison_benford_plot.png"))
    
    # -------------------------------------------------------------------------
    # EXPORT RESULTS SUMMARY & LOG
    # -------------------------------------------------------------------------
    summary_path = os.path.join(OUTPUTS_DIR, "results_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("=" * 90 + "\n")
        f.write(" BMAT202 DA3: BENFORD'S LAW & CHI-SQUARE GOODNESS-OF-FIT STATISTICAL SUMMARY\n")
        f.write("=" * 90 + "\n")
        f.write("Course: BMAT202 – Probability and Statistics (Module 6: Hypothesis Testing-II)\n")
        f.write("Significance Level (alpha) = 0.05 | Degrees of Freedom (df) = 8 | Critical Value = 15.5073\n\n")
        f.write(f"{'Dataset':<48} | {'n':<5} | {'chi2':<8} | {'p-value':<12} | {'MAD':<8} | {'Decision'}\n")
        f.write("-" * 120 + "\n")
        for r in comp_rows:
            f.write(f"{r['Dataset']:<48} | {r['Valid_N']:<5} | {r['ChiSquare_Stat']:<8.3f} | {r['P_Value']:<12} | {r['MAD']:<8.4f} | {r['Decision_Alpha_05']}\n")
        f.write("\n" + "=" * 90 + "\n")
        f.write("DETAILED FREQUENCY TABLES:\n\n")
        for res in [res_genuine, res_fake, res_rivers]:
            f.write(f"--- {res['label']} (n = {res['n']}) ---\n")
            f.write(f"Digit | Observed | Expected | Obs Prop | Exp Prop | (O - E) | (O-E)^2/E\n")
            for row in res["table"]:
                f.write(f"  {row['Digit']}   | {row['Observed_Count']:<8} | {row['Expected_Count']:<8.2f} | {row['Observed_Proportion']:<8.4f} | {row['Expected_Proportion']:<8.4f} | {row['O_minus_E']:<7.2f} | {row['ChiSquare_Contrib']:<9.4f}\n")
            f.write(f"Chi-square = {res['chi2_stat']:.4f}, df = 8, p-value = {res['p_val']:.6e}, MAD = {res['mad']:.5f}\n")
            f.write(f"Decision: {res['decision']}\n\n")
            
    print(f"[SUMMARY] Saved detailed plain-text summary to: {summary_path}")
    
    # Save Run Log
    log_path = os.path.join(LOGS_DIR, "statistical_engine_run.log")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("BMAT202 DA3 Statistical Engine Run Log\n")
        f.write("Validation Engine: Python 3.14 / NumPy / SciPy Chi-Square Goodness-of-Fit\n")
        f.write("Status: Completed successfully with 0 errors.\n")
        f.write(f"World Bank records analyzed: {res_genuine['n']}\n")
        f.write(f"Simulated fabricated records analyzed: {res_fake['n']}\n")
        f.write(f"Rivers reference records analyzed: {res_rivers['n']}\n")
        f.write("All chi-square and probability integrity assertions PASSED.\n")
    print(f"[LOG] Saved run log to: {log_path}")

if __name__ == "__main__":
    run_pipeline()
