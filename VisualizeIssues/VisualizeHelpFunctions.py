import math
def mean_responstime_bodylength(interval, body_length, time):
    overview = getOverview(interval, body_length, time)
    return calculateMean(overview)


def getOverview(interval, body_length, time):
    overview = {}
    for i in range(len(body_length)):
        if time[i] != None:
            length = body_length[i]
            key = math.floor(length/ interval)
            if key in overview:
                overview[key].append(time[i])
            else:
                overview[key] = [time[i]]
    return dict(sorted(overview.items()))


def calculateMean(overview):
    averages = {}
    for key in overview.keys():
        values = overview[key]
        average = sum(values) / len(values)
        averages[key] = average
    return averages

def get_mean_comments(comments,open_issues):
    true_count = 0
    true_sum = 0
    false_count = 0
    false_sum = 0

    for i in range(len(open_issues)):
        if open_issues[i]:
            true_sum += comments[i]
            true_count += 1
        else:
            false_sum += comments[i]
            false_count += 1

    true_average = true_sum / true_count if true_count > 0 else 0
    false_average = false_sum / false_count if false_count > 0 else 0

    return true_average, false_average

def get_comments_to_mean_answertime(comments,answer_time):
    overview = {}
    for i in range(len(comments)):
        if answer_time[i] != None:
            key = comments[i]
            if key in overview:
                overview[key].append(answer_time[i])
            else:
                overview[key] = [answer_time[i]]
    return calculateMean(dict(sorted(overview.items())))