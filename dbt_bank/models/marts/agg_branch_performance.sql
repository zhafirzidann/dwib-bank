{{ config(materialized='view') }}

select
    a.bank_branch,
    a.account_type,
    count(*) as total_transactions,
    round(sum(f.transaction_amount), 2) as total_transaction_amount,
    round(avg(f.transaction_amount), 2) as avg_transaction_amount
from {{ ref('fct_transactions') }} f
inner join {{ ref('dim_accounts') }} a
    on f.account_key = a.account_key
group by a.bank_branch, a.account_type
order by total_transaction_amount desc
