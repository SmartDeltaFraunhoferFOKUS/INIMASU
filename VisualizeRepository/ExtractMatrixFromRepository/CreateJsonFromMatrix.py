from VisualizeRepository.ExtractMatrixFromRepository.WriteInsightsToJson import get_matrix_in_json
import os

def createJsonFromMatrix(repo_owner,repo_name,matrix,access_token):
    matrix_json_file = f'next.js_{repo_owner}_{matrix}.json'
    if not os.path.exists(matrix_json_file):
        get_matrix_in_json(repo_owner, repo_name, matrix, access_token)
    return matrix_json_file