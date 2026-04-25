-- 1. Ringkasan volume dan nilai transaksi per jenis transaksi.
select
    transaction_type,
    count(*) as total_transactions,
    round(sum(transaction_amount), 2) as total_transaction_amount,
    round(avg(transaction_amount), 2) as avg_transaction_amount
from marts_marts.fct_transactions
group by transaction_type
order by total_transaction_amount desc;

-- 2. Top 10 cabang bank berdasarkan total nilai transaksi.
select
    a.bank_branch,
    count(*) as total_transactions,
    round(sum(f.transaction_amount), 2) as total_transaction_amount
from marts_marts.fct_transactions f
inner join marts_marts.dim_accounts a
    on f.account_key = a.account_key
group by a.bank_branch
order by total_transaction_amount desc
limit 10;

-- 3. Distribusi fraud per device type.
select
    f.device_type,
    count(*) as total_transactions,
    sum(case when f.is_fraud = 1 then 1 else 0 end) as fraudulent_transactions,
    round(
        100.0 * sum(case when f.is_fraud = 1 then 1 else 0 end) / count(*),
        2
    ) as fraud_rate_pct
from marts_marts.fct_transactions f
group by f.device_type
order by fraud_rate_pct desc, fraudulent_transactions desc;

-- 4. Top 10 kota dengan jumlah transaksi fraud tertinggi.
select
    c.city,
    c.state,
    count(*) as fraud_transactions,
    round(sum(f.transaction_amount), 2) as fraud_amount
from marts_marts.fct_transactions f
inner join marts_marts.dim_customers c
    on f.customer_key = c.customer_key
where f.is_fraud = 1
group by c.city, c.state
order by fraud_transactions desc, fraud_amount desc
limit 10;

-- 5. Tren harian transaksi dan fraud.
select
    d.full_date,
    count(*) as total_transactions,
    round(sum(f.transaction_amount), 2) as total_transaction_amount,
    sum(case when f.is_fraud = 1 then 1 else 0 end) as total_fraud_transactions
from marts_marts.fct_transactions f
inner join marts_marts.dim_date d
    on f.transaction_date_key = d.date_key
group by d.full_date
order by d.full_date;
