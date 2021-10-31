import os
from hdfs import InsecureClient
from airflow.hooks.postgres_hook import PostgresHook


POSTGRES_CONN_ID = "connection_to_dshop_bu_database"


def copy_to_storage(path_to_file, copy_sql, **kwargs):
    client = InsecureClient(f'http://127.0.0.1:50070/', user='user')

    client.makedirs('/bronze')
    client.makedirs('/bronze/homework1')

    pg_hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
    path_csv = os.path.join("bronze", "homework1", path_to_file)
    with client.write(path_csv) as csv_file:
        pg_hook.copy_expert(copy_sql, filename=csv_file)
    return True