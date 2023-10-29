import sqlite3
from PokemonType import Pokemon

def addUser(userId, userName):
    with sqlite3.connect("db/pokemon.db") as conn:
        conn.execute('''INSERT INTO User VALUES(?, ?)''', (userId, userName))
        conn.commit()

def addPokemon(poke: Pokemon, userId):
    with sqlite3.connect("db/pokemon.db") as conn:
        isShiny = 1 if poke.isShiny else 0
        conn.execute('''INSERT INTO Pokemon(name, image, isShiny, ownerID) 
                        VALUES(?, ?, ?, ?);''', (poke.name, poke.image, isShiny, userId ))
        conn.commit()

def getUserPokemon(userId):
    with sqlite3.connect("db/pokemon.db") as conn:
        data = conn.execute(f'SELECT * FROM Pokemon WHERE ownerID = {userId}').fetchall()
        pokemons:list[Pokemon] = []
        for i, p in enumerate(data):
            pokemons.append(Pokemon(p[1], p[2], "", p[3] > 0))
        return pokemons
    
def userExists(userId) -> bool:
    with sqlite3.connect("db/pokemon.db") as conn:
        cursor = conn.execute(f'''SELECT * FROM User WHERE id = {userId}''')
        data = cursor.fetchall()
        if len(data) == 0:
            return False
        else:
            return True
