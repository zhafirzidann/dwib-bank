## DWIB Banking Warehouse

Project ini membangun platform data warehouse modern untuk domain banking menggunakan **Airflow**, **DuckDB**, **dbt**, dan **Apache Superset**. Platform ini dirancang untuk mendeteksi fraud dan menganalisis performa transaksi perbankan secara end-to-end.

## Fitur Utama

- **Modern Data Stack**: Integrasi Airflow untuk orkestrasi, DuckDB sebagai core OLAP engine yang cepat, dbt untuk transformasi data, dan Superset untuk visualisasi.
- **SCD Type 2**: Implementasi *Slowly Changing Dimension* Type 2 pada tabel customer (`int_customer_scd.sql`) untuk melacak histori perubahan data pelanggan secara akurat.
- **Automated Testing & Validation**:
    - **dbt tests**: Pengecekan kualitas data otomatis (uniqueness, not null, relationships) saat proses build.
    - **Custom Python Validation**: Validasi integritas referensial dan pengecekan baris kosong pada data mart akhir.
- **Analytical Marts**: Menyediakan layer aggregasi siap pakai (`agg_*`) untuk menjawab berbagai pertanyaan bisnis kritis.

## Komponen Utama

### 1. Apache Airflow (Orkestrator)
Bertindak sebagai "otak" pengatur seluruh pipeline. Airflow menjadwalkan dan memantau tugas mulai dari pengambilan data mentah hingga validasi akhir.
- **Akses UI**: `http://localhost:8080`
- **Login**: `admin` / `REktMZUW5aa8gA5y`

### 2. Apache Superset (BI & Visualisasi)
Platform eksplorasi data yang digunakan untuk menyajikan metrik bisnis dan deteksi fraud dalam bentuk dashboard interaktif.
- **Akses UI**: `http://localhost:8088`
- **Login**: `admin` / `admin`

### 3. DuckDB & dbt
- **DuckDB**: Database OLAP yang sangat cepat untuk pemrosesan data lokal.
- **dbt**: Mengelola logika transformasi data di dalam DuckDB menggunakan SQL.

## Struktur Project

- `.astro/`: Konfigurasi Astronomer/Astro CLI untuk workflow Airflow yang terstandarisasi.
- `dags/etl_bank_transactions.py`: DAG utama orkestrasi seluruh pipeline ETL.
- `etl/`: Helper Python modular untuk ekstraksi dataset, pemuatan ke DuckDB, pemicu dbt, dan validasi data.
- `dbt_bank/`: Project dbt yang berisi logika transformasi data.
- `analytics/`: Pertanyaan bisnis dan query SQL analitik.
- `data/raw/`: Lokasi dataset input utama (Sumber: [Kaggle](https://www.kaggle.com/datasets/marusagar/bank-transaction-fraud-detection)).
- `include/bank_data.duckdb`: Database DuckDB lokal hasil pipeline.
- `superset/`: Konfigurasi visualisasi dashboard.

## Menjalankan Pipeline

### 1. Inisialisasi Environment
Pastikan Docker sudah berjalan, kemudian nyalakan semua service:
```bash
docker compose up --build -d
```

### 2. Eksekusi Pipeline
Trigger DAG secara manual melalui UI Airflow atau via CLI:
```bash
docker compose exec airflow-scheduler airflow dags trigger etl_bank_transactions
```

### 3. Verifikasi Hasil
Cek jumlah baris pada tabel utama di DuckDB:
```bash
docker compose exec airflow-scheduler python -c "import duckdb; con=duckdb.connect('/usr/local/airflow/include/bank_data.duckdb', read_only=True); tables=['marts_marts.fct_transactions','marts_marts.dim_customers','marts_marts.dim_accounts','marts_marts.dim_date']; [print(f'{t}={con.execute(f\"select count(*) from {t}\").fetchone()[0]}') for t in tables]; con.close()"
```

## Analisis & Visualisasi

Detail lengkap pertanyaan bisnis dapat dilihat di `analytics/dashboard_business_questions.md`.

Untuk melihat dashboard visual, buka **Apache Superset** di `http://localhost:8088` setelah menjalankan service.

## Pengembangan & Testing

- **dbt Manual**: 
  ```bash
  docker compose exec airflow-scheduler dbt build --project-dir /usr/local/airflow/dbt_bank --profiles-dir /usr/local/airflow/dbt_bank
  ```
- **Unit Testing**: 
  ```bash
  pytest tests/dags/test_dag_example.py
  ```
