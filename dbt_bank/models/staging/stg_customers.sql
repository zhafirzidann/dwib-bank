select
    customer_source_id,
    customer_name,
    gender,
    cast(age as integer) as age,
    state,
    city,
    customer_contact,
    customer_email,
    cast(valid_from as date) as valid_from_date
from {{ source('raw', 'customers_raw') }}
