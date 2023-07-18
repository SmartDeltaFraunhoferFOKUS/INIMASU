import json
import numpy as np
from datetime import datetime, timedelta
from GenerateDataUtils import get_event_per_day, align_dates_of_data

def getData(issuePath='../Main/next.js_vaadin_issues.json', commitPath='../Main/next.js_vaadin_commits.json', numberIssues = None):
    # Get dictionary with dates and issues per day
    with open(issuePath, "r") as f:
        issueData = json.load(f)
    issuesPerDay = get_event_per_day(issueData, "issues")

    # Get dictionary with dates and commits per day
    with open(commitPath, "r") as f:
        commitData = json.load(f)
    commitsPerDay = get_event_per_day(commitData, "commits")

    # Align the dateframes of commits and issues
    issuesPerDay, commitsPerDay = align_dates_of_data(issuesPerDay, commitsPerDay)

    # Convert dictionaries to lists for TensorFlow
    dates = sorted(list(issuesPerDay.keys()))  # Use datetime.date objects directly
    commit_counts = [commitsPerDay[date] for date in dates]
    issue_counts = [issuesPerDay[date] for date in dates]

    # Calculate average commit and issue counts for the last month
    average_commit_count = np.mean(commit_counts)
    average_issue_count = np.mean(issue_counts)



    # Convert the data to numpy arrays
    commit_counts = np.array(commit_counts)
    if numberIssues:
        return dates, commit_counts, issue_counts
    # Create labels for predicting if the number of issues is above average or not
    issue_labels = [1 if count > average_issue_count else 0 for count in issue_counts]
    issue_labels = np.array(issue_labels)

    return dates, commit_counts, issue_labels


# Now you can proceed to use the `dates`, `commit_counts`, and `issue_labels` in your TensorFlow model.
# Remember to implement the model as shown in the previous examples to complete the process.
