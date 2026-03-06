# 🥇 XAU/USD Gold Price — ELT Pipeline + ML Prediction

> Portfolio Project — Data Engineer / Data Analyst | by Ali Eddine Moncef

## 📌 Overview

End-to-end ELT pipeline built on XAU/USD (Gold) price data:
API extraction, Snowflake cloud storage, feature engineering,
Prophet ML forecasting model, and interactive Plotly Dash dashboard.

## 🏗️ Architecture
```
[Yahoo Finance API]
       ↓ EXTRACT
[CSV Local — data/raw/]
       ↓ LOAD
[Snowflake — RAW.GOLD_PRICES]
       ↓ TRANSFORM
[Snowflake — ANALYTICS]
       ↓
[Prophet ML Model]  +  [Plotly Dash Dashboard]
```

## 🛠️ Tech Stack

| Tool | Role |
|---|---|
| Python | Core language |
| yfinance | Yahoo Finance API extraction |
| Pandas | Data manipulation & transformation |
| Snowflake (Azure) | Cloud Data Warehouse |
| Prophet | ML price forecasting model |
| Plotly Dash | Interactive web dashboard |

## 📁 Project Structure
```
xauusd_project/
├── etl/
│   ├── extract.py       # Yahoo Finance API extraction
│   ├── load.py          # Load data to Snowflake
│   └── transform.py     # Feature engineering
├── analysis/
│   └── eda.py           # Exploratory Data Analysis + charts
├── ml/
│   └── train_prophet.py # Prophet model + 30-day predictions
├── dashboard/
│   └── app.py           # Interactive Plotly Dash dashboard
├── data/
│   ├── raw/             # Raw data (not versioned)
│   └── processed/       # Transformed data
├── requirements.txt
└── README.md
```

## 🚀 Getting Started
```bash
# 1. Clone the repository
git clone https://github.com/Moncef-Ali-Eddine/xauusd-elt-pipeline
cd xauusd-elt-pipeline

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
# Create a .env file with your Snowflake credentials
```

## ▶️ Usage
```bash
# Step 1 — Extract data from Yahoo Finance
python etl/extract.py

# Step 2 — Transform & feature engineering
python etl/transform.py

# Step 3 — Exploratory Data Analysis
python analysis/eda.py

# Step 4 — Train ML forecasting model
python ml/train_prophet.py

# Step 5 — Launch interactive dashboard
python dashboard/app.py
# Open: http://127.0.0.1:8050
```

## 📊 Key Results

- ✅ 1,047 days of historical XAU/USD data (2022 → 2026)
- ✅ 8 technical indicators engineered (MA7, MA30, MA90, RSI, etc.)
- ✅ Prophet ML model with 30-day price forecast
- ✅ Interactive dashboard with dynamic period selector
- ✅ Snowflake Data Warehouse on Azure (West Europe)

## 📈 Dashboard Preview

| Metric | Value |
|---|---|
| Current Price | ~$5,120 |
| Historical Min | $1,623 |
| Historical Max | $5,318 |
| 30-day Forecast | ~$5,315 |

## 👤 Author

**Ali Eddine Moncef**
[GitHub](https://github.com/Moncef-Ali-Eddine)