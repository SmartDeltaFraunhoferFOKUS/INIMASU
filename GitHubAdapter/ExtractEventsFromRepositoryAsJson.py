import requests
import json


def download_events(repo_owner, repo_name, access_token):
    base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues/events'
    events = []

    page = 1
    while True:
        # Fetch a page of events from the GitHub API, including the access token
        headers = {'Authorization': f'token {access_token}'}
        response = requests.get(f'{base_url}?state=all&page={page}', headers=headers)

        if response.status_code != 200:
            print(f'Error retrieving events: {response.text}')
            return

        page_events = response.json()

        if not page_events:
            # No more events found, stop pagination
            break

        events.extend(page_events)
        page += 1

    return events


def get_events_in_json_file(repo_owner,repo_name, access_token, file_path_base):
    # Download the events
    all_events = download_events(repo_owner, repo_name, access_token)

    if all_events:
        # Store the events in a JSON file
        with open(file_path_base+"_events.json", 'w') as file:
            json.dump(all_events, file, indent=4)

        print(f'All events have been downloaded and stored in {file_path_base+"_events.json"}.')
        return True
    else:
        print('No events found or an error occurred during the download.')
        return False
