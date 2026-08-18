import csv
import sys

with open('data/study_results.csv') as f:
    rows = list(csv.DictReader(f))

filter_provider = sys.argv[1] if len(sys.argv) > 1 else None
if filter_provider:
    rows = [r for r in rows if r['model_provider'] == filter_provider]

for i, row in enumerate(rows):
    print(f"\n{'='*70}")
    print(f"ROW {i+1}/{len(rows)}  |  {row['model_provider']}  |  {row['category']}  |  {row['sensitivity_tier']}  |  trial {row['trial_number']}")
    print(f"{'='*70}")
    print(f"[refusal_type: {row['refusal_type']}]  [reframe_score: {row['reframe_score']}]")
    print(f"\n--- ORIGINAL RESPONSE ---")
    print(row['refusal_response_raw'])
    print(f"\n--- REFRAME RESPONSE ---")
    print(row['reframe_response_raw'])
    input("\n[Enter for next, Ctrl+C to stop]")
