import random
from diceRoller import interpDice 
import traceback
from fileIO import getTextFileContent, appendToTextFile, findOrCreateFile

BASE_INSULTS_FILE = "baseInsults.txt"
SERVER_FILE_PARTIAL = "_insults.txt"

def getUserFileName(filePrefix: str) -> str: 
    return f"/data/userData/{filePrefix}{SERVER_FILE_PARTIAL}"

def insult(file_prefix) -> str:
    try:
        baseInsults = getTextFileContent(BASE_INSULTS_FILE)
        userfile = getUserFileName(file_prefix)
        findOrCreateFile(userfile)
        userInsults = getTextFileContent(userfile)
        insults = baseInsults + userInsults

        insultsMax = len(insults) - 1
        randomInsultIndex = random.randint(1, insultsMax)
        insult = insults[randomInsultIndex].replace("\n", "")
        dieResult = interpDice("2d4 + 4", file_prefix)
        result = f"**Vicious Mockery** \n *{insult}* \n `{dieResult[1]}`"
        return result
    except (OSError, FileExistsError, FileNotFoundError) as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return "An unknown file error has occured"

def isKnownInsult(input: str, userFileName: str) -> bool:
    savedInsults = getTextFileContent(BASE_INSULTS_FILE)
    userInsults = getTextFileContent(userFileName)
    insults = savedInsults + userInsults
    return input in set(insults)

def addInsult(input: str, file_prefix:str) -> str:
    if len(input) == 0:
        return "Insult cannot be empty"
    try: 
        userFile = getUserFileName(file_prefix)
        findOrCreateFile(userFile)
        # TODO add input cleaning hear so someone can't save some real bad stuff
        cleanInput = input
        isKnown = isKnownInsult(cleanInput, userFile)
        if isKnown:
            return "I already know this one."
        appendToTextFile(userFile, cleanInput)
        return "Congrats you're a bad influence"

    except (OSError, Exception) as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return "An unknown error has occured"

