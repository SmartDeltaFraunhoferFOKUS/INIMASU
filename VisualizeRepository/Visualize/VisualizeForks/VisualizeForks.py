from datetime import datetime

from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssueAttributes.VisualizeDates.VisualizeDates import \
    visualizeDates


def visualizeForks(forks, issues):
    #creates the data points for the plot
    #shows the forks in comparisson to avrg. closing time and generell trafic on the repo
    labels = [issue.labels if issue.labels else 'No Label' for issue in issues]
    created_dates = [datetime.strptime(issue.created_at, '%Y-%m-%dT%H:%M:%SZ') if issue.created_at else None for issue
                     in issues]
    closed_dates = [datetime.strptime(issue.closed_at, '%Y-%m-%dT%H:%M:%SZ') if issue.closed_at else None for issue in
                    issues]

    visualizeDates(created_dates, closed_dates, labels,forks=forks)