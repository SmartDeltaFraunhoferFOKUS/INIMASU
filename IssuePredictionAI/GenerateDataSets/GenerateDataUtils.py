from datetime import datetime, timedelta
import gensim
from nltk.tokenize import word_tokenize
import numpy as np
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import BertTokenizer, BertModel
import torch
from transformers import GPT2Tokenizer, GPT2Model
import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

nltk.download('punkt')


# Function to get events (commits or issues) per day
def get_event_per_day(data, event):
    if event == "commits":
        return check_missing_days(get_commits_per_day(data))
    elif event == "issues":
        return check_missing_days(get_issues_per_day(data))


# Function to align dates of two data dictionaries
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
        if len(data1) < len(data2):
            data1[current_day] = 0
        if len(data1) > len(data2):
            data2[current_day] = 0
        current_day += timedelta(days=1)

    return data1, data2


# Function to get commits per day from data
def get_commits_per_day(data):
    commitPerDays = {}
    for dicOfCommit in data:
        date_str = dicOfCommit["commit"]["author"]["date"]
        date_exact = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        date_truncated = date_exact.date()
        if date_truncated in commitPerDays:
            commitPerDays[date_truncated] += 1
        else:
            commitPerDays[date_truncated] = 1
    return commitPerDays


# Function to get issues per day from data
def get_issues_per_day(data):
    issuePerDays = {}
    for dicOfIssue in data:
        date_str = dicOfIssue["created_at"]
        date_exact = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        date_truncated = date_exact.date()
        if date_truncated in issuePerDays:
            issuePerDays[date_truncated] += 1
        else:
            issuePerDays[date_truncated] = 1
    return issuePerDays


# Function to check and fill missing days in an event dictionary
def check_missing_days(eventDic):
    first_day = min(eventDic.keys())
    last_day = max(eventDic.keys())
    current_day = first_day
    while current_day <= last_day:
        if current_day not in eventDic:
            eventDic[current_day] = 0
        current_day += timedelta(days=1)
    return eventDic


# Function to get metrics per day from data
def get_metric_from_data(data: dict, metric: list, date_key: list):
    metricPerDays = {}
    for dicOfMetric in data:
        date_str = get_value_from_nested_dict(dicOfMetric, date_key)
        date_exact = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        date_truncated = date_exact.date()
        if date_truncated in metricPerDays:
            metricPerDays[date_truncated].append(get_value_from_nested_dict(dicOfMetric, metric))
        else:
            metricPerDays[date_truncated] = [get_value_from_nested_dict(dicOfMetric, metric)]
    return check_missing_days(metricPerDays)


# Function to get a value from a nested dictionary using a list of keys
def get_value_from_nested_dict(nested_dict, keys):
    if len(keys) == 1:
        value = nested_dict.get(keys[0])
        if not value:
            return 0
        return nested_dict.get(keys[0])

    current_key = keys[0]
    if current_key in nested_dict:
        next_level_dict = nested_dict[current_key]
        return get_value_from_nested_dict(next_level_dict, keys[1:])

    return 0


# Function to resize a dictionary to a given length with zero values
def get_dic_to_given_length(dic, start_date, end_date):
    # Cut the dictionaries to the common date range
    new_dic = {date: dic[date] for date in dic if start_date <= date <= end_date}

    last_day = max(dic.keys())
    if last_day == end_date:
        return new_dic

    # Match the size of the dictionary to the given frame of start_date and end_date
    current_day = last_day + timedelta(days=1)
    while current_day <= end_date:
        new_dic[current_day] = 0
        current_day += timedelta(days=1)

    return new_dic


# Function for text vectorization using a custom model
def vectorizing_own_model(strings, giveLayer=False, vocab_size=1000):
    vectorize_layer = TextVectorization(
        standardize=None,
        max_tokens=vocab_size,
    )

    tensor = tf.constant([str(s) for s in strings])
    text_ds = tf.data.Dataset.from_tensor_slices(tensor)
    vectorize_layer.adapt(text_ds)

    if giveLayer:
        return vectorize_layer(tf.constant(tensor)), vectorize_layer

    return vectorize_layer(tf.constant(tensor))


