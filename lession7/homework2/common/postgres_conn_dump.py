import os
from airflow.hooks.postgres_hook import PostgresHook


POSTGRES_CONN_ID = "connection_to_dshop_database"


def copy_to_storage(path_to_file, copy_sql, **kwargs):
    pg_hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
    pg_hook.copy_expert(copy_sql, filename=path_to_file)
    return True