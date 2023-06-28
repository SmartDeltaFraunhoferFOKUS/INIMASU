import datetime
from collections import Counter
from VisualizeIssues.VisualizeLabels.HelpFunctionsLabels import getLabelNames, isValidLabel


def getavereageTimePerMonth(created_dates, closed_dates):
    months_data = {}

    # Calculate the counts and average times per month
    for created_date, closed_date in zip(created_dates, closed_dates):
        created_month_year = created_date.strftime("%Y-%m")
        if created_month_year not in months_data:
            months_data[created_month_year] = {"created_count": 0, "closed_count": 0, "total_time": 0,
                                               "average_time": 0}
        months_data[created_month_year]["created_count"] += 1

        if closed_date:  # Check if closed_date exists
            closed_month_year = closed_date.strftime("%Y-%m")
            if closed_month_year not in months_data:
                months_data[closed_month_year] = {"created_count": 0, "closed_count": 0, "total_time": 0,
                                                  "average_time": 0}
            months_data[closed_month_year]["closed_count"] += 1
            answer_time = (closed_date - created_date).days
            months_data[closed_month_year]["total_time"] += answer_time

    # Extract the month-year values and sort them
    month_years = sorted(months_data.keys())

    # Extract the counts and average times per month
    created_counts = [months_data[month_year]["created_count"] for month_year in month_years]
    closed_counts = [months_data[month_year]["closed_count"] for month_year in month_years]
    average_times = [
        months_data[month_year]["total_time"] / months_data[month_year]["closed_count"] if months_data[month_year]["closed_count"] != 0 else 0 for month_year in month_years]
    difference_counts = [created - closed for created, closed in zip(created_counts, closed_counts)]

    return month_years, created_counts, closed_counts, average_times, difference_counts

def getLabelsPerMonth(sorted_data_labels):
    monthly_labels = {}

    for label, created_date in sorted_data_labels:
        month = datetime.datetime(created_date.year, created_date.month, 1).strftime('%Y-%m')

        if month not in monthly_labels:
            monthly_labels[month] = []

        names = getLabelNames(label)
        for n in names:
            if n and isValidLabel(n):
                monthly_labels[month].append(n)

    return monthly_labels




def getTopUsedWords(labelsPerMonth):
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
