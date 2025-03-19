from GitHubAdapter.GraphQLGitHub import GetAllRelatedIssues
import json
from threading import Thread


def get_PullRequestRelatedIssueNumbres_in_json_file_threaded_function(repo_owner,repo_name, access_tokens, file_path_base):
    print('Start reading related issue numbers')
    DictRelatedIssues = GetAllRelatedIssues(repo_owner, repo_name, access_tokens)
    if DictRelatedIssues:
        # Store the issues in a JSON file
        with open(file_path_base+"_PullRequestRelatedIssueNumbres.json", 'w') as file:
            json.dump(DictRelatedIssues, file, indent=4)

        print(f'All PullRequestRelatedIssueNumbres have been downloaded and stored in {file_path_base+"_PullRequestRelatedIssueNumbres.json"}.')
        return True
    else:
        print('No PullRequestRelatedIssueNumbres found or an error occurred during the download.')
        return False


def get_PullRequestRelatedIssueNumbres_in_json_file(repo_owner,repo_name, access_tokens, file_path_base):
    thread = Thread(target = get_PullRequestRelatedIssueNumbres_in_json_file_threaded_function, args = (repo_owner,repo_name, access_tokens, file_path_base, ))
    thread.start()
    return True