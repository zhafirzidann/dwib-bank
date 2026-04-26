with distinct_dates as (
    select distinct transaction_date
    from {{ ref('stg_transactions') }}
)

select
    cast(strftime(transaction_date, '%Y%m%d') as integer) as date_key,
    transaction_date as full_date,
    cast(strftime(transaction_date, '%Y') as integer) as year_number,
    cast(strftime(transaction_date, '%m') as integer) as month_number,
    strftime(transaction_date, '%B') as month_name,
    cast(strftime(transaction_date, '%d') as integer) as day_of_month,
    strftime(transaction_date, '%A') as day_name
from distinct_dates
