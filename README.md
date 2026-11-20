# Premier League Standings ETL

This repository is a personal project, however, it is designed to be a reusable ETL pipeline for collecting Premier League standings data from an external API and loading it into PostgreSQL.

The project is designed around a repeatable data workflow

## Overview

The pipeline follows a standard ETL flow:

- Extract: fetch current standings from the API
- Transform: normalize the response into a structured pandas DataFrame
- Load: upsert records into PostgreSQL

The main orchestration happens in `main.py`, with each stage implemented in the `src/` package.

### Notes:
- The script expects PostgreSQL access to a database that already has the `staging.standings` table.
- The load step uses an upsert pattern keyed on `(season, team_id)`.
- Copy `.env.example` to `.env` and fill in your API key and PostgreSQL credentials before running.

## What Each Step Does

- `src/extract.py`: Makes two API calls for the Premier League (`leagueid=47`). One gets the standings, the other gets league details.
- `src/transform.py`: Gets the latest season, renames the API fields, and builds a DataFrame with these columns: `season`, `position`, `team_id`, `team`, `played`, `won`, `draw`, `lost`, `score_streak`, `goal_diff`, `points`.
- `src/load.py`: Checks that `staging.standings` exists (it raises an error if not and does not create it), then upserts the rows. If a `(season, team_id)` row already exists it is updated, otherwise it is inserted. If anything fails, the changes are rolled back.

## Current Project Structure

```text
.
├── main.py
├── requirements.txt
├── .env
├── .env.example
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

## Environment Variables

Place inside a `.env` file in the project root:

- API: `API_KEY`, `API_HOST`, `API_URL` (standings), `API_URL2` (league details)
- PostgreSQL: `host`, `port`, `username`, `pass`, `dbname`

## Notebooks

- `notebooks/standings-etl.ipynb`: exploratory work for building the ETL.

## Running the ETL

From the project root:

```bash
python main.py
```

This runs the transformation step and loads the data into the configured PostgreSQL database.

## Current Status

The ETL pipeline is active, with the current focus on stable extraction, transformation, and PostgreSQL loading for analytics use. Additionally, my next steps will include logging and automated batch loading, among other features. 

