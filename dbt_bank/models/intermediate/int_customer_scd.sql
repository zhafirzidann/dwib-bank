with ordered_customers as (
    select
        customer_source_id,
        customer_name,
        gender,
        age,
        state,
        city,
        customer_contact,
        customer_email,
        valid_from_date,
        lead(valid_from_date) over (
            partition by customer_source_id
            order by valid_from_date
        ) as next_valid_from_date
    from {{ ref('stg_customers') }}
)

select
    md5(customer_source_id || '|' || cast(valid_from_date as varchar)) as customer_key,
    customer_source_id,
    customer_name,
    gender,
    age,
    state,
    city,
    customer_contact,
    customer_email,
    valid_from_date,
    coalesce(next_valid_from_date - interval 1 day, date '9999-12-31') as valid_to_date,
    next_valid_from_date is null as is_current
from ordered_customers
