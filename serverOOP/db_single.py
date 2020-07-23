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
        print('ARGSHELPERS', args)
        dict = {}
        for arg in args[0][1:-1]:
            print(arg)
            dict[f':{arg}'] = arg
        return dict

    def values_string(*args):
        print('IN values_string', args)
        values_strings = []
        for arg in args[0][1:-1]:
            print(arg)
            values_strings.append(f':{arg}')
        ' '.join(values_strings)
        return values_strings


# TODO add Singletone inheritance to ServerDB


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
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users
                         (id integer PRIMARY KEY, name text, surname text, birthday text, telephone integer)""")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS companies
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
        print(args)
        insert_values = Helpers.values(args)
        print('INSERT_VALUESR')
        print(insert_values)
        print("ARGS", args)
        values = Helpers.values_string(args)
        print('VALUES')
        print(values)
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
