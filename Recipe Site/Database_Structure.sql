CREATE TABLE tbl_account (
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
);

CREATE TABLE tbl_recipe (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	RECIPE_OWNER INTEGER,
	RECIPE_NAME VARCHAR2(50) NOT NULL,
	RECIPE_DESCRIPTION TEXT NOT NULL,
	RECIPE_INGREDIENTS TEXT,
	FOREIGN KEY(RECIPE_OWNER) REFERENCES tbl_account(ID)
);

CREATE TABLE tbl_favourite (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	USER_ID INTEGER,
	RECIPE_ID INTEGER,
	FOREIGN KEY(USER_ID) REFERENCES tbl_account(ID),
	FOREIGN KEY(RECIPE_ID) REFERENCES tbl_recipe(ID)
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

