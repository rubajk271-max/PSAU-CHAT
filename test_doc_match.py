import pandas as pd
import re

df_docs = pd.read_excel('doctorsEE(1).xlsx')
df_level_core = pd.read_excel('level.xlsx', sheet_name=0)

subject = '3040 كهر مقدمة في الذكاء الاصطناعي'
print("Subject:", subject)

code_match = re.search(r'\d{3,4}', subject)
if code_match:
    subject_code = code_match.group()
    print("Subject code:", subject_code)
    mask = df_docs['Course code'].astype(str).apply(
        lambda x: str(x).strip().startswith(subject_code) or f" {subject_code} " in f" {str(x)} "
    )
    doc_row = df_docs[mask]
    print("Matches by code:", len(doc_row))
    if not doc_row.empty:
         doctors = doc_row['Doctor name'].dropna().unique().tolist()
         print("Doctors by code:", doctors)
    else:
         print("No matches by code. Trying by name")
         doc_row = df_docs[df_docs['Course name'].astype(str).str.lower().str.contains(subject.lower(), na=False)]
         print("Matches by name:", len(doc_row))

