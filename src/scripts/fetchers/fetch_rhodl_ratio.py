import pandas as pd
import requests
import os
from datetime import datetime


def fetch_rhodl_ratio_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Failed to fetch the data from the URL.")
    return response.json()


def parse_and_save_data(data, indicator_name):
    # Extract data from 'line'
    timestamps = data["data"]["line"]["timeList"]
    rhodl_values = data["data"]["line"]["value1"]
    btc_prices = data["data"]["line"]["btcPrice"]

    # Create DataFrame
    df = pd.DataFrame(
        {"timestamp": timestamps, "rhodl_ratio": rhodl_values, "price": btc_prices}
    )

    today = datetime.today().strftime("%B_%d_%Y")
    raw_data_path = os.path.join(
        os.path.dirname(__file__),
        "../../../data/raw",
        f"{indicator_name}_{today}_raw.csv",
    )
    os.makedirs(os.path.dirname(raw_data_path), exist_ok=True)
    df.to_csv(raw_data_path, index=False)

    print(f"Data saved to {raw_data_path}")
    return df


# Fetch and save raw data
url = "https://coinank.com/indicatorapi/chain/index/charts?type=%2Fcharts%2Frhodl-ratio%2F"
data = fetch_rhodl_ratio_data(url)
indicator_name = "RHODL_Ratio"
df_raw = parse_and_save_data(data, indicator_name)
print(df_raw.tail())
