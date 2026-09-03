from datetime import datetime
import subprocess

from airflow import DAG
from airflow.operators.python import PythonOperator

from airflow.providers.microsoft.azure.operators.data_factory import (
    AzureDataFactoryRunPipelineOperator
)

from airflow.providers.microsoft.azure.sensors.data_factory import (
    AzureDataFactoryPipelineRunStatusSensor
)

from airflow.providers.standard.operators.bash import BashOperator

# ============================================================
# CONFIGURAÇÕES
# ============================================================

INGESTION_SCRIPT = (
    "/usr/local/airflow/include/ingestion/run_ingestion.py"
)


# ============================================================
# FUNÇÕES
# ============================================================

def start_pipeline():
    print("Olist Analytics pipeline started successfully.")


def run_ingestion():
    subprocess.run(
        ["python", INGESTION_SCRIPT],
        check=True
    )


# ============================================================
# DAG
# ============================================================

with DAG(
    dag_id="olist_analytics_pipeline",
    description="End-to-end orchestration for Olist Analytics",
    start_date=datetime(2026, 8, 1),
    schedule=None,
    catchup=False,
    tags=["olist", "data-engineering"],
) as dag:

    # --------------------------------------------------------
    # 1. START
    # --------------------------------------------------------

    start = PythonOperator(
        task_id="start_pipeline",
        python_callable=start_pipeline,
    )


    # --------------------------------------------------------
    # 2. KAGGLE -> ADLS
    # --------------------------------------------------------

    ingest_olist_data = PythonOperator(
        task_id="ingest_olist_data",
        python_callable=run_ingestion,
    )


    # --------------------------------------------------------
    # 3. DISPARA ADF
    # --------------------------------------------------------

    run_adf_pipeline = AzureDataFactoryRunPipelineOperator(
        task_id="run_adf_pipeline",
        azure_data_factory_conn_id="azure_data_factory_default",
        resource_group_name="Projetos",
        factory_name="AdfProjetos",
        pipeline_name="CopyAdlsToSnowflake",
        wait_for_termination=False,
)


    # --------------------------------------------------------
    # 4. AGUARDA ADF
    # --------------------------------------------------------

    wait_adf_pipeline = AzureDataFactoryPipelineRunStatusSensor(
        task_id="wait_adf_pipeline",
        azure_data_factory_conn_id="azure_data_factory_default",
        resource_group_name="Projetos",
        factory_name="AdfProjetos",
        run_id="{{ ti.xcom_pull(task_ids='run_adf_pipeline', key='run_id') }}",
        poke_interval=20,
        timeout=1800,
)

    # --------------------------------------------------------
    # 5. DBT
    # --------------------------------------------------------
    
    prepare_dbt = BashOperator(
        task_id="prepare_dbt",
        bash_command="""
            rm -rf /tmp/dbt_project &&
            cp -r /usr/local/airflow/include/dbt /tmp/dbt_project &&
            cd /tmp/dbt_project &&
            dbt deps --profiles-dir /tmp/dbt_project/.dbt
        """,
)
    
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="""
            cd /tmp/dbt_project &&
            dbt run --profiles-dir /tmp/dbt_project/.dbt
        """,
)

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="""
            cd /tmp/dbt_project &&
            dbt test --profiles-dir /tmp/dbt_project/.dbt
        """,
)

    # ========================================================
    # DEPENDÊNCIAS
    # ========================================================

    start >> ingest_olist_data >> run_adf_pipeline >> wait_adf_pipeline >> prepare_dbt >> dbt_run >> dbt_test
