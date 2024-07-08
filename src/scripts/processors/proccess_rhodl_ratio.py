import pandas as pd
import os
from datetime import datetime


def calculate_z_score(indicator_name, date_today):
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

    # Ensure 'rhodl_ratio' column is numeric
    df["rhodl_ratio"] = pd.to_numeric(df["rhodl_ratio"], errors="coerce")

    # Convert timestamp to readable date format and remove the timestamp column
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.strftime("%Y-%m-%d")
    df.drop(columns=["timestamp"], inplace=True)

    # Reorder columns to place 'date' first
    df = df[["date", "rhodl_ratio", "price"]]

    # Rename 'price' to 'BTC price'
    df.rename(columns={"price": "BTC price"}, inplace=True)

    # Calculate mean and standard deviation
    mean = df["rhodl_ratio"].mean()
    std = df["rhodl_ratio"].std()

    # Calculate Z-score and invert it
    df["z_score"] = -((df["rhodl_ratio"] - mean) / std)

    # Define the processed data path
    processed_data_path = os.path.join(
        os.path.dirname(__file__),
        "../../../data/processed",
        f"{indicator_name}_{date_today}_processed.csv",
    )

    # Ensure the processed data directory exists
    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)

    # Save the processed dataframe
    df.to_csv(processed_data_path, index=False)

    print(f"Processed data saved to {processed_data_path}")

    # Print the latest Z-score
    latest_z_score = df.iloc[-1]["z_score"]
    print(f"Latest Z-score for {indicator_name}: {latest_z_score}")

    return df


# Usage
indicator_name = "RHODL_Ratio"
date_today = datetime.today().strftime("%B_%d_%Y")
df_processed = calculate_z_score(indicator_name, date_today)
print(df_processed.tail())
