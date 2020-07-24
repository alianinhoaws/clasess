import sqlite3
from serverOOP.serverException import ServerDatabaseException


def base_connect(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('server.db')
        c = conn.cursor()
        result = func(c, *args, **kwargs)
        conn.close()
        return result

    return wrapper


class Helpers:
    def values(*args):
        dict = {}
        for arg in args[0][1:-1]:
            dict[f':{arg}'] = arg
        return dict

    def values_string(*args):
        values_strings = []
        for name, arg in args[0][1:-1].items():
            values_strings.append(f':{arg}')
        ' '.join(values_strings)
        return values_strings


class ServerDB:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(ServerDB)
            return cls.instance
        return cls.instance

    def __init__(self, db_name='server.db'):
        self.name = db_name
        self.conn = self.connect()
        self.cursor = self.conn.cursor()

    def connect(self):
        try:
            return sqlite3.connect(self.name)
        except sqlite3.Error as exc:
            raise ServerDatabaseException(exc)

    def create_tables(self):
        try:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users
                         (id integer PRIMARY KEY, name text, surname text, birthday text, telephone integer)""")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS Companies
                         (id integer PRIMARY KEY, name text, address text, telephone integer)""")
        except Exception as exc:
            return exc

    def insert(self, *args):
        insert_values = Helpers.values(args)
        values = Helpers.values_string(args)
        try:
            self.cursor.execute("INSERT INTO {} VALUES {}".format(args[-1], values), insert_values)
        except Exception as exc:
            return exc

    def update(self, *args):
        insert_values = Helpers.values(args)
        values = Helpers.values_string(args)
        try:
            self.cursor.execute("""UPDATE {} SET {}, 
                                WHERE id = :{}""".format(args[-1], values, args[0]),
                                insert_values)
        except Exception as exc:
            return exc

    def remove(self, id, name):
        try:
            self.cursor.execute("DELETE from {} WHERE id = :{}".format(name, id))
        except sqlite3.Error as exc:
            return exc
        except Exception as exc:
            return exc

    def select(self, id, name):
        try:
            self.cursor.execute("SELECT * FROM {} WHERE id=:id".format(name), {'id': f'{id}'})
            response = self.cursor.fetchall()
        except Exception as exc:
            return exc
        return response
