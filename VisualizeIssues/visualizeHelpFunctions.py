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
