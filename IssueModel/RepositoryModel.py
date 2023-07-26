class RepositoryModel:
    def __init__(self, dict_issues = None, dict_pulls = None):
        self.dict_issues = dict_issues
        self.dict_pulls = dict_pulls

    def set_attribute(self, attribute, value):
        if hasattr(self, attribute):
            setattr(self, attribute, value)
        else:
            raise AttributeError(f"Issue object has no attribute '{attribute}'.")
