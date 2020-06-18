import sqlite3
from Recipe import Recipe
from UserDAO import UserDAO

'''
Class used to access Recipes in DB.
'''
class RecipeDAO:

    def __init__(self):
        print("Recipe DAO Initialised")
    
    '''
    Returns list of search results based on user input.
    '''
    def get_searched_recipe(self, search):
        connection = sqlite3.connect('recipe.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(f"SELECT r.RECIPE_NAME, a.USERNAME \
                         FROM tbl_recipe r \
                         JOIN tbl_account a ON r.RECIPE_OWNER = a.ID \
                         WHERE r.RECIPE_NAME like '%{search}%'")
        rows = cursor.fetchall()
        connection.close()

        return_val = list()

        for row in rows:
            return_val.append((row['RECIPE_NAME'], row['USERNAME']))
        return return_val
    
    '''
    Returns a list of all recipes a user has created for their account page.
    '''
    def get_recipes_for_user(self, user):
        connection = sqlite3.connect('recipe.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT r.ID, r.RECIPE_NAME, r.RECIPE_DESCRIPTION, r.RECIPE_INGREDIENTS, a.USERNAME \
                        FROM tbl_recipe r \
                        JOIN tbl_account a ON a.ID = r.RECIPE_OWNER \
                        WHERE a.USERNAME = ?", (user,))
        rows = cursor.fetchall()
        connection.close()
        recipes = []
        for row in rows:
            recipes.append(Recipe(row['ID'], row['RECIPE_NAME'], row['RECIPE_DESCRIPTION'],row["RECIPE_INGREDIENTS"], row['USERNAME']))
        return recipes
    
    '''
    Returns the ID of a recipe from a given recipe name and username.
    '''
    def get_recipe_id_from_user_and_name(self, cursor, user, recipeName):
        cursor.execute("SELECT r.ID FROM tbl_recipe r \
                        JOIN tbl_account a ON r.RECIPE_OWNER = a.ID \
                        WHERE a.USERNAME = ? AND r.RECIPE_NAME = ?",(user, recipeName))
        rows = cursor.fetchall()
        if (len(rows) > 0):
            return rows[0][0]
        return None

    '''
    Get a recipe based off a username and recipe name.
    SQL uses ID to get the recipe with the help of get_recipe_id_from_user_and_name().
    '''
    def get_recipe(self, user, recipeName):
        connection = sqlite3.connect('recipe.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        id = self.get_recipe_id_from_user_and_name(cursor, user, recipeName)
        cursor.execute("SELECT r.ID, a.USERNAME, r.RECIPE_NAME, r.RECIPE_DESCRIPTION, r.RECIPE_INGREDIENTS \
                        FROM tbl_recipe r \
                        JOIN tbl_account a ON a.ID = r.RECIPE_OWNER \
                        WHERE r.ID = ?", (id,))
        rows = cursor.fetchall()
        connection.close()
        if (len(rows) > 0):
            return Recipe(rows[0]['ID'], rows[0]['RECIPE_NAME'], rows[0]['RECIPE_DESCRIPTION'], rows[0]["RECIPE_INGREDIENTS"], rows[0]['USERNAME'])
        return None
    
    '''
    Delete a recipe based on a username and recipe name.
    SQL uses ID to get the recipe with the help of get_recipe_id_from_user_and_name().
    '''
    def delete_recipe(self, user, recipeName):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()
        id = self.get_recipe_id_from_user_and_name(cursor, user, recipeName)
        cursor.execute(f"DELETE FROM tbl_recipe WHERE ID = {id}")
        connection.commit()
        connection.close()

    '''
    Add a recipe to the database.
    '''
    def add_recipe(self, user, recipeName, recipeDesc, recipeIngr):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        udao = UserDAO()
        id = udao.get_user_id_from_name(cursor, user)
        cursor.execute("INSERT INTO tbl_recipe (RECIPE_OWNER, RECIPE_NAME, RECIPE_DESCRIPTION, RECIPE_INGREDIENTS) \
                        VALUES (?, ?, ?, ?)", (id, recipeName, recipeDesc, recipeIngr))
        connection.commit()
        connection.close()

    '''
    Get Recipe from a given recipe ID
    '''
    def get_recipe_by_id(self, id):
        connection = sqlite3.connect('recipe.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT a.USERNAME, r.ID, r.RECIPE_NAME, r.RECIPE_DESCRIPTION, r.RECIPE_INGREDIENTS \
                        FROM tbl_recipe r \
                        JOIN tbl_account a ON a.ID = r.RECIPE_OWNER \
                        WHERE r.ID = ?", (id,))
        rows = cursor.fetchall()
        connection.close()

        if len(rows) > 0:
            return Recipe(rows[0]['ID'], rows[0]['RECIPE_NAME'], rows[0]['RECIPE_DESCRIPTION'], rows[0]['RECIPE_INGREDIENTS'], rows[0]['USERNAME'])
        return None
    
    '''
    Get recipe ids based on a users subscriptions.
    '''
    def get_subscribed_recipes(self, user_ids):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        recipe_ids = []

        for id in user_ids:
            cursor.execute("SELECT ID FROM tbl_recipe \
                            WHERE RECIPE_OWNER = ?", (id,))
            rows = cursor.fetchall()
            recipe_ids += [x[0] for x in rows]

        connection.close()
        recipe_ids.sort(reverse=True)
        return recipe_ids