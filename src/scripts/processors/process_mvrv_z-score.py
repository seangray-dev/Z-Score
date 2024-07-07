import pandas as pd
import os
from datetime import datetime


def process_mvrv_zscore_data(indicator_name, date_today):
    # Define the raw data path
    raw_data_path = os.path.join(
        os.path.dirname(__file__),
        "../../../data/raw",
        f"{indicator_name}_{date_today}_raw.csv",
    )

    # Ensure the file exists
    if not os.path.exists(raw_data_path):
        raise FileNotFoundError(f"Raw data file not found: {raw_data_path}")

    # Read the raw data
    df = pd.read_csv(raw_data_path)

    # Convert timestamp column to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    # Invert the Z-score
    df["mvrv_z"] = -df["mvrv_z"]

    # Log the latest Z-Score from mvrv_z
    latest_z_score = df.loc[df["timestamp"].idxmax()]["mvrv_z"]
    print(f"Latest Inverted MVRV Z-Score: {latest_z_score}")

    # Save the processed dataframe
    processed_data_path = os.path.join(
        os.path.dirname(__file__),
        "../../../data/processed",
        f"{indicator_name}_{date_today}_processed.csv",
    )

    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)
    df.to_csv(processed_data_path, index=False)

    print(f"Processed data saved to {processed_data_path}")

    return df


# Usage
indicator_name = "MVRV_Z_Score"
date_today = datetime.today().strftime("%B_%d_%Y")
df_processed = process_mvrv_zscore_data(indicator_name, date_today)
print(df_processed.tail())
