import csv

with open('data/study_results.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

for i, row in enumerate(rows):
    print(f"\n{'='*70}")
    print(f"ROW {i+1}/{len(rows)}  |  {row['category']}  |  {row['sensitivity_tier']}  |  trial {row['trial_number']}")
    print(f"{'='*70}")
    print(f"[Auto-coded refusal_type: {row['refusal_type']}]")
    print(f"\n--- ORIGINAL RESPONSE ---")
    print(row['refusal_response_raw'])
    print(f"\n[Auto-coded reframe_score: {row['reframe_score']}]")
    print(f"\n--- REFRAME RESPONSE ---")
    print(row['reframe_response_raw'])
    input("\n\n[Press Enter for next row, or Ctrl+C to stop]")