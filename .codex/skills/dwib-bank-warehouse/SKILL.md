---
name: dwib-bank-warehouse
description: Use when working on the dwib-bank repository for the Data Warehouse and Business Intelligence assignment. Covers the repo layout, the Airflow to DuckDB to dbt pipeline, common run commands, and the expected deliverables for this banking domain project.
---

# DWIB Bank Warehouse

Use this skill when the task is specifically about the `dwib-bank` repository or the banking data warehouse assignment.

## Repo Focus

This project implements a banking warehouse pipeline with:
- Airflow DAG orchestration in `dags/etl_bank_transactions.py`
- Python ETL helpers in `etl/`
- DuckDB as the analytical store in `include/bank_data.duckdb`
- dbt project in `dbt_bank/`
- raw input data in `data/raw/`

## Expected Pipeline

The main DAG should run this sequence:
1. Generate source tables from the bundled transaction dataset.
2. Load raw tables into DuckDB schema `raw`.
3. Run `dbt build` to create `staging`, `intermediate`, and `marts`.
4. Validate row counts and referential integrity.

When changing the pipeline, preserve that end-to-end flow unless the user explicitly wants a redesign.

## Common Commands

Start the stack:

```bash
docker compose up --build -d
```

Trigger the DAG:

```bash
docker compose exec airflow-scheduler airflow dags trigger etl_bank_transactions
```

Check DAG runs:

```bash
docker compose exec airflow-scheduler airflow dags list-runs -d etl_bank_transactions
```

Run dbt manually:

```bash
docker compose exec airflow-scheduler dbt build --project-dir /opt/airflow/dbt_bank --profiles-dir /opt/airflow/dbt_bank
```

Open DuckDB:

```bash
docker compose exec airflow-scheduler duckdb /opt/airflow/include/bank_data.duckdb
```

Run Python syntax validation quickly:

```bash
python3 -m py_compile dags/etl_bank_transactions.py etl/__init__.py etl/extract.py etl/transform.py etl/load.py
```

## Assignment Constraints

Keep these requirements in mind when implementing or reviewing:
- at least 3 source tables
- at least 10,000 transaction rows
- dimensional modeling with `dim_*` and `fct_*`
- dbt documentation and tests in `schema.yml`
- validation queries and data quality checks

## Working Notes

- Prefer storing temporary notes or scratch plans in `planning/`. That folder is intentionally gitignored.
- Keep user-facing run instructions in `README.md`.
- If the task is about dimensional design or business questions, map changes back to the banking domain and the assignment PDF, not generic Airflow examples.
