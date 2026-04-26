{{ config(materialized='view') }}

select
    d.full_date,
    count(*) as total_transactions,
    round(sum(f.transaction_amount), 2) as total_transaction_amount,
    sum(case when f.is_fraud = 1 then 1 else 0 end) as total_fraud_transactions
from {{ ref('fct_transactions') }} f
inner join {{ ref('dim_date') }} d
    on f.transaction_date_key = d.date_key
group by d.full_date
order by d.full_date
