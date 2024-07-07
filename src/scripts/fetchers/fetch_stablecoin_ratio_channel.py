import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
from datetime import datetime


def extract_plotly_data(url, target_name):
    # Setup Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    # Wait for Plotly to be available
    WebDriverWait(driver, 20).until(
        lambda d: d.execute_script("return typeof window.Plotly !== 'undefined';")
    )

    # Get the Plotly chart data
    plotly_data = driver.execute_script(
        """
        var plotly_data = [];
        var charts = document.querySelectorAll('.js-plotly-plot');
        charts.forEach(function(chart) {
            var data = chart.data;
            plotly_data = plotly_data.concat(data);
        });
        return plotly_data;
    """
    )

    driver.quit()

    if not plotly_data:
        raise ValueError("Plotly data not found in the page.")

    # Process the chart data
    data_list = []
    for dataset in plotly_data:
        name = dataset.get("name", "Unnamed")

        # Only process the target dataset
        if name == target_name:
            x_values = dataset["x"]
            y_values = dataset["y"]

            for x, y in zip(x_values, y_values):
                data_list.append({"name": name, "date": x, "value": y})

    # Convert to DataFrame
    df = pd.DataFrame(data_list)

    # Remove old raw data files
    raw_dir = os.path.join(os.path.dirname(__file__), "../../../data/raw")
    for file in os.listdir(raw_dir):
        if file.startswith(indicator_name) and file.endswith(".csv"):
            os.remove(os.path.join(raw_dir, file))

    # Save new raw data with timestamp
    current_date = datetime.now().strftime("%B_%d_%Y")
    new_raw_data_path = os.path.join(
        raw_dir, f"{indicator_name}_{current_date}_raw.csv"
    )
    os.makedirs(os.path.dirname(new_raw_data_path), exist_ok=True)
    df.to_csv(new_raw_data_path, index=False)

    return df


# Usage
url = "https://charts.checkonchain.com/btconchain/stablecoins/stablecoins_ssr_channel/stablecoins_ssr_channel_light.html"
target_name = "SSR RSI Smoothed"
indicator_name = "Stablecoin_Ratio_Channel"
df = extract_plotly_data(url, target_name)
print(df.tail())
