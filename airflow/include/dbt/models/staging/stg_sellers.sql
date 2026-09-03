with source as (
    select * from {{ source('raw_data', 'SELLERS') }}
),

SELLERS as (
    SELECT
        SELLER_ID::VARCHAR                                  AS SELLER_ID,
        LPAD(TRIM(SELLER_ZIP_CODE_PREFIX::VARCHAR),5,'0')   AS SELLER_ZIP_CODE_PREFIX,
        LOWER(TRIM(SELLER_CITY))::VARCHAR                   AS SELLER_CITY,
        UPPER(TRIM(SELLER_STATE))::VARCHAR                  AS SELLER_STATE
    FROM source
)

select * from SELLERS