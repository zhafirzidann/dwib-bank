# DWIB Bank Data Warehouse

## Overview
**DWIB Bank Data Warehouse** adalah proyek *end-to-end* untuk membangun dan mengelola gudang data (**data warehouse**) pada domain perbankan. Proyek ini memanfaatkan **Apache Airflow** sebagai orkestrator alur ETL/ELT, **dbt (data build tool)** untuk transformasi data di dalam *warehouse*, serta **Apache Superset** untuk visualisasi dan pembuatan dasbor. Teknologi yang digunakan bersifat *open source* dan dapat dijalankan sepenuhnya di lingkungan lokal maupun *cloud*.

Tujuan proyek:
- Mengekstrak data transaksi, nasabah, dan produk dari sumber operasional (seperti file CSV, database relasional, atau API).
- Memuat data mentah ke dalam *data warehouse* (PostgreSQL atau *cloud-native* DWH).
- Melakukan transformasi bertahap (*staging → intermediate → mart*) menggunakan dbt untuk menghasilkan model analitik yang siap konsumsi.
- Menjadwalkan seluruh alur secara otomatis dengan Airflow DAG.
- Menyajikan hasil analisis dalam bentuk dasbor interaktif menggunakan Superset.

## Project Contents
Struktur proyek terdiri dari komponen-komponen berikut:

- **dags/**: Direktori utama untuk menyimpan definisi Airflow DAG.
  - `dag_elt_pipeline.py` – DAG utama yang mengatur eksekusi harian: ekstraksi dari sumber, *load* ke staging, menjalankan dbt, dan *refresh* dasbor.
  - `dag_example_astronauts.py` – Contoh DAG bawaan template Astronomer (dapat dihapus).
- **dbt/**: Proyek dbt untuk transformasi data.
  - `models/staging/` – Model awal yang membersihkan dan menstandarkan data mentah.
  - `models/intermediate/` – Model gabungan untuk logika bisnis (misal: saldo harian, agregasi transaksi).
  - `models/marts/` – Model akhir (tabel fakta/dimensi) siap untuk visualisasi.
  - `dbt_project.yml` – Konfigurasi proyek dbt.
  - `profiles.yml` – Profil koneksi ke data warehouse.
- **include/**: Berkas tambahan seperti skrip SQL manual, definisi data sumber, atau konfigurasi Superset.
- **docker-compose.yml**: Definisi layanan yang menjalankan:
  - **PostgreSQL** – Metadata DB Airflow dan sekaligus *data warehouse* sementara.
  - **Scheduler** – Penjadwal tugas Airflow.
  - **API Server** – Airflow UI (port 8080).
  - **dbt runner** – Container khusus untuk menjalankan perintah dbt.
  - **Superset** – Platform visualisasi (port 8088).
- **Dockerfile**: *Custom Airflow image* berdasarkan Astro Runtime, dilengkapi *provider* untuk PostgreSQL, dbt, dan Superset.
- **requirements.txt**: *Python dependencies* proyek (dbt-core, dbt-postgres, apache-airflow-providers-*).
- **packages.txt**: Paket level OS (misalnya `libpq-dev` untuk driver PostgreSQL).
- **airflow_settings.yaml**: Konfigurasi lokal untuk Airflow *Connections*, *Variables*, dan *Pools*, sehingga tidak perlu mengisi manual di UI.

## Deploy Your Project Locally
Untuk menjalankan seluruh *stack* di mesin lokal, pastikan **Docker** dan **Docker Compose** sudah terpasang.

1. **Clone repository**
   ```bash
   git clone https://github.com/zhafirzidann/dwib-bank.git
   cd dwib-bank
   ```

2. **Jalankan layanan**
   ```bash
   docker compose up -d
   ```
   Perintah ini akan menyalakan 6 container: Postgres (DWH & metadata), Scheduler, API Server, Triggerer (optional), dbt-runner (untuk menjalankan `dbt debug` saat startup), dan Superset.

3. **Akses antar-muka**
   - Airflow UI: [http://localhost:8080](http://localhost:8080) (login: `admin` / `admin`)
   - Superset: [http://localhost:8088](http://localhost:8088) (login: `admin` / `admin`)
   - Postgres DWH: `localhost:5432`, database `dwib_bank`, user `postgres` / `postgres`

4. **Inisialisasi dbt & Superset (hanya pertama kali)**
   - Masuk ke container dbt:
     ```bash
     docker exec -it dwib-bank-dbt-runner-1 bash
     dbt deps
     dbt run --full-refresh
     ```
   - Untuk Superset, lakukan *setup* awal:
     ```bash
     docker exec -it dwib-bank-superset-1 superset fab create-admin
     docker exec -it dwib-bank-superset-1 superset db upgrade
     docker exec -it dwib-bank-superset-1 superset init
     ```
   - Impor dasbor contoh dari folder `include/dashboards/` via UI Superset.

5. **Aktifkan DAG ELT**
   - Buka Airflow UI, *unpause* DAG `dag_elt_pipeline`. DAG akan berjalan sesuai jadwal, atau dapat di-*trigger* manual.

## Deploy Your Project to Production
Untuk *deployment* di lingkungan produksi, proyek ini dapat dipindahkan ke Astronomer Cloud, Google Cloud Composer, atau instance Airflow mandiri. Pastikan:
- Data warehouse yang digunakan (misal: BigQuery, Redshift, atau PostgreSQL server) telah dikonfigurasi ulang di `profiles.yml` dan `airflow_settings.yaml`.
- Variabel sensitif (kredensial) disimpan di Airflow *Secrets Backend*.
- Konfigurasi CI/CD untuk menjalankan `dbt test` sebelum *deploy*.

## Visualisasi
Dasbor analitik DWIB Bank mencakup:
- **Tren saldo & transaksi** harian per cabang.
- **Distribusi produk** (tabungan, deposito, kredit) berdasarkan segmen nasabah.
- **Monitoring kualitas data** (jumlah *null*, duplikasi, keterlambatan data).
Semua dasbor dibuat menggunakan Apache Superset dan dapat di-*embed* ke aplikasi internal
