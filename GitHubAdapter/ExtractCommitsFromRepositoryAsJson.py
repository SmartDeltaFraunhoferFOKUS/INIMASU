import requests
import json


def download_commits(repo_owner, repo_name, access_token):
    base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits'
    commits = []

    page = 1
    while True:
        # Fetch a page of commits from the GitHub API, including the access token
        headers = {'Authorization': f'token {access_token}'}
        response = requests.get(f'{base_url}?state=all&page={page}', headers=headers)

        if response.status_code != 200:
            print(f'Error retrieving commits: {response.text}')
            return

        page_commits = response.json()

        if not page_commits:
            # No more commits found, stop pagination
            break

        commits.extend(page_commits)
        page += 1

    return commits


def get_commits_in_json_file(repo_owner,repo_name, access_token, file_path_base):
    # Download the commits
    all_commits = download_commits(repo_owner, repo_name, access_token)

    if all_commits:
        # Store the commits in a JSON file
        with open(file_path_base+"_commits.json", 'w') as file:
            json.dump(all_commits, file, indent=4)

        print(f'All commits have been downloaded and stored in {file_path_base+"_commits.json"}.')
        return True
    else:
        print('No commits found or an error occurred during the download.')
        return False
