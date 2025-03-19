from VisualizeRepository.MatricesToClass.IssueInspection.Issue.IssueClass import IssueClass
from VisualizeRepository.MatricesToClass.MatricesToClass import matricesToClass
from VisualizeRepository.MatricesToClass.CommitsInspection.Commits import Commits
from VisualizeRepository.Visualize.VisualizeCommits.VisualizeCommits import visualizeCommits
from VisualizeRepository.Visualize.VisualizeForks.VisualizeForks import visualizeForks
from VisualizeRepository.Visualize.VisualizeIssues.VisualizeIssues import visualizeIssues
from VisualizeRepository.MatricesToClass.ForkInspection.Forks import Forks


def visualize(matrices, matricesFiles):
    # checks for the currently three supported matrices and visualizes them

    # Generates a list of list containing the objects of a class for a given matrix: [[issue,...],...]
    matricesClasses = matricesToClass(matrices, matricesFiles)

    # Boolean to check which matrices are given
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

    # Visualize the given matrices
    if commits and issues:
        visualizeCommits(commits, issues)
    if fork and issues:
        visualizeForks(fork, issues)
    elif not commits and issues:
        visualizeIssues(issues)
