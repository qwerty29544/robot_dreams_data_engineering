from airflow import DAG
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
import json


default_args = {
    'owner': 'Yurchenkov Ivan',
    'email': ['yurchenkov@mirea.ru'],
    'email_on_failure': True,
    'retries': 2
}

dhop_postgre_dump_dag = DAG(
    dag_id='postresql_dshop_data_dump',
    description='dag that dumps data from postgresql database dshop',
    schedule_interval='@daily',
    start_date=datetime(2021,10,20),
    default_args=default_args
)



