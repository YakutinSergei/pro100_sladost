import psycopg2
from environs import Env

env = Env()
env.read_env()



try:
    connection = psycopg2.connect(
        host=env('host'),
        user=env('user'),
        password=env('password'),
        database=env('db_name')
    )

    #cursor
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT version();'
        )
        print(f'Server version: {cursor.fechone()}')
except Exception as _ex:
    print('[INFO] Error ', _ex)

finally:
    global connection
    if connection:
        connection.close()
        print('[INFO] PostgresSQL closed')