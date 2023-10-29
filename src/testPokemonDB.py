import sqlite3

conn = sqlite3.connect('db/pokemon.db')

print("Database was opened")
c = conn.cursor()
c.execute("SELECT * FROM User")
print(c.fetchall())
c.execute("SELECT * FROM Pokemon")
print(c.fetchall())
