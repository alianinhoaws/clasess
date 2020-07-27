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

    def values_string(*args):
        values_strings = []
        for name in args[0][1].keys():
            values_strings.append(f'{name}')
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
        self.create_tables()

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

    def save_to_base(self, types, *args):
        values = []
        for x in args[1].values():
            values.append(x)
        values.insert(0, args[0])
        arguments = (Helpers.values_string(args))
        arguments.insert(0, 'id')
        values = tuple(values)
        print(("INSERT INTO {} VALUES ({})".format(args[-1], ', '.join(arguments)), values))
        try:
            if types == 'insert':
                self.cursor.execute("""UPDATE {} SET {}, 
                                            WHERE id = {}""".format(args[-1], " ".join(values), args[0]), values)
            else:
                self.cursor.execute("INSERT INTO {} VALUES (?,?,?,?) {}".format(args[-1], arguments), values)
                #self.cursor.execute("INSERT INTO {} VALUES ({})".format(args[-1], ', '.join(arguments)), values)
            self.conn.commit()
        except Exception as exc:
            return exc

    def remove(self, id, name):
        try:
            self.cursor.execute("DELETE from {} WHERE id = :{}".format(name, id))
        except Exception as exc:
            return exc

    def select(self, id, name):
        try:
            self.cursor.execute("SELECT * FROM {} WHERE id=:id".format(name), {'id': f'{id}'})
            response = self.cursor.fetchall()
        except Exception as exc:
            return exc
        print(response)
        return response
