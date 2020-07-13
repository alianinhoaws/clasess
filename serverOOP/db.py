import sqlite3


def create_tables():
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id integer PRIMARY KEY, name text, surname text, birthday text, telephone integer)''')
    c.execute('''CREATE TABLE IF NOT EXISTS companies
                 (id integer PRIMARY KEY, name text, address text, telephone integer)''')
    conn.commit()
    conn.close()


def insert_users(id, name, surname, birthday, telephone):
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (:id, :name, :surname, :birthday, :telephone)",
              {':id': id, ':name': name, ':surname': surname, ':birthday': birthday, ':telephone': telephone})
    conn.commit()
    conn.close()

def insert_companies(id, name, address, telephone):
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    c.execute("INSERT INTO companies VALUES (:id, :name, :address, :telephone)",
              {':id': id, 'name': name, ':address': address, ':telephone': telephone})
    conn.commit()
    conn.close()


def derive_users_from_db(id=None):
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    if id:
        c.execute("SELECT * FROM users WHERE id=:id", {'id': id})
    c.execute("SELECT * FROM users")
    result = c.fetchall()
    conn.close()
    return result


def derive_companies_from_db(id=None):
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    if id:
        c.execute("SELECT * FROM companies WHERE id=:id", {'id': id})
    c.execute("SELECT * FROM companies")
    result = c.fetchall()
    conn.close()
    return result
