import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from string import ascii_letters
import random
from UserDAO import UserDAO

'''
No comments for this class yet as I may re-write a lot of it in the near future.
'''

class EmailHandler():

    def __init__(self, to_email):
        self.server_address = "smtp.gmail.com"
        self.server_port  = 465
        self.email = "EMAIL"
        self.password = "PASSWORD"
        self.to_email = to_email

    def login_to_server(self, message):
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.server_address, self.server_port, context=context) as server:
                server.login(self.email, self.password)
                server.sendmail(self.email, self.to_email, message)
            
            return True
        except:
            return False

    def send_mail(self):
        message = MIMEMultipart("alternative")
        message['Subject'] = "Account Settings Code"
        message['From'] = self.email
        message['To'] = self.to_email
        code = self.generateCode()
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
    
    def generateCode(self):
        ret_code = ""
        for i in range(6):
            ret_code += ascii_letters[random.randint(0, len(ascii_letters) - 1)]
        return ret_code