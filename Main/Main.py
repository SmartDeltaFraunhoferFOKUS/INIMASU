import os

from VisualizeRepository.ExtractMatrixFromRepository.CreateJsonFromMatrix import createJsonFromMatrix
from VisualizeRepository.MatricesToClass.MatricesToClass import matricesToClass
from VisualizeRepository.Visualize.Visualize import visualize
"""
possible other repository to test on
#repo_owner = "vercel"
#repo_name = "next.js"
"""


def main(repo_owner='vaadin', repo_name='flow', matrices = ["issues"], access_token='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'):

    matricesFiles = []
    for matrix in matrices:
        matricesFiles.append(createJsonFromMatrix(repo_owner,repo_name,matrix,access_token))

    visualize(matrices, matricesFiles)


main(repo_owner="vercel", repo_name="next.js", matrices=["issues"])
