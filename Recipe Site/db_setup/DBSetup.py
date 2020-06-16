import sqlite3
import sys
import datetime
import hashlib

tbl_account = """CREATE TABLE tbl_account (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	USERNAME VARCHAR2(100) NOT NULL,
	PASSWORD VARCHAR2(128) NOT NULL,
	SIGNUP_DATE VARCHAR2(50),
	LAST_SIGNIN VARCHAR2(50),
	CURRENT_SESSION_KEY VARCHAR2(100),
	EMAIL_AUTH BIT DEFAULT 0,
	EMAIL VARCHAR2(255),
	EMAIL_RESET_LINK VARCHAR2(10),
	CAN_EDIT_SETTINGS BIT DEFAULT 0,
	SETTINGS_CODE VARCHAR2(6),
	BACKGROUND_PATH TEXT DEFAULT NULL
);"""

tbl_recipe = """CREATE TABLE tbl_recipe (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	RECIPE_OWNER INTEGER,
	RECIPE_NAME VARCHAR2(50) NOT NULL,
	RECIPE_DESCRIPTION TEXT NOT NULL,
	RECIPE_INGREDIENTS TEXT,
	FOREIGN KEY(RECIPE_OWNER) REFERENCES tbl_account(ID)
);"""

tbl_favourite = """CREATE TABLE tbl_favourite (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	USER_ID INTEGER,
	RECIPE_ID INTEGER,
	FOREIGN KEY(USER_ID) REFERENCES tbl_account(ID),
	FOREIGN KEY(RECIPE_ID) REFERENCES tbl_recipe(ID)
);"""

def validate_args():
    if len(sys.argv) == 3:
        if sys.argv[2].lower() == "reset":
            reset_tables()

    args = sys.argv[1].lower()
    if "a" in args:
        print("Adding accounts...")
        add_accounts()
        
        if "r" in args:
            print("Adding recipes...")
            add_recipes()

            if "f" in args:
                print("Adding favourites...")
                add_favourites()

def reset_tables():
    connection = sqlite3.connect('../recipe.db')
    cursor = connection.cursor()

    cursor.execute("drop table tbl_favourite")
    cursor.execute("drop table tbl_recipe")
    cursor.execute("drop table tbl_account")

    cursor.execute(tbl_account)
    cursor.execute(tbl_recipe)
    cursor.execute(tbl_favourite)

    connection.commit()
    connection.close()

def add_accounts():
    connection = sqlite3.connect('../recipe.db')
    cursor = connection.cursor()

    with open("accounts.txt", 'r') as file:
        for line in file.readlines():
            details = line.split("|")
            cursor.execute("INSERT INTO tbl_account (USERNAME, PASSWORD, SIGNUP_DATE) \
                            VALUES (?,?,?)", (details[0].rstrip(), 
                                              hashlib.sha512(details[1].rstrip().encode('utf-8')).hexdigest(), 
                                              datetime.datetime.now()))
    connection.commit()
    connection.close()

def add_recipes():
    connection = sqlite3.connect('../recipe.db')
    cursor = connection.cursor()

    with open("recipes.txt", 'r') as file:
        for line in file.readlines():
            details = line.rstrip().split("|")
            cursor.execute("INSERT INTO tbl_recipe (RECIPE_OWNER, RECIPE_NAME, RECIPE_DESCRIPTION, RECIPE_INGREDIENTS) \
                            VALUES (?,?,?,?)", (details[0], details[1], details[2], details[3]))
    connection.commit()
    connection.close()

def add_favourites():
    connection = sqlite3.connect('../recipe.db')
    cursor = connection.cursor()

    with open("favourites.txt", 'r') as file:
        for line in file.readlines():
            details = line.rstrip().split("|")
            cursor.execute("INSERT INTO tbl_favourite (USER_ID, RECIPE_ID) \
                            VALUES (?,?)", (details[0], details[1]))
    connection.commit()
    connection.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
        Data to add not specified! Example run : python DBSetup.py ar
        
        Available data to add : 
            a : Add accounts to database.
            r : Add recipes to database, must have added accounts as well.
            f : Add favourites to database, must have addeded accounts and recipes.
        
        Addiontal parameters :
            reset : Resets all tables in the database, has to be specified as last parameter.
        """)
    
    valid_args = validate_args()