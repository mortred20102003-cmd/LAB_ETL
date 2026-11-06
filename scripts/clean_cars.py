import pandas as pd
import re

# 1. Load from the data folder (added encoding='latin1' to fix the error)
df = pd.read_csv('data/cars_data.csv', encoding='latin1')
print(f"Original Rows: {len(df)}")

# 2. Fixed Price Cleaner (Removes ALL characters except numbers and decimals)
def clean_price(price):
    if pd.isna(price): return None
    cleaned = re.sub(r'[^\d.]', '', str(price).replace(',', '').split('-')[0])
    return float(cleaned) if cleaned else None

df['Cars Prices'] = df['Cars Prices'].apply(clean_price)

# 3. Clean Horsepower
def clean_hp(hp):
    if pd.isna(hp): return None
    cleaned = re.sub(r'[^\d.]', '', str(hp).split('-')[0])
    return float(cleaned) if cleaned else None

df['HorsePower'] = df['HorsePower'].apply(clean_hp)

# 4. Drop missing and Standardize
df = df.dropna(subset=['Company Names', 'Cars Prices'])
df['Company Names'] = df['Company Names'].str.upper().str.strip()

print(f"Cleaned Rows: {len(df)}")

# 5. Save to the data folder
df.to_csv('data/clean_cars_data.csv', index=False)
print("✅ Saved to data/clean_cars_data.csv")