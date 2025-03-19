from GitHubAdapter.ExtractFromRepositoryAsJson import get_from_repository_in_json_file
from GitHubAdapter.ExtractFromRepositoryAsJson import get_per_issue_from_repository_in_json_file
from GitHubAdapter.ExtractFromRepositoryAsJson import get_commit_details_from_repository_in_json_file
from GitHubAdapter.ExtractPullRequestRelatedIssueNumbresFromRepositoryAsJson import get_PullRequestRelatedIssueNumbres_in_json_file
from GitHubAdapter.ExtractPullRequestContributingUserInfosFromRepositoryAsJson import get_PullRequest_ContributingUserInfos_in_json_file
from GitHubAdapter.PopulateModelDatabase import PopulateRepositoryModelDatabase
from GitHubAdapter.PopulateModelDatabase import readJson

def ReadFromGitHubAndStoreInJson(repo_owner,repo_name,access_token,file_path_base):
    #get_from_repository_in_json_file(repo_owner,repo_name,'issues',access_token,file_path_base,'issues')
    ListOfDicOfIssues = readJson(file_path_base+"_issues.json")

    get_per_issue_from_repository_in_json_file(repo_owner,repo_name,'comments',access_token,file_path_base,'comments', ListOfDicOfIssues)
    get_per_issue_from_repository_in_json_file(repo_owner,repo_name,'events',access_token,file_path_base,'events', ListOfDicOfIssues)
    #get_from_repository_in_json_file(repo_owner,repo_name,'commits',access_token,file_path_base,'commits')
    #ListDictOfCommits=readJson(file_path_base+"_commits.json")
    #get_commit_details_from_repository_in_json_file(repo_owner,repo_name,access_token,file_path_base, ListDictOfCommits)

    #get_PullRequestRelatedIssueNumbres_in_json_file(repo_owner, repo_name, access_token, file_path_base)
    #get_PullRequest_ContributingUserInfos_in_json_file(repo_owner, repo_name, access_token, file_path_base)


def PopulateModelDatabaseFromJson(file_path_base):
    return PopulateRepositoryModelDatabase(file_path_base)