# Narasi Airflow sampai Integrasi Superset

## Narasi Utama

Pada project DWIB Banking Warehouse, Airflow digunakan sebagai pengatur utama jalannya pipeline data. Airflow tidak digunakan untuk membuat dashboard atau melakukan analisis bisnis secara langsung, tetapi berperan untuk memastikan setiap proses berjalan sesuai urutan, mulai dari data mentah sampai data siap divisualisasikan.

Pipeline ini dimulai dari dataset transaksi bank dalam bentuk CSV. Data tersebut masih berupa data mentah, sehingga perlu diproses terlebih dahulu. Airflow menjalankan proses awal untuk memecah dataset menjadi beberapa tabel sumber, seperti data customer, account, dan transaction. Setelah itu, data dimasukkan ke DuckDB sebagai database analytical lokal.

Setelah data mentah masuk ke DuckDB, Airflow menjalankan dbt untuk melakukan transformasi. Di tahap ini, data dibersihkan, distandardisasi, dan dibentuk menjadi model data warehouse. Model akhir yang dihasilkan berupa tabel dimensi dan tabel fakta, seperti `dim_customers`, `dim_accounts`, `dim_date`, dan `fct_transactions`.

Pendekatan yang digunakan dalam project ini adalah **Kimball bottom-up**, karena proses dimulai dari data mentah lalu dibangun bertahap menjadi data mart. Data mart ini dirancang agar mudah digunakan untuk analisis bisnis dan dashboard.

Setelah proses transformasi selesai, Airflow menjalankan validasi data. Validasi ini memastikan bahwa tabel fakta tidak kosong dan relasi antar tabel tetap benar. Jika validasi gagal, maka pipeline dianggap gagal. Dengan begitu, data yang masuk ke tahap visualisasi sudah lebih terpercaya.

Hasil akhir pipeline disimpan di DuckDB. Apache Superset kemudian membaca data dari DuckDB tersebut untuk membuat dashboard. Jadi, Superset tidak menjalankan proses ETL, tetapi hanya menggunakan data mart yang sudah disiapkan oleh pipeline Airflow dan dbt.

Dashboard Superset yang digunakan pada implementasi project ini juga disimpan dalam bentuk export zip di repository. File tersebut dapat di-import kembali ke Superset setelah Docker berjalan dan pipeline Airflow selesai menghasilkan data mart.

## Flow Singkat

```text
CSV mentah
  -> Airflow menjalankan pipeline
  -> Python ETL memecah data sumber
  -> DuckDB menyimpan data raw
  -> dbt membentuk staging, intermediate, dan mart
  -> Airflow melakukan validasi
  -> Superset membaca data mart
  -> Dashboard bisnis ditampilkan
```

## DAG yang Digunakan

DAG utama pada project ini bernama:

```text
etl_bank_transactions
```

DAG ini berjalan secara berurutan:

```text
generate_source_tables
  -> ingest_raw_to_duckdb
  -> build_dbt_models
  -> validate_datamart
```

Penjelasan sederhananya:

- `generate_source_tables`: memecah satu file CSV besar menjadi beberapa tabel sumber.
- `ingest_raw_to_duckdb`: memasukkan data sumber ke DuckDB.
- `build_dbt_models`: menjalankan dbt untuk membentuk data warehouse dan data mart.
- `validate_datamart`: mengecek apakah hasil akhir valid dan siap digunakan.

## Peran Masing-Masing Teknologi

| Teknologi | Peran Utama |
| --- | --- |
| Airflow | Mengatur urutan dan eksekusi pipeline |
| Python ETL | Memproses data mentah di tahap awal |
| DuckDB | Menyimpan data warehouse secara lokal |
| dbt | Membentuk model data: staging, intermediate, mart |
| Superset | Membuat visualisasi dan dashboard |

## Point Penting untuk Presentasi

- Airflow berperan sebagai **orkestrator pipeline**, bukan sebagai dashboard tool.
- Pipeline berjalan dari data mentah sampai data siap analisis.
- Data awal berasal dari file CSV transaksi bank.
- Dataset besar dipecah menjadi beberapa tabel sumber: customer, account, dan transaction.
- DuckDB digunakan sebagai database analytical untuk menyimpan hasil pipeline.
- dbt digunakan untuk membersihkan dan membentuk model data warehouse.
- Model akhir menggunakan konsep **fact table** dan **dimension table**.
- Pendekatan data warehouse yang digunakan adalah **Kimball bottom-up**.
- Airflow juga menjalankan validasi agar data mart tidak kosong dan relasinya benar.
- Superset membaca data mart dari DuckDB untuk membuat dashboard bisnis.

## Narasi Singkat untuk Diucapkan

Project ini menggunakan Airflow sebagai orkestrator pipeline data. Pipeline dimulai dari file CSV transaksi bank yang masih mentah, kemudian Airflow menjalankan proses Python ETL untuk memecah data menjadi beberapa tabel sumber. Setelah itu, data dimasukkan ke DuckDB sebagai database analytical.

Tahap berikutnya adalah transformasi menggunakan dbt. dbt membentuk data dari layer raw menjadi staging, intermediate, dan akhirnya data mart. Data mart ini berisi tabel fakta dan dimensi yang siap digunakan untuk analisis bisnis.

Setelah data mart selesai dibuat, Airflow menjalankan proses validasi untuk memastikan data sudah benar dan tidak ada relasi yang rusak. Jika validasi berhasil, data mart tersebut dapat dibaca oleh Apache Superset.

Superset kemudian digunakan sebagai layer visualisasi. Dashboard yang ditampilkan di Superset berasal dari data mart yang sudah diproses oleh Airflow, DuckDB, dan dbt. Jadi, alurnya jelas: Airflow mengatur pipeline, dbt membentuk data, DuckDB menyimpan data, dan Superset menampilkan hasilnya.

Dashboard implementasi yang digunakan pada project tersedia di `superset/exports/dashboard_export_20260426T142813.zip`. Setelah menjalankan Docker dan pipeline Airflow, file ini bisa di-import ke Superset untuk menampilkan dashboard yang sama dengan implementasi project.

## Kesimpulan

Secara keseluruhan, project ini membangun alur data end-to-end dari raw data sampai dashboard. Airflow menjadi pengatur proses, DuckDB menjadi tempat penyimpanan data, dbt menjadi alat transformasi, dan Superset menjadi alat visualisasi.

Pipeline ini termasuk pendekatan **Kimball bottom-up**, karena dimulai dari data mentah lalu dibangun menjadi data mart berbasis tabel fakta dan dimensi.
