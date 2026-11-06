import pandas as pd

# 1. Load the Excel file
print("Loading Excel file...")
df = pd.read_excel('data/Date_Fruit_Datasets/Date_Fruit_Datasets.xlsx', sheet_name='Date_Fruit_Datasets')

print(f"Original Rows: {len(df)}")

# 2. Clean column names (remove spaces, make lowercase)
# E.g., "MeanRR" becomes "meanrr", "Class" becomes "class"
df.columns = [c.strip().lower() for c in df.columns]

# 3. Drop any rows with missing values
df = df.dropna()

print(f"Cleaned Rows: {len(df)}")

# 4. Save to CSV for easier PostgreSQL loading
df.to_csv('data/clean_date_fruit.csv', index=False)
print("✅ Saved to data/clean_date_fruit.csv")