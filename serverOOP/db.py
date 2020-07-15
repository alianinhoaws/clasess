import sqlite3


def base_connect(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('server.db')
        c = conn.cursor()
        result = func(c, *args, **kwargs)
        conn.close()
        return result
    return wrapper


@base_connect
def create_tables(c):
    c.execute("""CREATE TABLE IF NOT EXISTS users
                 (id integer PRIMARY KEY, name text, surname text, birthday text, telephone integer)""")
    c.execute("""CREATE TABLE IF NOT EXISTS companies
                 (id integer PRIMARY KEY, name text, address text, telephone integer)""")

create_tables()


@base_connect
def insert_users(c, id, name, surname, birthday, telephone):
    c.execute("INSERT INTO users VALUES (:id, :name, :surname, :birthday, :telephone)",
                  {':id': id, ':name': name, ':surname': surname, ':birthday': birthday, ':telephone': telephone})


@base_connect
def update_users(c, id, name, surname, birthday, telephone):
    # TODO string builder
    #  entity name, id, list args (field_name, value)

    c.execute("""UPDATE users SET :name, :surname, :birthday, :telephone, 
                        WHERE id = :id""",
              {':id': id, ':name': name, ':surname': surname, ':birthday': birthday, ':telephone': telephone})


@base_connect
def update_companies(c, id, name, address, telephone):
    c.execute("""UPDATE companies SET :name, :address, :telephone
                    WHERE id = :id""",
        {':id': id, ':name': name, ':address': address, ':telephone': telephone})


@base_connect
def insert_companies(c, id, name, address, telephone):
    c.execute("INSERT INTO companies VALUES (:id, :name, :address, :telephone)",
              {':id': id, ':name': name, ':address': address, ':telephone': telephone})


@base_connect
def remove_users(c, id, name, surname, birthday, telephone):
    c.execute("DELETE from users WHERE id = :id ",
        {':id': id, 'name': name, 'surname': surname, ':birthday': birthday, ':telephone': telephone})


@base_connect
def remove_companies(c, id, name, address, telephone):
    c.execute("DELETE from companies WHERE id = :id ",
                {':id': id, 'name': name, ':address': address, ':telephone': telephone})

@base_connect
def derive_users_from_db(c, id=None):
    c.execute("SELECT * FROM users WHERE id=:id", {'id': id})
    response = c.fetchall()
    return response


@base_connect
def derive_companies_from_db(c, id=None):
    c.execute("SELECT * FROM companies WHERE id=:id", {'id': id})
    response = c.fetchall()
    return response


@base_connect
def del_companies_from_db(c, id):
    c.execute("DELETE FROM companies WHERE id=:id", {'id': id})


@base_connect
def del_users_from_db(c, id):
    c.execute("DELETE FROM users WHERE id=:id", {'id': id})
