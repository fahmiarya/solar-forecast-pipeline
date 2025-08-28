import joblib
import pandas as pd
from pathlib import Path

# Lokasi file model
model_path = Path(__file__).resolve().parents[1] / "data" / "pv_model_rf.joblib"

# Load model
model = joblib.load(model_path)
print("Model loaded from:", model_path)

# Contoh input data cuaca (bisa diganti sesuai kebutuhan)
# Format sesuai training: ["ghi_kwh_m2", "T2M", "RH2M", "WS2M"]
sample_data = {
    "ghi_kwh_m2": [5.2],   # radiasi matahari (kWh/m2)
    "T2M": [30.5],         # suhu udara (°C)
    "RH2M": [65.0],        # kelembapan relatif (%)
    "WS2M": [2.5]          # kecepatan angin (m/s)
}

# Konversi ke DataFrame
X_new = pd.DataFrame(sample_data)

# Prediksi output listrik PV (kWh)
pred = model.predict(X_new)
print("Predicted PV output (kWh):", pred[0])
