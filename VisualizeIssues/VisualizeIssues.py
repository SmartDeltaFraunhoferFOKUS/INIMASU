import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib.gridspec import GridSpec

from VisualizeIssues.VisualizeDatesOfIssues import visualizeDates
from VisualizeIssues.VisualizeHelpFunctions import mean_responstime_bodylength
from VisualizeIssues.VisualizeBodyAnswertime import visualizeBodyAnswertime
from VisualizeIssues.VisualizeComments import visualizeComments
from VisualizeIssues.VisualizeLabels.VisualizeLabels import visualizeLabels


def visualize(issues):
    labels = [issue.labels if issue.labels else 'No Label' for issue in issues]
    comments = [issue.comments for issue in issues]
    created_dates = [datetime.strptime(issue.created_at, '%Y-%m-%dT%H:%M:%SZ') if issue.created_at else None for issue in issues]
    openIssues = [True if issue.state == "open" else False for issue in issues]
    closed_dates = [datetime.strptime(issue.closed_at, '%Y-%m-%dT%H:%M:%SZ') if issue.closed_at else None for issue in issues]
    updated_dates = [datetime.strptime(issue.updated_at, '%Y-%m-%dT%H:%M:%SZ') if issue.updated_at else None for issue in issues]
    bodies = [len(issue.body) if issue.body else 0 for issue in issues]
    answer_times = [(closed - created).days if closed and created else None for created, closed in
                    zip(created_dates, closed_dates)]

    open_answer_body = []
    for i in range(len(bodies)):
        if closed_dates[i] is None:
            open_answer_body.append(bodies[i])

    visualizeDates(created_dates, closed_dates)
    visualizeBodyAnswertime(bodies, answer_times, open_answer_body)
    visualizeComments(comments,openIssues,answer_times,bodies)
    visualizeLabels(openIssues, answer_times, labels)

    """Next up is the correlation between reactions and closed request, reactions body length, labels and reactions"""
