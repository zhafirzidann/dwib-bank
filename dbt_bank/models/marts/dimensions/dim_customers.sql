select
    customer_key,
    customer_source_id,
    customer_name,
    gender,
    age,
    state,
    city,
    customer_contact,
    customer_email,
    valid_from_date,
    valid_to_date,
    is_current
from {{ ref('int_customer_scd') }}
