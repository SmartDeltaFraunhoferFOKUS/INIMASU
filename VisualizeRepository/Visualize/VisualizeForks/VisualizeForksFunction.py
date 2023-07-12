from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssueAttributes.VisualizeDates.VisualizeDatesFunctions import \
    calculate_forks_per_month


def getFigureforks(fig,ax1,ax2,forks, x_labels, gs):
    # Calculate average forks per month
    average_forks_per_month = calculate_forks_per_month(forks)

    fork_counts = [average_forks_per_month[x] if x in average_forks_per_month else 0 for x in x_labels]

    # Plotting the average monthly forks
    ax3 = fig.add_subplot(gs[2, 0])
    fork_line, = ax3.plot(x_labels, fork_counts, marker="o", color="red")
    ax3.set_xlabel("Month-Year")
    ax3.set_ylabel("Number of pushed Forks")
    ax3.set_title("Monthly forks")

    # Set x-axis tick positions and labels
    ax3.set_xticks(range(len(x_labels)))
    ax3.set_xticklabels(x_labels, rotation=90)

    # Remove labels from ax1 and ax2
    ax1.set_xlabel("")
    ax2.set_xlabel("")
    ax1.set_xticklabels([])
    ax2.set_xticklabels([])
    return fig