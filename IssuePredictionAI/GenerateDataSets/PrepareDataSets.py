import os
import numpy as np

# Import functions from external modules
from IssuePredictionAI.GenerateDataSets.GenerateDataUtils import (
    get_dic_to_given_length, get_metric_from_data,
    get_code_frequency, code_frequency_to_given_length,
    get_releases, releases_to_given_length
)
from IssuePredictionAI.GenerateDataSets.PreprocessText import process_labels, process_description

# This function prepares datasets based on the specified setType.
def prepareDataSets(issueData, commitData, setType, dates):
    if setType == "textVectorization":
        return prepareTextVectorization(issueData, commitData, dates)

# This function retrieves basic data from issue and commit data.
def getBasicData(issueData, commitData, dates):
    # Get Information from JSON
    descriptionIssuePerDays = get_metric_from_data(issueData, ["body"], ["created_at"])
    labelsIssuesPerDays = get_metric_from_data(issueData, ["labels"], ["created_at"])
    messageCommitPerDays = get_metric_from_data(commitData, ["commit", "message"], ["commit", "author", "date"])

    start_date = min(dates)
    end_date = max(dates)

    # Get data for the right date frame
    descriptionIssuePerDays = get_dic_to_given_length(descriptionIssuePerDays, start_date, end_date)
    labelsIssuesPerDays = get_dic_to_given_length(labelsIssuesPerDays, start_date, end_date)
    messageCommitPerDays = get_dic_to_given_length(messageCommitPerDays, start_date, end_date)

    # Extract string-based inputs
    description_issue = [descriptionIssuePerDays[date] for date in dates]
    labels_issues = [labelsIssuesPerDays[date] for date in dates]
    message_commit = [messageCommitPerDays[date] for date in dates]

    # Preprocess Text Data: Remove stop words and simplify
    labels_issues = process_labels(labels_issues)
    description_issue = process_description(description_issue)
    message_commit = process_description(message_commit)

    return labels_issues, description_issue, message_commit

# This function prepares text vectorization-based data.
def prepareTextVectorization(issueData, commitData, dates):
    if os.path.exists('../processed_data_text_vectorizer.npz'):
        # Load the processed data from the file if it exists
        processed_data = np.load('../processed_data_text_vectorizer.npz', allow_pickle=True)
        labels_issues = processed_data['labels_issues']
        description_issue = processed_data['description_issue']
        message_commit = processed_data['message_commit']
    else:
        # Get Basic Data
        labels_issues, description_issue, message_commit = getBasicData(issueData, commitData, dates)

        # Save processed data to a file
        np.savez('../processed_data_text_vectorizer.npz', labels_issues=labels_issues,
                 description_issue=description_issue,
                 message_commit=message_commit, allow_pickle=True)

    return labels_issues, description_issue, message_commit

# This function prepares code frequency data.
def prepareCodeFrequency(code_frequencyData, dates):
    start_date = min(dates)
    end_date = max(dates)

    code_frequency = get_code_frequency(code_frequencyData)

    code_frequency = code_frequency_to_given_length(code_frequency, start_date, end_date)

    # Extract 'added' and 'subtracted' values
    added = [entry["added"] for entry in code_frequency.values()]
    subtracted = [entry["subtracted"] for entry in code_frequency.values()]

    return added, subtracted

# This function prepares version data.
def prepareVersion(releaseData, dates):
    start_date = min(dates)
    end_date = max(dates)

    releases = get_releases(releaseData)
    releases = releases_to_given_length(releases, start_date, end_date)

    # Extract release versions and calculate the difference
    releases_list = [releases[date] for date in releases.keys()]

    new_release_list = []
    previous_release = 0

    for release in releases_list:
        difference = release - previous_release
        new_release_list.append(difference)
        previous_release = release

    return new_release_list
