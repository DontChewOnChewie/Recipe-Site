import sqlite3
from Recipe import Recipe

class RecipeDAO:

    def __init__(self):
        print("Recipe DAO Initialised")
    
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
    
    def get_recipes_for_user(self, user):
        connection = sqlite3.connect('recipe.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT r.ID, r.RECIPE_NAME, r.RECIPE_DESCRIPTION, a.USERNAME \
                        FROM tbl_recipe r \
                        JOIN tbl_account a ON a.ID = r.RECIPE_OWNER \
                        WHERE a.USERNAME = ?", (user,))
        rows = cursor.fetchall()
        connection.close()
        recipes = []
        for row in rows:
            recipes.append(Recipe(row['ID'], row['RECIPE_NAME'], row['RECIPE_DESCRIPTION'], row['USERNAME']))
        return recipes
    
    def get_recipe_id_from_user_and_name(self, cursor, user, recipeName):
        cursor.execute("SELECT r.ID FROM tbl_recipe r \
                        JOIN tbl_account a ON r.RECIPE_OWNER = a.ID \
                        WHERE a.USERNAME = ? AND r.RECIPE_NAME = ?",(user, recipeName))
        rows = cursor.fetchall()
        if (len(rows) > 0):
            return rows[0][0]
        return None

    def get_recipe(self, user, recipeName):
        connection = sqlite3.connect('recipe.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        id = self.get_recipe_id_from_user_and_name(cursor, user, recipeName)
        cursor.execute("SELECT r.ID, a.USERNAME, r.RECIPE_NAME, r.RECIPE_DESCRIPTION \
                        FROM tbl_recipe r \
                        JOIN tbl_account a ON a.ID = r.RECIPE_OWNER \
                        WHERE r.ID = ?", (id,))
        rows = cursor.fetchall()
        connection.close()
        if (len(rows) > 0):
            return Recipe(rows[0]['ID'], rows[0]['RECIPE_NAME'], rows[0]['RECIPE_DESCRIPTION'], rows[0]['USERNAME'])
        return None
    
    def delete_recipe(self, user, recipeName):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()
        id = self.get_recipe_id_from_user_and_name(cursor, user, recipeName)
        cursor.execute(f"DELETE FROM tbl_recipe WHERE ID = {id}")
        connection.commit()
        connection.close()
    
    def get_user_id_from_name(self, cursor, user):
        cursor.execute("SELECT ID FROM tbl_account \
                        WHERE USERNAME = ?", (user,))
        rows = cursor.fetchall()
        return rows[0][0]

    def add_recipe(self, user, recipeName, recipeDesc):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()
        id = self.get_user_id_from_name(cursor, user)
        cursor.execute("INSERT INTO tbl_recipe (RECIPE_OWNER, RECIPE_NAME, RECIPE_DESCRIPTION) \
                        VALUES (?, ?, ?)", (id, recipeName, recipeDesc))
        connection.commit()
        connection.close()

