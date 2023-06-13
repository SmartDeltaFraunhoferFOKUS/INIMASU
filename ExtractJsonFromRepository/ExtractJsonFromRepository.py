import json
import gitlab

# Create a GitLab API object
api = gitlab.Gitlab('https://gitlab.com', private_token='YOUR_PRIVATE_TOKEN')

# Retrieve a project by its ID or path
project = api.projects.get('your_project_id')

# Get all issues from the project
issues = project.issues.list()

# Create a list to store the issues
issue_list = []

# Iterate over the issues and store relevant information in the list
for issue in issues:
    issue_info = {
        'id': issue.id,
        'title': issue.title,
        'description': issue.description,
        'status': issue.state,
    }
    issue_list.append(issue_info)

# Write the issue list to a JSON file
with open('issues.json', 'w') as file:
    json.dump(issue_list, file)

print("Issues have been stored in issues.json.")