import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
from pathlib import Path


# Load gabungan dari InfluxDB -> CSV hasil export, atau langsung pakai CSV NASA lalu hitung target
csv_path = Path(__file__).resolve().parents[1] / "data" / "nasa_power_daily1.csv"
df = pd.read_csv(
    csv_path,
    names=["DATE", "ALLSKY_SFC_SW_DWN", "T2M", "RH2M", "WS2M"],
    header=0,   # karena baris pertama sudah ada judul kolom, header=0
    parse_dates=["DATE"],
    index_col="DATE"
)

# Fisika sederhana untuk simulasi target PV
AREA_M2 = 2.0
EFF = 0.18

# Fixed: Use the correct column name 'ALLSKY_SF' instead of 'ALLSKY_SFC_SW_DWN'
df["ghi_kwh_m2"] = df["ALLSKY_SFC_SW_DWN"].astype(float)
df["pv_kwh"] = df["ghi_kwh_m2"] * AREA_M2 * EFF

# Fitur (bisa ditambah: moving average, lag, dsb.)
X = df[["ghi_kwh_m2", "T2M", "RH2M", "WS2M"]].astype(float)
y = df["pv_kwh"].astype(float)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
model = RandomForestRegressor(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

pred = model.predict(X_test)
print("R2:", r2_score(y_test, pred))
print("MAE:", mean_absolute_error(y_test, pred))

out = Path(__file__).resolve().parents[1] / "data" / "pv_model_rf.joblib"
joblib.dump(model, out)
print("Saved model:", out)