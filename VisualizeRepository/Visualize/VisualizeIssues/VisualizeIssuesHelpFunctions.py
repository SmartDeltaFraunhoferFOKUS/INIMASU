import math

# Function to calculate the mean response time based on body length and time interval
def mean_responstime_bodylength(interval, body_length, time):
    # Get an overview of data points within specified intervals
    overview = getOverview(interval, body_length, time)
    # Calculate the mean for each interval
    return calculateMean(overview)

# Function to create an overview of data points within specified intervals
def getOverview(interval, body_length, time):
    overview = {}
    for i in range(len(body_length)):
        if time[i] is not None:
            length = body_length[i]
            # Determine the key based on the interval
            key = math.floor(length / interval)
            if key in overview:
                overview[key].append(time[i])
            else:
                overview[key] = [time[i]]
    # Sort and return the overview
    return dict(sorted(overview.items()))

# Function to calculate the mean for each interval in the overview
def calculateMean(overview):
    averages = {}
    for key in overview.keys():
        values = overview[key]
        # Calculate the average for the values in each interval
        average = sum(values) / len(values)
        averages[key] = average
    return averages

# Function to calculate the mean number of comments for open and closed issues
def get_mean_comments(comments, open_issues):
    true_count = 0
    true_sum = 0
    false_count = 0
    false_sum = 0

    # Iterate through the comments and open_issues lists
    for i in range(len(open_issues)):
        if open_issues[i]:
            true_sum += comments[i]
            true_count += 1
        else:
            false_sum += comments[i]
            false_count += 1

    # Calculate the average number of comments for open and closed issues
    true_average = true_sum / true_count if true_count > 0 else 0
    false_average = false_sum / false_count if false_count > 0 else 0

    return true_average, false_average

# Function to calculate the mean answer time based on the number of comments
def get_comments_to_mean_answertime(comments, answer_time):
    overview = {}
    for i in range(len(comments)):
        if answer_time[i] is not None:
            key = comments[i]
            if key in overview:
                overview[key].append(answer_time[i])
            else:
                overview[key] = [answer_time[i]]
    # Calculate the mean answer time for each number of comments
    return calculateMean(dict(sorted(overview.items())))
