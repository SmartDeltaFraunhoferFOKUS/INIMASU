import json
from Issue.IssueClass import IssueClass
def jsonToIssue(path):
    ListOfDicOfIssues = readJson(path)
    keys = list(ListOfDicOfIssues[0].keys())
    allIssues = createAllIssues(ListOfDicOfIssues, keys)
    return allIssues
def createAllIssues(ListOfDicOfIssues, keys):
    allIssues = []
    Keys = ["body", "created_at", "labels", "updated_at", "closed_at", "reactions","comments","state"]
    for dicOfIssue in ListOfDicOfIssues:
        newIssue = IssueClass(**{ key : dicOfIssue[key] for key in Keys})
        allIssues.append(newIssue)
    return allIssues
def readJson(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data