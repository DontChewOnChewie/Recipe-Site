'''
Class used for alerts throughout the website.
Alert type can currently be alert-suc, alert-fail and alert-info which map to relevant
CSS classes.
'''

class Alert:

    def __init__(self, alertTitle, alertBody, alertType):
        self.title = alertTitle
        self.body = alertBody
        self.type = alertType  
    
    def __repr__(self):
        return f"Title : {self.alertTitle}\nBody : {self.alertBody}\nType : {self.alertType}"