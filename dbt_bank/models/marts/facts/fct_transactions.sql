select
    t.transaction_id,
    c.customer_key,
    a.account_key,
    d.date_key as transaction_date_key,
    t.transaction_date,
    t.transaction_time,
    t.transaction_amount,
    t.merchant_id,
    t.transaction_type,
    t.merchant_category,
    t.account_balance,
    t.transaction_device,
    t.transaction_location,
    t.device_type,
    t.is_fraud,
    t.transaction_currency,
    t.transaction_description
from {{ ref('stg_transactions') }} t
inner join {{ ref('dim_accounts') }} a
    on t.account_id = a.account_id
inner join {{ ref('dim_date') }} d
    on t.transaction_date = d.full_date
inner join {{ ref('dim_customers') }} c
    on t.customer_source_id = c.customer_source_id
    and t.transaction_date between c.valid_from_date and c.valid_to_date
