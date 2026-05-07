# 🌫️ Korea Air Quality Alert Pipeline

An end-to-end automated data engineering pipeline that monitors real-time air quality across all 17 regions of South Korea and sends alerts when pollution levels reach dangerous thresholds.

---

## 🏗️ Architecture

```
Korea Public Data Portal API (data.go.kr)
              ↓
     Python Ingestion Script
              ↓
    Bronze Layer (Raw Data)
              ↓
    Silver Layer (Cleaned Data)       ← Supabase SQL Function
              ↓
    Gold Layer (Business Logic)       ← Supabase SQL Function
              ↓
    ┌─────────────────────┐
    │    Alert Check      │
    │  khai_grade >= 3?   │
    └──────┬──────────────┘
           ↓              ↓
    Twitter/X Bot      Stay Silent
    Posts Alert
           ↓
    Tableau Dashboard (always updates)

    ⟳ Repeats every hour via Apache Airflow
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Data Source | Korea Public Data Portal AirKorea API |
| Ingestion | Python (requests, pandas) |
| Storage | Supabase (PostgreSQL) |
| Transformation | SQL (Supabase stored functions) |
| Orchestration | Apache Airflow 3 (Docker) |
| Alerting | Twitter/X Bot (tweepy) |
| Visualization | Tableau Public |

---

## 📊 Data Pipeline Layers

### Bronze Layer
Stores raw API response exactly as received — no transformation, no cleaning. Every field stored as VARCHAR to preserve original data integrity.

### Silver Layer
Cleans and transforms bronze data:
- Converts VARCHAR fields to proper types (FLOAT, INTEGER, TIMESTAMP)
- Handles null values and invalid readings (`'-'` → NULL)
- Drops sensor flag columns not needed for analysis

### Gold Layer
Business-ready data with one row per region:
- Finds the worst station per city using `DISTINCT ON`
- Calculates grade labels (Good / Moderate / Bad / Very Bad)
- Sets `should_tweet = true` when `khai_grade >= 3`

---

## 🌡️ Air Quality Metrics

| Metric | Description | Dangerous Level |
|---|---|---|
| `khai_value` | Overall Air Quality Index (CAI) | > 100 |
| `khai_grade` | Grade 1-4 (1=Good, 4=Very Bad) | >= 3 |
| `pm25_value` | Ultra-fine dust PM2.5 (μg/m³) | > 35 |
| `pm10_value` | Fine dust PM10 (μg/m³) | > 80 |
| `o3_value` | Ozone (ppm) | > 0.09 |
| `no2_value` | Nitrogen dioxide (ppm) | > 0.1 |

---

## 📁 Project Structure

```
air_quality_pipeline/
├── dags/
│   └── weather_alert_dag.py    # Airflow DAG — hourly pipeline
├── api/
│   ├── __init__.py
│   └── weather.py              # AirKorea API ingestion
├── database/
│   ├── __init__.py
│   ├── database.py             # Supabase connection & queries
│   └── init_db.sql             # Bronze/Silver/Gold table schemas
├── twitter/
│   ├── __init__.py
│   └── bot.py                  # Twitter alert bot
├── docker-compose.yaml         # Airflow Docker setup
├── .env                        # Environment variables (not committed)
├── .gitignore
└── README.md
```

---

## ⚙️ Airflow DAG

The pipeline runs every hour with 4 sequential tasks:

```
fetch_insert_data → load_silver → load_gold → send_alerts
```

| Task | Operator | Description |
|---|---|---|
| `fetch_insert_data` | PythonOperator | Calls AirKorea API for all 17 regions, bulk inserts ~638 stations to bronze |
| `load_silver` | SQLExecuteQueryOperator | Runs `load_silver()` Supabase function |
| `load_gold` | SQLExecuteQueryOperator | Runs `load_gold()` Supabase function |
| `send_alerts` | PythonOperator | Queries gold table, tweets where `should_tweet = true` |

---

## 🚀 Getting Started

### Prerequisites
- Docker Desktop
- Python 3.10+
- Supabase account (free)
- Korea Public Data Portal account (free)
- Twitter Developer account

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/air-quality-pipeline.git
cd air-quality-pipeline
```

### 2. Set up environment variables
```bash
cp .env.example .env
```

Fill in your `.env`:
```
WEATHER_API=your_airkorea_api_key
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_SERVICE_KEY=your_service_role_key
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_SECRET=your_token_secret
AIRFLOW_UID=501
_PIP_ADDITIONAL_REQUIREMENTS=apache-airflow-providers-postgres supabase tweepy requests python-dotenv
```

### 3. Set up Supabase tables
Run the SQL in `database/init_db.sql` in your Supabase SQL editor to create bronze, silver, and gold tables along with the transformation functions.

### 4. Start Airflow
```bash
docker compose up airflow-init
docker compose up
```

### 5. Configure Airflow connection
Go to `http://localhost:8080` → Admin → Connections → Add:
```
Conn Id:   supabase_postgres
Conn Type: Postgres
Host:      aws-1-ap-south-1.pooler.supabase.com
Database:  postgres
Login:     postgres.xxxx
Password:  your_db_password
Port:      5432
```

### 6. Enable the DAG
Go to `http://localhost:8080` → toggle `weather_alert_dag` on → it runs automatically every hour!

---

## 📈 Tableau Dashboard

Live dashboard showing air quality trends across all 17 Korean regions:
- Line graphs of PM2.5 and PM10 over time
- Regional comparison charts
- Historical trend analysis

🔗 [View Dashboard](#) ← Add your Tableau Public link here

---

## 📬 Twitter Bot

The bot tweets whenever any Korean region hits khai_grade 3 (Bad) or 4 (Very Bad):

```
🔴 Air Quality Alert — 부산!

Worst area: 해운대구
AQI Score: 112
Grade: Bad 😷
Time: 14:00

PM2.5: 45 μg/m³
PM10: 78 μg/m³

Stay indoors and wear a mask!
#Korea #AirQuality #미세먼지
```

---

## 📄 License

MIT License — feel free to use and modify.
