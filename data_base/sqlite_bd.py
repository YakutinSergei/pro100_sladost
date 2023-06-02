import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('prosto_sladost.db')
    cur = base.cursor()
    if base:
        print('База запущена')

    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY,'
                 'description TEXT, price TEXT)')

async def sql_add_command(state):

    cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(state.values()))
    base.commit()
