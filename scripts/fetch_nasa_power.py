import requests, pandas as pd
from pathlib import Path


# ==== PARAMETER LOKASI & TANGGAL ====
LAT, LON = -7.4, 112.69 # Jakarta contoh
START, END = "20250101", "20250731" # YYYYMMDD


# Variabel yang diambil (harian):
# ALLSKY_SFC_SW_DWN = Global horizontal irradiance (kWh/m^2/day)
# T2M = Temperature at 2m (°C), RH2M = Relative Humidity (%), WS2M = Wind Speed at 2m (m/s)
PARAMS = ["ALLSKY_SFC_SW_DWN", "T2M", "RH2M", "WS2M"]


url = "https://power.larc.nasa.gov/api/temporal/daily/point"
q = {
"latitude": LAT,
"longitude": LON,
"start": START,
"end": END,
"parameters": ",".join(PARAMS),
"community": "RE",
"format": "JSON",
}


print("Requesting NASA POWER…")
r = requests.get(url, params=q, timeout=60)
r.raise_for_status()
js = r.json()


# Parse ke DataFrame
data = js["properties"]["parameter"]
df = pd.DataFrame(data)
df.index = pd.to_datetime(df.index) # index tanggal


out = Path(__file__).resolve().parents[1] / "data" / "nasa_power_daily1.csv"
out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out)
print("Saved:", out)
print("Columns:", list(df.columns))