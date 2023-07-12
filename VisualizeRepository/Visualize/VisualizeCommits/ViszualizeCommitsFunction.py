from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssueAttributes.VisualizeDates.VisualizeDatesFunctions import \
    calculate_average_commits


def getFigureCommits(fig,ax1,ax2,commits, x_labels, gs):
    # Calculate average commits per month
    average_commits_per_month = calculate_average_commits(commits)

    commit_counts = [average_commits_per_month[x] if x in average_commits_per_month else 0 for x in x_labels]

    # Plotting the average monthly commits
    ax3= fig.add_subplot(gs[2, 0])
    commit_line, = ax3.plot(x_labels, commit_counts, marker="o", color="red")
    ax3.set_xlabel("Month-Year")
    ax3.set_ylabel("Commits")
    ax3.set_title("Monthly Commits")

    # Set x-axis tick positions and labels
    ax3.set_xticks(range(len(x_labels)))
    ax3.set_xticklabels(x_labels, rotation=90)


    # Remove labels from ax1 and ax2
    ax1.set_xlabel("")
    ax2.set_xlabel("")
    ax1.set_xticklabels([])
    ax2.set_xticklabels([])
    return fig