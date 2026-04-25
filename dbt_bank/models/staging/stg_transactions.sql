select
    transaction_id,
    account_id,
    customer_source_id,
    cast(transaction_date as date) as transaction_date,
    cast(transaction_time as time) as transaction_time,
    cast(transaction_amount as double) as transaction_amount,
    merchant_id,
    transaction_type,
    merchant_category,
    cast(account_balance as double) as account_balance,
    transaction_device,
    transaction_location,
    device_type,
    cast(is_fraud as integer) as is_fraud,
    transaction_currency,
    transaction_description
from {{ source('raw', 'transactions_raw') }}
