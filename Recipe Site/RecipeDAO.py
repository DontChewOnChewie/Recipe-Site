import sqlite3

class RecipeDAO:

    def __init__(self):
        print("Recipe DAO Initialised")
    
    def get_recipe_for_user(self, user):
        connection = sqlite3.connect('recipe.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tbl_recipe r \
                        JOIN tbl_account a ON r.RECIPE_OWNER = a.ID \
                        WHERE RECIPE_OWNER = " + str(user))
        rows = cursor.fetchall()
        for row in rows:
            print("Recipe ID : " + str(row['ID']) + 
                  "\nUser ID : " + str(row['RECIPE_OWNER']) + 
                  "\nRecipe Name : " + str(row['RECIPE_NAME']))
        connection.close()
    
    def get_searched_recipe(self, search):
        connection = sqlite3.connect('recipe.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(f"SELECT RECIPE_NAME FROM tbl_recipe \
                        WHERE RECIPE_NAME like '%{search}%'")
        rows = cursor.fetchall()
        connection.close()

        return_val = list()

        for row in rows:
            return_val.append(row['RECIPE_NAME'])
        return return_val
