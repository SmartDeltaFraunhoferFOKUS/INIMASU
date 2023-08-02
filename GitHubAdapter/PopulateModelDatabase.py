import json
import os.path
from IssueModel.IssueModel import IssueModel
from IssueModel.CommentModel import CommentModel
from IssueModel.PullModel import PullModel
from IssueModel.RepositoryModel import RepositoryModel
from IssueModel.ContributingUserInfo import ContributingUserInfo
from GitHubAdapter.GraphQLGitHub import GetAllRelatedIssues

def PopulateRepositoryModelDatabase(base_path):
    ListOfDicOfIssues = readJson(base_path+"_issues.json")   
    ListOfDicOfComments = readJson(base_path+"_comments.json") if os.path.exists(base_path+"_comments.json") else None
    ListOfDicOfCommits = readJson(base_path+"_commits.json") if os.path.exists(base_path+"_commits.json") else None
    ListOfDicOfEvents = readJson(base_path+"_events.json") if os.path.exists(base_path+"_events.json") else None
    DictRelatedIssues = readJson(base_path+"_PullRequestRelatedIssueNumbres.json") if os.path.exists(base_path+"_PullRequestRelatedIssueNumbres.json") else None
    Dict_PullRequestNumber_ContributingUserInfos = readJson(base_path+"_PullRequestNumber_ContributingUserInfos.json") if os.path.exists(base_path+"_PullRequestNumber_ContributingUserInfos.json") else None
    if Dict_PullRequestNumber_ContributingUserInfos:
        for keyPullNumber in Dict_PullRequestNumber_ContributingUserInfos.keys():
            for index in range(len(Dict_PullRequestNumber_ContributingUserInfos[keyPullNumber])):
                Dict_PullRequestNumber_ContributingUserInfos[keyPullNumber][index] = ContributingUserInfo(login=Dict_PullRequestNumber_ContributingUserInfos[keyPullNumber][index]['login'], start_working_on_it=Dict_PullRequestNumber_ContributingUserInfos[keyPullNumber][index]['start_working_on_it'])

    return createAllIssuesAndPulls(ListOfDicOfIssues, ListOfDicOfComments, ListOfDicOfCommits, ListOfDicOfEvents, DictRelatedIssues, Dict_PullRequestNumber_ContributingUserInfos)

def createAllIssuesAndPulls(ListOfDicOfIssues, ListOfDicOfComments, ListOfDicOfCommits, ListOfDicOfEvents, DictRelatedIssues, Dict_PullRequestNumber_ContributingUserInfos):
    keys = list(ListOfDicOfIssues[0].keys())
    dictAllIssues = dict()
    dictAllPulls=dict()
    Keys = ["id", "number", "user", "body", "created_at", "labels", "updated_at", "closed_at", "reactions","state", "reactions"]
    for dicOfIssue in ListOfDicOfIssues:
        if not "pull_request" in dicOfIssue:
            newIssue = IssueModel(**{ key : dicOfIssue[key] for key in Keys})
            if ListOfDicOfComments:
                for dicOfComments in ListOfDicOfComments:
                    if ( dicOfComments["issue_url"] == dicOfIssue["url"]):
                        if newIssue.comments_list == None:
                            newIssue.comments_list = []
                        newIssue.comments_list.append(createComment(dicOfComments))
            dictAllIssues[int(newIssue.number)] = newIssue
        else:
            newPull = PullModel(**{ key : dicOfIssue[key] for key in Keys})
            if ListOfDicOfComments:
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

    if Dict_PullRequestNumber_ContributingUserInfos:
        for keyPullNumber in Dict_PullRequestNumber_ContributingUserInfos.keys():
            if int(keyPullNumber) in dictAllPulls:
                dictAllPulls[int(keyPullNumber)].contributing_user_infos = Dict_PullRequestNumber_ContributingUserInfos[keyPullNumber]
                if dictAllPulls[int(keyPullNumber)].related_issues:
                    for related_issue_number in dictAllPulls[int(keyPullNumber)].related_issues:
                        if related_issue_number in dictAllIssues:
                            if dictAllIssues[int(related_issue_number)].solution_contributing_user_infos == None:
                                dictAllIssues[int(related_issue_number)].solution_contributing_user_infos = []
                            for contributing_user_info in Dict_PullRequestNumber_ContributingUserInfos[keyPullNumber]:
                                if not contributing_user_info in dictAllIssues[int(related_issue_number)].solution_contributing_user_infos:
                                    dictAllIssues[int(related_issue_number)].solution_contributing_user_infos.append(contributing_user_info)


    return RepositoryModel( dictAllIssues, dictAllPulls )

def createComment(dicOfComments):
    Keys = ["user", "body", "created_at"]
    return CommentModel(**{ key : dicOfComments[key] for key in Keys})

def readJson(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data