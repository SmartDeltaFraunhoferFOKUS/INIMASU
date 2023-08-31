from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssuesHelpFunctions import calculateMean

# Help functions for visualizeLabels

# Function to extract label names from various input formats
def getLabelNames(labels):
    # Labels are sometimes given in different formats, this function handles inconsistency
    names = []
    for label in labels:
        if type(label) == list:
            names.append(getNamesFromList(label))
        elif type(label) == dict:
            names.append(getNamesFromDict(label))
        else:
            names.append(None)
    return names

# Function to extract label names from a dictionary format
def getNamesFromDict(label):
    return label["name"]

# Function to extract label names from a list of dictionaries
def getNamesFromList(label):
    names = []
    for l in label:
        names.append(l["name"])
    return names

# Function to calculate labels with their average answer times
def get_labels_with_average_answer_time(labels, answer_times):
    overview = {}
    for i in range(len(labels)):
        if answer_times[i] != None and labels[i] != None:
            overview = updateOverview(overview, labels[i], answer_times[i])
    return calculateMean(dict(sorted(overview.items())))

# Function to update the label overview with answer times
def updateOverview(overview, labels, answer_time):
    for l in labels:
        key = l
        if isValidLabel(key):
            if key in overview:
                overview[key].append(answer_time)
            else:
                overview[key] = [answer_time]
    return overview

# Function to check if a label is valid (does not contain digits or certain special characters)
def isValidLabel(label):
    for s in label:
        if s.isdigit() or s in ["/", "\\"]:
            return False
    return True
