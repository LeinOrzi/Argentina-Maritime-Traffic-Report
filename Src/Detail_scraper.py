import requests
from bs4 import BeautifulSoup
import pandas as pd

output_file = "Septiembre_24.xlsx"

url = "https://www.isa-agents.com.ar/info/line_up_mndrn.php?lang=es&select_day=24&select_month=09&select_year=2025"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table")

headers = [th.get_text(strip=True) for th in table.find_all("th")]

rows = []
for tr in table.find_all("tr"):
    cells = tr.find_all("td")
    if cells:
        row = [cell.get_text(strip=True) for cell in cells]
        rows.append(row)

df = pd.DataFrame(rows, columns=headers[:len(rows[0])])

df.to_excel(output_file, index=False)

meses = {
    "-jan": "/01", "-feb": "/02", "-mar": "/03", "-apr": "/04",
    "-may": "/05", "-jun": "/06", "-jul": "/07", "-aug": "/08",
    "-sep": "/09", "-oct": "/10", "-nov": "/11", "-dec": "/12"
}

def normalizar_fechas(col):
    col = col.astype(str).str.lower()
    for abbr, num in meses.items():
        col = col.str.replace(abbr, num + "/2025", regex=False)
    col = pd.to_datetime(col, errors="coerce", dayfirst=True).dt.strftime("%d/%m")
    return col

for fecha_col in ["ETA", "ETB", "ETS"]:
    if fecha_col in df.columns:
        df[fecha_col] = normalizar_fechas(df[fecha_col])

def calcular_waiting_time(quantity):
    try:
        quantity = float(quantity)
    except:
        return None
    if quantity <= 10000:
        return 0.0
    elif quantity <= 20000:
        return 0.5
    elif quantity <= 30000:
        return 1.0
    elif quantity <= 40000:
        return 1.5
    elif quantity <= 50000:
        return 2.0
    else:
        return 2.5

if "Quantity" in df.columns:
    df["WaitingTime_Days"] = df["Quantity"].apply(calcular_waiting_time)

df.to_excel(output_file, index=False)

print(f"Datos guardados en {output_file} en una sola hoja con WaitingTime_Days y fechas normalizadas")
