import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssueAttributes.VisualizeLabels.HelpFunctionsLabels import getLabelNames, get_labels_with_average_answer_time
from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssueAttributes.VisualizeLabels.LabelHeatmapWhenClosed import generate_label_heatmap

#Visualizes the labels attached to the issues to avrg. closing time
def visualizeLabels(openIssues, answer_times, labels):
    sns.set_palette("Set2")


    fig = plt.figure(figsize=(12, 8))

    gs = GridSpec(1, 1, figure=fig)

    labelNames = getLabelNames(labels)
    meanLabels = get_labels_with_average_answer_time(labelNames, answer_times)
    meanLabels = dict(sorted(meanLabels.items(), key=lambda x: x[1]))

    # Plot 1: labelname vs. answer time
    ax1 = fig.add_subplot(gs[0, 0])
    keys = [key for key in meanLabels.keys()]
    values = list(meanLabels.values())
    ax1.scatter(keys, values)
    ax1.set_ylabel('Average answer time', fontsize=14)
    ax1.set_xlabel('Labels', fontsize=14)


    plt.xticks(rotation=90, fontsize=12)

    plt.tick_params(axis='x', which='major', pad=10)


    fig.suptitle('Distribution Analysis of Issues', fontsize=16)

    plt.subplots_adjust(hspace=0.6)
    plt.tight_layout()

    num_entries = len(meanLabels)
    ax1.text(1.02, 0.5, f"Number of Entries:\n{num_entries}", transform=ax1.transAxes, fontsize=12,
             verticalalignment='center')
    ax1.tick_params(axis='both', labelsize=12)


    plt.show()
    #generates a heatmap to get overview between two labels and their avrg. combined closing time
    generate_label_heatmap(labels, answer_times)