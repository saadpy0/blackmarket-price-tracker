import pandas as pd
import re

RAW_CSV = 'data/market_data.csv'
CLEAN_CSV = 'data/market_data_clean.csv'


def clean_price(price):
    if pd.isna(price):
        return None
    # Remove any non-numeric (except dot and minus)
    price = re.sub(r'[^0-9.\-]', '', str(price))
    try:
        return float(price)
    except ValueError:
        return None

def main():
    df = pd.read_csv(RAW_CSV)
    # Clean price
    df['price'] = df['price'].apply(clean_price)
    # Drop rows with missing or invalid price
    df = df.dropna(subset=['price'])
    # Strip whitespace from product_name, vendor, currency
    for col in ['product_name', 'vendor', 'currency']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    df.to_csv(CLEAN_CSV, index=False)
    print(f"Cleaned data saved to {CLEAN_CSV}. Rows: {len(df)}")

if __name__ == "__main__":
    main() 