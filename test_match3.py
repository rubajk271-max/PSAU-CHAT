import pandas as pd
import re

df_docs = pd.read_excel('doctorsEE(1).xlsx')
print(repr(df_docs['Course code'].dropna().head(10).tolist()))
