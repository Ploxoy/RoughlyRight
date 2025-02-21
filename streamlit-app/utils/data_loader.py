import pandas as pd
import requests
from io import StringIO

# URL of KNMI dataset
URL = "https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/maandgegevens/mndgeg_260_tg.txt"
LOCAL_FILE = "mndgeg_260_tg.txt"  # Local fallback if URL fails

def load_temperature_data():
    """Loads and processes temperature data from the KNMI website or local file."""
    
    try:
        response = requests.get(URL)
        data = response.text
        if not data.strip():
            raise ValueError("Failed to download data from KNMI. The response is empty.")
    except requests.RequestException:
        print("⚠️ Could not fetch data from KNMI. Using local file instead.")
        with open(LOCAL_FILE, "r", encoding="utf-8") as file:
            data = file.read()
    
    # Split into lines
    lines = data.split("\n")

    # Find the header line index
    header_line_index = next((i for i, line in enumerate(lines) if "STN,YYYY" in line), None)

    if header_line_index is None:
        raise ValueError("Could not find the header line in the file.")

    # Read the data from the correct position, skipping the next line after the header
    data_lines = lines[header_line_index:]  # Keep header row

    # Read the CSV with explicit header handling
    df = pd.read_csv(
        StringIO("\n".join(data_lines)),
        delimiter=",",
        skipinitialspace=True,
        header=0,  # Use the first line as column headers
        skip_blank_lines=True
    )

    # Print columns for debugging
   # print("Columns found:", df.columns)

    # Ensure required columns exist
    required_columns = {"YYYY", "YEAR"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Unexpected data format. Expected columns: {required_columns}, but found: {df.columns}")

    df = df[["YYYY", "YEAR"]].dropna()
    df.columns = ["Year", "Mean_Temperature"]
    df["Mean_Temperature"] = df["Mean_Temperature"].astype(float) / 10  # Convert to degrees Celsius
    df["Year"] = df["Year"].astype(int)

    return df
