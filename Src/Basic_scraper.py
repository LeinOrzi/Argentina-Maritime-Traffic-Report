import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.isa-agents.com.ar/info/line_up_mndrn.php?lang=es&select_day=15&select_month=09&select_year=2025"

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

df.to_excel("Septiembre_15.xlsx", index=False)

print("Datos guardados en lineup.xlsx con headers")