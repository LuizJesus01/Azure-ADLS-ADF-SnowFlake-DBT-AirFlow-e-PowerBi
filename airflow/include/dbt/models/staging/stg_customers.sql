with source as (
    select * from {{ source('raw_data', 'CUSTOMERS') }}
),

CUSTOMERS as (
    SELECT
        RAW_CUSTOMERS:customer_id::STRING AS CUSTOMER_ID,
        RAW_CUSTOMERS:customer_unique_id::STRING AS CUSTOMER_UNIQUE_ID,
        LPAD(RAW_CUSTOMERS:customer_zip_code_prefix::STRING,5,'0') AS CUSTOMER_ZIP_CODE_PREFIX,
        LOWER(TRIM(RAW_CUSTOMERS:customer_city::STRING)) AS CUSTOMER_CITY,
        UPPER(TRIM(RAW_CUSTOMERS:customer_state::STRING)) AS CUSTOMER_STATE

    FROM source
)

select * from CUSTOMERS