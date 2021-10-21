import os
import psycopg2


pg_creds = {
    "host": "192.168.1.71",
    "port": "5432",
    "dbname": "omdb",
    "user": "pguser",
    "password": "secret"
}


def read_pg():
    tables_to_load = ["movies", "jobs", "categories"]
    with psycopg2.connect(**pg_creds) as pg_connection:
        # запрос через курсор
        cursor = pg_connection.cursor()
        for table_name in tables_to_load:
            # SQL запрос по табличкам из списка при помощи форматной строки
            sql = f"SELECT * FROM {table_name} WHERE id%2 = 0"
            with open(os.path.join(".", "data", f"{table_name}.csv"), "w") as csv_file:
                # Проброс в виде запроса в готовый мастер

                # Обрабатывать каждую строчку из курсора не надо, лучше вычислять все интересующее
                # На локальной машине, чтобы не нагружать базу кучей маленьких запросов
                cursor.copy_expert(f"COPY ({sql}) TO STDOUT WITH HEADER CSV", csv_file)


def write_pg():
    tables_to_write = ["movies", "jobs", "categories"]
    with psycopg2.connect(**pg_creds) as pg_connection:
        # запрос через курсор
        cursor = pg_connection.cursor()

        for table_name in tables_to_write:
            with open(os.path.join('.', 'data', table_name+".csv"), 'r') as csv_file:
                cursor.copy_expert(f'COPY {table_name} FROM STDIN WITH HEADER CSV', csv_file)


if __name__ == "__main__":
    read_pg()
    # write_pg()