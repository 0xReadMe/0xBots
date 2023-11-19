import sqlite3

conn = sqlite3.connect('../database.db')
cur = conn.cursor()


cur.execute('''CREATE TABLE users
(
user_id integer
);''')

cur.execute('''CREATE TABLE admins
(
user_id integer
);''')

cur.execute('''CREATE TABLE bot
(
admin text,
promo text,
hello text,
users integer
);''')