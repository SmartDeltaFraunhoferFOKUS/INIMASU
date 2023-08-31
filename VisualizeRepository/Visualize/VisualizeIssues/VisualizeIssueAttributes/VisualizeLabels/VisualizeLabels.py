# Import necessary libraries
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssueAttributes.VisualizeLabels.HelpFunctionsLabels import getLabelNames, get_labels_with_average_answer_time
from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssueAttributes.VisualizeLabels.LabelHeatmapWhenClosed import generate_label_heatmap

# Define a function to visualize labels and their average closing time
def visualizeLabels(answer_times, labels):
    # Set the color palette for the plots
    sns.set_palette("Set2")

    # Create a new figure with a specified size
    fig = plt.figure(figsize=(12, 8))

    # Define a grid for subplots
    gs = GridSpec(1, 1, figure=fig)

    # Get the names of labels
    labelNames = getLabelNames(labels)

    # Calculate the average closing time for each label
    meanLabels = get_labels_with_average_answer_time(labelNames, answer_times)

    # Sort labels by average closing time
    meanLabels = dict(sorted(meanLabels.items(), key=lambda x: x[1]))

    # Plot 1: Label name vs. average answer time
    ax1 = fig.add_subplot(gs[0, 0])
    keys = [key for key in meanLabels.keys()]
    values = list(meanLabels.values())
    ax1.scatter(keys, values)
    ax1.set_ylabel('Average answer time', fontsize=14)
    ax1.set_xlabel('Labels', fontsize=14)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=90, fontsize=12)

    # Add some padding to x-axis tick labels
    plt.tick_params(axis='x', which='major', pad=10)

    # Set the title of the figure
    fig.suptitle('Distribution Analysis of Issues', fontsize=16)

    # Adjust subplot spacing and layout
    plt.subplots_adjust(hspace=0.6)
    plt.tight_layout()

    # Display the number of entries in the plot
    num_entries = len(meanLabels)
    ax1.text(1.02, 0.5, f"Number of Entries:\n{num_entries}", transform=ax1.transAxes, fontsize=12, verticalalignment='center')
    ax1.tick_params(axis='both', labelsize=12)

    # Show the plot
    plt.show()

    # Generate a heatmap to visualize the relationship between labels and their average combined closing time
    generate_label_heatmap(labels, answer_times)

