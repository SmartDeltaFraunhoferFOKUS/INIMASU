from ReadJson import readJson
def jsonToIssue(path):
    dicOfIssues = readJson(path)
    keys = list(dicOfIssues.keys())
    allIssues = createAllIssues(dicOfIssues, keys)
    return allIssues
def createAllIssues(dicOfIssues, keys):
    return None
