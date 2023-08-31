import json
import os

import numpy as np
from datetime import datetime, timedelta

# Import utility functions from other modules
from IssuePredictionAI.GenerateDataSets.GenerateDataUtils import get_event_per_day, align_dates_of_data
from IssuePredictionAI.GenerateDataSets.PrepareDataSets import prepareDataSets, prepareCodeFrequency, prepareVersion


# Define a function to get data for your project
def getData(issuePath='../Main/next.js_vaadin_issues.json', commitPath='../Main/next.js_vaadin_commits.json',
            code_frequencyPath='../Main/next.js_vaadin_stats_code_frequency.json',
            release_path='../Main/next.js_vaadin_releases.json',
            numberIssues=None, textVectorization=None):
    # Load issue data from the specified JSON file
    with open(issuePath, "r") as f:
        issueData = json.load(f)

    # Get a dictionary with dates and the number of issues per day
    issuesPerDay = get_event_per_day(issueData, "issues")

    # Load commit data from the specified JSON file
    with open(commitPath, "r") as f:
        commitData = json.load(f)

    # Get a dictionary with dates and the number of commits per day
    commitsPerDay = get_event_per_day(commitData, "commits")

    # Load code frequency data from the specified JSON file
    with open(code_frequencyPath, "r") as f:
        code_frequencyData = json.load(f)

    # Load release data from the specified JSON file
    with open(release_path, "r") as f:
        releaseData = json.load(f)

    # Align the dateframes of commits and issues to have the same dates
    issuesPerDay, commitsPerDay = align_dates_of_data(issuesPerDay, commitsPerDay)

    # Convert dictionaries to lists for TensorFlow
    dates = sorted(list(issuesPerDay.keys()))  # List of dates
    commit_counts = [commitsPerDay[date] for date in dates]  # List of commit counts per date
    issue_counts = [issuesPerDay[date] for date in dates]  # List of issue counts per date

    # Prepare code frequency data
    added, subtracted = prepareCodeFrequency(code_frequencyData, dates)

    # Prepare release data
    new_release = prepareVersion(releaseData, dates)

    # Convert the data to numpy arrays
    commit_counts = np.array(commit_counts)

    # Check if text vectorization is requested
    if textVectorization:
        # Prepare data for text vectorization and return it
        labels_issues, description_issue, message_commit = prepareDataSets(issueData, commitData, "textVectorization",
                                                                           dates)
        return dates, commit_counts, issue_counts, labels_issues, description_issue, message_commit, added, subtracted

    # Check if number of issues is requested
    if numberIssues:
        # Return the relevant data
        return dates, commit_counts, issue_counts, added, subtracted, new_release

    # Create labels for predicting if the number of issues is above average or not
    average_issue_count = np.mean(issue_counts)
    issue_above_average = [1 if count > average_issue_count else 0 for count in issue_counts]
    issue_above_average = np.array(issue_above_average)

    # Return the relevant data
    return dates, commit_counts, issue_above_average, added, subtracted, new_release
