from __future__ import annotations

import csv
import hashlib
import logging
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import duckdb

LOGGER = logging.getLogger(__name__)

DATE_FORMAT = "%d-%m-%Y"
TIME_FORMAT = "%H:%M:%S"


def airflow_home() -> Path:
    return Path(os.environ.get("AIRFLOW_HOME", "/opt/airflow"))


def source_dataset_path() -> Path:
    return airflow_home() / "data" / "raw" / "Bank_Transaction_Fraud_Detection.csv"


def raw_dir() -> Path:
    return airflow_home() / "data" / "raw"


def duckdb_path() -> Path:
    return airflow_home() / "include" / "bank_data.duckdb"


def _transaction_timestamp(row: dict[str, str]) -> datetime:
    return datetime.strptime(
        f"{row['Transaction_Date']} {row['Transaction_Time']}",
        f"{DATE_FORMAT} {TIME_FORMAT}",
    )


def _account_id(customer_id: str, branch_name: str, account_type: str) -> str:
    raw_value = f"{customer_id}|{branch_name}|{account_type}".encode("utf-8")
    return hashlib.md5(raw_value).hexdigest()


def generate_source_tables() -> None:
    source_path = source_dataset_path()
    target_dir = raw_dir()
    target_dir.mkdir(parents=True, exist_ok=True)

    customers_path = target_dir / "customers_raw.csv"
    accounts_path = target_dir / "accounts_raw.csv"
    transactions_path = target_dir / "transactions_raw.csv"

    customer_history: dict[str, list[dict[str, str]]] = defaultdict(list)
    accounts: dict[str, dict[str, str]] = {}
    transactions: list[dict[str, str]] = []

    with source_path.open(newline="", encoding="utf-8") as source_file:
        reader = csv.DictReader(source_file)
        ordered_rows = sorted(reader, key=_transaction_timestamp)

    for row in ordered_rows:
        transaction_ts = _transaction_timestamp(row)
        transaction_date = transaction_ts.strftime("%Y-%m-%d")
        account_id = _account_id(
            row["Customer_ID"], row["Bank_Branch"], row["Account_Type"]
        )

        customer_profile = {
            "customer_source_id": row["Customer_ID"],
            "customer_name": row["Customer_Name"],
            "gender": row["Gender"],
            "age": row["Age"],
            "state": row["State"],
            "city": row["City"],
            "customer_contact": row["Customer_Contact"],
            "customer_email": row["Customer_Email"],
            "valid_from": transaction_date,
        }
        history = customer_history[row["Customer_ID"]]
        comparable_profile = {
            key: value for key, value in customer_profile.items() if key != "valid_from"
        }
        if not history or {
            key: value for key, value in history[-1].items() if key != "valid_from"
        } != comparable_profile:
            history.append(customer_profile)

        existing_account = accounts.get(account_id)
        if existing_account is None:
            accounts[account_id] = {
                "account_id": account_id,
                "customer_source_id": row["Customer_ID"],
                "bank_branch": row["Bank_Branch"],
                "account_type": row["Account_Type"],
                "opened_date": transaction_date,
                "current_balance": row["Account_Balance"],
            }
        else:
            existing_account["current_balance"] = row["Account_Balance"]

        transactions.append(
            {
                "transaction_id": row["Transaction_ID"],
                "account_id": account_id,
                "customer_source_id": row["Customer_ID"],
                "transaction_date": row["Transaction_Date"],
                "transaction_time": row["Transaction_Time"],
                "transaction_amount": row["Transaction_Amount"],
                "merchant_id": row["Merchant_ID"],
                "transaction_type": row["Transaction_Type"],
                "merchant_category": row["Merchant_Category"],
                "account_balance": row["Account_Balance"],
                "transaction_device": row["Transaction_Device"],
                "transaction_location": row["Transaction_Location"],
                "device_type": row["Device_Type"],
                "is_fraud": row["Is_Fraud"],
                "transaction_currency": row["Transaction_Currency"],
                "transaction_description": row["Transaction_Description"],
            }
        )

    customer_rows = [
        row
        for customer_snapshots in customer_history.values()
        for row in customer_snapshots
    ]

    _write_csv(customers_path, customer_rows)
    _write_csv(accounts_path, list(accounts.values()))
    _write_csv(transactions_path, transactions)

    LOGGER.info(
        "Generated source tables: %s customers, %s accounts, %s transactions",
        len(customer_rows),
        len(accounts),
        len(transactions),
    )


def ingest_raw_to_duckdb() -> None:
    db_path = duckdb_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    customers_path = raw_dir() / "customers_raw.csv"
    accounts_path = raw_dir() / "accounts_raw.csv"
    transactions_path = raw_dir() / "transactions_raw.csv"

    con = duckdb.connect(str(db_path), read_only=False)
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")
        con.execute("DROP TABLE IF EXISTS raw.customers_raw")
        con.execute("DROP TABLE IF EXISTS raw.accounts_raw")
        con.execute("DROP TABLE IF EXISTS raw.transactions_raw")

        con.execute(
            "CREATE TABLE raw.customers_raw AS SELECT * FROM read_csv_auto(?, HEADER=TRUE)",
            [str(customers_path)],
        )
        con.execute(
            "CREATE TABLE raw.accounts_raw AS SELECT * FROM read_csv_auto(?, HEADER=TRUE)",
            [str(accounts_path)],
        )
        con.execute(
            "CREATE TABLE raw.transactions_raw AS SELECT * FROM read_csv_auto(?, HEADER=TRUE)",
            [str(transactions_path)],
        )
    finally:
        con.close()


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"No rows available for {path.name}")

    with path.open("w", newline="", encoding="utf-8") as target_file:
        writer = csv.DictWriter(target_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
