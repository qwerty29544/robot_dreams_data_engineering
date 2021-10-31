from airflow import DAG
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
from common.postgres_conn_dump import copy_to_storage


tables = ['clients', 'orders', 'products', 'aisles', 'departments']
postgres_tasks = []


default_args = {
    'owner': 'Yurchenkov Ivan',
    'email': ['yurchenkov@mirea.ru'],
    'email_on_failure': True,
    'retries': 2
}

dshop_postgre_dump_dag = DAG(
    dag_id='postresql_dshop_data_dump',
    description='dag that dumps data from postgresql database dshop',
    schedule_interval='@daily',
    start_date=datetime(2021, 10, 20),
    default_args=default_args
)

# Динамические таски
for table in tables:
    path_to_file = f'{table}.csv'
    copy_sql = f"""
                copy (select * from {table}) to STDOUT 
                with csv delimiter ',' header;
                """
    postgres_tasks.append(
        PythonOperator(
            task_id=f'dump_{table}',
            dag=dshop_postgre_dump_dag,
            python_callable=copy_to_storage,
            op_kwargs={"path_to_file": path_to_file,
                       "copy_sql": copy_sql},
            provide_context=True
        )
    )