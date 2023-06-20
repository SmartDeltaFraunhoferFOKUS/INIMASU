import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib.gridspec import GridSpec
from VisualizeIssues.VisualizeHelpFunctions import mean_responstime_bodylength

def visualizeBodyAnswertime(bodies, answer_times, open_answer_body ):
    # Plot: Average answertime per length interval
    interval = 1000
    meanResponse = mean_responstime_bodylength(interval, bodies, answer_times)

    # Set seaborn color palette
    sns.set_palette("Set2")

    # Create GridSpec for flexible subplots arrangement
    fig = plt.figure(figsize=(10, 8))
    gs = GridSpec(3, 1, figure=fig)

    # Plot 1: Body Length vs. Closed Time
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.scatter(bodies, answer_times)
    ax1.set_xlabel('Body Length')
    ax1.set_ylabel('Closed Time (in days)')

    # Plot 2: Average answertime per length interval
    ax2 = fig.add_subplot(gs[1, 0])
    scaled_keys = [key * interval for key in meanResponse.keys()]
    values = list(meanResponse.values())
    ax2.plot(scaled_keys, values)
    ax2.set_xlabel("Body length")
    ax2.set_ylabel("Mean response time")

    # Plot 3: Boxplot of the non-answered issues
    ax3 = fig.add_subplot(gs[2, 0])
    ax3.boxplot(open_answer_body)
    ax3.set_xlabel('')
    ax3.set_ylabel('Values')

    # Set common title for the entire figure
    fig.suptitle('Distribution Analysis of Issues', fontsize=16)

    # Adjust spacing between subplots
    plt.subplots_adjust(hspace=0.6)

    # Display the plot
    plt.show()