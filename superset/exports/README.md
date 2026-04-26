# Superset Dashboard Export

Folder ini menyimpan export dashboard Superset yang digunakan pada implementasi DWIB Banking Warehouse.

File dashboard:

```text
dashboard_export_20260426T142813.zip
```

Gunakan file ini setelah Docker berjalan dan pipeline Airflow `etl_bank_transactions` selesai sukses. Setelah data mart tersedia di DuckDB, buka Superset di:

```text
http://localhost:8088
```

Lalu import file zip melalui menu import dashboard Superset. Dashboard ini membaca dataset dari koneksi DuckDB `dwib_bank_duckdb` dan menggunakan tabel mart hasil pipeline dbt.
