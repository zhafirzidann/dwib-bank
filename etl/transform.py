from __future__ import annotations

import os
import subprocess
from pathlib import Path

from etl.extract import duckdb_path


def run_dbt_build() -> None:
    airflow_home = Path(os.environ.get("AIRFLOW_HOME", "/opt/airflow"))
    project_dir = airflow_home / "dbt_bank"
    env = os.environ.copy()
    env["DUCKDB_PATH"] = str(duckdb_path())

    subprocess.run(
        ["dbt", "build", "--project-dir", str(project_dir), "--profiles-dir", str(project_dir)],
        check=True,
        env=env,
    )
