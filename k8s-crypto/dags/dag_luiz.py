from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonVirtualenvOperator
from airflow.utils.dates import days_ago
import requests


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
        }


def check_https(url, **kwargs):
    response_code = {}
    if isinstance(url, str):
        if url.split('/')[0] in ['https:', 'http:']:
            try:
                response_code[url] = requests.get(url, timeout=30, headers=headers).text
            except Exception:
                response_code[url] = 'offline'
        else:
            try:
                response_code[url] =  requests.get('https://' + url, timeout=30, headers=headers).text
            except Exception:
                try:
                    response_code[url] = requests.get('http://' + url, timeout=30, headers=headers).text,
                except Exception:
                    response_code[url] = 'offline'
    else:
        pass
    return response_code




with DAG(
    'dag_luiz',
    default_args=default_args,
    description='teste dag',
    schedule_interval=days_ago(1),
    start_date=datetime(2021, 12, 7),
    catchup=False,
    tags=['teste'],
) as dag:
    
    virtualenv_task = PythonVirtualenvOperator(
    task_id="check_https",
    python_callable=check_https,
    requirements=["requests"],
    op_kwargs={'url':'google.com'},
    system_site_packages=True,
)

