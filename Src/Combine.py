import pandas as pd
import os

ruta = r""
output_file = os.path.join(ruta, "Mensual.xlsx")

cols_clave = ["Port", "Berth", "Vessel", "Cargo", "Quantity", "Shipper"]

dfs = []

for file in os.listdir(ruta):
    if file.endswith(".xlsx") or file.endswith(".xls"):
        df_temp = pd.read_excel(os.path.join(ruta, file))
        if not df_temp.empty:
            dfs.append(df_temp)

df_combined = pd.concat(dfs, ignore_index=True)

df_combined.columns = df_combined.columns.str.strip()
df_combined = df_combined.drop(columns=[c for c in df_combined.columns if "Unnamed" in c or "Column" in c], errors='ignore')

def normalizar(val):
    if pd.isna(val):
        return ""
    return str(val).strip().lower()

df_combined["hash"] = df_combined[cols_clave].apply(lambda row: '-'.join(row.map(normalizar)), axis=1)

df_final = df_combined.groupby("hash", as_index=False).last()
df_final = df_final.drop(columns=["hash"])

df_final.to_excel(output_file, index=False)
print(f"Excel combinado y filtrado guardado en: {output_file}")

