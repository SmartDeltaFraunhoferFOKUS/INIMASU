from datetime import datetime, timedelta


def get_event_per_day(data, event):
    if event == "commits":
        return check_missing_days(get_commits_per_day(data))
    elif event == "issues":
        return check_missing_days(get_issues_per_day(data))
def align_dates_of_data(data1, data2):
    # Find the common start and end dates
    common_start_date = max(min(data1.keys()), min(data2.keys()))
    common_end_date = min(max(data1.keys()), max(data2.keys()))
    uncommon_end_date = max(max(data1.keys()), max(data2.keys()))

    # Cut the dictionaries to the common date range
    data1 = {date: data1[date] for date in data1 if common_start_date <= date}
    data2 = {date: data2[date] for date in data2 if common_start_date <= date}

    # Extend the shorter dictionary to the uncommon end date
    current_day = common_end_date + timedelta(days=1)
    while current_day <= uncommon_end_date:
        if len(data1)<len(data2):
            data1[current_day] = 0
        if len(data1)>len(data2):
            data2[current_day] = 0
        current_day += timedelta(days=1)

    return data1, data2



def get_commits_per_day(data):
    commitPerDays = {}
    for dicOfCommit in data:
        date_str = dicOfCommit["commit"]["author"]["date"]
        date_exact = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        date_truncated = date_exact.date()  # Get the date object by calling the .date() method
        if date_truncated in commitPerDays:
            commitPerDays[date_truncated] += 1
        else:
            commitPerDays[date_truncated] = 1
    return commitPerDays


def get_issues_per_day(data):
    issuePerDays = {}
    for dicOfIssue in data:
        date_str = dicOfIssue["created_at"]
        date_exact = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        date_truncated = date_exact.date()  # Get the date object by calling the .date() method
        if date_truncated in issuePerDays:
            issuePerDays[date_truncated] += 1
        else:
            issuePerDays[date_truncated] = 1
    return issuePerDays

def check_missing_days(eventDic):
    first_day = min(eventDic.keys())
    last_day = max(eventDic.keys())
    current_day = first_day
    while current_day <= last_day:
        if current_day not in eventDic:
            eventDic[current_day] = 0
        current_day += timedelta(days=1)

    return eventDic