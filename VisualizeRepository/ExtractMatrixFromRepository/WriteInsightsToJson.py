import os
from datetime import datetime

import requests
import json


def download_matrix(repo_owner, repo_name, access_token, matrix):
    base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/{matrix}'

    # Fetch the code-frequency matrix from the GitHub API
    headers = {'Authorization': f'token {access_token}'}

    result_matrix = []

    page = 1
    while True:
        response = requests.get(base_url, headers=headers, params={'page': page})

        if response.status_code != 200:
            print(f'Error retrieving {matrix}: {response.text}')
            return []

        matrix_page = response.json()

        if not matrix_page:
            break

        result_matrix.extend(matrix_page)
        page += 1

    print(f'Total entries retrieved: {len(result_matrix)}')

    return result_matrix


def get_matrix_in_json(repo_owner, repo_name, matrix, access_token):
    # Download the matrix
    all_matrix = download_matrix(repo_owner, repo_name, access_token, matrix)

    if all_matrix:
        # Store the matrix in a JSON file
        file_path = f'next.js_{repo_owner}_{matrix.replace("/", "_")}.json'
        with open(file_path, 'w') as file:
            json.dump(all_matrix, file, indent=4)

        print(f'All {matrix} have been downloaded and stored in {file_path}.')
    else:
        print(f'No {matrix} found or an error occurred during the download.')
