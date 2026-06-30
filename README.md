# Telecom Churn — Synthetic Data Generation

*Synthetic, intentionally-messy multi-source telecom data for a churn-analytics / data-engineering pipeline exercise.*

![Python](https://img.shields.io/badge/python-3.12-blue)
![pandas](https://img.shields.io/badge/pandas-2.3.1-150458)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

This project generates a set of synthetic, multi-source telecom datasets — call records, customer profiles, recharge transactions, network outages, and churn labels — built while training for a Data Engineering job switch. It deliberately simulates the kind of messy, multi-source raw data a real telecom company would produce, as the data-source layer for a downstream customer-churn analytics pipeline.

The repo currently contains **Phase 1: data generation only**. There is no cleaning pipeline, no ETL, and no churn model here yet — those are planned next phases (see [Roadmap](#roadmap)).

## Why this project

Customer churn is one of the most common and high-value analytics problems in telecom: predicting which customers are about to leave drives retention spend, pricing, and network investment decisions. In the real world, the data that feeds churn analysis is rarely clean — it arrives from disconnected systems (billing, network ops, CRM, call switches) full of missing values, duplicates, typos, and inconsistent identifiers.

Rather than starting from a tidy CSV, this project fabricates that mess on purpose. The goal is to have realistic, dirty, multi-source raw data to practice the data engineering skills that actually matter: profiling, validation, cleaning, and integration — before any modeling happens.

## Datasets

| Dataset (file) | Format | Rows | Description | Key injected data-quality issues |
|---|---|---|---|---|
| `call_logs_2024.csv` | CSV | 252,501 | Call Detail Records (CDR): caller/receiver numbers, duration, call type, tower, location, signal strength, dropped-call flag | ~20% tower/location mismatch, ~2% missing values across columns, ~1% duplicate rows, shuffled |
| `churn_flag.csv` / `churn_flag.parquet` | CSV + Parquet | 51,001 | Customer churn labels and features (demographics, plan, usage, complaints) — holds the **churn_flag** target column | Misspelled city anomalies ("Ney York", "Loz Angeles", "Chigaco", "Huston", "Pheonix"), missing age/gender/plan, 2% duplicates. **Seeded/reproducible** |
| `customer_details.json` | JSON (array, indent=4) | 50,500 | Customer master data: demographics, income, region, signup/login dates, preferred device, loyalty points | Gender anomalies ("M", "F", "Unknown", "X", "Malee", "Fem"), age outliers (5, 120 injected ~3%), region anomalies beyond the 5 real regions, ~2% missing, ~1% duplicates, shuffled |
| `network_outages.csv` | CSV | 20,201 | Tower outage events: tower, region, location, start/end time, duration, outage type, affected users, reporter | Outage-type typos ("Unkown", "S0ftware"), **negative durations** (end up to 30 min before start), ~15% location mismatch tags, 2% missing, 1% duplicates, shuffled |
| `recharge_history.csv` | CSV | 113,301 | Recharge/payment transactions: amount, plan, payment method, location, device type, status | ~5% location vs reported_location mismatch, ~2% missing in amount/location/payment_method, 3% duplicates. **Seeded/reproducible** |

## Data quality issues (by design)

All anomalies below are **intentional** — injected by the generator scripts to give a downstream cleaning/ETL exercise realistic problems to solve, not bugs in the generators themselves.

- **Missing values** — null/None values scattered across most columns in every dataset (~1–2% rates)
- **Duplicates** — 1–3% duplicate rows appended and shuffled into each output
- **Typos / spelling anomalies** — misspelled cities (`churn_flag`), malformed genders (`customer_details`), garbled outage types like `"Unkown"` / `"S0ftware"` (`network_outages`)
- **Out-of-range values / outliers** — age outliers of 5 and 120 years in `customer_details`
- **Location / identifier mismatches** — tower-to-location mismatches in `call_logs`, mismatch tags in `network_outages`, location vs. reported_location drift in `recharge_history`
- **Negative durations** — outage end timestamps that precede the start timestamp in `network_outages`

## Data model & relationships

These datasets are **independent simulated source systems**, not a pre-joined star schema. Each script generates its own `uuid4` identifiers independently (`user_id` in `churn_flag` / `recharge_history`, `customer_id` in `customer_details`), so these IDs **do not match across files** — there is no referential integrity to rely on between them as-is.

The one natural shared dimension is **`tower_id`**, used conceptually by both `call_logs_2024.csv` (`TWR001`–`TWR050`) and `network_outages.csv` (`TWR001`–`TWR100`), though the ranges only partially overlap.

This mirrors a realistic multi-source ingestion scenario: separate operational systems (billing, network ops, CRM) that a data engineer must profile, key, and integrate — rather than a dataset that arrives already joined.

## Tech stack

| Library | Role |
|---|---|
| Python 3.12 | Runtime |
| pandas | DataFrame construction, transformations, CSV/Parquet I/O |
| numpy | Random/numeric distributions (durations, amounts, affected users) |
| Faker | Realistic fake names, addresses, cities, dates, phone numbers |
| pyarrow | Parquet engine used for `churn_flag.parquet` |

## Project structure

```
telecom_churn/
├── README.md
├── requirements.txt
├── .gitignore
├── scripts/
│   ├── call_logs.py            # -> call_logs_2024.csv
│   ├── churn.py                # -> churn_flag.csv, churn_flag.parquet
│   ├── customer_details.py     # -> customer_details.json
│   ├── network_out.py          # -> network_outages.csv
│   └── history.py              # -> recharge_history.csv
└── (generated data outputs — gitignored, reproducible by running the scripts)
```

## Getting started

**Windows (PowerShell)**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux (bash)**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run any generator from the repo root — each script writes its output file(s) to the current working directory:

```bash
python scripts/call_logs.py
python scripts/churn.py
python scripts/customer_details.py
python scripts/network_out.py
python scripts/history.py
```

`churn.py` and `history.py` set explicit random seeds and are reproducible across runs. `call_logs.py`, `customer_details.py`, and `network_out.py` are not seeded, so their output will differ on each run.

## Skills demonstrated

- Synthetic data generation at scale (20K–250K rows per dataset)
- Deliberately simulating real-world data quality problems (missing data, duplicates, typos, outliers, mismatches)
- Working across multiple file formats: CSV, JSON, Parquet
- Data manipulation with pandas and numpy (distributions, sampling, shuffling)
- Realistic fake data generation with Faker
- Reproducible pipelines via explicit random seeding

## Roadmap

The following phases are **not yet implemented** and represent planned next steps:

- [ ] Data-cleaning and validation layer for the raw outputs
- [ ] ETL pipeline loading cleaned data into a warehouse / star schema
- [ ] Automated data quality checks (e.g. Great Expectations, pandera)
- [ ] Exploratory data analysis notebooks
- [ ] Churn prediction model (scikit-learn)
- [ ] Pipeline orchestration (Airflow / Prefect)
- [ ] Parameterizing the generators via CLI args/config (row counts, seeds, error rates)
- [ ] Unit tests for the generator logic
- [ ] Dockerization for reproducible environments

## Notes

- All data is **fully synthetic**, produced with Faker and Python's `random`/`numpy` — it contains **no real personal data**.
- Anomalies (missing values, duplicates, typos, outliers, mismatches, negative durations) are **intentional**, designed to support a downstream data-cleaning exercise.
