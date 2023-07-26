import os

from VisualizeRepository.ExtractMatrixFromRepository.CreateJsonFromMatrix import createJsonFromMatrix
from VisualizeRepository.MatricesToClass.MatricesToClass import matricesToClass
from VisualizeRepository.Visualize.Visualize import visualize


# Extracts information from a GitHub Repository and writes the Information into a json
# The Json is visualized afterwards


def main(repo_owner='vaadin', repo_name='flow', matrices=["issues"], access_token=None):
    matricesFiles = []
    # checks if the json for the regarding matrix exists and creates a json if needed
    for matrix in matrices:
        matricesFiles.append(createJsonFromMatrix(repo_owner, repo_name, matrix, access_token))

    # visualies the given data
    visualize(matrices, matricesFiles)


main(matrices=["issues","commits"])

"""
possible other repository to test on
#repo_owner = "vercel"
#repo_name = "next.js"
"""
