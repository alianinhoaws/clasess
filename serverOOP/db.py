import sqlite3


conn = sqlite3.connect('server.db')
c = conn.cursor()

c.execute('''CREATE TABLE users
             (name text, surname text, birthday text, telephone integer)''')

c.execute('''CREATE TABLE companies
             (name text, address text, telephone integer)''')

conn.commit()
conn.close()