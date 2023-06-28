from ExtractJsonFromRepository.ExtractJsonFromRepository import get_issues_in_json
from JsonToIssue.JsonToIssue import jsonToIssue
from VisualizeIssues.VisualizeIssues import visualize



get_issues_in_json('vaadin', 'flow')
issues = jsonToIssue("C:/Users/joh11155/PycharmProjects/issue-intelligence/Main/next.js_issues.json")
visualize(issues)
