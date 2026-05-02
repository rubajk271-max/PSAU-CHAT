import pandas as pd
import re

df_docs = pd.read_excel('doctorsEE(1).xlsx')
subject_code = '3121'

mask = df_docs['Course code'].astype(str).str.contains(rf'\b[A-Za-z]*{subject_code}\b', regex=True, na=False)
doc_row = df_docs[mask]
print("Code matching:")
print(doc_row[['Course name', 'Course code']])

subject_code_2 = '101'
mask2 = df_docs['Course code'].astype(str).str.contains(rf'\b[A-Za-z]*{subject_code_2}\b', regex=True, na=False)
print("Code matching 2:")
print(df_docs[mask2][['Course name', 'Course code']])
