
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import duckdb
import os

def extract_and_load_to_duckdb():
    csv_file_path = os.path.join(os.environ.get("AIRFLOW_HOME", "/opt/airflow"), "dags", "..", "Bank_Transaction_Fraud_Detection.csv")
    duckdb_path = os.path.join(os.environ.get("AIRFLOW_HOME", "/opt/airflow"), "include", "bank_data.db")

    # Connect to DuckDB
    con = duckdb.connect(database=duckdb_path, read_only=False)

    # Read CSV into pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Create a raw table in DuckDB and insert data
    con.execute("DROP TABLE IF EXISTS raw_transactions")
    con.execute("CREATE TABLE raw_transactions AS SELECT * FROM df")

    con.close()

def transform_data_and_create_datamart():
    duckdb_path = os.path.join(os.environ.get("AIRFLOW_HOME", "/opt/airflow"), "include", "bank_data.db")
    con = duckdb.connect(database=duckdb_path, read_only=False)

    # Create Dimension Table: dim_customers
    con.execute("""
        CREATE TABLE IF NOT EXISTS dim_customers AS
        SELECT DISTINCT
            Customer_ID,
            Customer_Name,
            Gender,
            Age,
            State,
            City,
            Customer_Contact,
            Customer_Email
        FROM raw_transactions
    """)

    # Create Fact Table: fact_transactions
    con.execute("""
        CREATE TABLE IF NOT EXISTS fact_transactions AS
        SELECT
            Transaction_ID,
            Customer_ID,
            Bank_Branch,
            Account_Type,
            Transaction_Date,
            Transaction_Time,
            Transaction_Amount,
            Merchant_ID,
            Transaction_Type,
            Merchant_Category,
            Account_Balance,
            Transaction_Device,
            Transaction_Location,
            Device_Type,
            Is_Fraud,
            Transaction_Currency,
            Transaction_Description
        FROM raw_transactions
    """)

    con.close()

with DAG(
    dag_id=\'etl_bank_transactions\',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=[\'etl\', \'duckdb\', \'bank_fraud\'],
) as dag:
    extract_load_task = PythonOperator(
        task_id=\'extract_and_load_raw_data\',
        python_callable=extract_and_load_to_duckdb,
    )

    transform_task = PythonOperator(
        task_id=\'transform_data_and_create_datamart\',
        python_callable=transform_data_and_create_datamart,
    )

    extract_load_task >> transform_task
