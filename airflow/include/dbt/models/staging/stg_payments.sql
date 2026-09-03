with source as (
    select * from {{ source('raw_data', 'PAYMENTS') }}
),

PAYMENTS as (
    SELECT
        RAW_PAYMENTS:order_id::STRING AS ORDER_ID,
        TRY_TO_NUMBER(RAW_PAYMENTS:payment_sequential::STRING) AS PAYMENT_SEQUENTIAL,
        LOWER(TRIM(RAW_PAYMENTS:payment_type::STRING)) AS PAYMENT_TYPE,
        TRY_TO_NUMBER(RAW_PAYMENTS:payment_installments::STRING) AS PAYMENT_INSTALLMENTS,
        TRY_TO_DECIMAL(RAW_PAYMENTS:payment_value::STRING,12,2) AS PAYMENT_VALUE
    FROM source
)

select * from PAYMENTS