class PullModel:
    def __init__(self, id=None, number=None, user =None, body=None, created_at= None, labels=None, updated_at=None, closed_at=None, comments_list = None, state = None, reactions = None, commits = None, related_issues = None, contributing_user_logins = None):
        self.id = id
        self.number = number
        self.user = user
        self.body = body
        self.labels = labels
        self.created_at = created_at
        self.updated_at = updated_at
        self.closed_at = closed_at
        self.reactions = reactions
        self.comments_list = comments_list
        self.state = state
        self.commits=commits
        self.related_issues = related_issues
        self.contributing_user_logins = contributing_user_logins

    def set_attribute(self, attribute, value):
        if hasattr(self, attribute):
            setattr(self, attribute, value)
        else:
            raise AttributeError(f"Issue object has no attribute '{attribute}'.")
