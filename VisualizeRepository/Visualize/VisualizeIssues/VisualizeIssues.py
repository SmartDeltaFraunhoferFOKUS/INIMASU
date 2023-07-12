from datetime import datetime

from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssueAttributes.VisualizeBodyAnswertime import visualizeBodyAnswertime
from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssueAttributes.VisualizeComments import visualizeComments
from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssueAttributes.VisualizeDates.VisualizeDates import visualizeDates
from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssueAttributes.VisualizeLabels.VisualizeLabels import visualizeLabels


# creates data points from the issues to get insight
def visualizeIssues(issues):
    labels = [issue.labels if issue.labels else 'No Label' for issue in issues]
    comments = [issue.comments for issue in issues]
    created_dates = [datetime.strptime(issue.created_at, '%Y-%m-%dT%H:%M:%SZ') if issue.created_at else None for issue in issues]
    openIssues = [True if issue.state == "open" else False for issue in issues]
    closed_dates = [datetime.strptime(issue.closed_at, '%Y-%m-%dT%H:%M:%SZ') if issue.closed_at else None for issue in issues]
    updated_dates = [datetime.strptime(issue.updated_at, '%Y-%m-%dT%H:%M:%SZ') if issue.updated_at else None for issue in issues]
    bodies = [len(issue.body) if issue.body else 0 for issue in issues]
    answer_times = [(closed - created).days if closed and created else None for created, closed in
                    zip(created_dates, closed_dates)]
    open_answer_body = [bodies[i] for i in range(len(bodies)) if closed_dates[i] is None]

    #different visualization functions
    visualizeDates(created_dates, closed_dates, labels)
    visualizeBodyAnswertime(bodies, answer_times, open_answer_body)
    visualizeComments(comments,openIssues,answer_times,bodies)
    visualizeLabels(openIssues, answer_times, labels)


