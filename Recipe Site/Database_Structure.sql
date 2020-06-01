CREATE TABLE tbl_account (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	USERNAME VARCHAR2(100) NOT NULL,
	PASSWORD VARCHAR2(128) NOT NULL,
	SIGNUP_DATE VARCHAR2(50),
	LAST_SIGNIN VARCHAR2(50)
	CURRENT_SESSION_KEY VARCHAR2(100)
);

CREATE TABLE tbl_recipe (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	RECIPE_OWNER INTEGER,
	RECIPE_NAME VARCHAR2(50) NOT NULL,
	RECIPE_DESCRIPTION TEXT NOT NULL,
	RECIPE_INGREDIENTS TEXT,
	FOREIGN KEY(RECIPE_OWNER) REFERENCES tbl_account(ID)
);

/* Recipe Ingredients JSON format. */
/*
{
	"ingredients": {
		"eggs": "2",
		"flour": "200g",
		"sugar": "100g",
		"butter": "100g"
	},

	"optional": {
		"chocolate-chips": "100g"
	}
}
*/

CREATE TABLE tbl_logs (
	ID INTEGER PRIMARY AUTOINCREMENT,
	USERID INTEGER,
	PLATFORM VARCHAR2(50),
	USER_AGENT VARCHAR2(255),
	REQ_TIME VARCHAR2(50)
);

CREATE TABLE tbl_favourite (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	USER_ID INTEGER,
	RECIPE_ID INTEGER,
	FOREIGN KEY(USER_ID) REFERENCES tbl_account(ID),
	FOREIGN KEY(RECIPE_ID) REFERENCES tbl_recipe(ID)
);


/*
---||||||| USER DAO |||||||---
*/

/* Check if a user with username already exists
	(check_user_exists) */
SELECT * FROM tbl_account
WHERE USERNAME = ("Given Username");

/* Get users ID from Username
	(get_user_id_from_name) */
SELECT ID FROM tbl_account
WHERE USERNAME = ('Given username');

/* Add new user with given credentials
	(signup_user) */
INSERT INTO tbl_account (USERNAME, PASSWORD, SIGNUP_DATE, LAST_SIGNIN)
VALUES (('Given Username'), ('Given Hashed Password'), ('Current Date/Time'), ('Current Date/Time'));

/* Update last user sign in value
	(update_user_last_login) */
UPDATE tbl_account
SET LAST_SIGNIN = ('Current Date/Time')
WHERE USERNAME = ('Given Username');

/* Update users session key 
	(update_user_session_key) */
UPDATE tbl_account
SET CURRENT_SESSION_KEY = ('Randomly Generated Key')
WHERE ID = ("Given User ID");

/* Check a users session ket against a username
	(check_user_session_key) */
SELECT CURRENT_SESSION_KEY
FROM tbl_account
WHERE USERNAME = ('Given Username');

/* Log a user in with given credentials
	(login_user) */
SELECT * FROM tbl_account
WHERE USERNAME = ('Given Username') AND PASSWORD = ('Given Password')

/*
---||||||| RECIPE DAO |||||||---
*/

/* Get Recipes for search results 
	(get_searched_recipe) */
SELECT r.RECIPE_NAME, a.USERNAME FROM tbl_recipe r
JOIN tbl_account a ON r.RECIPE_OWNER = a.ID
WHERE r.RECIPE_NAME like '%(search string)%';

/* Get Recipes for a users account page
	(get_recipes_for_user) */
SELECT r.ID, r.RECIPE_NAME, r.RECIPE_DESCRIPTION, r.RECIPE_INGREDIENTS, a.USERNAME
FROM tbl_recipe r
JOIN tbl_account a ON a.ID = r.RECIPE_OWNER
WHERE a.USERNAME = ('Account Page Name');

/* Get Recipe ID from Recipe name and Account name
	(get_recipe_id_from_user_and_name) */
SELECT r.ID FROM tbl_recipe r
JOIN tbl_account a ON r.RECIPE_OWNER = a.ID
WHERE a.USERNAME = ('Given User') AND r.RECIPE_NAME = ('Given Recipe Name');

/* Get specific for recipe for full page
	(get_recipe) */
SELECT r.ID, a.USERNAME, r.RECIPE_NAME, r.RECIPE_DESCRIPTION, r.RECIPE_INGREDIENTS
FROM tbl_recipe r
JOIN tbl_account a ON a.ID = r.RECIPE_OWNER
WHERE r.ID = ('ID got from function above');

/* Delete recipe from database
	(delete_recipe) */
DELETE FROM tbl_recipe
WHERE ID = ('ID got from function above');

/* Add recipe to database
	(add_recipe) */
INSERT INTO tbl_recipe (RECIPE_OWNER, RECIPE_NAME, RECIPE_DESCRIPTION, RECIPE_INGREDIENTS)
VALUES ('ID from function above', 'Given Recipe Name', 'Given Description', 'Given Ingredients');

/* Get Recipe by ID
	(get_recipe_by_id) */
SELECT a.USERNAME, r.ID, r.RECIPE_NAME, r.RECIPE_DESCRIPTION, r.RECIPE_INGREDIENTS
FROM tbl_recipe r
JOIN tbl_account a ON a.ID = r.RECIPE_OWNER
WHERE r.ID = ('Given ID')

/*
---||||||| Favourite DAO |||||||---
*/

/* Get recipe ID's of users favourite recipes
	(get_users_favourites_recipe_ids) */
SELECT RECIPE_ID
FROM tbl_favourite 
WHERE USER_ID = ('Given ID');

/* Add new favourite item for user
	(add_favourite) */
INSERT INTO tbl_favourite (USER_ID, RECIPE_ID)
VALUES ('Given User ID', 'Given Recipe ID')

/* Check if recipe is a users favourite
	(check_if_favourited) */
SELECT * FROM tbl_favourite
WHERE USER_ID = ('Given user id') AND RECIPE_ID = ('Given recipe id')

/* Delete favourite for user
	(delete_favourite) */
DELETE FROM tbl_favourite
WHERE USER_ID = ('Given user ID') AND RECIPE_ID = ('Given recipe ID')