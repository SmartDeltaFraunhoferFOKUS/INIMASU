class IssueClass:
    def __init__(self, body=None, created_at= None, labels=None, updated_at=None, closed_at=None, reactions=None, comments = None, state = None):
        self.body = body
        self.labels = labels
        self.created_at = created_at
        self.updated_at = updated_at
        self.closed_at = closed_at
        self.reactions = reactions
        self.comments = comments
        self.state = state


    def set_attribute(self, attribute, value):
        if hasattr(self, attribute):
            setattr(self, attribute, value)
        else:
            raise AttributeError(f"Issue object has no attribute '{attribute}'.")


