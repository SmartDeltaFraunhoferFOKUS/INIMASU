import re
import time
from urllib import request
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError

def GetAllRelatedIssues(repo_owner, repo_name, access_token):

    _headers= {'Authorization': 'bearer ' + access_token}
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers=_headers)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport)

    DictRelatedIssues=dict()

    AtOnce=50
    endCursor="null"
    HasMorePages = True

    while HasMorePages:

        query = gql(
            """
            query
            {
                repository(owner:\"""" + repo_owner + "\", name:\"" + repo_name +"""\")
                {
                    pullRequests(first:""" + str(AtOnce) + """, after:""" + endCursor + """)
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
        )

        response = ExecuteGQLQuery(client,query)

        for PullEdge in response['repository']['pullRequests']['edges']:
            for edge in PullEdge['node']['closingIssuesReferences']['edges']:
                if not int(PullEdge['node']['number']) in DictRelatedIssues:
                    DictRelatedIssues[int(PullEdge['node']['number'])]=[]
                DictRelatedIssues[int(PullEdge['node']['number'])].append(int(edge['node']['number']))
        HasMorePages = response['repository']['pullRequests']['pageInfo']['hasNextPage']
        endCursor = "\""+response['repository']['pullRequests']['pageInfo']['endCursor']+"\""

        
    return DictRelatedIssues

def GetContributingUserLoginNamesForPullRequests(repo_owner, repo_name, access_token):

    _headers= {'Authorization': 'bearer ' + access_token}
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers=_headers)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport)

    Dict_PullRequestNumber_ContributingUserLoginNames=dict()
    
    AtOnce=50
    endCursor="null"
    HasMorePages = True

    while HasMorePages:

        query = gql(
            """
            query
            {
                repository(owner:\"""" + repo_owner + "\", name:\"" + repo_name +"""\")
                {
                    pullRequests(first:""" + str(AtOnce) + """, after:""" + endCursor + """)
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
                                        }
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
        )

        response = ExecuteGQLQuery(client,query)

        for PullEdge in response['repository']['pullRequests']['edges']:
            if not int(PullEdge['node']['number']) in Dict_PullRequestNumber_ContributingUserLoginNames:
                Dict_PullRequestNumber_ContributingUserLoginNames[int(PullEdge['node']['number'])]=[]
            if PullEdge['node']['author'] and PullEdge['node']['author']['login']:
                Dict_PullRequestNumber_ContributingUserLoginNames[int(PullEdge['node']['number'])].append(PullEdge['node']['author']['login'])
            for CommitEdge in PullEdge['node']['commits']['edges']:
                for AuthorEdge in CommitEdge['node']['commit']['authors']['edges']:
                    if AuthorEdge['node']['user'] and AuthorEdge['node']['user']['login']:
                        if not AuthorEdge['node']['user']['login'] in Dict_PullRequestNumber_ContributingUserLoginNames[int(PullEdge['node']['number'])]:
                            Dict_PullRequestNumber_ContributingUserLoginNames[int(PullEdge['node']['number'])].append(AuthorEdge['node']['user']['login'])
                if CommitEdge['node']['commit']['committer']['user'] and CommitEdge['node']['commit']['committer']['user']['login']:
                    if not CommitEdge['node']['commit']['committer']['user']['login'] in Dict_PullRequestNumber_ContributingUserLoginNames[int(PullEdge['node']['number'])]:
                        Dict_PullRequestNumber_ContributingUserLoginNames[int(PullEdge['node']['number'])].append(CommitEdge['node']['commit']['committer']['user']['login'])
        HasMorePages = response['repository']['pullRequests']['pageInfo']['hasNextPage']
        endCursor = "\""+response['repository']['pullRequests']['pageInfo']['endCursor']+"\""

        
    return Dict_PullRequestNumber_ContributingUserLoginNames


def ExecuteGQLQuery(client, query):
    reuqest_needed = True
    response = None
    while reuqest_needed:
        # Execute the query on the transport
        try:
            response = client.execute(query)
            reuqest_needed = False
        except TransportQueryError as err:
            if err.errors[0]['type']=='RATE_LIMITED':
                print(f"RATE_LIMIT exceeded - waiting for 5 minutes")
                time.sleep(300)
            else:
                print(f"Unexpected {err=}, {type(err)=}")
                raise
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
    return response
