from issueInspection.ExtractJsonFromRepository.ExtractJsonFromRepository import get_issues_in_json
from issueInspection.JsonToIssue.JsonToIssue import jsonToIssue
from issueInspection.VisualizeIssues.VisualizeIssues import visualize
from insightsInspection.ExtractInsightsFromRepository.WriteInsightsToJson import get_matrix_in_json


get_matrix_in_json('vaadin', 'flow',"code-frequency")

#repo_owner = "vercel"
#repo_name = "next.js"
#get_issues_in_json("vercel","next.js")
#issues = jsonToIssue(f"C:/Users/joh11155/PycharmProjects/issue-intelligence/Main/next.js_issues_{repo_owner}.json")
#visualize(issues)
