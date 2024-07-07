import os
import pandas as pd
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

    # Ensure 'value' column is numeric
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # Calculate mean and standard deviation
    mean = df["value"].mean()
    std = df["value"].std()

    # Calculate Z-score
    df["z_score"] = (df["value"] - mean) / std

    # Invert the Z-score for interpretation purposes
    df["z_score"] = -df["z_score"]

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

    return df


# Usage
indicator_name = "Stablecoin_Ratio_Channel"
date_today = datetime.today().strftime("%B_%d_%Y")
df = calculate_z_score(indicator_name, date_today)
print(df.tail())

# Get the highest and lowest Z-scores
highest_z_score = df.loc[df["z_score"].idxmax()]
lowest_z_score = df.loc[df["z_score"].idxmin()]

print(
    f"Highest Z-score Value: {highest_z_score['value']} on {highest_z_score['date']}, Z-score: {highest_z_score['z_score']}"
)
print(
    f"Lowest Z-score Value: {lowest_z_score['value']} on {lowest_z_score['date']}, Z-score: {lowest_z_score['z_score']}"
)
