# ProjetoSnowFlake

Pipeline de dados do conjunto Olist, orquestrado pelo Apache Airflow/Astro. A
ingestão baixa e prepara os arquivos, envia-os ao ADLS, aciona o pipeline do
Azure Data Factory e, após sua conclusão, executa as transformações dbt no
Snowflake.

## Estrutura

- `airflow/dags/`: DAGs do projeto.
- `airflow/include/ingestion/`: scripts executados pela etapa de ingestão.
- `airflow/include/dbt/`: projeto dbt usado pela DAG.
- `airflow/tests/`: testes locais de integridade das DAGs.
- `data/landing/`: arquivos preparados durante execuções locais.

O diretório `airflow/` é a raiz do projeto Astro. Os comandos Astro devem ser
executados a partir dele.

## Configuração

O perfil Snowflake está em `airflow/include/dbt/.dbt/profiles.yml` e não contém
credenciais literais. Antes de executar dbt, configure as variáveis abaixo com
os valores correspondentes ao ambiente Snowflake já utilizado pelo projeto:

```text
DBT_SNOWFLAKE_ACCOUNT
DBT_SNOWFLAKE_USER
DBT_SNOWFLAKE_PASSWORD
DBT_SNOWFLAKE_WAREHOUSE
DBT_SNOWFLAKE_DATABASE
DBT_SNOWFLAKE_SCHEMA
DBT_SNOWFLAKE_ROLE
```

A ingestão também requer `AZURE_STORAGE_SAS_TOKEN`. Variáveis locais podem ser
mantidas em `.env`; esse arquivo é ignorado pelo Git e não deve ser versionado.

## Execução local

Para iniciar o Airflow com Astro:

```bash
cd airflow
astro dev start
```

Para validar o projeto dbt localmente sem executar modelos:

```bash
cd airflow/include/dbt
dbt deps --profiles-dir .dbt
dbt parse --profiles-dir .dbt
```

A DAG continua executando a ingestão como um subprocesso e copia o projeto dbt
para `/tmp/dbt_project`, preservando o comportamento operacional anterior.
