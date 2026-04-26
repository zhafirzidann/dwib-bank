{{ config(materialized='view') }}

select
    device_type,
    count(*) as total_transactions,
    sum(case when is_fraud = 1 then 1 else 0 end) as fraudulent_transactions,
    round(
        100.0 * sum(case when is_fraud = 1 then 1 else 0 end) / count(*),
        2
    ) as fraud_rate_pct
from {{ ref('fct_transactions') }}
group by device_type
order by fraud_rate_pct desc, fraudulent_transactions desc
