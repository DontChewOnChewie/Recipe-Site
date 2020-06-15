import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from string import ascii_letters
import random
from UserDAO import UserDAO

class EmailHandler():

    SETTINGS_CODE_LENGTH = 6
    PASSWORD_RESET_LENGTH = 10

    def __init__(self, to_email):
        self.server_address = "smtp.gmail.com"
        self.server_port  = 465
        self.email = "EMAIL"
        self.password = "PASSWORD"
        self.to_email = to_email

    '''
    Logs into email server and sends the given message.
    '''
    def login_to_server(self, message):
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.server_address, self.server_port, context=context) as server:
                server.login(self.email, self.password)
                server.sendmail(self.email, self.to_email, message)
            
            return True
        except:
            return False

    '''
    Creates email to allow user to access their settings page.
    '''
    def send_settings_code(self):
        message = MIMEMultipart("alternative")
        message['Subject'] = "Account Settings Code"
        message['From'] = self.email
        message['To'] = self.to_email
        code = self.generateCode(self.SETTINGS_CODE_LENGTH)
        html = f"""
            <html>
                <body>
                    <h1>Account Settings Code Requested</h1>
                    <h3>Code : {code}</h3>
                </body>
            </html>
        """
        mime_message = MIMEText(html, "html")
        message.attach(mime_message)
        
        if self.login_to_server(message.as_string()):
            return code
        return None
    
    '''
    Creates email for user to reset their password.
    '''
    def send_reset_link(self):
        message = MIMEMultipart("alternative")
        message['Subject'] = "Password Reset Request"
        message['From'] = self.email
        message['To'] = self.to_email
        code = self.generateCode(self.PASSWORD_RESET_LENGTH)
        html = f"""
            <html>
                <body>
                    <h1>Password Reset Requested</h1>
                    <p>A request to change the password for your account has been made.<br/>
                    If this wasn't you think about changing you password or email to stay secure.</p>
                    <br/>
                    <a href='/passwordreset?code={code}'>Password Reset Link</a>
                </body>
            </html>
        """
        mime_message = MIMEText(html, "html")
        message.attach(mime_message)
        
        if self.login_to_server(message.as_string()):
            return code
        return None
    
    '''
    Generates a random code with a specified length.
    '''
    def generateCode(self, length):
        ret_code = ""
        for i in range(length):
            ret_code += ascii_letters[random.randint(0, len(ascii_letters) - 1)]
        return ret_code