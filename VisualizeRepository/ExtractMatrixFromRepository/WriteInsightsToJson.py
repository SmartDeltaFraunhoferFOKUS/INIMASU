import requests
import json


def download_matrix(repo_owner, repo_name, access_token, matrix):
    base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/{matrix}'
    matrix = []

    page = 1
    while True:
        # Fetch a page of issues from the GitHub API, including the access token
        headers = {'Authorization': f'token {access_token}'}
        response = requests.get(f'{base_url}?state=all&page={page}', headers=headers)

        if response.status_code != 200:
            print(f'Error retrieving matrix: {response.text}')
            return

        page_matrix = response.json()

        if not page_matrix:
            # No more issues found, stop pagination
            break

        matrix.extend(page_matrix)
        page += 1

    return matrix

def get_matrix_in_json(repo_owner,repo_name, matrix, access_token):
    # Download the issues
    all_matrix = download_matrix(repo_owner, repo_name, access_token,matrix)

    if all_matrix:
        # Store the issues in a JSON file
        file_path = f'next.js_{repo_owner}_{matrix}.json'
        with open(file_path, 'w') as file:
            json.dump(all_matrix, file, indent=4)

        print(f'All {matrix} have been downloaded and stored in {file_path}.')
    else:
        print(f'No {matrix} found or an error occurred during the download.')
