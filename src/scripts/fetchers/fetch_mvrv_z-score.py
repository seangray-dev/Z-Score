import pandas as pd
import requests
import os
from datetime import datetime


def fetch_mvrv_zscore_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Failed to fetch the data from the URL.")
    return response.json()


def parse_and_save_data(data, indicator_name):
    # Extract x and y values for mvrv_z and price separately
    x_mvrv_timestamps = data["mvrv_z"]["x"]
    y_mvrv_values = data["mvrv_z"]["y"]

    x_price_timestamps = data["price"]["x"]
    y_price_values = data["price"]["y"]

    # Create DataFrame for mvrv_z
    data_list_mvrv = [
        {"timestamp": ts, "mvrv_z": mvrv_z}
        for ts, mvrv_z in zip(x_mvrv_timestamps, y_mvrv_values)
    ]
    df_mvrv = pd.DataFrame(data_list_mvrv)

    # Create DataFrame for price
    data_list_price = [
        {"timestamp": ts, "price": price}
        for ts, price in zip(x_price_timestamps, y_price_values)
    ]
    df_price = pd.DataFrame(data_list_price)

    # Merge the two DataFrames on timestamp
    df = pd.merge(df_mvrv, df_price, on="timestamp", how="outer")

    # Reorder columns to ensure correct CSV format
    df = df[["timestamp", "mvrv_z", "price"]]

    today = datetime.today().strftime("%B_%d_%Y")
    raw_data_path = os.path.join(
        os.path.dirname(__file__), "../../../data/raw", f"{indicator_name}_{today}_raw.csv"
    )
    os.makedirs(os.path.dirname(raw_data_path), exist_ok=True)
    df.to_csv(raw_data_path, index=False)

    print(f"Data saved to {raw_data_path}")
    return df


# Fetch and save raw data
url = "https://woocharts.com/bitcoin-mvrv-z/data/chart.json?1720391567040"
data = fetch_mvrv_zscore_data(url)
indicator_name = "MVRV_Z_Score"
df_raw = parse_and_save_data(data, indicator_name)
print(df_raw.tail())
