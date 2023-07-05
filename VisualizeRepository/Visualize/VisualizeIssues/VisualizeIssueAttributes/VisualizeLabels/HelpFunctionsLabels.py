from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssuesHelpFunctions import calculateMean


def getLabelNames(labels):
    names = []
    for label in labels:
        if type(label) == list:
            names.append(getNamesFromList(label))
        elif type(label) == dict:
            names.append(getNamesFromDict(label))
        else:
            names.append(None)
    return names

def getNamesFromDict(label):
    return label["name"]

def getNamesFromList(label):
    names = []
    for l in label:
        names.append(l["name"])
    return names

def get_labels_with_average_answer_time(labels, answer_times):
    overview = {}
    for i in range(len(labels)):
        if answer_times[i] != None and labels[i] != None:
            overview = updateOverview(overview, labels[i], answer_times[i])
    return calculateMean(dict(sorted(overview.items())))

def updateOverview(overview, labels, answer_time):
    for l in labels:
        key = l
        if isValidLabel(key):

            if key in overview:
                overview[key].append(answer_time)
            else:
                overview[key] = [answer_time]

    return overview

def isValidLabel(label):
    for s in label:
        if s.isdigit() or s in ["/","\\"]:
            return False
    return True

