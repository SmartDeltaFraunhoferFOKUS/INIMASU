import os
from issueInspection.ExtractJsonFromRepository.ExtractJsonFromRepository import get_issues_in_json
from issueInspection.JsonToIssue.JsonToIssue import jsonToIssue
from issueInspection.VisualizeIssues.VisualizeIssues import visualize
from insightsInspection.ExtractInsightsFromRepository.WriteInsightsToJson import get_matrix_in_json

"""
possible other repository to test on
#repo_owner = "vercel"
#repo_name = "next._js"
"""


def main(repo_owner='vaadin', repo_name='flow', matrix=None, access_token='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'):
    matrix_json_file = f'next.js_{repo_owner}_{matrix}.json'
    if matrix:

        if not os.path.exists(matrix_json_file):
            get_matrix_in_json(repo_owner, repo_name, matrix, access_token)

    if matrix == "issues":
        issues = jsonToIssue(matrix_json_file)
        visualize(issues)


main(matrix = "issues")
