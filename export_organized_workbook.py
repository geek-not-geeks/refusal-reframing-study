"""
Builds ONE clean, organized Excel workbook from the raw data -- no
terminal artifacts, no scrolling, clearly separated by provider,
category, tier, and pilot-vs-full-run status. This replaces the need
to ever look at raw CSVs or copy-pasted terminal output again.

Sheets produced:
  1. Overview          -- the clean summary pivot table (all providers)
  2. Full_Run_Detail    -- every full-run trial, one row per trial,
                           clean columns, text wrapped, sortable/filterable
  3. Pilot_Detail       -- same, but for pilot-phase trials (kept
                           separate for transparency, excluded from
                           official stats)
"""

import pandas as pd
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows

CSV_PATH = Path("data/study_results.csv")
OUTPUT_PATH = Path("data/research_workbook_ORGANIZED.xlsx")

df = pd.read_csv(CSV_PATH)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# --- Tag pilot vs full-run (same logic as clean_and_finalize.py) ---
def tag(group):
    group = group.sort_values('timestamp')
    n = len(group)
    group = group.copy()
    if n <= 5:
        group['data_source'] = 'Full Run'
    else:
        group['data_source'] = 'Pilot'
        group.iloc[-5:, group.columns.get_loc('data_source')] = 'Full Run'
    return group

df = df.groupby(
    ['model_provider', 'category', 'sensitivity_tier'], group_keys=False
).apply(tag, include_groups=False).reset_index(drop=True)
# re-attach grouping columns lost by include_groups=False in newer pandas
orig = pd.read_csv(CSV_PATH)
orig['timestamp'] = pd.to_datetime(orig['timestamp'])
orig_sorted = orig.sort_values(['model_provider','category','sensitivity_tier','timestamp']).reset_index(drop=True)
df = orig_sorted.copy()
def tag2(g):
    g = g.sort_values('timestamp').copy()
    n = len(g)
    g['data_source'] = 'Pilot'
    g.iloc[-5:, g.columns.get_loc('data_source')] = 'Full Run' if n >= 5 else 'Pilot'
    return g
df = df.groupby(['model_provider','category','sensitivity_tier'], group_keys=False).apply(tag2)

df['is_refusal'] = df['refusal_type'].isin(['EXPLANATORY', 'BARE'])
correction_markers = ['ground truth', 'fact-check', 'fact check', 'not established',
    'research has not shown', 'is a myth', 'no scientific evidence',
    'this claim is false', 'no correlation', 'does not cause', 'debunked']
df['has_self_correction'] = df['refusal_response_raw'].apply(
    lambda t: any(m in str(t).lower() for m in correction_markers) if pd.notna(t) else False)

full_run = df[df['data_source'] == 'Full Run'].copy()
pilot = df[df['data_source'] == 'Pilot'].copy()

# --- Build the Overview summary (full-run only, official numbers) ---
overview = full_run.groupby(['model_provider', 'category', 'sensitivity_tier']).agg(
    trials=('trial_number', 'count'),
    refusals=('is_refusal', 'sum'),
    self_corrections=('has_self_correction', 'sum'),
).reset_index().sort_values(['model_provider', 'category', 'sensitivity_tier'])
overview.columns = ['Provider', 'Category', 'Sensitivity Tier', 'Trials', 'Refusals', 'Self-Corrections']

# --- Build clean per-trial detail tables ---
def clean_detail(source_df):
    out = source_df[['model_provider', 'category', 'sensitivity_tier', 'trial_number',
                      'refusal_type', 'reframe_score', 'has_self_correction',
                      'original_prompt', 'refusal_response_raw',
                      'reframe_prompt', 'reframe_response_raw']].copy()
    out.columns = ['Provider', 'Category', 'Tier', 'Trial #', 'Refusal Type',
                   'Reframe Score', 'Self-Correction?', 'Original Prompt',
                   'Original Response', 'Reframe Prompt', 'Reframe Response']
    return out.sort_values(['Provider', 'Category', 'Tier', 'Trial #'])

full_detail = clean_detail(full_run)
pilot_detail = clean_detail(pilot)

# --- Write to Excel with formatting ---
with pd.ExcelWriter(OUTPUT_PATH, engine='openpyxl') as writer:
    overview.to_excel(writer, sheet_name='Overview', index=False)
    full_detail.to_excel(writer, sheet_name='Full_Run_Detail', index=False)
    pilot_detail.to_excel(writer, sheet_name='Pilot_Detail', index=False)

# --- Formatting pass: headers bold, wrap text, freeze panes, column widths ---
from openpyxl import load_workbook
wb = load_workbook(OUTPUT_PATH)

header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
header_font = Font(color="FFFFFF", bold=True)

for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(wrap_text=True, vertical='center')
    ws.freeze_panes = "A2"
    for col_cells in ws.columns:
        col_letter = get_column_letter(col_cells[0].column)
        header_text = str(col_cells[0].value or "")
        if header_text in ('Original Prompt', 'Original Response', 'Reframe Prompt', 'Reframe Response'):
            ws.column_dimensions[col_letter].width = 60
            for cell in col_cells[1:]:
                cell.alignment = Alignment(wrap_text=True, vertical='top')
        else:
            ws.column_dimensions[col_letter].width = 16

wb.save(OUTPUT_PATH)
print(f"Organized workbook saved to: {OUTPUT_PATH}")
print(f"Sheets: Overview ({len(overview)} rows), Full_Run_Detail ({len(full_detail)} rows), Pilot_Detail ({len(pilot_detail)} rows)")