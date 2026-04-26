{{ config(materialized='view') }}

select
    c.city,
    c.state,
    count(*) as total_transactions,
    sum(case when f.is_fraud = 1 then 1 else 0 end) as fraudulent_transactions,
    round(sum(case when f.is_fraud = 1 then f.transaction_amount else 0 end), 2) as fraudulent_amount
from {{ ref('fct_transactions') }} f
inner join {{ ref('dim_customers') }} c
    on f.customer_key = c.customer_key
group by c.city, c.state
order by fraudulent_transactions desc, fraudulent_amount desc
