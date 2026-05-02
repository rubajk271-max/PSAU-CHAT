import pandas as pd

file_name = 'navigation_updated.xlsx'

try:
    xl = pd.ExcelFile(file_name)
    print("Sheets available:", xl.sheet_names)
    
    for sheet in ['locations', 'paths', 'keywords']:
        if sheet in xl.sheet_names:
            df = pd.read_excel(file_name, sheet_name=sheet)
            print(f"\n--- {sheet} ---")
            print("Columns:", df.columns.tolist())
            print("Sample data:")
            print(df.head(3).to_string())
except Exception as e:
    print(f"Error reading {file_name}: {e}")
