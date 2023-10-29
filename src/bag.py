from fileIO import getCSVFileContent, findOrCreateFile, overwriteCSVFile
from csvUtls import getIndexOfItem, getMostSimilar, listDictToCSVString

BAG_OF_HOLDING_FILENAME = "bagOfHolding.csv"

FIELDS = ["name", "count", "value(gp)", "description"]

def addToBag(name: str) -> str:
    try:
        findOrCreateFile(BAG_OF_HOLDING_FILENAME)
        saved = getCSVFileContent(BAG_OF_HOLDING_FILENAME)
        index = getIndexOfItem("name", name, saved)

        if index != -1:
            saved[index]["count"] = int(saved[index]["count"]) + 1
        else:
            saved.append({"name": name, "count": 1})
        
        data = listDictToCSVString(saved, ["name", "count"])
        overwriteCSVFile(BAG_OF_HOLDING_FILENAME, data)  
        return f"{name} has been added to the bag of holding."
    except Exception as e:
        print(e)
        return f"{name} could not be added to the bag of holding."
    

def removeFromBag(name: str) -> str:
    try:
        saved = getCSVFileContent(BAG_OF_HOLDING_FILENAME)
        index = getIndexOfItem("name", name, saved)

        if index == -1:
            return f"{name} was not found in the bag of holding."
        count = int(saved[index]["count"])
        if count > 1:
            saved[index]["count"] = count -1
        else:
            del saved[index]
        
        data = listDictToCSVString(saved, ["name", "count"])
        overwriteCSVFile(BAG_OF_HOLDING_FILENAME, data)  
        return f"{name} has been removed from the bag of holding."
    except OSError as e:
        print(e)
        return f"{name} could not be added to the bag of holding."
    
def printBag() -> str:
    try:
        bag = getCSVFileContent(BAG_OF_HOLDING_FILENAME)
        if len(bag) == 0:
            return "Bag is empty."
        result = ""
        for item in bag: 
            name = item["name"]
            count = item["count"]
            result += f"\n - {count} x {name}"
        return result
    except Exception as e:
        print(e);
        return "Somekind of error."
    

def findInbag(name: str) -> str:
    try:
        bag = getCSVFileContent(BAG_OF_HOLDING_FILENAME)
        if len(bag) <= 0:
            return "The bag is empty."
        
        names = []
        for item in bag:
            names.append(item["name"])
        
        possibles = getMostSimilar(names, name)

        if len(possibles) <= 0:
            return f"{name} could not be found in the bag."
        
        if possibles[0]["factor"] >= 0.9:
            possibleName = possibles[0]["name"]
            index = getIndexOfItem("name", possibleName, bag)
            count = bag[index]["count"]
            return f"{possibleName} found in bag you have {count}."
        
        result = "Did you mean ?"
        for x in possibles:
            possibleName = x["name"]
            index = getIndexOfItem("name", possibleName, bag)
            count = bag[index]["count"]
            result += f"\n  -{possibleName} you have {count}"
        return result

    except Exception as e:
        print(e)
        return "An error occured"