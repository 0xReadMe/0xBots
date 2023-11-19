import sqlite3


conn = sqlite3.connect('database.db')
cur = conn.cursor()


def is_user(user_id):
    res = cur.execute(f'SELECT * FROM users where user_id = ?', (user_id,)).fetchall()
    return res

def is_admin(user_id):
    res = cur.execute(f'SELECT * FROM admins where user_id = ?', (user_id,)).fetchall()
    return res


def new_user(user_id):
    cur.execute(f"INSERT INTO users VALUES ({user_id})")
    conn.commit()


def del_user(user_id):
    cur.execute(f'delete from users where user_id = "{user_id}"')
    conn.commit()


def get_all_users():
    res = cur.execute(f'SELECT * FROM users').fetchall()
    return res


def get_users():
    res = cur.execute(f'SELECT users FROM bot').fetchall()
    return res[0][0]

def get_hello_text():
    res = cur.execute(f'SELECT hello FROM bot').fetchall()
    return res[0][0]


def get_admin_text():
    res = cur.execute(f'SELECT admin FROM bot').fetchall()
    return res[0][0]


def get_promo_text():
    res = cur.execute(f'SELECT promo FROM bot').fetchall()
    return res[0][0]


def edit_text_promo(text):
    cur.execute(f'UPDATE bot set promo = ?', (text, ))
    conn.commit()


def edit_text_admin(text):
    cur.execute(f'UPDATE bot set admin = ?', (text, ))
    conn.commit()

def edit_text_hello(text):
    cur.execute(f'UPDATE bot set hello = ?', (text, ))
    conn.commit()


def update_users(users):
    cur.execute(f'UPDATE bot set users = ?', (users, ))
    conn.commit()


def get_admins():
    res = cur.execute(f'SELECT * FROM admins').fetchall()
    return res


def new_admin(user_id):
    cur.execute(f'INSERT INTO admins(user_id) VALUES ({user_id})')
    conn.commit()

def del_admin(user_id):
    cur.execute(f'delete from admins where user_id = {int(user_id)}')
    conn.commit()