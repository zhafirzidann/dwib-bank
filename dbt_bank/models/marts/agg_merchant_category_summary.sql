{{ config(materialized='view') }}

select
    merchant_category,
    count(*) as total_transactions,
    round(sum(transaction_amount), 2) as total_transaction_amount,
    round(avg(transaction_amount), 2) as avg_transaction_amount,
    sum(case when is_fraud = 1 then 1 else 0 end) as fraudulent_transactions
from {{ ref('fct_transactions') }}
group by merchant_category
order by total_transaction_amount desc
