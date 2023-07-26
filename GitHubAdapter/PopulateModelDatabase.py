import json
from IssueModel.IssueModel import IssueModel
from IssueModel.CommentModel import CommentModel
from IssueModel.PullModel import PullModel
from IssueModel.RepositoryModel import RepositoryModel
from GitHubAdapter.GraphQLGitHub import GetAllRelatedIssues

def PopulateRepositoryModelDatabase(base_path):
    ListOfDicOfIssues = readJson(base_path+"_issues.json")
    ListOfDicOfComments = readJson(base_path+"_comments.json")
    ListOfDicOfCommits = readJson(base_path+"_commits.json")
    ListOfDicOfEvents = readJson(base_path+"_events.json")
    DictRelatedIssues = readJson(base_path+"_PullRequestRelatedIssueNumbres.json")
    Dict_PullRequestNumber_ContributingUserLoginNames = readJson(base_path+"_PullRequestNumber_ContributingUserLoginNames.json")
    return createAllIssuesAndPulls(ListOfDicOfIssues, ListOfDicOfComments, ListOfDicOfCommits, ListOfDicOfEvents, DictRelatedIssues, Dict_PullRequestNumber_ContributingUserLoginNames)

def createAllIssuesAndPulls(ListOfDicOfIssues, ListOfDicOfComments, ListOfDicOfCommits, ListOfDicOfEvents, DictRelatedIssues, Dict_PullRequestNumber_ContributingUserLoginNames):
    keys = list(ListOfDicOfIssues[0].keys())
    dictAllIssues = dict()
    dictAllPulls=dict()
    Keys = ["id", "number", "user", "body", "created_at", "labels", "updated_at", "closed_at", "reactions","state", "reactions"]
    for dicOfIssue in ListOfDicOfIssues:
        if not "pull_request" in dicOfIssue:
            newIssue = IssueModel(**{ key : dicOfIssue[key] for key in Keys})
            for dicOfComments in ListOfDicOfComments:
                if ( dicOfComments["issue_url"] == dicOfIssue["url"]):
                    if newIssue.comments_list == None:
                        newIssue.comments_list = []
                    newIssue.comments_list.append(createComment(dicOfComments))
            dictAllIssues[int(newIssue.number)] = newIssue
        else:
            newPull = PullModel(**{ key : dicOfIssue[key] for key in Keys})
            for dicOfComments in ListOfDicOfComments:
                if ( dicOfComments["issue_url"] == dicOfIssue["url"]):
                    if newPull.comments_list == None:
                        newPull.comments_list = []
                    newPull.comments_list.append(createComment(dicOfComments))
            dictAllPulls[int(newPull.number)] = newPull


    if DictRelatedIssues:
        for keyPullNumber in DictRelatedIssues.keys():
            if int(keyPullNumber) in dictAllPulls:
                dictAllPulls[int(keyPullNumber)].related_issues = DictRelatedIssues[keyPullNumber]
                for related_issue_number in DictRelatedIssues[keyPullNumber]:
                    if related_issue_number in dictAllIssues:
                        if dictAllIssues[int(related_issue_number)].solutions == None:
                            dictAllIssues[int(related_issue_number)].solutions = []
                        dictAllIssues[int(related_issue_number)].solutions.append(int(keyPullNumber))

    if Dict_PullRequestNumber_ContributingUserLoginNames:
        for keyPullNumber in Dict_PullRequestNumber_ContributingUserLoginNames.keys():
            if int(keyPullNumber) in dictAllPulls:
                dictAllPulls[int(keyPullNumber)].contributing_user_logins = Dict_PullRequestNumber_ContributingUserLoginNames[keyPullNumber]
                if dictAllPulls[int(keyPullNumber)].related_issues:
                    for related_issue_number in dictAllPulls[int(keyPullNumber)].related_issues:
                        if related_issue_number in dictAllIssues:
                            if dictAllIssues[int(related_issue_number)].solution_contributing_user_logins == None:
                                dictAllIssues[int(related_issue_number)].solution_contributing_user_logins = []
                            for contributing_user_name in Dict_PullRequestNumber_ContributingUserLoginNames[keyPullNumber]:
                                if not contributing_user_name in dictAllIssues[int(related_issue_number)].solution_contributing_user_logins:
                                    dictAllIssues[int(related_issue_number)].solution_contributing_user_logins.append(contributing_user_name)


    return RepositoryModel( dictAllIssues, dictAllPulls )

def createComment(dicOfComments):
    Keys = ["user", "body", "created_at"]
    return CommentModel(**{ key : dicOfComments[key] for key in Keys})

def readJson(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data