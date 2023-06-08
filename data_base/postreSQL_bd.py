import psycopg2
from environs import Env

env = Env()
env.read_env()


def postreSQL_connect():
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )


    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')


def postreSQL_read(cat):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT * FROM menu WHERE category ='{cat}'")
            category = cursor.fetchall()


    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')
            return category


def postres_add_command(state):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True
        with connect.cursor() as cursor:
            cursor.execute(f"INSERT INTO menu (category, img, name, description, price) VALUES ('{state['category']}', "
                                                                                                f"'{state['photos']}', "
                                                                                                f"'{state['name']}',"
                                                                                                f"'{state['description']}',"
                                                                                                f"'{state['price']}');")



    except psycopg2.Error as _ex:
        print('[INFO] ОШИБКА ДОБАВЛЕНИЯ ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] Запись добавлена')

#Функция чтения данных пользователя
def postreSQL_user_read(user_id):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE user_id ='{user_id}'")
            category = cursor.fetchall()


    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')
            return category


 # Добавление нового пользователя или изменение категории выбора
def postreSQL_up(user_id, pg, category):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
            users = cursor.fetchall()
        if users:
            with connect.cursor() as cursor:
                cursor.execute(
                    f"UPDATE users SET category = '{category}',"
                    f"page = '0' "
                    f"WHERE user_id = '{user_id}';")
        else:
            with connect.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO users (user_id, category, page, status) VALUES ('{user_id}', "
                    f"'{category}', "
                    f"'{pg}', "
                    "'user');")

    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')
            return users

#Функция обновления страницы
def postreSQL_pg_up(user_id, pg):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT page FROM users WHERE user_id = '{user_id}'")
            pg_user = int(cursor.fetchone()[0][0])

        with connect.cursor() as cursor:
            cursor.execute(
                f"UPDATE users SET page = '{pg_user + pg}' "
                f"WHERE user_id = '{user_id}';")

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT page FROM users WHERE user_id = '{user_id}'")
            pg_user = int(cursor.fetchone()[0][0])



    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')
            return pg_user


def postreSQL_del(name):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        with connect.cursor() as cursor:
            cursor.execute(f"DELETE FROM menu WHERE name = '{name}'")

    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')