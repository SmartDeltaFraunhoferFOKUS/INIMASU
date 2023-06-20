import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from VisualizeIssues.VisualizeHelpFunctions import get_mean_comments, get_comments_to_mean_answertime, \
    mean_responstime_bodylength
from VisualizeIssues.VisualizeLabels.HelpFunctionsLabels import getLabelNames, get_labels_with_average_answer_time


def visualizeLabels( openIssues, answer_times, labels):
    sns.set_palette("Set2")

    # Create GridSpec for flexible subplots arrangement
    fig = plt.figure(figsize=(10, 8))
    gs = GridSpec(1, 1, figure=fig)

    labelNames = getLabelNames(labels)
    meanLabels = get_labels_with_average_answer_time(labelNames, answer_times)

    # Plot 1: labelname vs. answer time
    ax1 = fig.add_subplot(gs[0, 0])
    keys = [key for key in meanLabels.keys()]
    values = list(meanLabels.values())
    ax1.scatter(keys, values)
    ax1.set_ylabel('Average answer time')
    ax1.set_xlabel('Labels')



    # Set common title for the entire figure
    fig.suptitle('Distribution Analysis of Issues', fontsize=16)

    # Adjust spacing between subplots
    plt.subplots_adjust(hspace=0.6)

    # Display the plot
    plt.show()