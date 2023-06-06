import sqlite3
import sqlite3 as sq

global pg, res, categor

res = dict()
pg = 0
categor = None


def sql_users():
    try:
        global base_users, cur_users
        base_users = sq.connect('users.db')
        cur_users = base_users.cursor()
        if base_users:
            print('База данный юзеров подключена')

        base_users.execute('CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, status TEXT, Page TEXT,'
                     'Category TEXT)')
        cur_users.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if base_users:
            base_users.close()
            print("Соединение с SQLite закрыто")


def sql_users_update_pg(user_id, page):
    try:
        base_users = sq.connect('users.db')
        cur_users = base_users.cursor()
        cur_users.execute('UPDATE users SET Page = 6')
        base_users.commit()
        cur_users.close()

        #cur_users.execute('SELECT *FROM users WHERE user_id = ?', (user_id, ))
        record = cur_users.execute('SELECT * FROM users').fetchall()
        print(record)
        #return record[2]
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if base_users:
            base_users.close()
            print("Соединение с SQLite закрыто")




def append_pg(N):
    global pg
    pg = pg + N
    return pg

def append_categor():
    global categor
    return categor

def append_res():
    global res
    return res

def sql_start():
    global base, cur
    base = sq.connect('prosto_sladost.db')
    cur = base.cursor()
    if base:
        print('База запущена')

    base.execute('CREATE TABLE IF NOT EXISTS menu(category TEXT, img TEXT, name TEXT PRIMARY KEY,'
                 'description TEXT, price TEXT)')

async def sql_add_command(state):
    cur.execute('INSERT INTO menu VALUES(?, ?, ?, ?, ?)', (state['category'],
                                                            state['photos'],
                                                            state['name'],
                                                            state['description'],
                                                            state['price']))
    base.commit()


async def sql_read(cat):
    global res
    res = cur.execute('SELECT * FROM menu WHERE category == ?', (cat, )).fetchall()
    return res


async def delete_sql(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data, ))
    base.commit()