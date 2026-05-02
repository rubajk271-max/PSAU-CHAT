import pandas as pd
df_core = pd.read_excel('level.xlsx', sheet_name=0)
df_elec = pd.read_excel('level.xlsx', sheet_name=1)
print("Core Levels:", df_core['Level'].unique() if 'Level' in df_core else "No Level column")
print("Elec Levels:", df_elec['Level'].unique() if 'Level' in df_elec else "No Level column")
print("\nCore columns:", df_core.columns.tolist())
print(df_core.head(10))
