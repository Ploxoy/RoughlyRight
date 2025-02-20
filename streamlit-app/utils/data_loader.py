import pandas as pd
import requests
from io import StringIO

URL = "https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/maandgegevens/mndgeg_260_tg.txt"

def load_temperature_data():
    response = requests.get(URL)
    data = response.text

    # Проверим, действительно ли данные загружены
    if not data:
        raise ValueError("Failed to download data from KNMI.")

    lines = data.split("\n")

    # Найдем строку, где начинаются данные
    start_index = next((i for i, line in enumerate(lines) if "=====" in line), None)

    if start_index is None:
        raise ValueError("Could not find the start of the data in the downloaded file.")

    # Пропустим строки заголовка
    data_lines = lines[start_index + 1:]

    # Преобразуем в DataFrame
    df = pd.read_csv(StringIO("\n".join(data_lines)), delim_whitespace=True, comment="#", error_bad_lines=False)
    
    if "YYYY" not in df.columns or "YEAR" not in df.columns:
        raise ValueError("Unexpected data format: required columns not found.")

    df = df[["YYYY", "YEAR"]].dropna()
    df.columns = ["Year", "Mean_Temperature"]
    df["Mean_Temperature"] = df["Mean_Temperature"].astype(float) / 10
    df["Year"] = df["Year"].astype(int)

    return df
