from airflow import DAG
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
from airflow.operators.http_operator import SimpleHttpOperator
import json
from common.get_json_data import get_json_data


log_info = {"username": "rd_dreams", "password": "djT6LasE"}
headers_auth = {"content-type": "application/json"}


default_args = {
    'owner': 'Yurchenkov Ivan',
    'email': ['yurchenkov@mirea.ru'],
    'email_on_failure': True,
    'retries': 2
}

dhop_api_dag = DAG(
    dag_id='api_data_download_dag',
    description='Sample DAG',
    schedule_interval='@daily',
    start_date=datetime(2021,2,14,1,15),
    default_args=default_args
)


# Оператор, который постит запрос на токен
t1 = SimpleHttpOperator(
    task_id='get_auth_token_via_http_post',
    http_conn_id='http_rd_auth_token',
    endpoint='auth',
    method='POST',
    # TODO: можно ли здесь читать что-то из конфига, или это не нужно
    # Логика была бы в изолированности данных от кода, а то я тут некрасиво кидаю сюда пароль с логином
    data=json.dumps(log_info),
    headers=headers_auth,
    xcom_push=True,         # Кидаю токен в xcom_push
    dag=dhop_api_dag
)


t2 = PythonOperator(
    task_id='get_json_data',
    provide_context=True,           # Читаю токен из xcom при помощи xcom.pull из ti
    python_callable=get_json_data,  # common
    dag=dhop_api_dag
)

t1 >> t2