import pandas as pd
df_docs = pd.read_excel('doctorsEE(1).xlsx')
print(df_docs[df_docs['Course name'].astype(str).str.contains('الذكاء الاصطناعي', na=False)][['Doctor name', 'Course name']])
