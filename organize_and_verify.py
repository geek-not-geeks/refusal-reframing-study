"""
Builds a clean, organized summary table from the raw CSV -- no terminal
artifacts, no scrolling through transcripts. This single script answers
all three open verification questions in one run:
  1. Does any cell have the wrong number of trials? (Google bug check)
  2. What's the REAL self-correction rate, computed precisely?
  3. Are pilot and full-run rows properly separated/tagged?

Outputs a clean summary CSV you can open directly in Numbers/Excel --
already organized by provider > category > tier, easy to scan visually,
zero artifacts.
"""

import csv
import pandas as pd
from pathlib import Path
from collections import Counter

CSV_PATH = Path("data/study_results.csv")

df = pd.read_csv(CSV_PATH)
print(f"Total rows loaded: {len(df)}\n")

# ============================================================
# CHECK 1: Trial count per cell -- catches duplicate/missing trials
# ============================================================
print("="*70)
print("CHECK 1: Trial count per (provider, category, tier) cell")
print("Expected: 5 per cell for full runs. Anything != 5 needs review.")
print("="*70)
cell_counts = df.groupby(['model_provider', 'category', 'sensitivity_tier']).size()
problem_cells = cell_counts[cell_counts != 5]
print(cell_counts.to_string())
print()
if len(problem_cells) > 0:
    print("!!! CELLS WITH UNEXPECTED TRIAL COUNTS (not exactly 5):")
    print(problem_cells.to_string())
else:
    print("All cells have exactly 5 trials. No count issues found.")

# Check for actual duplicate trial_numbers within a cell (the specific
# Google bug reported: two rows both labeled "trial 1")
print("\n--- Checking for duplicate trial_number values within any cell ---")
dupes = df.groupby(['model_provider', 'category', 'sensitivity_tier', 'trial_number']).size()
dupes = dupes[dupes > 1]
if len(dupes) > 0:
    print("!!! DUPLICATE trial_number FOUND:")
    print(dupes.to_string())
else:
    print("No duplicate trial_numbers found within any cell.")

# ============================================================
# CHECK 2: Real self-correction rate, computed precisely
# ============================================================
print("\n" + "="*70)
print("CHECK 2: Self-correction rate -- precise definition")
print("Counting ORIGINAL responses that contain an unprompted")
print("correction/fact-check (not just any pedagogical framing)")
print("="*70)

# Narrow, precise markers for genuine unprompted correction --
# deliberately stricter than a broad "pedagogical framing" match
correction_markers = [
    'ground truth', 'fact-check', 'fact check', 'not established',
    'research has not shown', 'is a myth', 'no scientific evidence',
    'this claim is false', 'no correlation', 'does not cause',
    'debunked',
]

def has_correction(text):
    if pd.isna(text):
        return False
    t = str(text).lower()
    return any(m in t for m in correction_markers)

df['has_self_correction'] = df['refusal_response_raw'].apply(has_correction)
by_provider = df.groupby('model_provider')['has_self_correction'].agg(['sum', 'count', 'mean'])
by_provider.columns = ['corrections_found', 'total_rows', 'rate']
print(by_provider.to_string())
print(f"\nOverall: {df['has_self_correction'].sum()} / {len(df)} "
      f"({df['has_self_correction'].mean()*100:.1f}%)")

# ============================================================
# CHECK 3: Pilot vs full-run separation, by timestamp
# ============================================================
print("\n" + "="*70)
print("CHECK 3: Pilot vs full-run rows (by timestamp order)")
print("="*70)
df['timestamp'] = pd.to_datetime(df['timestamp'])
for provider in df['model_provider'].unique():
    sub = df[df['model_provider'] == provider].sort_values('timestamp')
    print(f"\n{provider}: {len(sub)} total rows")
    print(f"  Earliest: {sub['timestamp'].min()}")
    print(f"  Latest:   {sub['timestamp'].max()}")
    # crude pilot/full split heuristic: pilot runs happened in distinct
    # earlier time clusters -- print the timestamp gaps to help you see
    # the boundary visually
    gaps = sub['timestamp'].diff().dt.total_seconds()
    big_gaps = gaps[gaps > 300]  # gaps over 5 minutes = likely session boundary
    if len(big_gaps) > 0:
        print(f"  Possible session boundaries (>5 min gap) at rows: {list(big_gaps.index)}")

# ============================================================
# EXPORT: Clean, organized summary table
# ============================================================
print("\n" + "="*70)
print("Exporting clean organized summary...")
print("="*70)

summary = df.groupby(['model_provider', 'category', 'sensitivity_tier']).agg(
    total_trials=('trial_number', 'count'),
    refusals=('refusal_type', lambda x: (x.isin(['EXPLANATORY', 'BARE'])).sum()),
    self_corrections=('has_self_correction', 'sum'),
).reset_index()
summary = summary.sort_values(['model_provider', 'category', 'sensitivity_tier'])

output_path = Path("data/organized_summary.csv")
summary.to_csv(output_path, index=False)
print(f"Clean summary table saved to: {output_path}")
print("\nOpen this in Numbers/Excel for a fully organized, artifact-free view:")
print(summary.to_string(index=False))