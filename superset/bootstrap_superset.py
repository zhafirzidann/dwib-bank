from __future__ import annotations

import sqlite3
from pathlib import Path


SUPERSET_DB = Path("/app/superset_home/superset.db")
DUCKDB_URI = "duckdb:////app/data/bank_data.duckdb"
DATABASE_NAME = "dwib_bank_duckdb"
MART_TABLES = (
    "fct_transactions",
    "dim_customers",
    "dim_accounts",
    "dim_date",
    "agg_account_type_summary",
    "agg_branch_performance",
    "agg_city_fraud_summary",
    "agg_daily_transactions",
    "agg_device_fraud_summary",
    "agg_merchant_category_summary",
    "agg_state_summary",
    "agg_transaction_type_summary",
)


def main() -> None:
    con = sqlite3.connect(SUPERSET_DB)
    try:
        cur = con.cursor()
        cur.execute(
            """
            UPDATE dbs
            SET sqlalchemy_uri = ?, expose_in_sqllab = 1
            WHERE database_name = ?
            """,
            (DUCKDB_URI, DATABASE_NAME),
        )
        cur.execute(
            """
            UPDATE tables
            SET schema = 'marts', catalog = NULL
            WHERE table_name IN ({})
              AND (schema IN ('marts_marts', 'bank_data.marts_marts') OR schema IS NULL)
            """.format(",".join("?" for _ in MART_TABLES)),
            MART_TABLES,
        )
        con.commit()
    finally:
        con.close()


if __name__ == "__main__":
    main()
