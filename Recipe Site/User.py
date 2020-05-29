'''
Class used as a model for user.
Created when user signs in and used for custom header and CRUD request validation.
'''
class User:

    def __init__(self, username, sessionKey):
        self.username = username
        self.sessionKey = sessionKey
    
    def __repr__(self):
        return f"Username : {self.username}\nCurrent Session Key {self.sessionKey}"