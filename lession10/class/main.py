from hdfs import InsecureClient
import psycopg2

pg_creds = {
    "host": "192.168.0.17",
    "user": "pguser",
    "password": "secret",
    "port": "5432",
    "database": "omdb"
}


def main():
    client = InsecureClient(f'http://127.0.0.1:50070/', user='user')
    with psycopg2.connect(**pg_creds) as pg_connection:
        cursor = pg_connection.cursor()
        with client.write("/lession10/casts.csv") as csv:
            cursor.copy_expert("COPY public.casts TO STDOUT WITH HEADER CSV", csv)


if __name__ == "__main__":
    main()