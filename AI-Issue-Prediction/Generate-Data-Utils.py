from datetime import datetime


def get_event_per_day(data, event):
    if event == "commits":
        return get_commits_per_day(data)
    elif event == "issues":
        return get_issues_per_day(data)


def get_commits_per_day(data):
    commitPerDays = {}
    for dicOfCommit in data:
        date = dicOfCommit["commit"]["author"]["date"]
        date_timestamps = datetime.strptime(date, "%Y-%m-%d").timestamp()
        if commitPerDays[date_timestamps]:
            commitPerDays[date_timestamps] += 1
        else:
            commitPerDays[date_timestamps] = 1
    return commitPerDays


def get_issues_per_day(data):
    issuePerDays = {}
    for dicOfIssue in data:
        date = dicOfIssue["created_at"]
        date_timestamps = datetime.strptime(date, "%Y-%m-%d").timestamp()
        if issuePerDays[date_timestamps]:
            issuePerDays[date_timestamps] += 1
        else:
            issuePerDays[date_timestamps] = 1
    return issuePerDays
