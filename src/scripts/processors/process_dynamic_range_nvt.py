import os
import pandas as pd
from datetime import datetime


def calculate_z_score(indicator_name, date_today):
    # Define the raw data path
    raw_data_path = os.path.join(
        os.path.dirname(__file__),
        "../../../data/raw",
        f"{indicator_name}_{date_today}.csv",
    )

    # Ensure the file exists
    if not os.path.exists(raw_data_path):
        raise FileNotFoundError(f"Raw data file not found: {raw_data_path}")

    # Read the raw data
    df = pd.read_csv(raw_data_path)

    # Ensure columns are numeric
    df["nvts"] = pd.to_numeric(df["nvts"], errors="coerce")
    df["nvts_low"] = pd.to_numeric(df["nvts_low"], errors="coerce")
    df["nvts_high"] = pd.to_numeric(df["nvts_high"], errors="coerce")

    # Calculate mean and standard deviation for nvts
    mean_nvts = df["nvts"].mean()
    std_nvts = df["nvts"].std()

    print(f"Mean of NVT Signal: {mean_nvts}")
    print(f"Standard Deviation of NVT Signal: {std_nvts}")

    # Calculate deviations
    df["deviation_from_low"] = df["nvts"] - df["nvts_low"]
    df["deviation_from_high"] = df["nvts"] - df["nvts_high"]

    # Calculate Z-scores based on deviations and invert them
    df["z_score_low"] = (
        -(df["deviation_from_low"] - df["deviation_from_low"].mean())
        / df["deviation_from_low"].std()
    )
    df["z_score_high"] = (
        -(df["deviation_from_high"] - df["deviation_from_high"].mean())
        / df["deviation_from_high"].std()
    )

    # Average the Z-scores to get a more accurate measure
    df["z_score"] = (df["z_score_low"] + df["z_score_high"]) / 2

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


def print_highest_lowest_nvts(df):
    highest_nvts = df.loc[df["nvts"].idxmax()]
    lowest_nvts = df.loc[df["nvts"].idxmin()]

    print(
        f"Highest NVT Signal Value: {highest_nvts['nvts']} on {highest_nvts['date']}, Z-score: {highest_nvts['z_score']}"
    )
    print(
        f"Lowest NVT Signal Value: {lowest_nvts['nvts']} on {lowest_nvts['date']}, Z-score: {lowest_nvts['z_score']}"
    )


# Calculate Z-scores
indicator_name = "Dynamic_Range_NVT"
date_today = datetime.today().strftime("%B_%d_%Y")
df = calculate_z_score(indicator_name, date_today)
print(df.tail())

# Print the highest and lowest NVT signal values along with their Z-scores
print_highest_lowest_nvts(df)
