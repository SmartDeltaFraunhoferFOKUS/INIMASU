import numpy as np
import matplotlib.pyplot as plt
from VisualizeIssues.VisualizeLabels.HelpFunctionsLabels import getLabelNames

def generate_label_heatmap(labels, answer_times):
    label_names = getLabelNames(labels)
    label_data = get_combined_label_data(label_names, answer_times)

    # Calculate the average answer time for label pairs
    for key1 in label_data.keys():
        for key2 in label_data[key1].keys():
            numbers = label_data[key1][key2]
            label_data[key1][key2] = sum(numbers) / len(numbers) if numbers else 0

    heatmap_data_list = []
    allKeys = list(label_data.keys())

    # Populate the heatmap data
    for i in range(len(allKeys)):
        row = []
        for j in range(len(allKeys)):
            label1 = allKeys[i]
            label2 = allKeys[j]

            if label1 in label_data and label2 in label_data[label1]:
                row.append(label_data[label1][label2])
            else:
                row.append(np.nan)
        heatmap_data_list.append(row)

    # Plot the heatmap
    fig, ax = plt.subplots(figsize=(15, 12))
    im = ax.imshow(heatmap_data_list, cmap='coolwarm')

    # Set x-axis and y-axis labels
    ax.set_xticks(np.arange(len(allKeys)))
    ax.set_yticks(np.arange(len(allKeys)))
    ax.set_xticklabels(allKeys, rotation=90, ha='right', fontsize=10)
    ax.set_yticklabels(allKeys, fontsize=10)

    # Enable zooming and panning
    fig.colorbar(im)
    plt.tight_layout()
    plt.show()






def updateLabelNames(labels):
    if type(labels) != list:
        return None
    for i in range(len(labels) - 1, -1, -1):
        if not is_valid_label(labels[i]):
            labels.pop(i)
    if labels == []:
        return None
    else:
        return labels


def get_combined_label_data(labels, answer_times):
    label_data = {}
    for i in range(len(labels)):
        newLabels = updateLabelNames(labels[i])
        if answer_times[i] is not None and labels[i] is not None:
            label_data = updateLabelData(label_data, labels[i], answer_times[i])
    return label_data


def updateKeyLabelData(label_data, key, labels, answer_time):
    if key not in label_data:
        label_data[key] = {}

    for l in labels:
        if label_data[key].get(l) is not None:
            label_data[key][l].append(answer_time)
        else:
            label_data[key][l] = [answer_time]

    return label_data



def updateLabelData(label_data, labels, answer_time):
    for key in labels:

        if key not in label_data:
            label_data[key] = {}

        updateKeyLabelData(label_data, key, labels, answer_time)
    return label_data


def get_names_from_dict(label_dict):
    names = []
    for key, value in label_dict.items():
        if isinstance(value, str):
            names.append(value)
        elif isinstance(value, dict):
            nested_names = get_names_from_dict(value)
            names.extend(nested_names)
    return names


def is_valid_label(label):
    if not label:
        return False

    for s in label:
        if s.isdigit():
            return False
    return True


