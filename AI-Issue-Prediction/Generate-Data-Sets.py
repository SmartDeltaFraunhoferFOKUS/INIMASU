import json
import numpy as np

def getData( issuePath="Main/next.js_vaadin_issues.json", commitPath="Main/next.js_vaadin_commits.json"):

    with open(issuePath,"r") as f:
        issueData = json.load(f)
    issuesPerDay = get_event_per_day(issueData,"issues")

    with open(commitPath,"r") as f:
        commitData = json.load(f)
    commitsPerDay = get_event_per_day(commitData,"commits")

