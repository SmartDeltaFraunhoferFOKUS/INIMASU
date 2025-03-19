import re
import time
from urllib import request
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError
from IssueModel.ContributingUserInfo import ContributingUserInfo

def GetAllRelatedIssues(repo_owner, repo_name, access_tokens):

    DictRelatedIssues=dict()

    AtOnce=50
    query_before_cursor = """
            query
            {
                repository(owner:\"""" + repo_owner + "\", name:\"" + repo_name +"""\")
                {
                    pullRequests(first:""" + str(AtOnce) + """, after:"""

    query_after_cursor = """)
                    {
                        edges
                        {
                            node
                            {
                                number
                                closingIssuesReferences (first: 50)
                                {
                                  edges
                                  {
                                    node
                                    {
                                      number
                                    }
                                  }
                                }
                            }
                        }
                        pageInfo
                        {
                            hasNextPage
                            endCursor
                        }
                    }
                }
            }
        """

    results = ExecuteGQLQuery(access_tokens,query_before_cursor, query_after_cursor)

    for response in results:
        for PullEdge in response['repository']['pullRequests']['edges']:
            for edge in PullEdge['node']['closingIssuesReferences']['edges']:
                if not int(PullEdge['node']['number']) in DictRelatedIssues:
                    DictRelatedIssues[int(PullEdge['node']['number'])]=[]
                DictRelatedIssues[int(PullEdge['node']['number'])].append(int(edge['node']['number']))
        
    return DictRelatedIssues

def GetContributingUserInfosForPullRequests(repo_owner, repo_name, access_tokens):
    Dict_PullRequestNumber_ContributingUserInfos=dict()
    
    AtOnce=50

    query_before_cursor = """
            query
            {
                repository(owner:\"""" + repo_owner + "\", name:\"" + repo_name +"""\")
                {
                    pullRequests(first:""" + str(AtOnce) + """, after:"""

    query_after_cursor = """)
                        {
                        edges
                        {
                            node
                            {
                                number
                                author
                                {
                                    login
                                }
                                commits (first:50)
                                {
                                  edges
                                  {
                                    node
                                    {
                                        commit
                                        {
                                            authors (first:50)
                                            {
                                              edges
                                              {
                                                node
                                                {
                                                    user
                                                    {
                                                        login
                                                    }
                                                }
                                              }
                                            }
                                            committer
                                            {
                                                user
                                                {
                                                    login
                                                }
                                            }
                                            authoredDate
                                            committedDate
                                        }
                                    }
                                  }
                                }
                                createdAt
                            }
                        }
                        pageInfo
                        {
                            hasNextPage
                            endCursor
                        }
                    }
                }
            }
        """
        

    results = ExecuteGQLQuery(access_tokens,query_before_cursor, query_after_cursor)


    for response in results:
       for PullEdge in response['repository']['pullRequests']['edges']:
            if not int(PullEdge['node']['number']) in Dict_PullRequestNumber_ContributingUserInfos:
                Dict_PullRequestNumber_ContributingUserInfos[int(PullEdge['node']['number'])]=[]
            if PullEdge['node']['author'] and PullEdge['node']['author']['login']:
                Dict_PullRequestNumber_ContributingUserInfos[int(PullEdge['node']['number'])].append(ContributingUserInfo(PullEdge['node']['author']['login'], PullEdge['node']['createdAt']))
            for CommitEdge in PullEdge['node']['commits']['edges']:
                for AuthorEdge in CommitEdge['node']['commit']['authors']['edges']:
                    if AuthorEdge['node']['user'] and AuthorEdge['node']['user']['login']:
                        if not AuthorEdge['node']['user']['login'] in Dict_PullRequestNumber_ContributingUserInfos[int(PullEdge['node']['number'])]:
                            Dict_PullRequestNumber_ContributingUserInfos[int(PullEdge['node']['number'])].append(ContributingUserInfo(AuthorEdge['node']['user']['login'], CommitEdge['node']['commit']['authoredDate'] if CommitEdge['node']['commit']['authoredDate'] else PullEdge['node']['createdAt']))
                if CommitEdge['node']['commit']['committer']['user'] and CommitEdge['node']['commit']['committer']['user']['login']:
                    if not CommitEdge['node']['commit']['committer']['user']['login'] in Dict_PullRequestNumber_ContributingUserInfos[int(PullEdge['node']['number'])]:
                        Dict_PullRequestNumber_ContributingUserInfos[int(PullEdge['node']['number'])].append(ContributingUserInfo(CommitEdge['node']['commit']['committer']['user']['login'], CommitEdge['node']['commit']['committedDate'] if CommitEdge['node']['commit']['committedDate'] else PullEdge['node']['createdAt']))

        
    return Dict_PullRequestNumber_ContributingUserInfos


def ExecuteGQLQuery(access_tokens, query_before_cursor, query_after_cursor):
    clients=[]
    for access_token in access_tokens:
        _headers= {'Authorization': 'bearer ' + access_token}
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers=_headers)

        # Create a GraphQL client using the defined transport
        client = Client(transport=transport)
        clients.append(client)

    endCursor="null"
    HasMorePages = True

    results = []
    iIndexAccessToken=0
    RateLimitsReached = 0

    while HasMorePages:
        # Execute the query on the transport
        try:
            query = gql( query_before_cursor + endCursor + query_after_cursor)
            response = clients[iIndexAccessToken].execute(query)
            iIndexAccessToken += 1
            if iIndexAccessToken >= len(access_tokens):
                iIndexAccessToken=0

            HasMorePages = response['repository']['pullRequests']['pageInfo']['hasNextPage']
            endCursor = "\""+response['repository']['pullRequests']['pageInfo']['endCursor']+"\""
            results.append(response)
            print("#")
            RateLimitsReached = 0
        except TransportQueryError as err:
            if err.errors[0]['type']=='RATE_LIMITED':
                RateLimitsReached += 1
                if RateLimitsReached >= len(access_tokens):
                    print(f"RATE_LIMIT exceeded - waiting for 5 minutes")
                    time.sleep(300)
                    RateLimitsReached = 0
                else:
                    iIndexAccessToken += 1
                    if iIndexAccessToken >= len(access_tokens):
                        iIndexAccessToken=0

            else:
                print(f"Unexpected {err=}, {type(err)=}")
                raise
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
    return results
