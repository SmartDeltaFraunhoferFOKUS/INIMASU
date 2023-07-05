from VisualizeRepository.MatricesToClass.MatricesToClass import matricesToClass
from VisualizeRepository.MatricesToClass.IssueInspection.Issue.IssueClass import IssueClass
from VisualizeRepository.MatricesToClass.CommitsInspection.Commits.Commits import Commits
from VisualizeRepository.Visualize.VisualizeCommits.VisualizeCommits import visualizeCommits
from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssues import visualizeIssues


def visualize(matrices, matricesFiles):
    matricesClasses = matricesToClass(matrices, matricesFiles)
    issues = None
    commits = None
    for matrixClass in matricesClasses:
        if isinstance(matrixClass[0], IssueClass):
            issues= matrixClass
        elif isinstance(matrixClass[0], Commits):
            commits=matrixClass
        if commits and issues:
            break

    if commits and issues:
        visualizeCommits(commits, issues)
    elif not commits and issues:
        visualizeIssues(issues)
