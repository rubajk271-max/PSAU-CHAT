import pandas as pd
df = pd.read_excel('doctorsEE(1).xlsx')
print(df.columns)
if 'Level' in df.columns:
    print(df[['Course name', 'Level']].head(10))
