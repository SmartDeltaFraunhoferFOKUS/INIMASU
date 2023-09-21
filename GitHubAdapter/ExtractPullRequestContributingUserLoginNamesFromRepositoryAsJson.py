from GitHubAdapter.GraphQLGitHub import GetContributingUserLoginNamesForPullRequests
import json

def get_PullRequest_ContributingUserLoginNames_in_json_file(repo_owner,repo_name, access_token, file_path_base):

    Dict_PullRequestNumber_ContributingUserLoginNames = GetContributingUserLoginNamesForPullRequests(repo_owner, repo_name, access_token)
    if Dict_PullRequestNumber_ContributingUserLoginNames:
        # Store the issues in a JSON file
        with open(file_path_base+"_PullRequestNumber_ContributingUserLoginNames.json", 'w') as file:
            json.dump(Dict_PullRequestNumber_ContributingUserLoginNames, file, indent=4)

        print(f'All PullRequestContributingUserLoginNames have been downloaded and stored in {file_path_base+"_PullRequestNumber_ContributingUserLoginNames.json"}.')
        return True
    else:
        print('No PullRequestContributingUserLoginNames found or an error occurred during the download.')
        return False
