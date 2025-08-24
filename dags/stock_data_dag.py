from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='stock_data_pipeline_v2',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    # This task runs the Python script to fetch and store stock data.
    fetch_and_store_data = BashOperator(
        task_id='fetch_and_store_stock_data',
        bash_command='python /opt/airflow/dags/stock_api_script.py',
    )
