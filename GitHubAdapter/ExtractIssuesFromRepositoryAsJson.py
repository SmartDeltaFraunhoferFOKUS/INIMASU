import requests
import json
from threading import Thread
from time import sleep


def download_issues(repo_owner, repo_name, access_token):
    base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'
    issues = []

    page = 1
    totalNumberOfPages = 0
    percent = 0
    while True:
        # Fetch a page of issues from the GitHub API, including the access token
        headers = {'Authorization': f'token {access_token}'}
        response = requests.get(f'{base_url}?state=all&page={page}', headers=headers)

        if response.status_code != 200:
            print(f'Error retrieving issues: {response.text}')
            return

        if totalNumberOfPages <= 0:
            totalNumberOfPages = int(response.links['last']['url'][response.links['last']['url'].find("page=")+5:])
            print(f'Total Number of issue Pages = {totalNumberOfPages}')

        page_issues = response.json()

        if not page_issues:
            # No more issues found, stop pagination
            break

        if ( (page * 100) // totalNumberOfPages) > percent:
            percent = (page * 100) // totalNumberOfPages
            print(f'{percent}% of {totalNumberOfPages} issue pages completed (i.e. {page} pages)')

        issues.extend(page_issues)
        page += 1

    return issues


def get_issues_in_json_file_threaded_function(repo_owner,repo_name, access_token, file_path_base):
    # Download the issues
    all_issues = download_issues(repo_owner, repo_name, access_token)

    if all_issues:
        # Store the issues in a JSON file
        with open(file_path_base+"_issues.json", 'w') as file:
            json.dump(all_issues, file, indent=4)

        print(f'All issues have been downloaded and stored in {file_path_base+"_issues.json"}.')
        return True
    else:
        print('No issues found or an error occurred during the download.')
        return False


def get_issues_in_json_file(repo_owner,repo_name, access_token, file_path_base):
    thread = Thread(target = get_issues_in_json_file_threaded_function, args = (repo_owner,repo_name, access_token, file_path_base, ))
    thread.start()
    return True
   
