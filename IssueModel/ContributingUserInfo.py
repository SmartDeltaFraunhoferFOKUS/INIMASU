class ContributingUserInfo(dict):
    def __init__(self, login = None, start_working_on_it=None):
        dict.__init__(self, login=login, start_working_on_it=start_working_on_it)

    def __repr__(self):
        return f"User with login: {self['login']} started contributing: {self['start_working_on_it']}"

    def __eq__(self, other):
        if isinstance(other, ContributingUserInfo):
            return (self['login']  == other['login']) and ( self['start_working_on_it'] == other['start_working_on_it'])
        else:
            return self['login'] == other

    def __hash__(self):
        return hash(self['login'])