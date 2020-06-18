import sqlite3
import datetime
from UserDAO import UserDAO

class SubscribeDAO:

    def __init__(self):
        print("Subscribe DAO Initialised")

    '''
    Check if a user is already subscribed to another user.
    '''
    def check_already_subscribed(self, cursor, user_id, sub_id):
        cursor.execute("SELECT * FROM tbl_subscribe \
                        WHERE USER_ID = ? AND SUBBED_USER_ID = ?", (user_id, sub_id))
        rows = cursor.fetchall()
        if len(rows) > 0:
            return True
        return False
    
    '''
    Check if a user is subscribed to a user. Builds own connection and cursor
    unlike the function above.
    '''
    def is_subscribed(self, user, sub):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        udao = UserDAO()
        user_id = udao.get_user_id_from_name(cursor, user)
        sub_id = udao.get_user_id_from_name(cursor, sub)

        subsribed = self.check_already_subscribed(cursor, user_id, sub_id)
        connection.close()
        return subsribed

    '''
    Add a new subscritpion.
    '''
    def subscribe(self, user, sub):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        udao = UserDAO()
        user_id = udao.get_user_id_from_name(cursor, user)
        sub_id = udao.get_user_id_from_name(cursor, sub)

        if user_id and sub_id and not self.check_already_subscribed(cursor, user_id, sub_id):
            cursor.execute("INSERT INTO tbl_subscribe (USER_ID, SUBBED_USER_ID, SUBSCRIBE_DATE) \
                            VALUES (?, ?, ?)", (user_id, sub_id, datetime.datetime.now()))
            connection.commit()
        connection.close()
    
    '''
    Remove a subscription for a user.
    '''
    def unsubscribe(self, user, sub):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        udao = UserDAO()
        user_id = udao.get_user_id_from_name(cursor, user)
        sub_id = udao.get_user_id_from_name(cursor, sub)

        cursor.execute("DELETE FROM tbl_subscribe \
                        WHERE USER_ID = ? AND SUBBED_USER_ID = ?", (user_id, sub_id))
        connection.commit()
        connection.close()

    '''
    Get all user IDs of subscribed pages for a user.
    '''
    def get_subscribed_pages_for_user(self, user):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        udao = UserDAO()
        user_id = udao.get_user_id_from_name(cursor, user)

        cursor.execute("SELECT SUBBED_USER_ID FROM tbl_subscribe \
                        WHERE USER_ID = ?", (user_id,))
        rows = cursor.fetchall()
        connection.close()
        return rows