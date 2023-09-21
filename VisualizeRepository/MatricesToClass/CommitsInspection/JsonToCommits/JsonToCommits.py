import json

from VisualizeRepository.MatricesToClass.CommitsInspection.Commits.Commits import Commits


def jsonToCommits(path):
    ListOfDicOfcommits = readJson(path)
    allcommits = createAllcommits(ListOfDicOfcommits)
    return allcommits


def createAllcommits(ListOfDicOfcommits):
    allcommits = []
    for dicOfCommit in ListOfDicOfcommits:
        newCommit = Commits(date=dicOfCommit["commit"]["author"]["date"])
        allcommits.append(newCommit)
    return allcommits


def readJson(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data
