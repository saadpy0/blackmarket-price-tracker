import pandas as pd
from prophet import Prophet

RAW_CSV = 'data/market_data_clean_no_anomaly.csv'  # Use anomaly-free data
PRODUCT = 'Tipping the Velvet'
FORECAST_CSV = f'data/forecast_{PRODUCT.replace(" ", "_")}_no_anomaly.csv'
PERIODS = 30  # Forecast 30 days into the future


def main():
    df = pd.read_csv(RAW_CSV)
    product_df = df[df['product_name'] == PRODUCT].copy()
    # Prepare data for Prophet
    product_df['ds'] = pd.to_datetime(product_df['timestamp'])
    product_df['y'] = product_df['price'].astype(float)
    prophet_df = product_df[['ds', 'y']].sort_values('ds')
    if len(prophet_df) < 2:
        print(f"Not enough data to forecast for {PRODUCT}.")
        return
    model = Prophet()
    model.fit(prophet_df)
    future = model.make_future_dataframe(periods=PERIODS)
    forecast = model.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(FORECAST_CSV, index=False)
    print(f"Forecast for {PRODUCT} (no anomaly) saved to {FORECAST_CSV}.")

if __name__ == "__main__":
    main() 