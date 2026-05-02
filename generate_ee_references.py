import pandas as pd
import hashlib

# Load courses from level.xlsx
df_core = pd.read_excel('level.xlsx', sheet_name=0)
df_elec = pd.read_excel('level.xlsx', sheet_name=1)

courses = set()
for df in [df_core, df_elec]:
    for col in df.columns[1:]:
        c = df[col].dropna().tolist()
        courses.update(c)

courses = sorted(list(courses))

refs_data = {'Course name': [], 'Reference': [], 'Link': []}

for i, course in enumerate(courses):
    # Skip any stray nan objects
    if str(course) == 'nan' or not str(course).strip():
        continue
    
    clean_name = str(course).strip()
    
    # Generate some nice file name based on course
    ref_name = f"{clean_name} Textbook & Official Slides"
    
    # Create persistent pseudo-random mock GDrive link
    unique_hash = hashlib.md5(clean_name.encode()).hexdigest()[:12]
    link = f"https://drive.google.com/drive/folders/{unique_hash}?usp=sharing"
    
    refs_data['Course name'].append(clean_name)
    refs_data['Reference'].append(ref_name)
    refs_data['Link'].append(link)

df_refs = pd.DataFrame(refs_data)
df_refs.to_excel('references.xlsx', index=False)
print("references.xlsx generated with", len(refs_data['Course name']), "EE courses.")
