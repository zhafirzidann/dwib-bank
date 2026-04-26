from __future__ import annotations

import duckdb

from etl.extract import duckdb_path


def validate_datamart() -> None:
    con = duckdb.connect(str(duckdb_path()), read_only=True)
    try:
        mart_schema = "marts"
        checks = {
            "dim_customers_count": f"SELECT COUNT(*) FROM {mart_schema}.dim_customers",
            "dim_accounts_count": f"SELECT COUNT(*) FROM {mart_schema}.dim_accounts",
            "dim_date_count": f"SELECT COUNT(*) FROM {mart_schema}.dim_date",
            "fct_transactions_count": f"SELECT COUNT(*) FROM {mart_schema}.fct_transactions",
            "orphan_customer_keys": f"""
                SELECT COUNT(*)
                FROM {mart_schema}.fct_transactions f
                LEFT JOIN {mart_schema}.dim_customers d
                    ON f.customer_key = d.customer_key
                WHERE d.customer_key IS NULL
            """,
            "orphan_account_keys": f"""
                SELECT COUNT(*)
                FROM {mart_schema}.fct_transactions f
                LEFT JOIN {mart_schema}.dim_accounts d
                    ON f.account_key = d.account_key
                WHERE d.account_key IS NULL
            """,
            "orphan_date_keys": f"""
                SELECT COUNT(*)
                FROM {mart_schema}.fct_transactions f
                LEFT JOIN {mart_schema}.dim_date d
                    ON f.transaction_date_key = d.date_key
                WHERE d.date_key IS NULL
            """,
        }

        results = {name: con.execute(sql).fetchone()[0] for name, sql in checks.items()}
        if results["fct_transactions_count"] <= 0:
            raise ValueError("Fact table is empty")
        for key in ("orphan_customer_keys", "orphan_account_keys", "orphan_date_keys"):
            if results[key] != 0:
                raise ValueError(f"Data mart validation failed: {key}={results[key]}")
    finally:
        con.close()
