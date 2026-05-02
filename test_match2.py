import pandas as pd
import re

df_docs = pd.read_excel('doctorsEE(1).xlsx')
subject_code = '101'

row_old = df_docs[df_docs['Course code'].astype(str).str.contains(subject_code, na=False)]
row_new = df_docs[df_docs['Course code'].astype(str).str.contains(rf'(^|\D){subject_code}(\D|$)', regex=True, na=False)]

print(f"Old matches: {len(row_old)}")
print(f"New matches: {len(row_new)}")
