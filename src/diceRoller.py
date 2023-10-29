import re
import random
import traceback
from fileIO import getJSONFileContent, addToJSONFile, findOrCreateFile

SAVED_ROLL_MACRO_FILENAME = "baseRollMacros.json"

class MacroNestingException(Exception): ...
class MacroFormatException(Exception): ... 
class MacroNotMathSymbolException(Exception): ...

def interpDice(query: str, filePrefix: str) -> tuple:
    try:
        macros = getSavedMacros(filePrefix)
        replacedQuery = replaceWithSavedMacros(query, macros, 3)
        resolvedMarcro = resolveDieMacro(replacedQuery)
        dieResult = evaulateMacro(resolvedMarcro[0])
        return (dieResult[0], dieResult[1], replacedQuery)
    except (OSError, FileNotFoundError) as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return ( 0,"A file error occured.")
    except (MacroFormatException, ZeroDivisionError, MacroNotMathSymbolException, MacroNestingException) as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return (0, str(e), "")
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return (0, "An unknown error occured.", "")

def addMacro(macro_name: str, macro_body: str, filePrefix: str) -> str:
    try:
        if len(macro_name) == 0:
            return "macro name cannot be empty."
        if len(macro_body) == 0:
            return "macro body cannot be empty."

        macros = getSavedMacros(filePrefix)
        replaceWithSavedMacros(macro_body, macros, 2)
        
        fileName = f"{filePrefix}Macros.json"

        error = findOrCreateFile(fileName)
        if error is not None:
            return error
        addToJSONFile(fileName, macro_name, macro_body)
        return f"{macro_name} was added to macros."
    
    except (OSError, FileNotFoundError) as e:
        print(e) 
        traceback.print_tb(e.__traceback__)
        return "A file error occured."
    except (MacroFormatException, ZeroDivisionError, MacroNotMathSymbolException) as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return str(e)
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return "An unknown error occured."

def evaulateMacro(commands: list) -> tuple:
    sum = 0
    operation = None
    dieMacro = ""

    for command in commands:
        current = None
        if isDieCommand(command):
            current = evaluateDieCommand(command)
            dieMacro += str(current) + " "
        elif isMathSymbol(command):
            operation = command
            dieMacro += operation + " "
        elif command.isdigit():
            current = int(command)
            dieMacro += command + " "

        if current is not None and operation is None:
            sum = current
        elif current is not None and operation is not None:
            sum = evaluateMathOperation(sum, current, operation)
            operation = None
    dieMacro += f"= {sum}"
    return (sum, dieMacro)

def evaluateDieCommand(input: str) -> int:
    breakdown = input.split("d")
    count = 1 if breakdown[0] == "" else int(breakdown[0])
    return rollDice(int(breakdown[1]), count)

def evaluateMathOperation(input_a: int, input_b: int, operation: str) -> int:
    if operation == "-":
        return input_a - input_b
    elif operation == "+":
        return input_a + input_b
    elif operation == "*":
        return input_a * input_b
    elif operation == "/":
        try:
           return input_a // input_b
        except ZeroDivisionError as e:
            traceback.print_tb(e.__traceback__)
            raise ZeroDivisionError("In this house we obey the laws of thermodynamics!")
    else:
        raise MacroNotMathSymbolException("This is not an operation")

# resolve the entire macro to a resolvable list of instructions
def resolveDieMacro(input: str) -> tuple:
    if not parseDieMacro(input):
        raise MacroFormatException(f"{input} was not a die macro")
    dividedQuery = input.replace("+", " + ").replace("-", " - ").replace("*", " * ").replace("/", " / ").split()
    resolveQuery = ""
    for item in dividedQuery:
        resolveQuery += item
        item = item.strip()
    
    return (dividedQuery, resolveQuery)

def replaceWithSavedMacros(input: str, savedMacros: dict, maxDepth: int) -> str:
    inputBuffer = input

    for _ in range(maxDepth):
        segmentBuffer = []
        if parseDieMacro(inputBuffer):
            return inputBuffer
        split = re.split("[*-+/]", inputBuffer)
        for seg in split:
            trimmed = seg.strip()

            if not parseDieMacro(seg):
                if trimmed in savedMacros.keys():
                    segmentBuffer.append(trimmed)
                    continue
                raise MacroFormatException(f"{trimmed} is not valid in a die macro")
        
        for seg in segmentBuffer:
            trimmed = seg.strip()
            inputBuffer = inputBuffer.replace(trimmed, savedMacros[trimmed])

    if not parseDieMacro(inputBuffer):
        raise MacroNestingException(f"The macro {inputBuffer} is too deeply nested")
    
    return inputBuffer

def getSavedMacros(filePrefix: str) -> dict:
    fileName = f"/data/userData/{filePrefix}Macros.json"
    findOrCreateFile(fileName)
    content = getJSONFileContent(SAVED_ROLL_MACRO_FILENAME)
    serverContent = getJSONFileContent(fileName)
    
    return content | serverContent

def rollDice(die: int, count: int) -> int:
    total = 0
    for _ in range(count):
        total += random.randint(1, die)
    return total

def isMathSymbol(character:str) -> bool:
    return character in ["+", "-", "/", "*"];

def isDieCommand(input:str) -> bool:
    if len(input) < 2:
        return False
    dCharacters = input.lower().count('d')
    if dCharacters != 1:
        return False
    spilt = input.lower().split('d')
    if len(spilt) != 2:
        return False

    for index, sec in enumerate(spilt):
        if index == 0 and sec == '':
            continue
        if sec.isdigit() and sec[0] != '0' and len(sec) <= 3:
            continue
        return False

    return True    

def padMathSymbols(input:str) -> str:
    split = input.replace("+", " + ").replace("-", " - ").replace("*", " * ").replace("/", " / ").split()
    return " ".join(split)

def parseDieMacro(input:str) -> bool:
    input = padMathSymbols(input)
    if len(input) == 0:
        return False
    if input[0] == '0':
        return False
    
    split = input.lower().split()
    for index,sec in enumerate(split):
        prev = None if 0 == index else split[index-1]

        if isMathSymbol(sec):
            if prev is not None and not isMathSymbol(prev):
                continue
        if isDieCommand(sec):
            if prev is None or isMathSymbol(prev):
                continue
        if sec.isdigit() and len(sec) <=3 and sec[0] != '0':
            if prev is None or isMathSymbol(prev):
                continue
        return False
    return True
