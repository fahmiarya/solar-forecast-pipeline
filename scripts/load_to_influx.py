import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Config
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "super-token-123"
ORG = "myorg"
BUCKET = "energy"

csv_path = "data/nasa_power_daily1.csv"

# Baca CSV
df = pd.read_csv(
    csv_path,
    names=["DATE", "ALLSKY_SFC_SW_DWN", "T2M", "RH2M", "WS2M"],
    header=0,
    parse_dates=["DATE"]
)

# Connect
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

points = []
for _, row in df.iterrows():
    point = (
        Point("weather")  # measurement name
        .tag("location", "jakarta")
        .field("ghi_kwh_m2", float(row["ALLSKY_SFC_SW_DWN"]))
        .field("temp_c", float(row["T2M"]))
        .field("rh_pct", float(row["RH2M"]))
        .field("wind_ms", float(row["WS2M"]))
        .time(row["DATE"], WritePrecision.NS)  # gunakan tanggal CSV
    )
    points.append(point)

print(f"📤 Writing {len(points)} points...")
write_api.write(bucket=BUCKET, record=points)
print("✅ Done!")

client.close()
