import matplotlib.pyplot as plt
import datetime
import seaborn as sns
from matplotlib.gridspec import GridSpec

from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssueAttributes.VisualizeDates.VisualizeDatesFunctions import \
    getavereageTimePerMonth, getLabelsPerMonth, \
    getTopUsedWords, calculate_average_commits


def visualizeDates(created_dates, closed_dates, labels, commits=None):
    # Extract the counts and average times per month
    month_years, created_counts, closed_counts, average_times, difference_counts = getavereageTimePerMonth(created_dates, closed_dates)

    combined_data = zip(labels, created_dates)
    sorted_data_labels = sorted(combined_data, key=lambda x: x[1])
    labelsPerMonth = getLabelsPerMonth(sorted_data_labels)
    labelsMonthTopUsed = getTopUsedWords(labelsPerMonth)

    # Generate the x-axis labels in the format "YYYY-MM"
    x_labels = [datetime.datetime.strptime(month_year, "%Y-%m").strftime("%Y-%m") for month_year in month_years]

    # Set seaborn style
    sns.set()

    # Create GridSpec for flexible subplots arrangement
    fig = plt.figure(figsize=(10, 10))
    gs = GridSpec(3 if commits is not None else 2, 1, figure=fig)

    # Plotting the created, closed, and difference issues per month
    ax1 = fig.add_subplot(gs[0, 0])
    created_line, = ax1.plot(x_labels, created_counts, label="Created Issues", color="blue")
    closed_line, = ax1.plot(x_labels, closed_counts, label="Closed Issues", color="orange")
    difference_line, = ax1.plot(x_labels, difference_counts, label="Difference", color="green")
    ax1.set_xlabel("Month-Year")
    ax1.set_ylabel("Number of Issues")
    ax1.set_title("Number of Created, Closed, and Difference Issues per Month")
    ax1.legend()

    # Set x-axis tick positions and labels
    ax1.set_xticks(range(len(x_labels)))
    ax1.set_xticklabels(x_labels, rotation=90)

    # Plotting the average time to close issues per month
    ax2 = fig.add_subplot(gs[1, 0])
    average_line, = ax2.plot(x_labels, average_times, marker="o", color="green")
    ax2.set_xlabel("Month-Year")
    ax2.set_ylabel("Average Time to Close (days)")
    ax2.set_title("Average Time to Close Issues per Month")

    # Set x-axis tick positions and labels
    ax2.set_xticks(range(len(x_labels)))
    ax2.set_xticklabels(x_labels, rotation=90)

    if commits is not None:
        # Calculate average commits per month
        average_commits_per_month = calculate_average_commits(commits)
        commit_month_years = list(average_commits_per_month.keys())
        commit_counts = list(average_commits_per_month.values())
        commit_x_labels = [datetime.datetime.strptime(month_year, "%Y-%m").strftime("%Y-%m") for month_year in
                           commit_month_years]

        # Plotting the average monthly commits
        ax3 = fig.add_subplot(gs[2, 0])
        commit_line, = ax3.plot(commit_x_labels, commit_counts, marker="o", color="red")
        ax3.set_xlabel("Month-Year")
        ax3.set_ylabel("Average Commits")
        ax3.set_title("Average Monthly Commits")

        # Set x-axis tick positions and labels
        ax3.set_xticks(range(len(commit_x_labels)))
        ax3.set_xticklabels(commit_x_labels, rotation=90)

    # Add the number of entries in Created Date as a text box
    num_entries = len(created_dates)
    plt.text(1.02, 0.5, f"Number of Entries:\n{num_entries}", transform=ax1.transAxes, fontsize=12,
             verticalalignment='center')

    def display_top_labels(event):
        if event.inaxes == ax1:
            month_index = int(event.xdata)
            if 0 <= month_index < len(month_years):
                month_year = month_years[month_index]
                top_labels = labelsMonthTopUsed[month_year]
                top_labels_str = "\n".join([f"{label[0]}: {label[1]}" for label in top_labels])
                plt.gcf().suptitle("")  # Clear previous annotation
                plt.gcf().text(0.5, 0.5, f"Top Used Labels for {month_year}:\n{top_labels_str}",
                               ha='center', va='center',
                               bbox=dict(boxstyle="round", fc="w"),
                               fontsize=12)
                plt.draw()

    # Connect the click event to the function
    fig.canvas.mpl_connect('button_press_event', display_top_labels)

    # Adjust spacing between subplots
    plt.tight_layout()

    # Display the plot
    plt.show()

