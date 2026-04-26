{{ config(materialized='view') }}

select
    c.state,
    count(*) as total_transactions,
    round(sum(f.transaction_amount), 2) as total_transaction_amount,
    sum(case when f.is_fraud = 1 then 1 else 0 end) as fraudulent_transactions
from {{ ref('fct_transactions') }} f
inner join {{ ref('dim_customers') }} c
    on f.customer_key = c.customer_key
group by c.state
order by total_transaction_amount desc
