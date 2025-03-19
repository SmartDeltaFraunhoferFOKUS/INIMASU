class IssueModel:
    def __init__(self, id=None, title=None, number=None, user =None, body=None, created_at= None, labels=None, updated_at=None, closed_at=None, comments_list = None, state = None, reactions = None, solutions=None, solution_contributing_user_infos = None):
        self.id = id
        self.title=title
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
        self.solutions = solutions
        self.solution_contributing_user_infos = solution_contributing_user_infos
        self.events=None

    def set_attribute(self, attribute, value):
        if hasattr(self, attribute):
            setattr(self, attribute, value)
        else:
            raise AttributeError(f"Issue object has no attribute '{attribute}'.")


