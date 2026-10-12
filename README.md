# PL Standings ETL

This repository is a personal-use project. It is a reusable ETL pipeline for collecting Premier League standings data from an external API and loading it into PostgreSQL for analysis.

The project is designed around a repeatable data workflow rather than ad hoc personal tracking. It expects production-style inputs and environment configuration, and it is intended to support downstream analytics.

## Overview

The pipeline follows a standard ETL flow:

- Extract: fetch current standings from the API
- Transform: normalize the response into a structured pandas DataFrame
- Load: upsert records into PostgreSQL

The main orchestration happens in `main.py`, with each stage implemented in the `src/` package.

## Current Project Structure

```text
.
├── main.py
├── requirements.txt
├── .env
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── notebooks/
│   └── standings-etl.ipynb
├── screenshots/
│   └── previous-standings.png
└── README.md
```

## Dependencies

The project currently uses:

- pandas
- requests
- python-dotenv
- psycopg

Install dependencies with:

```bash
pip install -r requirements.txt
```

Notes:
- The app expects PostgreSQL access to a database that already has the `staging.standings` table.
- The load step uses an upsert pattern keyed on `(season, team_id)`.
- API values are loaded from the environment rather than hardcoded into the code.

## Running the ETL

From the project root:

```bash
python main.py
```

This runs the transformation step and loads the data into the configured PostgreSQL database.

## Current Status

The ETL pipeline is active, with the current focus on stable extraction, transformation, and PostgreSQL loading for analytics use.
