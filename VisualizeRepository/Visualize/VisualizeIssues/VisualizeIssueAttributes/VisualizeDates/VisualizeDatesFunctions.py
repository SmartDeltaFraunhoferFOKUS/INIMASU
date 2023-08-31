from datetime import datetime
from collections import defaultdict
from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssueAttributes.VisualizeLabels.HelpFunctionsLabels import getLabelNames, isValidLabel
import matplotlib.pyplot as plt



#Help function to create the needed datapoints for visualizeDates
def getavereageTimePerMonth(created_dates, closed_dates):
    # Dic containing the amount of closed, created and answer_time per month
    months_data = getMonthsData(created_dates, closed_dates)

    # Extract the month-year values and sort them
    month_years = sorted(months_data.keys())

    # Extract the counts and average times per month
    created_counts = [months_data[month_year]["created_count"] for month_year in month_years]
    closed_counts = [months_data[month_year]["closed_count"] for month_year in month_years]
    average_times = [months_data[month_year]["total_time"] / months_data[month_year]["closed_count"] if months_data[month_year]["closed_count"] != 0 else 0 for month_year in month_years]
    difference_counts = [created - closed for created, closed in zip(created_counts, closed_counts)]

    return month_years, created_counts, closed_counts, average_times, difference_counts

def getLabelsPerMonth(sorted_data_labels):
    # generates a dic containing the labels used per month
    monthly_labels = {}

    for label, created_date in sorted_data_labels:
        month = datetime(created_date.year, created_date.month, 1).strftime('%Y-%m')

        if month not in monthly_labels:
            monthly_labels[month] = []

        # gives back valid label as a string
        names = getLabelNames(label)
        for n in names:
            if n and isValidLabel(n):
                monthly_labels[month].append(n)

    return monthly_labels

def getMonthsData(created_dates, closed_dates):
    # creating a dic containing the amount of closed, created and answer_time per month
    months_data = {}

    for created_date, closed_date in zip(created_dates, closed_dates):
        created_month_year = created_date.strftime("%Y-%m")

        if created_month_year not in months_data:
            months_data[created_month_year] = {"created_count": 0, "closed_count": 0, "total_time": 0}

        months_data[created_month_year]["created_count"] += 1

        # Check if closed_date exists
        if closed_date:
            closed_month_year = closed_date.strftime("%Y-%m")

            if closed_month_year not in months_data:
                months_data[closed_month_year] = {"created_count": 0, "closed_count": 0, "total_time": 0}

            months_data[closed_month_year]["closed_count"] += 1
            answer_time = (closed_date - created_date).days
            months_data[closed_month_year]["total_time"] += answer_time

    return months_data


def getTopUsedWords(labelsPerMonth):
    # Generates a dict, key = month, values = top 5 used labels per month
    top_words_per_month = {}

    for month, labels in labelsPerMonth.items():
        word_count = {}

        for label in labels:
            if isinstance(label, list):
                label = ' '.join(label)

            words = label.split()  # Split the label into individual words

            for word in words:
                if isValidLabel(word):
                    if word in word_count:
                        word_count[word] += 1
                    else:
                        word_count[word] = 1

        top_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:5]  # Get the top 5 words
        top_words_per_month[month] = top_words

    return top_words_per_month


def calculate_average_commits(commits):
    commits_per_month = defaultdict(list)

    for commit in commits:
        commit_date = datetime.strptime(commit.date, "%Y-%m-%dT%H:%M:%SZ")
        month_year = commit_date.strftime("%Y-%m")
        commits_per_month[month_year].append(commit_date)

    average_commits_per_month = {}
    for month_year, commit_list in sorted(commits_per_month.items()):
        average_commits_per_month[month_year] = len(commit_list)

    return average_commits_per_month

def calculate_forks_per_month(forks):
    forks_per_month = defaultdict(list)

    for fork in forks:
        fork_date = datetime.strptime(fork.created_at, "%Y-%m-%dT%H:%M:%SZ")
        month_year = fork_date.strftime("%Y-%m")
        forks_per_month[month_year].append(fork_date)

    count_forks_per_month = {}
    for month_year, commit_list in sorted(forks_per_month.items()):
        count_forks_per_month[month_year] = len(commit_list)

    return count_forks_per_month





