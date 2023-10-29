import os
import csv
import json

def findOrCreateFile(filename: str) -> None:
    if not os.path.exists(filename):
        with open(filename, "x") as f:
            if ".json" in filename:
                emptyDict = {}
                json.dump(emptyDict, f, ensure_ascii=False, indent=4)
    
def fileExists(filename: str) -> bool:
    return os.path.exists(filename)


def getCSVFileContent(fileName: str) -> list[dict[str, str]]:
    result = []
    with open(fileName, "r") as file:
        dictReader = csv.DictReader(file)
        for row in dictReader: 
            result.append(row)
        return result

def overwriteCSVFile(fileName: str, csvData: str) -> None:
    with open(fileName, "w") as file:
        file.write(csvData)

def getJSONFileContent(fileName: str) -> dict:
    with open(fileName, "r") as file:
        data = json.load(file)
        return data

def addToJSONFile(filename: str, key:str, value:str) -> None:
    with open(filename, "r+", encoding="utf-8") as file:
        data:dict = json.load(file)
        if data.get(key) == None:
            data[key] = value
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()
    
def getTextFileContent(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return file.readlines()
    
def appendToTextFile(filename: str, line: str) -> None:
    with open(filename, "a") as file:
        file.write(f"{line}\n")

MAX_FILE_LENGTH = 500
def isFileToolarge(filename: str) -> bool:
    with open(filename, "rbU") as f:
        lines = sum(1 for _ in f)
        return MAX_FILE_LENGTH > lines