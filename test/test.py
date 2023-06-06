from data_base.sqlite_bd import sql_users_update_pg, sql_users

sql_users()
pg = sql_users_update_pg(12, 15)

print(pg)