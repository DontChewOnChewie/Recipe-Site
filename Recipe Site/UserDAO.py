import sqlite3
import datetime
import hashlib
from User import User
import random
from string import ascii_letters, punctuation

class UserDAO:

    def __init__(self):
        print("Setting up User DAO")
    
    '''
    Return SHA512 digest of password.
    '''
    def hash_password(self, password):
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    '''
    Check if the given username is all ready taken.
    '''
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

    '''
    Try sign up a user with given credentials.
    '''
    def signup_user(self, username, password):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        if self.check_user_exists(username):
            return None

        hashedPass = self.hash_password(password)

        cursor.execute("INSERT INTO tbl_account (USERNAME, PASSWORD, SIGNUP_DATE, LAST_SIGNIN) \
                        VALUES (?, ?, ?, ?)", (username, hashedPass, datetime.datetime.now(), datetime.datetime.now()))
        
        session_key = self.update_user_session_key(self.get_user_id_from_name(cursor, username), cursor)

        connection.commit()
        connection.close()
        return User(username, session_key)

    '''
    Update users last sign in after successful login.
    '''
    def update_user_last_login(self, cursor, username):
        cursor.execute("UPDATE tbl_account \
                        SET LAST_SIGNIN = ? \
                        WHERE USERNAME = ?", (datetime.datetime.now(), username))

    '''
    Update a users session key when user signs up and logs in.
    '''
    def update_user_session_key(self, id, cursor):
        chars = ascii_letters + punctuation
        session_key = ""

        for i in range(100):
            session_key += chars[random.randint(0, len(chars)-1)]

        cursor.execute("UPDATE tbl_account \
                        SET CURRENT_SESSION_KEY = ? \
                        WHERE ID = ?", (session_key, id))
        return session_key

    '''
    Try and log a user in with given credentials.
    Update last sign in date and session key.
    '''
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
            new_key = self.update_user_session_key(rows[0]['ID'], cursor)
            connection.commit()
            connection.close()
            return User(str(rows[0]['USERNAME']), new_key)
        else:
            connection.close()
            return None

    '''
    Check a users session key against their username.
    '''
    def check_user_session_key(self, user, key):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        cursor.execute("SELECT CURRENT_SESSION_KEY \
                        FROM tbl_account \
                        WHERE USERNAME = ?", (user,))
        rows = cursor.fetchall()
        connection.close()
        
        if (len(rows) > 0):
            if rows[0][0] == key:
                return True
            else : return False
        else:
             return False

    '''
    Return user ID from username.
    '''
    def get_user_id_from_name(self, cursor, user):
        cursor.execute("SELECT ID FROM tbl_account \
                        WHERE USERNAME = ?", (user,))
        rows = cursor.fetchall()
        return rows[0][0]