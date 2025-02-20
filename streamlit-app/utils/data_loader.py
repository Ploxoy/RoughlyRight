import pandas as pd
import requests
from io import StringIO

URL = 'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/maandgegevens/mndgeg_260_tg.txt'

def load_temperature_data():
    response = requests.get(URL)
    data = response.text
    
    lines = data.split('\\n')
    start_index = next(i for i, line in enumerate(lines) if '=====' in line) + 1
    data_lines = lines[start_index:]

    df = pd.read_csv(StringIO('\\n'.join(data_lines)), delim_whitespace=True)
    df = df[['YYYY', 'YEAR']].dropna()
    df.columns = ['Year', 'Mean_Temperature']
    df['Mean_Temperature'] = df['Mean_Temperature'].astype(float) / 10
    df['Year'] = df['Year'].astype(int)
    return df