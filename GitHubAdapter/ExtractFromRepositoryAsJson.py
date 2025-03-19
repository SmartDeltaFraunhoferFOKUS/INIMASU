from operator import indexOf
import requests
import json
from threading import Thread
from time import sleep
from multiprocessing.pool import ThreadPool
from threading import Lock
import time


def download_content(repo_owner, repo_name, path_after_repo_name_slash, access_tokens, what_is_retrived):
    base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/{path_after_repo_name_slash}'
    content = []

    page = 1
    totalNumberOfPages = 0
    percent = 0
    iIndexAccessToken=0
    RateLimitsReached = 0
    while True:
        # Fetch a page of content from the GitHub API, including the access token
        headers = {'Authorization': f'token {access_tokens[iIndexAccessToken]}'}
        iIndexAccessToken += 1
        if iIndexAccessToken >= len(access_tokens):
            iIndexAccessToken=0
        response = requests.get(f'{base_url}?state=all&per_page=100&page={page}', headers=headers)
        
        if response.status_code == 200:

            if totalNumberOfPages <= 0:
                totalNumberOfPages = int(response.links['last']['url'][response.links['last']['url'].find("&page=")+6:])
                print(f'Total number of {what_is_retrived} pages = {totalNumberOfPages}')

            page_content = response.json()

            if not page_content:
                # No more content found, stop pagination
                break

            if ( (page * 100) // totalNumberOfPages) > percent:
                percent = (page * 100) // totalNumberOfPages
                print(f'{percent}% of {totalNumberOfPages} {what_is_retrived} pages completed (i.e. {page} pages)')

            content.extend(page_content)
            page += 1
            RateLimitsReached = 0

        else:
            if response.text and (response.text.find('rate limit exceeded') >= 0):
                RateLimitsReached += 1
                if RateLimitsReached >= len(access_tokens):
                    print('rate limit reached - waiting')
                    time.sleep(300)
                    RateLimitsReached=0
            else:
                print(f'Error retrieving {what_is_retrived}: {response.text}')
                return content


    return content


def get_from_repository_in_json_file_threaded_function(repo_owner,repo_name, path_after_repo_name_slash, access_tokens, file_path_base, what_is_retrived):
    # Download the content
    all_content = download_content(repo_owner, repo_name, path_after_repo_name_slash, access_tokens, what_is_retrived)

    if all_content:
        # Store the content in a JSON file
        with open(file_path_base+"_" + what_is_retrived + ".json", 'w') as file:
            json.dump(all_content, file, indent=4)

        print(f'All {what_is_retrived} have been downloaded and stored in {file_path_base+"_" + what_is_retrived + ".json"}.')
        return True
    else:
        print(f'No {what_is_retrived} found or an error occurred during the download.')
        return False


def get_from_repository_in_json_file(repo_owner,repo_name, path_after_repo_name_slash, access_tokens, file_path_base, what_is_retrived):
    thread = Thread(target = get_from_repository_in_json_file_threaded_function, args = (repo_owner,repo_name, path_after_repo_name_slash, access_tokens, file_path_base, what_is_retrived, ))
    thread.start()
    return True
   


def download_per_issue_content(repo_owner, repo_name, path_after_issue_number_slash, access_tokens, what_is_retrived, list_dict_issues):
    content = dict()
    lock = Lock()
    totalNumberOfIssues = len(list_dict_issues)
    print(f'Total number of issues to get {what_is_retrived} from = {totalNumberOfIssues}')
    counter = [0]*2
    def download_content_for_issue(dicOfIssue):
        RateLimitsReached = 0
        content_for_single_issue = []
        result=[]
        try:
            issue_number=dicOfIssue["number"]
            result.append(issue_number)
            result.append(content_for_single_issue)
            base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/{path_after_issue_number_slash}'

            page = 1
            iIndexAccessToken=0

            while True:
                # Fetch a page of content from the GitHub API, including the access token
                headers = {'Authorization': f'token {access_tokens[iIndexAccessToken]}'}
                iIndexAccessToken += 1
                if iIndexAccessToken >= len(access_tokens):
                    iIndexAccessToken=0
                response = requests.get(f'{base_url}?state=all&page={page}', headers=headers)

                if response.status_code == 200:
                    RateLimitsReached = 0
                    page_content = response.json()

                    if not page_content:
                        # No more content found, stop pagination
                        break

                    content_for_single_issue.extend(page_content)
                    page += 1
                else:
                    if response.text and (response.text.find('rate limit exceeded') >= 0):
                        RateLimitsReached += 1
                        if RateLimitsReached >= len(access_tokens):
                            print('rate limit reached - waiting')
                            time.sleep(300)
                            RateLimitsReached=0
                    else:
                        print(f'Error retrieving {what_is_retrived}: {response.text}')
                        break


            with lock:
                counter[0] = counter[0] + 1
                if ( (counter[0] * 100) // totalNumberOfIssues) > counter[1]:
                    counter[1] = (counter[0] * 100) // totalNumberOfIssues
                    print(f'{counter[1]}% of {totalNumberOfIssues} issues to laod {what_is_retrived} from completed (i.e. {counter[0]} issues processed)')
        except:
            print("Exception")
        finally:
            return result

    with ThreadPool() as pool:
        for results in pool.map(download_content_for_issue,list_dict_issues):
            content[int(results[0])]=results[1]

    return content


def get_per_issue_from_repository_in_json_file_threaded_function(repo_owner,repo_name, path_after_issue_number_slash, access_tokens, file_path_base, what_is_retrived, list_dict_issues):
    # Download the content
    all_content = download_per_issue_content(repo_owner, repo_name, path_after_issue_number_slash, access_tokens, what_is_retrived, list_dict_issues)

    if all_content:
        # Store the content in a JSON file
        with open(file_path_base+"_" + what_is_retrived + ".json", 'w') as file:
            json.dump(all_content, file, indent=4)

        print(f'All {what_is_retrived} have been downloaded and stored in {file_path_base+"_" + what_is_retrived + ".json"}.')
        return True
    else:
        print(f'No {what_is_retrived} found or an error occurred during the download.')
        return False


def get_per_issue_from_repository_in_json_file(repo_owner,repo_name, path_after_issue_number_slash, access_tokens, file_path_base, what_is_retrived, list_dict_issues):
    thread = Thread(target = get_per_issue_from_repository_in_json_file_threaded_function, args = (repo_owner,repo_name, path_after_issue_number_slash, access_tokens, file_path_base, what_is_retrived, list_dict_issues, ))
    thread.start()
    return True







def download_commit_details(repo_owner, repo_name, access_tokens, list_dict_commits):
    content=dict()
    lock = Lock()
    totalNumberOfCommits = len(list_dict_commits)
    print(f'Total number of commits to get details from = {totalNumberOfCommits}')
    counter = [0]*2
    def download_content_for_issue(dicOfCommit):
        RateLimitsReached = 0
        result = []
        try:
            commit_sha=dicOfCommit["sha"]
            base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{commit_sha}'

            iIndexAccessToken=0

            #todo: pagination for >300 files
            while (True):
                headers = {'Authorization': f'token {access_tokens[iIndexAccessToken]}'}
                iIndexAccessToken += 1
                if iIndexAccessToken >= len(access_tokens):
                    iIndexAccessToken=0
                response = requests.get(f'{base_url}?state=all', headers=headers)

                if response.status_code == 200:
                    RateLimitsReached = 0
                    page_content = response.json()

                    if page_content:
                        result=page_content

                    break
                else:
                    if response.text and (response.text.find('rate limit exceeded') >= 0):
                        RateLimitsReached += 1
                        if RateLimitsReached >= len(access_tokens):
                            print('rate limit reached - waiting')
                            time.sleep(300)
                            RateLimitsReached=0
                    else:
                        print(f'Error retrieving commit details: {response.text}')
                        break


            with lock:
                counter[0] = counter[0] + 1
                if ( (counter[0] * 100) // totalNumberOfCommits) > counter[1]:
                    counter[1] = (counter[0] * 100) // totalNumberOfCommits
                    print(f'{counter[1]}% of {totalNumberOfCommits} commits to laod details from completed (i.e. {counter[0]} commits processed)')
        except:
            print("Exception")
        finally:
            return result

    with ThreadPool() as pool:
        for results in pool.map(download_content_for_issue,list_dict_commits):
            content[results['sha']]=results

    return content


def get_commit_details_from_repository_in_json_file_threaded_function(repo_owner,repo_name, access_tokens, file_path_base, list_dict_commits):
    # Download the content
    all_content = download_commit_details(repo_owner, repo_name, access_tokens, list_dict_commits)

    if all_content:
        # Store the content in a JSON file
        with open(file_path_base+"_commit_details.json", 'w') as file:
            json.dump(all_content, file, indent=4)

        print(f'All commit details have been downloaded and stored in {file_path_base+"_commit_details.json"}.')
        return True
    else:
        print(f'No commit details found or an error occurred during the download.')
        return False


def get_commit_details_from_repository_in_json_file(repo_owner,repo_name, access_tokens, file_path_base, list_dict_commits):
    thread = Thread(target = get_commit_details_from_repository_in_json_file_threaded_function, args = (repo_owner,repo_name, access_tokens, file_path_base, list_dict_commits, ))
    thread.start()
    return True