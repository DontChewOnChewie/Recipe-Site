CREATE TABLE tbl_account (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	USERNAME VARCHAR2(100) NOT NULL,
	PASSWORD VARCHAR2(128) NOT NULL,
	SIGNUP_DATE VARCHAR2(50),
	LAST_SIGNIN VARCHAR2(50)

);

CREATE TABLE tbl_recipe (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	RECIPE_OWNER INTEGER,
	RECIPE_NAME VARCHAR2(50) NOT NULL,
	RECIPE_DESCRIPTION VARCHAR2(255) NOT NULL,
	FOREIGN KEY(RECIPE_OWNER) REFERENCES tbl_account(ID)
);

CREATE TABLE tbl_logs (
	ID INTEGER PRIMARY AUTOINCREMENT,
	USERID INTEGER,
	PLATFORM VARCHAR2(50),
	USER_AGENT VARCHAR2(255),
	REQ_TIME VARCHAR2(50)
);

/* Get Recipe based on user */
SELECT * FROM TBL_RECIPE R 
JOIN TBL_ACCOUNT A ON A.ID = R.RECIPE_OWNER 
WHERE RECIPE_OWNER = ('Given User')

/* Get Recipes for search results*/
SELECT r.RECIPE_NAME, a.USERNAME FROM TBL_RECIPE r
JOIN tbl_account a ON r.RECIPE_OWNER = a.ID
WHERE r.RECIPE_NAME like '%(search string)%'

/* Update last user sign in value */
UPDATE tbl_account
SET LAST_SIGNIN = ('New Sign In Date')
WHERE USERNAME = ('Given Username')

/* Get Recipes for a users account page */
SELECT r.RECIPE_NAME, a.USERNAME
FROM tbl_recipe r
JOIN tbl_account a ON a.ID = r.RECIPE_OWNER
WHERE a.USERNAME = ('Account Page Name')

/* Get Recipe ID from Recipe name and Account name */
SELECT r.ID FROM tbl_recipe r
JOIN tbl_account a ON r.RECIPE_OWNER = a.ID
WHERE a.USERNAME = ('Given User') AND r.RECIPE_NAME = ('Given Recipe Name')

/* Get specific for recipe for full page */
SELECT r.ID, a.USERNAME, r.RECIPE_NAME
FROM tbl_recipe r
JOIN tbl_account a ON a.ID = r.RECIPE_OWNER
WHERE r.ID = ('ID got from function above')

/* Delete recipe from database */
DELETE FROM tbl_recipe
WHERE ID = ('ID got from function above')

/* Get users ID from Username */
SELECT ID FROM tbl_account
WHERE USERNAME = ('Given username')

/* Add recipe to database */
INSERT INTO tbl_recipe (RECIPE_OWNER, RECIPE_NAME, RECIPE_DESCRIPTION)
VALUES ('ID from function above', 'Given Recipe Name', 'Given Description')