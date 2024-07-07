import os
import pandas as pd
import requests
from datetime import datetime
from io import StringIO


def fetch_and_save_csv(url, indicator_name):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Failed to fetch the data from the URL.")

    # Parse the CSV content
    df = pd.read_csv(StringIO(response.text))

    # Define the raw data path
    today = datetime.today().strftime("%B_%d_%Y")
    raw_data_path = os.path.join(
        os.path.dirname(__file__), "../../../data/raw", f"{indicator_name}_{today}_raw.csv"
    )

    # Ensure the raw data directory exists
    os.makedirs(os.path.dirname(raw_data_path), exist_ok=True)

    # Save the dataframe to the raw data directory
    df.to_csv(raw_data_path, index=False)

    print(f"Data saved to {raw_data_path}")

    return df


# Usage
url = "https://static.dwcdn.net/data/l2ZFL.csv?v=1720364700000"
indicator_name = "Dynamic_Range_NVT"
df = fetch_and_save_csv(url, indicator_name)
print(df.tail())
