import pandas as pd
import numpy as np

RAW_CSV = 'data/market_data_clean.csv'
ANOMALY_CSV = 'data/price_anomalies.csv'

# Parameters
MAD_THRESHOLD = 3.5  # Common threshold for MAD
JUMP_FACTOR = 10     # Flag if price is 10x higher/lower than previous


def mad_based_outlier(series, thresh=MAD_THRESHOLD):
    median = np.median(series)
    abs_dev = np.abs(series - median)
    mad = np.median(abs_dev)
    if mad == 0:
        return np.zeros(len(series), dtype=bool)
    modified_z_score = 0.6745 * abs_dev / mad
    return modified_z_score > thresh

def detect_anomalies(df):
    anomalies = []
    grouped = df.groupby('product_name')
    for product, group in grouped:
        group = group.sort_values('timestamp').reset_index(drop=True)
        prices = group['price'].astype(float)
        # MAD-based anomaly
        group['mad_anomaly'] = mad_based_outlier(prices)
        # Sudden jump anomaly
        group['jump_anomaly'] = False
        for i in range(1, len(prices)):
            prev = prices.iloc[i-1]
            curr = prices.iloc[i]
            if prev > 0 and (curr > prev * JUMP_FACTOR or curr < prev / JUMP_FACTOR):
                group.at[i, 'jump_anomaly'] = True
        # Debug for 'A Light in the Attic'
        if product == 'A Light in the Attic':
            print(f"\nDEBUG: {product}")
            print("Prices:", list(prices))
            print("MAD anomaly flags:", list(group['mad_anomaly']))
            print("Jump anomaly flags:", list(group['jump_anomaly']))
        # Collect anomalies
        for _, row in group[group['mad_anomaly'] | group['jump_anomaly']].iterrows():
            anomalies.append({
                'timestamp': row['timestamp'],
                'product_name': product,
                'price': row['price'],
                'mad_anomaly': bool(row['mad_anomaly']),
                'jump_anomaly': bool(row['jump_anomaly']),
                'marketplace': row.get('marketplace', ''),
                'vendor': row.get('vendor', ''),
                'url': row.get('url', '')
            })
    return pd.DataFrame(anomalies)

def main():
    df = pd.read_csv(RAW_CSV)
    anomalies_df = detect_anomalies(df)
    anomalies_df.to_csv(ANOMALY_CSV, index=False)
    print(f"Anomaly detection complete. {len(anomalies_df)} anomalies saved to {ANOMALY_CSV}.")

if __name__ == "__main__":
    main() 