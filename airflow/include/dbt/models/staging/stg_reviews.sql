with source as (
    select * from {{ source('raw_data', 'REVIEWS') }}
),

REVIEWS as (
    SELECT
        RAW_REVIEWS:review_id::STRING AS REVIEW_ID,
        RAW_REVIEWS:order_id::STRING AS ORDER_ID,
        TRY_TO_NUMBER(RAW_REVIEWS:review_score::STRING) AS REVIEW_SCORE,
        NULLIF(TRIM(RAW_REVIEWS:review_comment_title::STRING),'') AS REVIEW_COMMENT_TITLE,
        NULLIF(TRIM(RAW_REVIEWS:review_comment_message::STRING),'') AS REVIEW_COMMENT_MESSAGE,
        TRY_TO_TIMESTAMP_NTZ(RAW_REVIEWS:review_creation_date::STRING) AS REVIEW_CREATION_DATE,
        TRY_TO_TIMESTAMP_NTZ(RAW_REVIEWS:review_answer_timestamp::STRING) AS REVIEW_ANSWER_TIMESTAMP
    FROM source
)

select * from REVIEWS