import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from VisualizeIssues.VisualizeHelpFunctions import get_mean_comments, get_comments_to_mean_answertime, \
    mean_responstime_bodylength
from VisualizeIssues.VisualizeLabels.HelpFunctionsLabels import getLabelNames, get_labels_with_average_answer_time
from VisualizeIssues.VisualizeLabels.LabelHeatmapWhenClosed import generate_label_heatmap


def visualizeLabels(openIssues, answer_times, labels):
    sns.set_palette("Set2")

    # Create GridSpec for flexible subplots arrangement
    fig = plt.figure(figsize=(12, 8))  # Increase the figure size

    gs = GridSpec(1, 1, figure=fig)

    labelNames = getLabelNames(labels)
    meanLabels = get_labels_with_average_answer_time(labelNames, answer_times)
    meanLabels = dict(sorted(meanLabels.items(), key=lambda x: x[1]))

    # Plot 1: labelname vs. answer time
    ax1 = fig.add_subplot(gs[0, 0])
    keys = [key for key in meanLabels.keys()]
    values = list(meanLabels.values())
    ax1.scatter(keys, values)
    ax1.set_ylabel('Average answer time', fontsize=14)  # Increase font size for the ylabel
    ax1.set_xlabel('Labels', fontsize=14)  # Increase font size for the xlabel

    # Rotate x-axis labels with a larger angle
    plt.xticks(rotation=90, fontsize=12)  # Increase font size for the x-axis labels

    # Adjust spacing between tick marks
    plt.tick_params(axis='x', which='major', pad=10)

    # Set common title for the entire figure
    fig.suptitle('Distribution Analysis of Issues', fontsize=16)

    # Adjust spacing between subplots
    plt.subplots_adjust(hspace=0.6)
    plt.tight_layout()

    num_entries = len(meanLabels)
    ax1.text(1.02, 0.5, f"Number of Entries:\n{num_entries}", transform=ax1.transAxes, fontsize=12,
             verticalalignment='center')

    # Increase font size for the tick labels
    ax1.tick_params(axis='both', labelsize=12)

    # Display the plot
    plt.show()

    generate_label_heatmap(labels, answer_times)