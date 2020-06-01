import sqlite3
from UserDAO import UserDAO
from RecipeDAO import RecipeDAO

class FavouriteDAO:

    def __init__(self):
        print("Setting up Favourite DAO")
    
    '''
    Get a users favourite recipes for their account page filter.
    '''
    def get_users_favourites_recipe_ids(self, user):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()
        udao = UserDAO()
        id = udao.get_user_id_from_name(cursor, user)
        cursor.execute("SELECT RECIPE_ID \
                        FROM tbl_favourite \
                        WHERE USER_ID = ?", (id,))
        rows = cursor.fetchall()
        return rows
    
    '''
    Add a new favourite recipe for a user.
    '''
    def add_favourite(self, user, recipe_id):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        udao = UserDAO()
        user_id = udao.get_user_id_from_name(cursor, user)

        if user_id and recipe_id:
            cursor.execute("INSERT INTO tbl_favourite (USER_ID, RECIPE_ID) \
                            VALUES (?, ?)", (user_id, recipe_id))
            connection.commit()
            connection.close()
            return True
        
        connection.close()
        return False
    
    '''
    Delete a favourited recipe for a user.
    '''
    def delete_favourite(self, user, recipe):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        udao = UserDAO()
        user_id = udao.get_user_id_from_name(cursor, user)

        print(user_id, recipe)

        if user_id and recipe:
            cursor.execute("DELETE FROM tbl_favourite \
                            WHERE USER_ID = ? AND RECIPE_ID = ?", (user_id, recipe))
            connection.commit()
            connection.close()
            return True
        
        connection.close()
        return False

    '''
    Checks if a user has already favourited a recipe when visiting a recipe page.
    '''
    def check_if_favourited(self, user, owner, recipeName):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        udao = UserDAO()
        user_id = udao.get_user_id_from_name(cursor, user)

        rdao = RecipeDAO()
        recipe_id = rdao.get_recipe_id_from_user_and_name(cursor, owner, recipeName)

        cursor.execute("SELECT * FROM tbl_favourite \
                        WHERE USER_ID = ? AND RECIPE_ID = ?", (user_id, recipe_id))
        rows = cursor.fetchall()
        connection.close()
        if len(rows) > 0:
            return True
        else:
            return False        
