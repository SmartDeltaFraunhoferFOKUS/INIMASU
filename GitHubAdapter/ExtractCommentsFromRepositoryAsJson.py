import requests
import json


def download_comments(repo_owner, repo_name, access_token):
    base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues/comments'
    comments = []

    page = 1
    while True:
        # Fetch a page of comments from the GitHub API, including the access token
        headers = {'Authorization': f'token {access_token}'}
        response = requests.get(f'{base_url}?state=all&page={page}', headers=headers)

        if response.status_code != 200:
            print(f'Error retrieving comments: {response.text}')
            return

        page_comments = response.json()

        if not page_comments:
            # No more comments found, stop pagination
            break

        comments.extend(page_comments)
        page += 1

    return comments


def get_comments_in_json_file(repo_owner,repo_name, access_token, file_path_base):
    # Download the comments
    all_comments = download_comments(repo_owner, repo_name, access_token)

    if all_comments:
        # Store the comments in a JSON file
        with open(file_path_base+"_comments.json", 'w') as file:
            json.dump(all_comments, file, indent=4)

        print(f'All comments have been downloaded and stored in {file_path_base+"_comments.json"}.')
        return True
    else:
        print('No comments found or an error occurred during the download.')
        return False
