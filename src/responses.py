from bag import addToBag, findInbag, printBag, removeFromBag
from diceRoller import interpDice, addMacro
from insulter import insult, addInsult

BAG_OF_HOLDING_FILENAME = "/bagOfHolding.csv"
ROLL = "roll"
ROLL_2 = "r"
HELLO = "hello"
SEARCH_BAG = "searchbag"
ADD_TO_BAG = "addtobag"
REMOVE_FROM_BAG = "removefrombag"
PRINT_BAG = "printbag"
HELP = "help"
ADD_MACRO = "addmacro"

def errorMsg(message):
    return f":x: {message} :x:"

def unpackMessage(input:str) -> tuple:
    divided = input.split(" ", 1)
    operation = divided[0].lower().strip()
    arguments = [] if len(divided) <= 1 else divided[1].split("|")
    trimmedArgs = []
    for a in arguments:
        trimmedArgs.append(a.strip())
    hasArgs = len(trimmedArgs) > 0
    return (operation, trimmedArgs, hasArgs)
    

def handleRepsone(message) -> str:
    unpackMessaged = unpackMessage(message)
    operation = unpackMessaged[0]
    arguments = unpackMessaged[1]
    hasArgs = unpackMessaged[2]

    if operation == HELLO:
        return "Hello UwU I'm a \"bot\" I'm here to help you and your party go on wonderous adventures together."
    
    if operation == ROLL or operation == ROLL_2 and hasArgs:
        value = interpDice(arguments[0].lower())
        if type(value) == OSError:
            return errorMsg("An interal error occured.")
        if type(value) == Exception:
            return errorMsg(value)
        num = str(value[0])
        expanded = str(value[1])
        return f"{arguments[0]} = {num}`\n {value[2]} \n {expanded}`"
    if operation == "sleep":
        return "Even machines need rest. Goodnight UwU"
    if operation == ADD_MACRO and len(arguments) >= 2: 
        result = addMacro(arguments[0].lower(), arguments[1].lower())
        if type(result) == Exception:
            return errorMsg(result)
        return result
    if operation == SEARCH_BAG and hasArgs:
        return findInbag(arguments[0].lower())
    
    if operation == ADD_TO_BAG and hasArgs:
        return addToBag(arguments[0].lower())
    
    if operation == REMOVE_FROM_BAG and hasArgs:
        return removeFromBag(arguments[0].lower())
    
    if operation == PRINT_BAG:
        return printBag()
    
    if operation == "dispardis":
        value = insult()
        if type(value) == Exception:
            return errorMsg(value)
        return value
    
    if operation == "addbarb" and hasArgs:
        value = addInsult(arguments[0])
        if type(value) == Exception:
            return errorMsg(value)
        return value

    if operation == HELP:
        return "`This is a help message that you can modify`"
    
    return "I'm sorry but I don't understand that command."