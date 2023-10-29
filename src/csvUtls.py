import csv
import io
from difflib import SequenceMatcher
from jellyfish import jaro_similarity, jaro_winkler_similarity

def listDictToCSVString(data: list[dict[str, str]], fields: list[str]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()

def getIndexOfItem(key: str, value: str, data: list[dict[str, str]]) -> int:
    for index, item in enumerate(data):
        if item[key] == value:
            return index
    return -1

def getMostSimilar(words: list[str], targetWord:str) -> list[dict[str, float]]:
    sims = []
    
    for word in words:
        if word == targetWord:
            sims.append({"name": targetWord, "factor": 1.0})
            break
        currentSimilarity = complexSimilar(targetWord, word)
        if currentSimilarity > 0.6:
            sims.append({"name": word, "factor": currentSimilarity})

    result = sorted(sims, key=lambda d:d["factor"], reverse=True)[:3]
    return result

def simpleSimilar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def complexSimilar(a, b):
    return jaro_similarity(a.lower(), b.lower())

def moreComplexSimiar(a, b):
    return jaro_winkler_similarity(a.lower(), b.lower())