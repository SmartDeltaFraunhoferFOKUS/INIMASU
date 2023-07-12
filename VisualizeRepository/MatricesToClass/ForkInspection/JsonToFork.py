import json

from VisualizeRepository.MatricesToClass.ForkInspection.Forks import Forks


def jsonToForks(path):
    ListOfDicOfforks = readJson(path)
    allforks = createAllforks(ListOfDicOfforks)
    return allforks


def createAllforks(ListOfDicOfforks):
    allforks = []
    for dicOffork in ListOfDicOfforks:
        newfork = Forks(created_at=dicOffork['created_at'], pushed_at =dicOffork['pushed_at'], size=dicOffork["size"])
        allforks.append(newfork)
    return allforks


def readJson(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data
