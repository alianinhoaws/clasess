import sqlite3


def base_connect(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('server.db')
        c = conn.cursor()
        result = func(c, *args, **kwargs)
        conn.close()
        return result
    return wrapper

#TODO add Singletone inheritance to ServerDB


class ServerDB:

    def __init__(self):
        self.values_dict = None
        self.create_tables()

    @base_connect
    def create_tables(self, c):
        try:
            c.execute("""CREATE TABLE IF NOT EXISTS users
                         (id integer PRIMARY KEY, name text, surname text, birthday text, telephone integer)""")
            c.execute("""CREATE TABLE IF NOT EXISTS companies
                         (id integer PRIMARY KEY, name text, address text, telephone integer)""")
        except Exception as exc:
            return exc

    def values_dict(self, *args):
        self.values_dict = {}
        for x in args[:-1]:
            self.values_dict[f':{x}'] = x

    def values_string(*args):
        values_strings = []
        for x in args[:-1]:
            values_strings.append(f':{x}')
        return ' '.join(values_strings)

    @base_connect
    def insert(self, c, *args):
        insert_values = self.values_dict(args)
        values = self.values_string(args)
        try:
            c.execute("INSERT INTO {} VALUES {}".format(args[-1], values), insert_values)
        except Exception as exc:
            return exc

    @base_connect
    def update(self, c, *args):
        insert_values = self.values_dict(args)
        values = self.values_string(args)
        try:
            c.execute("""UPDATE {} SET {}, 
                                WHERE id = :{}""".format(args[-1], values, args[0]),
                      insert_values)
        except Exception as exc:
            return exc

    @base_connect
    def remove(self, c, id, name):
        try:
            c.execute("DELETE from {} WHERE id = :{}".format(name, id))
        except sqlite3.Error as exc:
            return exc
        except Exception as exc:
            return exc

    @base_connect
    def select(self, c, id, name):
        try:
            c.execute("SELECT * FROM {} WHERE id=:id".format(name), {'id': f'{id}'})
            response = c.fetchall()
        except Exception as exc:
            return exc
        return response
