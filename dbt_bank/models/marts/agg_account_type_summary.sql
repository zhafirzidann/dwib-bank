{{ config(materialized='view') }}

select
    account_type,
    count(*) as total_accounts,
    round(avg(current_balance), 2) as avg_current_balance,
    round(sum(current_balance), 2) as total_current_balance
from {{ ref('dim_accounts') }}
group by account_type
order by total_accounts desc
