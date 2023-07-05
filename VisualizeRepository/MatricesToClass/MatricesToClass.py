from VisualizeRepository.MatricesToClass.CommitsInspection.JsonToCommits.JsonToCommits import jsonToCommits
from VisualizeRepository.MatricesToClass.IssueInspection.JsonToIssue.JsonToIssue import jsonToIssue


def matricesToClass(matrices, matricesFiles):
    matricesClasses = []

    for matrix, matrix_file in zip(matrices, matricesFiles):
        if matrix == "issues":
            issues = jsonToIssue(matrix_file)
            matricesClasses.append(issues)
        elif matrix == "commits":
            commits = jsonToCommits(matrix_file)
            matricesClasses.append(commits)

    return matricesClasses
