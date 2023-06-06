import psycopg2
from environs import Env

env = Env()
env.read_env()

# host = "127.0.0.1"
# user = "postgres"
# password = "Ex-531966"
# db_name = "prosto_sladost"
def postreSQL_connect():
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        #cursor
        with connect.cursor() as cursor:
            cursor.execute(
                'SELECT version();'
            )
            print(f'Server version: {cursor.fetchall()}')
    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')