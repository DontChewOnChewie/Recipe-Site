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
        
        user_id = self.get_user_id_from_name(cursor, username)

        session_key = self.update_user_session_key(user_id, cursor)

        connection.commit()
        connection.close()
        return User(user_id, username, session_key, 0, None, 0, None)

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
            return User(rows[0]['ID'], rows[0]['USERNAME'], new_key, rows[0]['EMAIL_AUTH'], rows[0]['EMAIL'], rows[0]['CAN_EDIT_SETTINGS'], rows[0]['BACKGROUND_PATH'])
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

        if len(rows) > 0:
            return rows[0][0]
        else:
            return None
    
    '''
    Check users password matches and return result.
    '''
    def check_users_password_matches(self, user, password):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM tbl_account \
                        WHERE USERNAME = ? AND PASSWORD = ?", (user, self.hash_password(password)))
        rows = cursor.fetchall()
        if len(rows) > 0:
            return True
        else:
            return False
    
    '''
    Change the current password of the user. Checks are done to authenticate this prior
    to this function.
    '''
    def update_password(self, user, password):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()
        user_id = self.get_user_id_from_name(cursor, user)
        cursor.execute("UPDATE tbl_account \
                        SET PASSWORD = ? \
                        WHERE ID = ?", (self.hash_password(password), user_id))
        connection.commit()
        connection.close()
    
    '''
    Enable a user to be using email authentication.
    '''
    def enable_email_auth(self, user, email):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        user_id = self.get_user_id_from_name(cursor, user)
        
        cursor.execute("UPDATE tbl_account \
                        SET EMAIL_AUTH = 1, EMAIL = ? \
                        WHERE ID = ?", (email, user_id))

        connection.commit()
        connection.close()
    
    '''
    Return all details about a user.
    '''
    def get_user(self, user):
        connection = sqlite3.connect('recipe.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        user_id = self.get_user_id_from_name(cursor, user)

        cursor.execute("SELECT * FROM tbl_account \
                        WHERE ID = ?", (user_id,))
        
        rows = cursor.fetchall()
        if len(rows) > 0:
            return User(rows[0]['ID'], rows[0]['USERNAME'], rows[0]['CURRENT_SESSION_KEY'], rows[0]['EMAIL_AUTH'], 
                        rows[0]['EMAIL'], rows[0]['CAN_EDIT_SETTINGS'], rows[0]['BACKGROUND_PATH'])
        return None
    
    '''
    Set a users code so that they can access and modufy their account if they are
    using email authentication.
    '''
    def set_user_settings_code(self, user_id, code):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        cursor.execute("UPDATE tbl_account \
                        SET SETTINGS_CODE = ? \
                        WHERE ID = ?", (code, user_id))
        connection.commit()
        connection.close()
    
    '''
    Get a users code to see if they can access and modify their account.
    '''
    def get_user_settings_code(self, user):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        user_id = self.get_user_id_from_name(cursor, user)

        cursor.execute("SELECT SETTINGS_CODE \
                        FROM tbl_account \
                        WHERE ID = ?", (user_id,))
        rows = cursor.fetchall()
        if len(rows) > 0:
            return rows[0][0]
        return None

    '''
    Allow a user to edit their settings after a correct code has been given.
    '''
    def allow_edit_settings(self, user):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        user_id = self.get_user_id_from_name(cursor, user)

        cursor.execute("UPDATE tbl_account \
                        SET CAN_EDIT_SETTINGS = 1 \
                        WHERE ID = ?", (user_id,))
        connection.commit()
        connection.close()

    '''
    Change a users email.
    '''
    def change_email(self, user, email):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        user_id = self.get_user_id_from_name(cursor, user)

        cursor.execute("UPDATE tbl_account \
                        SET EMAIL = ?  \
                        WHERE ID = ?", (email, user_id))
        connection.commit()
        connection.close()

    '''
    Update a users background image.
    '''
    def update_user_background(self, user, path):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        user_id = self.get_user_id_from_name(cursor, user)

        cursor.execute("UPDATE tbl_account \
                        SET BACKGROUND_PATH = ? \
                        WHERE ID = ?", (path, user_id))
        connection.commit()
        connection.close()
    
    '''
    Get URL of users account page background.
    '''
    def get_user_background(self, user):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        user_id = self.get_user_id_from_name(cursor, user)

        cursor.execute("SELECT BACKGROUND_PATH FROM tbl_account \
                        WHERE ID = ?", (user_id,))
        rows = cursor.fetchall()
        if len(rows) > 0:
            return rows[0][0]
        return None
    
    '''
    Delete a user from the database.
    '''
    def delete_user(self, user):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        user_id = self.get_user_id_from_name(cursor, user)

        cursor.execute("DELETE FROM tbl_account \
                        WHERE ID = ?", (user_id,))
        connection.commit()
        connection.close()
    
    '''
    Updates the current password reset link, also used to remove used reset links.
    '''
    def update_password_reset_link(self, email, link):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        cursor.execute("UPDATE tbl_account \
                        SET EMAIL_RESET_LINK = ? \
                        WHERE EMAIL = ?", (link, email))
        connection.commit()
        connection.close()
    
    '''
    Used for reseting password from emailed code.
    '''
    def get_user_id_from_reset_code(self, cursor, code):
        cursor.execute("SELECT ID FROM tbl_account \
                        WHERE EMAIL_RESET_LINK = ?", (code,))
        rows = cursor.fetchall()
        if len(rows) > 0:
            return rows[0][0]
        return None

    '''
    Resets user password if valid code is given.
    '''
    def reset_password(self, code, password):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        user_id = self.get_user_id_from_reset_code(cursor, code)
        if user_id:
            cursor.execute("UPDATE tbl_account \
                            SET PASSWORD = ?, EMAIL_RESET_LINK = ? \
                            WHERE ID = ?", (self.hash_password(password), None, user_id))
            connection.commit()
            connection.close()
            return True
        
        connection.close()
        return False
    
    '''
    Check Admin credentials
    '''
    def check_admin(self, user, session_key):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        user_id = self.get_user_id_from_name(cursor, user)
        valid_key = self.check_user_session_key(user, session_key)

        if valid_key:
            cursor.execute("SELECT ADMIN_USER FROM tbl_account \
                            WHERE ID = ?", (user_id,))
            admin = cursor.fetchall()[0][0]
            if admin == 1:
                return True
        return False
                