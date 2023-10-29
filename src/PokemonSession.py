from PokemonType import Pokemon
import random
import datetime
import DatabaseInteraction
import requests
import requests_cache
import json
import os

NOT_STARTED = "NOT_STARTED"
STARTED = "STARTED"
FINISHED = "FINISHED"

class PokemonSession:
    MAX_DIFFICULTY = 20
    MAX_ATTEMPTS = 8
    def __init__(self) -> None:
        self.state = NOT_STARTED
        self.maxAttempts = random.randint(1, PokemonSession.MAX_ATTEMPTS)
        self.difficulty = 0
        self.attemptedUsers: list[str] = []
        self.pokemon = None
        self.maxDuration = None
        self.lastSessionStart = None

    def resetSession(self):
        self.state = NOT_STARTED
        self.maxAttempts = 4
        self.attemptedUsers: list[str] = []
        self.difficulty = 0
        self.pokemon = None
        self.maxDuration = None

    def startSession(self) -> None | str:
        if self.isSessionStarted() and self.hasSessionExpired():
            self.resetSession()
        if self.isSessionStarted() and not self.hasSessionExpired():
            return "Cannot find a new pokemon right now."      
        if self.state != FINISHED and self.state != NOT_STARTED:
            return "Cannot find a new pokemon right now."
        
        self.lastSessionStart = datetime.datetime.now()
        self.state = STARTED
        self.pokemon = generatePokemon()
        self.difficulty = random.randint(1, PokemonSession.MAX_DIFFICULTY)
        self.maxDuration = datetime.datetime.now() + datetime.timedelta(minutes=10)
        return None

    def hasSessionExpired(self) -> bool:
        if self.lastSessionStart is None:
            return False
        expiredTime = self.lastSessionStart + datetime.timedelta(seconds=15)
        hasSessionExpired = datetime.datetime.now() > expiredTime
        return hasSessionExpired

    def getPokemon(self) -> Pokemon | None:
        return self.pokemon
    
    def isSessionStarted(self) -> bool:
        return self.state == STARTED and self.pokemon is not None
    
    def attemptCatch(self, user) -> str:
        if self.pokemon is None:
            return "Pokemon is not set what went wrong"
        if self.maxDuration is not None and datetime.datetime.now() > self.maxDuration:
            result = f"{self.pokemon.displayName} has gotten away."
            self.state = FINISHED
            return result
        
        userId = user.id
        userName = user.name
        result = f"{userName} has failed to catch {self.pokemon.displayName}."

        self.maxAttempts -= 1
        self.attemptedUsers.append(userId)

        if random.randint(1, self.difficulty) == self.difficulty:
            result = f"{userName} has caught a {self.pokemon.displayName}"
            DatabaseInteraction.addPokemon(self.pokemon, userId)
            self.state = FINISHED

        if self.maxAttempts == 0:
            result = f"{self.pokemon.displayName } has gotten away."
            self.state = FINISHED
        
        return result
    
def generatePokemon() -> Pokemon:
    data = loadPokemonFromAPI()
    index = random.randint(1, len(data))
    return getPokemonDataFromAPI(data[index].get("url"), data[index].get("name"))

def getPokemonDataFromAPI(url: str, name: str) -> Pokemon:
    requests_cache.install_cache(f"~/poke/poke_cache_{name}")
    request = requests.get(url)
    value:dict = json.loads(request.text)
    isShiny = random.randint(1, 100) == 100
    sprite = dict(dict(dict(value.get("sprites")).get("other")).get("official-artwork")).get("front_default")
    if isShiny:
        sprite = dict(dict(dict(value.get("sprites")).get("other")).get("official-artwork")).get("front_shiny")
    return Pokemon( name=name, url=url, image=sprite, isShiny=isShiny)

def loadPokemonFromAPI() -> list[dict]:
    ENDPOINT = os.environ["POKEMON_ENDPOINT"]
    requests_cache.install_cache("~/poke/poke_cache")
    request = requests.get(f"{ENDPOINT}?limit=1000&offset=0")
    value:dict = json.loads(request.text)
    names = []
    results: list(dict) = value.get("results")
    for p in results:
        names.append({"name": p.get("name"), "url": p.get("url")})
    return names
