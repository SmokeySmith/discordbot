import sqlite3

conn = sqlite3.connect('db/pokemon.db')

print("Database was opened")

cursor = conn.cursor()

cursor.execute('''CREATE TABLE User
    (id INT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL);
    ''')

cursor.execute('''CREATE TABLE Pokemon
    (ID INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    image TEXT NOT NULL,
    isShiny INT NOT NULL,
    ownerID INT NOT NULL,
    FOREIGN KEY(ownerID) REFERENCES User(id));
    ''')
conn.commit()
conn.close()