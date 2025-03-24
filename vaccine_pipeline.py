"""
This Test project for Assessment for Senior Python Backend Engineer
This project  is a Python-based data pipeline that fetches,
processes, and visualizes global COVID-19 vaccine coverage data using the disease.sh API.
"""

import logging
import os

import matplotlib.pyplot as plt
import pandas as pd
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("vaccine_pipeline.log"), logging.StreamHandler()],
)


def fetch_vaccine_data(lastdays: int = 1) -> list:
    """
    Fetches COVID-19 vaccine coverage data for all countries from the disease.sh API.

    Returns:
        list: Processed vaccine coverage data (country and number of vaccines administered) or an error message.
    """
    url = (
        f"https://disease.sh/v3/covid-19/vaccine/coverage/countries?lastdays={lastdays}"
    )
    logging.info("Fetching vaccine data from API...")

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        vaccine_data = [
            {
                "country": item.get("country"),
                "vaccines_administered": (
                    list(item["timeline"].values())[0]
                    if "timeline" in item and item["timeline"]
                    else "N/A"
                ),
            }
            for item in data
        ]
        logging.info(f"Successfully fetched data for {len(vaccine_data)} countries.")
        return vaccine_data

    except requests.exceptions.RequestException as e:
        logging.error(f"Network error: {e}")
        return {"error": f"Network error: {e}"}
    except (KeyError, TypeError) as e:
        logging.error(f"Unexpected response format: {e}")
        return {"error": f"Unexpected response format: {e}"}
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        return {"error": f"Unexpected error: {e}"}


def save_to_csv(data, filename="vaccine_coverage.csv"):
    """
    Saves vaccine data to a CSV file.

    Args:
        data (list): List of dictionaries containing vaccine data.
        filename (str): Output CSV file name.
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    logging.info(f"✅ Data saved to {filename}")
    logging.info(f"First 10 rows:\n{df.head(10)}")  # Log first 10 rows


def plot_vaccine_data(data: list):
    """
    Converts the vaccine data to a pandas DataFrame and plots a bar chart.

    Args:
        data (list): Vaccine coverage data (country and number of vaccines administered).
    """
    df = pd.DataFrame(data)
    df["vaccines_administered"] = pd.to_numeric(
        df["vaccines_administered"], errors="coerce"
    )
    df = df.dropna()

    df = df.sort_values(by="vaccines_administered", ascending=False).head(10)
    df.plot(kind="bar", x="country", y="vaccines_administered", legend=False)
    plt.ylabel("Vaccines Administered in Billions")
    plt.title("Top 10 Countries by COVID-19 Vaccines Administered")
    plt.tight_layout()
    plt.savefig("vaccine_coverage.png")  # Save the plot to a file
    logging.info("📊 Vaccine data plot saved as 'vaccine_coverage.png'.")
    plt.show()


if __name__ == "__main__":
    data = fetch_vaccine_data()
    if "error" in data:
        logging.error(data["error"])
    else:
        save_to_csv(data)
        plot_vaccine_data(data)

    logging.info("✅ Vaccine pipeline completed.")
