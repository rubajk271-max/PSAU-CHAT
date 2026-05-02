import pandas as pd

def print_cols(file, sheet=0):
    try:
        df = pd.read_excel(file, sheet_name=sheet)
        print(f"--- {file} (Sheet {sheet}) ---")
        print("Columns:", df.columns.tolist())
        print("Sample data:")
        print(df.head(3))
        print("\n")
    except Exception as e:
        print(f"Error reading {file}: {e}")

print_cols('doctorsEE(1).xlsx')
print_cols('rooms.xlsx')
print_cols('level.xlsx', sheet=0)
print_cols('level.xlsx', sheet=1)
