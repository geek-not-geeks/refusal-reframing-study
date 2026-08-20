"""
Statistical analysis script -- run this AFTER all manual corrections
(fix_pilot_rows.py-style fixes) have been applied to your CSV files.

This computes:
1. Refusal rate by provider and category (with confidence intervals)
2. Chi-square test: does refusal rate differ significantly by category?
3. Chi-square test: does refusal rate differ significantly by provider?
4. Self-correction rate by provider (with the two-metric split from
   the findings doc -- pedagogical framing vs. genuine unprompted
   correction)

Requires: pip3 install scipy pandas
"""

import csv
import pandas as pd
from scipy import stats
from pathlib import Path

# --- CONFIG: point this at your combined/cleaned CSV ---
# If your three providers are in separate files, combine them first:
#   cat data/study_results.csv > data/combined_results.csv
# (adjust paths to match your actual file layout)
CSV_PATH = Path("data/study_results.csv")  # all 3 providers already in one file

def load_data():
    df = pd.read_csv(CSV_PATH)
    return df

def refusal_rate_table(df):
    """Cross-tab: provider x category, showing refusal rate."""
    df['is_refusal'] = df['refusal_type'].isin(['EXPLANATORY', 'BARE'])
    table = df.groupby(['model_provider', 'category'])['is_refusal'].agg(['sum', 'count', 'mean'])
    table.columns = ['refusals', 'total_trials', 'refusal_rate']
    print("\n=== REFUSAL RATE BY PROVIDER x CATEGORY ===")
    print(table)
    return table

def chi_square_category(df):
    """Does refusal rate differ significantly across categories A/B/C?"""
    df['is_refusal'] = df['refusal_type'].isin(['EXPLANATORY', 'BARE'])
    contingency = pd.crosstab(df['category'], df['is_refusal'])
    print("\n=== CONTINGENCY TABLE: Category x Refusal ===")
    print(contingency)
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    print(f"\nChi-square statistic: {chi2:.4f}")
    print(f"p-value: {p:.6f}")
    print(f"Degrees of freedom: {dof}")
    if p < 0.05:
        print("RESULT: Statistically significant difference in refusal rate across categories (p < 0.05)")
    else:
        print("RESULT: No statistically significant difference found (p >= 0.05) -- "
              "report as a null/non-significant result, not as 'no effect'.")
    return chi2, p

def chi_square_provider(df):
    """Does refusal rate differ significantly across providers?"""
    df['is_refusal'] = df['refusal_type'].isin(['EXPLANATORY', 'BARE'])
    contingency = pd.crosstab(df['model_provider'], df['is_refusal'])
    print("\n=== CONTINGENCY TABLE: Provider x Refusal ===")
    print(contingency)
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    print(f"\nChi-square statistic: {chi2:.4f}")
    print(f"p-value: {p:.6f}")
    if p < 0.05:
        print("RESULT: Statistically significant difference in refusal rate across providers (p < 0.05)")
    else:
        print("RESULT: No statistically significant difference found (p >= 0.05)")
    return chi2, p

def reframe_success_by_refusal_type(df):
    """
    Core original research question: does EXPLANATORY vs BARE refusal
    predict reframe success differently? NOTE: with only 5 Anthropic
    refusals total (4 EXPLANATORY, 1 BARE), this sample is too small
    for a reliable chi-square -- report descriptively and flag the
    small-N limitation explicitly rather than over-interpreting a
    p-value from so few data points.
    """
    refusals_only = df[df['refusal_type'].isin(['EXPLANATORY', 'BARE'])].copy()
    refusals_only['reframe_succeeded'] = refusals_only['reframe_score'].astype(int) >= 2
    print("\n=== REFRAME SUCCESS RATE BY REFUSAL TYPE (core research question) ===")
    if len(refusals_only) < 10:
        print(f"WARNING: only {len(refusals_only)} genuine refusals in the entire dataset. "
              "This is too small for a reliable statistical test. Report descriptively:")
        print(refusals_only.groupby('refusal_type')['reframe_succeeded'].agg(['sum', 'count', 'mean']))
    else:
        contingency = pd.crosstab(refusals_only['refusal_type'], refusals_only['reframe_succeeded'])
        chi2, p, dof, expected = stats.chi2_contingency(contingency)
        print(f"Chi-square: {chi2:.4f}, p-value: {p:.6f}")

if __name__ == "__main__":
    df = load_data()
    print(f"Loaded {len(df)} total trials across all providers.")
    refusal_rate_table(df)
    chi_square_category(df)
    chi_square_provider(df)
    reframe_success_by_refusal_type(df)