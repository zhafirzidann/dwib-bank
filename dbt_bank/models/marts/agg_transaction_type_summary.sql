{{ config(materialized='view') }}

select
    transaction_type,
    count(*) as total_transactions,
    round(sum(transaction_amount), 2) as total_transaction_amount,
    round(avg(transaction_amount), 2) as avg_transaction_amount,
    sum(case when is_fraud = 1 then 1 else 0 end) as total_fraud_transactions
from {{ ref('fct_transactions') }}
group by transaction_type
order by total_transaction_amount desc
