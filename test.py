import pandas as pd
df = pd.read_excel('level.xlsx', sheet_name=0)
for i, row in df.iterrows():
    vals = [str(x).strip() for x in row.values[1:] if pd.notna(x) and str(x).strip()]
    print(f"[{row['Level']}] -> {vals}")
