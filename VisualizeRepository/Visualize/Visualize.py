from VisualizeRepository.MatricesToClass.MatricesToClass import matricesToClass
from VisualizeRepository.MatricesToClass.IssueInspection.Issue.IssueClass import IssueClass
from VisualizeRepository.MatricesToClass.CommitsInspection.Commits.Commits import Commits
from VisualizeRepository.Visualize.VisualizeCommits.VisualizeCommits import visualizeCommits
from VisualizeRepository.Visualize.VisualizeForks.VisualizeForks import visualizeForks
from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssues import visualizeIssues
from VisualizeRepository.MatricesToClass.ForkInspection.Forks import Forks


def visualize(matrices, matricesFiles):
    # checks for the currently three supported matrices and visualizes them
    matricesClasses = matricesToClass(matrices, matricesFiles)
    issues = None
    commits = None
    fork = None
    for matrixClass in matricesClasses:
        if isinstance(matrixClass[0], IssueClass):
            issues = matrixClass
        elif isinstance(matrixClass[0], Commits):
            commits = matrixClass
        elif isinstance(matrixClass[0], Forks):
            fork = matrixClass
        if commits and issues:
            break

    if commits and issues:
        visualizeCommits(commits, issues)
    if fork and issues:
        visualizeForks(fork, issues)
    elif not commits and issues:
        visualizeIssues(issues)
