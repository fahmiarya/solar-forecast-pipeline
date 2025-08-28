# scripts/replay_to_influx.py
import time, pandas as pd
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import timezone
from pathlib import Path

INFLUX_URL = "http://localhost:8086"
TOKEN = "super-token-123"
ORG = "myorg"
BUCKET = "energy"

csv_path = Path(__file__).resolve().parents[1] / "data" / "nasa_power_daily1.csv"
df = pd.read_csv(
    csv_path,
    names=["DATE", "ALLSKY_SFC_SW_DWN", "T2M", "RH2M", "WS2M"],
    header=0,
    parse_dates=["DATE"],
    index_col="DATE"
)

cli = InfluxDBClient(url=INFLUX_URL, token=TOKEN, org=ORG)
write = cli.write_api(write_options=SYNCHRONOUS)

try:
    while True:
        for ts, row in df.iterrows():
            p = Point("weather").tag("source", "nasa_power").time(ts.tz_localize(timezone.utc))
            for k in ["ALLSKY_SFC_SW_DWN", "T2M", "RH2M", "WS2M"]:
                if pd.notna(row[k]):
                    p = p.field(k, float(row[k]))
            write.write(BUCKET, ORG, p)
            print("📤 sent:", ts)
            time.sleep(2)  # replay speed
except KeyboardInterrupt:
    print("⏹ Replay stopped by user")
finally:
    cli.close()
