from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'teste',
    default_args=default_args,
    description='teste dag',
    schedule_interval=days_ago(1),
    start_date=datetime(2021, 11, 22),
    catchup=False,
    tags=['teste'],
) as dag:

    t1 = BashOperator(
        task_id='print_date',
        bash_command='date'
    )