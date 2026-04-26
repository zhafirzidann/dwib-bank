from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from etl.extract import generate_source_tables, ingest_raw_to_duckdb
from etl.load import validate_datamart
from etl.transform import run_dbt_build


with DAG(
    dag_id="etl_bank_transactions",
    start_date=datetime(2026, 4, 1),
    schedule=None,
    catchup=False,
    default_args={"owner": "dwib-bank", "retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["etl", "duckdb", "dbt", "banking"],
) as dag:
    generate_source_task = PythonOperator(
        task_id="generate_source_tables",
        python_callable=generate_source_tables,
    )

    ingest_raw_task = PythonOperator(
        task_id="ingest_raw_to_duckdb",
        python_callable=ingest_raw_to_duckdb,
    )

    transform_task = PythonOperator(
        task_id="build_dbt_models",
        python_callable=run_dbt_build,
    )

    validate_task = PythonOperator(
        task_id="validate_datamart",
        python_callable=validate_datamart,
    )

    generate_source_task >> ingest_raw_task >> transform_task >> validate_task
