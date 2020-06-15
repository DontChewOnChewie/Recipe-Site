'''
Class used as a model for user.
Created when user signs in and used for custom header and CRUD request validation.
'''
class User:

    def __init__(self, id, username, sessionKey, email_auth, email, can_edit_settings, background_path):
        self.id = id
        self.username = username
        self.sessionKey = sessionKey
        self.email_auth = email_auth
        self.email = email
        self.can_edit_settings = can_edit_settings
        self.background_path = background_path
    
    def __repr__(self):
        return f"Username : {self.username}\nCurrent Session Key {self.sessionKey}"