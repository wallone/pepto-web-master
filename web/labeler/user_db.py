import sqlite3 as lite

con = lite.connect('user_info.db')
admin = ['admin','admin','admin','admin@admin.com']
with con:
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS user')
    cur.execute('CREATE TABLE user(name TEXT, username TEXT, password TEXT, email TEXT, user_id INTEGER PRIMARY KEY)')
    cur.executemany('INSERT INTO user(name, username, password, email) VALUES (?, ?, ?, ?)', (admin,))