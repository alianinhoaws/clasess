import sqlite3
from serverOOP.serverException import ServerDatabaseException


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
                         (id integer PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, birthday TEXT, telephone TEXT)""")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS Companies
                         (id integer PRIMARY KEY AUTOINCREMENT, name TEXT, address TEXT, telephone TEXT )""")
            print("Tables has been created")
        except Exception as exc:
            return exc

    def save_to_base(self, *args):
        try:
            if args[0] == 'save':
                self.cursor.execute(f"""INSERT INTO {args[-1]} ({", ".join(args[1].keys())}) VALUES 
        ({f"'%s'" % "','".join(args[1].values())})""")
            else:
                self.cursor.execute("SELECT * FROM {} WHERE id ={}".format(args[-1], args[-2]))
                if not self.cursor.fetchall():
                    return '400'
                self.cursor.execute(f"""UPDATE {args[-1]} SET {", ".join(
                "%s = '%s'" % (k, v) for k, v in args[1].items())}
                                       WHERE id={args[-2]}""")
            self.conn.commit()
            print(f"Saved to the base {args}")
        except Exception as exc:
            return exc

    def remove(self, id, name):
        try:
            self.cursor.execute("SELECT * FROM {} WHERE id ={}".format(name, id))
            if not self.cursor.fetchall():
                return '400'
            self.cursor.execute("DELETE from {} WHERE id ={}".format(name, id))
            self.conn.commit()
            print(f"Removed from the base {id, name}")
        except Exception as exc:
            return exc

    def select(self, name, id=None):
        try:
            if id:
                self.cursor.execute("SELECT * FROM {} WHERE id ={}".format(name, id))
            else:
                self.cursor.execute("SELECT * FROM {}".format(name))
            result = self.cursor.fetchall()
            response = ', '.join(map(str, result))
            print(f"Derived from the base {id, name}")
        except Exception as exc:
            return exc
        return response
