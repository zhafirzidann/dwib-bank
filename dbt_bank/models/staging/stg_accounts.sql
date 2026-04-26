select
    account_id,
    customer_source_id,
    bank_branch,
    account_type,
    cast(opened_date as date) as opened_date,
    cast(current_balance as double) as current_balance
from {{ source('raw', 'accounts_raw') }}
