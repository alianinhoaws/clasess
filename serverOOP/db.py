import sqlite3

def base_connect(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('server.db')
        c = conn.cursor()
        result = func(c, *args, **kwargs)
        conn.close()
        return result

    return wrapper


class ServerDB:

    def __init__(self):
        self.values_dict = None
        self.create_tables()

    @base_connect
    def create_tables(self, c):
        c.execute("""CREATE TABLE IF NOT EXISTS users
                     (id integer PRIMARY KEY, name text, surname text, birthday text, telephone integer)""")
        c.execute("""CREATE TABLE IF NOT EXISTS companies
                     (id integer PRIMARY KEY, name text, address text, telephone integer)""")

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
        c.execute("INSERT INTO {} VALUES {}".format(args[-1], values), insert_values)

    @base_connect
    def update(self, c, *args):
        # TODO string builder
        #  entity name, id, list args (field_name, value)
        insert_values = self.values_dict(args)
        values = self.values_string(args)
        c.execute("""UPDATE {} SET {}, 
                            WHERE id = :{}""".format(args[-1], values, args[0]),
                  insert_values)

    @base_connect
    def remove(self, c, id, name):
        c.execute("DELETE from {} WHERE id = :{}".format(name, id))

    @base_connect
    def select(self, c, id, name):
        c.execute("SELECT * FROM {} WHERE id=:id".format(name), {'id': f'{id}'})
        response = c.fetchall()
        return response