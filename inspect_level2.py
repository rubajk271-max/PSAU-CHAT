import pandas as pd
df_core = pd.read_excel('level.xlsx', sheet_name=0)
for _, row in df_core.iterrows():
    print(f"{row['Level']}: {[x for x in row.values[1:] if pd.notna(x)]}")
