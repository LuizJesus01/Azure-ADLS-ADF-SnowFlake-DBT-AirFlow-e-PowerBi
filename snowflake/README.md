# Snowflake — Olist Analytics

SQL scripts used to provision, secure and validate the Snowflake layer.

- `setup/`: database, schemas, warehouses and resource monitor.
- `raw/`: RAW table definitions.
- `security/`: RBAC, masking, row access and classification.
- `validation/`: representative reconciliation/data-quality checks.
- `labs/`: isolated Time Travel recovery experiment.

Silver and Gold transformations are managed by dbt under `airflow/include/dbt/`.
No passwords, tokens, account identifiers or personal user grants are included here.
