# solar-forecast-pipeline

\# NASA PV Realtime ML



🚀 Project sederhana untuk memprediksi energi listrik dari panel surya (PV) menggunakan data cuaca NASA POWER.  

Project ini juga dilengkapi pipeline data yang meniru alur \*\*real-time streaming\*\*: data cuaca di-\*replay\* ke InfluxDB, lalu divisualisasi di Grafana.



\## ✨ Fitur

* Ambil data harian NASA POWER (radiation, temperature, humidity, wind).
* Replay data ke InfluxDB agar terlihat seperti data real-time.
* Visualisasi data di Grafana.
* Training model Machine Learning (Random Forest) untuk prediksi energi PV.
* Model tersimpan dalam format `.joblib` dan bisa digunakan untuk prediksi baru.


  🛠️ Stack



* Python (pandas, scikit-learn, joblib)
* InfluxDB 2.x
* Grafana
* Docker Compose
* NASA POWER dataset
