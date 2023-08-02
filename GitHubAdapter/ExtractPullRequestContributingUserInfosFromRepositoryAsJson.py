from GitHubAdapter.GraphQLGitHub import GetContributingUserInfosForPullRequests
import json
from IssueModel.ContributingUserInfo import ContributingUserInfo


def get_PullRequest_ContributingUserInfos_in_json_file(repo_owner,repo_name, access_token, file_path_base):

    Dict_PullRequestNumber_ContributingUserInfos = GetContributingUserInfosForPullRequests(repo_owner, repo_name, access_token)
    if Dict_PullRequestNumber_ContributingUserInfos:
        # Store the issues in a JSON file
        with open(file_path_base+"_PullRequestNumber_ContributingUserInfos.json", 'w') as file:
            json.dump(Dict_PullRequestNumber_ContributingUserInfos, file, indent=4)

        print(f'All PullRequestContributingUserInfos have been downloaded and stored in {file_path_base+"_PullRequestNumber_ContributingUserInfos.json"}.')
        return True
    else:
        print('No PullRequestContributingUserInfos found or an error occurred during the download.')
        return False