# Function to process code frequency data
def get_code_frequency(code_frequency):
    frequency_overview = {}
    for entry in code_frequency:
        timestamp = entry[0]
        date = datetime.utcfromtimestamp(timestamp).date()
        added = entry[1]
        subtracted = entry[2]

        if date in frequency_overview:
            frequency_overview[date]["added"].append(added)
            frequency_overview[date]["subtracted"].append(subtracted)
        else:
            frequency_overview[date] = {"added": [added], "subtracted": [subtracted]}

    return frequency_overview


# Function to resize code frequency data to a given length
def code_frequency_to_given_length(dic, start_date, end_date):
    new_dic = {}

    current_day = start_date
    while current_day <= end_date:
        if current_day in dic:
            new_dic[current_day] = dic[current_day]
        else:
            new_dic[current_day] = {"added": [0], "subtracted": [0]}
        current_day += timedelta(days=1)

    return new_dic


# Function to process release data
def get_releases(releases):
    releases_overview = {}
    for entry in releases:
        published_at_str = entry["published_at"]
        timestamp = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%SZ")
        date = timestamp.date()
        version_number = version_to_integer(entry["tag_name"])

        if date in releases_overview:
            releases_overview[date] = version_number
        else:
            releases_overview[date] = version_number

    return releases_overview


# Function to resize release data to a given length
def releases_to_given_length(dic, start_date, end_date):
    new_dic = {}
    current_day = start_date
    last_version = 0

    while current_day <= end_date:
        if current_day in dic:
            last_version = dic[current_day]
            new_dic[current_day] = last_version
        else:
            if last_version is not None:
                new_dic[current_day] = last_version
        current_day += timedelta(days=1)

    return new_dic


# Function to convert a version string to an integer
def version_to_integer(version):
    components = version.split('.')
    major, minor, patch = map(int, components[:3])
    return major * 1000000 + minor * 10000 + patch * 100


import os
import numpy as np

import os
import numpy as np


def generate_input_sequences(input_data_train, predict_window, analysis_window, output_file):
    if not os.path.isfile(output_file):
        # Initialize a list to store input sequences
        input_sequences = []

        # Iterate through the input data to create input sequences
        size = len(input_data_train)
        for i in range(0, size, predict_window + analysis_window):
            if size - i >= analysis_window:
                # Extract the historical data for the current sequence
                sequence = input_data_train[i: i + analysis_window]
                sequence = np.concatenate(sequence, axis=0).flatten().astype(np.float32)

            #else:
            #    # Add zeros to the end of the sequence to match the rolling window size
            #    pad_length = analysis_window - (size - i)
            #    sequence = input_data_train[i: size]

            #   zeros = np.zeros((pad_length, input_data_train.shape[1]), dtype=np.float32)
            #    sequence = np.concatenate([sequence, zeros], axis=0).flatten()

            # Append the sequence to the list
                input_sequences.append(sequence)
        input_sequences = np.array(input_sequences)
        # Save input_sequences to a file
        np.save(output_file, input_sequences, allow_pickle=True)

    else:
        # Load input_sequences from the file
        input_sequences = np.load(output_file, allow_pickle=True)

    return input_sequences


def generate_label_sequences(input_labels, predict_window, analysis_window, output_file):
    if not os.path.isfile(output_file):
        # Initialize a list to store input sequences
        input_sequences = []

        # Iterate through the input data to create input sequences
        size = len(input_labels)
        for i in range(analysis_window - 1, size, predict_window + analysis_window):
            if size - i >= predict_window:
                # Extract the historical data for the current sequence
                sequence = np.array(input_labels[i: i + predict_window]).astype(np.float32)

            else:
                # Add zeros to the end of the sequence to match the rolling window size
                pad_length = predict_window - (size - i)
                sequence = input_labels[i: size]

                zeros = np.zeros((pad_length, input_labels.shape[1]), dtype=np.float32)
                sequence = np.concatenate([sequence, zeros], axis=0).flatten()

            # Append the sequence to the list
            input_sequences.append(sequence)
        input_sequences = np.array(input_sequences)
        # Save input_sequences to a file
        np.save(output_file, input_sequences, allow_pickle=True)

    else:
        # Load input_sequences from the file
        input_sequences = np.load(output_file, allow_pickle=True)

    return input_sequences
