import json

def readJson(path)
    with open(path, 'r') as file:
        data = json.load(file)
    return data

