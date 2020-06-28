import sqlite3
from UserDAO import UserDAO
import datetime
from Log import Log

class LogDAO:

    REQUEST_SIGNIN = "SIGN-IN"
    REQUEST_SIGNUP = "SIGN-UP"
    REQUEST_SIGNOUT = "SIGN-OUT"
    REQUEST_DEL_ACCOUNT = "DEL_ACCOUNT"
    REQUEST_ADD_RECIPE = "ADD-RECIPE"
    REQUEST_DEL_RECIPE = "DEL-RECIPE"
    REQUEST_EDIT_RECIPE = "EDIT-RECIPE"
    REQUEST_PASSWORD_CHANGE = "PASS-CHANGE"
    REQUEST_PASSWORD_RESET = "PASS-RESET"
    REQUEST_EMAIL_AUTH_ENABLE = "ENABLE-EMAIL-AUTH"
    REQUEST_EMAIL_AUTH_CHANGE = "EMAIL-AUTH-CHANGE"
    REQUEST_USER_BGR_CHANGE = "USER-BGR-CHANGE"
    REQUEST_ADD_COMMENT = "ADD-COMMENT"
    REQUEST_EDIT_COMMENT = "EDIT-COMMENT"
    REQUEST_DEL_COMMENT = "DEL-COMMENT"

    def __init__(self):
        print("Intialising Log DAO")
    
    def add_log(self, request, user, _type, status):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()

        print(type(request.user_agent))

        udao = UserDAO()
        user_id = udao.get_user_id_from_name(cursor, user) if user else None

        cursor.execute("INSERT INTO tbl_log (USER_ID, REQ_TYPE, REQ_IP, REQ_PORT, REQ_URL, REQ_DATE, REQ_STATUS, USER_AGENT, HOST) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (user_id, _type, request.remote_addr, int(request.environ['REMOTE_PORT']),
                         request.url, str(datetime.datetime.now()).split(".")[0], status, str(request.user_agent), request.host))
        connection.commit()
        connection.close()
    
    def get_logs(self, _type, status, url, ip, user_agent):
        connection = sqlite3.connect('recipe.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        _type = "%" if not _type else _type
        status = "%" if not status else status
        url = "%" if not url else "%" + url + "%"
        ip = "%" if not ip else "%" + ip + "%"
        user_agent = "%" if not user_agent else "%" + user_agent + "%"

        cursor.execute("SELECT * FROM tbl_log \
                        WHERE REQ_TYPE LIKE ? \
                        AND REQ_STATUS LIKE ? \
                        AND REQ_URL LIKE ? \
                        AND REQ_IP LIKE ? \
                        AND USER_AGENT LIKE ? \
                        ORDER BY 1 DESC", (_type, status, url, ip, user_agent))

        rows = cursor.fetchall()
        connection.close()
        logs = []
        for row in rows:
            logs.append(Log(row['ID'], row['USER_ID'], row['REQ_TYPE'],
                            row['REQ_IP'], row['REQ_PORT'], row['REQ_URL'],
                            row['REQ_DATE'], row['REQ_STATUS'], row['USER_AGENT'],
                            row['HOST']))
        return logs
