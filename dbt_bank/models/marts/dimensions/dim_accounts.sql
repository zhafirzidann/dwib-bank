select
    md5(account_id) as account_key,
    account_id,
    customer_source_id,
    bank_branch,
    account_type,
    opened_date,
    current_balance
from {{ ref('stg_accounts') }}
