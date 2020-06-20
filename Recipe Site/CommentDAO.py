import sqlite3
import datetime
from Comment import Comment
from RecipeDAO import RecipeDAO
from UserDAO import UserDAO

class CommentDAO:

    def __init__(self):
        print("CommentDAO Initialised")
    
    '''
    Check to see if a user has already left a comment so they can't spam.
    '''
    def user_already_left_comment(self, cursor, user, recipe):
        cursor.execute("SELECT * FROM tbl_comment \
                        WHERE USER_ID = ? AND RECIPE_ID = ?", (user, recipe))
        rows = cursor.fetchall()
        if len(rows) > 0:
            return True
        return False

    '''
    Add a new comment to a recipe.
    '''
    def add_comment(self, user, recipe_user, recipe, comment):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        udao = UserDAO()
        user_id = udao.get_user_id_from_name(cursor, user)

        rdao = RecipeDAO()
        recipe_id = rdao.get_recipe_id_from_user_and_name(cursor, recipe_user, recipe.replace("-", " "))

        if self.user_already_left_comment(cursor, user_id, recipe_id):
            return        

        cursor.execute("INSERT INTO tbl_comment (USER_ID, RECIPE_ID, COMMENT_DETAILS, COMMENT_DATE) \
                        VALUES (?, ?, ?, ?)", (user_id, recipe_id, comment, datetime.datetime.now()))
        connection.commit()
        connection.close()
    
    '''
    Remove a users comment on a recipe.
    '''
    def remove_comment(self, user, recipe_user, recipe):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        udao = UserDAO()
        user_id = udao.get_user_id_from_name(cursor, user)

        rdao = RecipeDAO()
        recipe_id = rdao.get_recipe_id_from_user_and_name(cursor, recipe_user, recipe.replace("-", " "))

        cursor.execute("DELETE FROM tbl_comment \
                        WHERE USER_ID = ? AND RECIPE_ID = ?", (user_id, recipe_id))
        connection.commit()
        connection.close()
        return True

    '''
    Edit a users comment and show that it has been edited.
    '''
    def edit_comment(self, user, recipe_user, recipe, comment):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        udao = UserDAO()
        user_id = udao.get_user_id_from_name(cursor, user)

        rdao = RecipeDAO()
        recipe_id = rdao.get_recipe_id_from_user_and_name(cursor, recipe_user, recipe.replace("-", " "))

        print(user_id, recipe_id, comment)

        cursor.execute("UPDATE tbl_comment \
                        SET COMMENT_DETAILS = ?, COMMENT_EDITED = 1 \
                        WHERE USER_ID = ? AND RECIPE_ID = ?", (comment, user_id, recipe_id))
        connection.commit()
        connection.close()
        return True

    '''
    Get all the comments about a recipe.
    '''
    def get_comments_for_recipe(self, user, user_recipe, recipe):
        connection = sqlite3.connect('recipe.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        rdao = RecipeDAO()
        recipe_id = rdao.get_recipe_id_from_user_and_name(cursor, user_recipe, recipe.replace("-", " "))

        cursor.execute("SELECT c.ID, c.USER_ID, a.USERNAME, c.RECIPE_ID, c.COMMENT_DETAILS, c.COMMENT_DATE, c.COMMENT_EDITED \
                        FROM tbl_comment c \
                        JOIN tbl_account a on a.ID = c.USER_ID \
                        WHERE RECIPE_ID = ?", (recipe_id,))
        rows = cursor.fetchall()
        comments = []

        for row in rows:
            ratings = self.get_comment_ratings_for_comment(cursor, row['ID'])
            comments.append(Comment(row['ID'], row['USER_ID'], row['USERNAME'], row['RECIPE_ID'], row['COMMENT_DETAILS'], row['COMMENT_DATE'], row['COMMENT_EDITED'], ratings))
        
        connection.close()
        return comments
    
    '''
    Check if the user has already left a rating for specified comment.
    '''
    def check_comment_rating_exists(self, cursor, comment_id, user_id):
        cursor.execute("SELECT * FROM tbl_comment_rating \
                        WHERE COMMENT_ID = ? AND USER_ID = ?", (comment_id, user_id))
        rows = cursor.fetchall()
        if len(rows) > 0:
            return True
        return False

    '''
    Get a users current opinion on a comment.
    '''
    def get_current_comment_rating(self, cursor, comment_id, user_id):
        cursor.execute("SELECT OPINION from tbl_comment_rating \
                        WHERE COMMENT_ID = ? AND USER_ID = ?", (comment_id, user_id))
        return cursor.fetchall()[0][0]

    '''
    Responsible for adding a new rating for a comment and editing.
    Edited if the user has already left a rating, and returns new rating so 
    that page can be manipulated through the XHR response.
    '''
    def add_comment_rating(self, user, comment_id, rating):
        connection = sqlite3.connect('recipe.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        udao = UserDAO()
        user_id = udao.get_user_id_from_name(cursor, user)

        new_rating = 1 if rating > 0 else -1

        if self.check_comment_rating_exists(cursor, comment_id, user_id):
            current_rating = int(self.get_current_comment_rating(cursor, comment_id, user_id))
            if current_rating == new_rating:
                new_rating = 0    

            cursor.execute("UPDATE tbl_comment_rating \
                            SET OPINION = ? \
                            WHERE COMMENT_ID = ? AND USER_ID = ?", (new_rating, comment_id, user_id))
        else:
            cursor.execute("INSERT INTO tbl_comment_rating (COMMENT_ID, USER_ID, OPINION) \
                            VALUES (?, ?, ?)", (comment_id, user_id, new_rating))

        connection.commit()
        connection.close()
        return new_rating
    
    '''
    Gets all current ratings for a comment and returns a dictionary of user IDs
    and their given rating.
    '''
    def get_comment_ratings_for_comment(self, cursor, comment_id):
        cursor.execute("SELECT USER_ID, OPINION FROM tbl_comment_rating \
                        WHERE COMMENT_ID = ? AND OPINION != 0", (comment_id,))
        return {x[0]:x[1] for x in cursor.fetchall()}