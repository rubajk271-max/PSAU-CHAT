import pandas as pd
df_docs = pd.read_excel('doctorsEE(1).xlsx')
print(df_docs[['Course name', 'Course code']].dropna().head(20).to_string())
