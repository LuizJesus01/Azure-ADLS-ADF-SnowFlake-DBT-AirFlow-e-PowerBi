with source as (
    select * from {{ source('raw_data', 'ORDER_ITEMS') }}
),

ORDER_ITEMS as (
    SELECT
        ORDER_ID::VARCHAR                         AS ORDER_ID,
        TRY_TO_NUMBER(ORDER_ITEM_ID)              AS ORDER_ITEM_ID,
        PRODUCT_ID::VARCHAR                       AS PRODUCT_ID,
        SELLER_ID::VARCHAR                        AS SELLER_ID,
        TRY_TO_TIMESTAMP_NTZ(SHIPPING_LIMIT_DATE) AS SHIPPING_LIMIT_DATE,
        TRY_TO_DECIMAL(PRICE, 12, 2)              AS PRICE,
        TRY_TO_DECIMAL(FREIGHT_VALUE, 12, 2)      AS FREIGHT_VALUE
    FROM source
)

select * from ORDER_ITEMS