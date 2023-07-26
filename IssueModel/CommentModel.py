class CommentModel:
    def __init__(self, id=None, user=None, body=None, created_at= None):
        self.id = id
        self.user = user
        self.body = body
        self.created_at = created_at

    def set_attribute(self, attribute, value):
        if hasattr(self, attribute):
            setattr(self, attribute, value)
        else:
            raise AttributeError(f"Issue object has no attribute '{attribute}'.")

