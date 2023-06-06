import sqlite3
import sqlite3 as sq

global pg, res, categor

res = dict()
pg = 0
categor = None


def append_pg(N):
    global pg
    if N == None:
        pg = 0
        return pg
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