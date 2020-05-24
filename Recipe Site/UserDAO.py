import sqlite3
import datetime
import hashlib
from User import User

class UserDAO:

    def __init__(self):
        print("Setting up DAO")
    
    def hash_password(self, password):
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    def check_user_exists(self, username):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tbl_account  \
                        WHERE USERNAME = ?", (username, ))
        rows = cursor.fetchall()
        connection.close()

        if len(rows) > 0:
            return True
        else:
            return False

    def signup_user(self, username, password):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        if self.check_user_exists(username):
            return False

        hashedPass = self.hash_password(password)
        cursor.execute("INSERT INTO tbl_account (USERNAME, PASSWORD, SIGNUP_DATE, LAST_SIGNIN) \
                        VALUES (?, ?, ?, ?)", (username, hashedPass, datetime.datetime.now(), datetime.datetime.now()))
        connection.commit()
        connection.close()
        return True

    def update_user_last_login(self, cursor, username):
        cursor.execute("UPDATE tbl_account \
                        SET LAST_SIGNIN = ? \
                        WHERE USERNAME = ?", (datetime.datetime.now(), username))

    def login_user(self, username, password):
        connection = sqlite3.connect('recipe.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        hashedPass = self.hash_password(password)
        cursor.execute("SELECT * FROM tbl_account \
                        WHERE USERNAME = ? AND PASSWORD = ?", (username, hashedPass))

        rows = cursor.fetchall()
        if len(rows) > 0:
            self.update_user_last_login(cursor, username)
            connection.commit()
            connection.close()
            return User(str(rows[0]['USERNAME']))
        else:
            return None