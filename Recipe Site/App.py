from flask import Flask, render_template, request, make_response, redirect
from UserDAO import UserDAO
from RecipeDAO import RecipeDAO
from FavouriteDAO import FavouriteDAO
from SubscribeDAO import SubscribeDAO
from LogDAO import LogDAO
from CommentDAO import CommentDAO
from Comment import Comment
from User import User
from Log import Log
from Alert import Alert
from Recipe import Recipe
from EmailHandler import EmailHandler
import urllib.parse
import os

app = Flask(__name__)

'''
Root of website 

GET --:--
signedIn : To decide what the header should include in it.
user :     To add a link to the header for the users account and 
           potential avatar for user in the future.
alert :    Used to display alert if needed.
'''
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':     
        alertParam = request.args.get("alert")
        alert = None
        
        if alertParam:
            alertData = urllib.parse.unquote(alertParam)
            alertData = alertData.split("|")
            alert = Alert(alertData[0], alertData[1], alertData[2])

        resp = make_response(render_template('index.html', signedIn = request.cookies.get("signedIn"),
                                                           user = request.cookies.get("user"),
                                                           alert = alert))
        return resp

'''
Signup page of website

GET --:--
signedIn : To decide what the header should include in it.
user :     To add a link to the header for the users account and 
           potential avatar for user in the future.
alert :    Used to display alert if needed.

POST --:--
Get username and password from the submitted form and try add it to database.
If it fails redirect with an alert displayed.
If it succeeds redirect back to home page and set needed cookies.
'''
@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dao = UserDAO()
        user = dao.signup_user(username, password)
        ldao = LogDAO()

        if not user:
            ldao.add_log(request, None, ldao.REQUEST_SIGNUP, 0)
            resp = make_response(redirect("/signup?alert=Username is Already Taken|Try another username and sign up again.|alert-fail"))
            return resp
        else:
            ldao.add_log(request, user.username, ldao.REQUEST_SIGNUP, 1)
            resp = make_response(redirect("/?alert=Sign Up Success|Start creating and browsing awesome recipes.|alert-suc"))
            resp.set_cookie("signedIn", "true")
            resp.set_cookie("user", user.username)
            resp.set_cookie("session_key", user.sessionKey)
            return resp
    else:
        alertParam = request.args.get("alert")
        alert = None

        if alertParam:
            alertData = urllib.parse.unquote(alertParam)
            alertData = alertData.split("|")
            alert = Alert(alertData[0], alertData[1], alertData[2]) 

        resp = make_response(render_template("signup.html", signedIn = request.cookies.get("signedIn"),
                                                            user = request.cookies.get("user"),
                                                            alert = alert))
        return resp

'''
Signs users out and immedaitely redirects to home page.
Delete needed cookies to protect other accounts.
'''
@app.route("/signout", methods=['GET'])
def signout():
    if request.method == 'GET':
        ldao = LogDAO()
        ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_SIGNOUT, 1)
        resp = make_response(redirect("/"))
        resp.delete_cookie("signedIn")
        resp.delete_cookie("user")
        resp.delete_cookie("session_key")
        return resp

'''
Try log in the user, if no User() object is returned sign in failed.
If fails return user to home page with alert.
If succeeds show alert and set assocaited user cookies.
'''
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dao = UserDAO()
        user = dao.login_user(username, password)
        ldao = LogDAO()
        
        if user == None:
            ldao.add_log(request, None, ldao.REQUEST_SIGNIN, 0)
            return redirect("/login?alert=Sign In Failed!|Make sure the details you entered are correct and try again.|alert-fail")
        else:
            ldao.add_log(request, user.username, ldao.REQUEST_SIGNIN, 1)
            resp = make_response(redirect("/?alert=Sign In Success|Start creating and browsing awesome recipes.|alert-suc"))
            resp.set_cookie("signedIn", "true")
            resp.set_cookie("user", user.username)
            resp.set_cookie("session_key", user.sessionKey)
            return resp
    elif request.method == 'GET':
        alertParam = request.args.get("alert")
        alert = None

        if alertParam:
            alertData = urllib.parse.unquote(alertParam)
            alertData = alertData.split("|")
            alert = Alert(alertData[0], alertData[1], alertData[2]) 

        return render_template("login.html", signedIn = request.cookies.get("signedIn"),
                                             user = request.cookies.get("user"),
                                             alert = alert)

'''
Used through javascript XHR request to display the search results in the header.
Return HTML to page so that it can be displayed to user.
'''
@app.route("/searchResult", methods=['GET'])
def searchResult():
    if request.method == 'GET':
        param = request.args.get("s")

        if(param):
            param = urllib.parse.unquote(param)
            dao = RecipeDAO()
            results = dao.get_searched_recipe(str(param))
            print(results)
        
        returnHTML = ""
        for result in results:
            returnHTML += f'<div><a href="/account/{result[1]}/{result[0].replace(" ", "-")}">{result[0]}</a><a href="/account/{result[1]}">{result[1]}</a></div>'
        return(returnHTML)

'''
Specified users account page.

GET --:--
signedIn :  To decide what the header should include in it.
user :      To add a link to the header for the users account and 
            potential avatar for user in the future.
recipes :   A list of recipes that the specified user created.
allowEdit : Whether or not the user can edit the page, for the most part
            this means that the current page is the signed in users page.
            However could allow shared recipe editing in future.
'''
@app.route("/account/<user>", methods=['GET'])
def account(user):
    if request.method == 'GET':
        udao = UserDAO()

        if not udao.check_user_exists(user):
            return render_template("errors/user_not_found.html")

        rdao = RecipeDAO()
        recipes = rdao.get_recipes_for_user(user)

        valid_session_key = udao.check_user_session_key(user, request.cookies.get("session_key"))
        allowEdit = False
        user_bgr = udao.get_user_background(user)

        sdao = SubscribeDAO()
        subscribed = sdao.is_subscribed(request.cookies.get("user"), user)

        if valid_session_key:
            allowEdit = True

        return render_template("account.html", signedIn = request.cookies.get("signedIn"),
                                               user = request.cookies.get("user"),
                                               recipes = recipes,
                                               allowEdit = allowEdit,
                                               userBackground = user_bgr,
                                               subscribed = subscribed)

'''
Specified users recipe page.

GET --:--
signedIn : To decide what the header should include in it.
user :     To add a link to the header for the users account and 
           potential avatar for user in the future.
recipe :   The recipe that is to be displayed on the page.
'''
@app.route("/account/<user>/<recipeName>", methods=['GET'])
def recipe(user, recipeName):
    if request.method == 'GET':
        dao = RecipeDAO()
        recipe = dao.get_recipe(user, recipeName.replace("-", " "))

        fdao = FavouriteDAO()
        favourited = fdao.check_if_favourited(request.cookies.get("user"), user, recipeName.replace("-", " "))

        cdao = CommentDAO()
        comments = cdao.get_comments_for_recipe(request.cookies.get("user"), user, recipeName)

        udao = UserDAO()
        u = udao.get_user(request.cookies.get("user"))
        
        if not recipe:
            return render_template("errors/recipe_not_found.html")

        return render_template("recipe.html", signedIn = request.cookies.get("signedIn"),
                                               user = request.cookies.get("user"),
                                               recipe = recipe,
                                               favourite = favourited,
                                               comments = comments,
                                               userobj = u)

'''
Delete recipe.

Uses users session key cookie and user cookie to determine whether or not the request
is valid. Could be used for API purposes in the future. Done through XHR request in JS.

If return Y the recipe is visibliy deleted from the users page.
'''
@app.route("/account/<user>/<recipeName>/delete", methods=['DELETE'])
def recipe_delete(user, recipeName):
    if request.method == "DELETE":
        ldao = LogDAO()
        udao = UserDAO()
        valid_key = udao.check_user_session_key(user, request.cookies.get("session_key"))

        if valid_key: 
            dao = RecipeDAO()
            dao.delete_recipe(user, recipeName.replace("-", " "))
            ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_DEL_RECIPE, 1)
            return "Y"
        else: 
            ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_DEL_RECIPE, 0)
            return "N"

'''
Add new recipe.

Uses users session key cookie and user cookie to determine whether or not the request
is valid. Could be used for API purposes in the future. Done through XHR request in JS

Return value currently does not matter.
'''
@app.route("/account/<user>/<recipeName>/add", methods=['PUT'])
def recipe_add(user, recipeName):
    if request.method == 'PUT':
        ldao = LogDAO()
        udao = UserDAO()
        valid_key = udao.check_user_session_key(user, request.cookies.get("session_key"))
        

        if valid_key:
            desc = request.args.get("desc")
            ingredients = request.args.get("ingredients")
            dao = RecipeDAO()
            dao.add_recipe(user, recipeName, desc, ingredients)
            ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_ADD_RECIPE, 1)
            return "Y"  
        else:
            ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_ADD_RECIPE, 0)
            return "N"

'''
Retrieve uses favourites for account filter.

Have to reference recipe get as [0] as sql returns tuple with one value.
'''
@app.route("/account/<user>/favourites", methods=['GET'])
def favourites(user):
    fdao = FavouriteDAO()
    ids = fdao.get_users_favourites_recipe_ids(user)

    rdao = RecipeDAO()
    recipes = ""
    for id in ids:
        recipe = rdao.get_recipe_by_id(id[0]) 
        if recipe:
            recipes = recipes + f"{recipe.name}|{recipe.description}|{recipe.creator}|{recipe.id}|||"
    return recipes

'''
Add a recipe to be a users favourite.

Added by clicking star on recipe page through XHR request.
'''
@app.route("/account/<user>/<recipeName>/favourites/add", methods=['PUT'])
def favourite_add(user, recipeName):
    if request.method == 'PUT':
        udao = UserDAO()
        valid_key = udao.check_user_session_key(request.cookies.get("user"), request.cookies.get("session_key"))

        if valid_key:
            recipe_id = request.args.get("recipe")
            print(recipe_id)
            fdao = FavouriteDAO()
            result = "Y" if fdao.add_favourite(request.cookies.get("user"), recipe_id) else "N"
            return result
        
        return "N"

'''
Delete a recipe to be a users favourite.

Deleted by clicking star on recipe page through XHR request.
'''
@app.route("/account/<user>/<recipeName>/favourites/delete/<recipeID>", methods=['DELETE'])
def favourite_delete(user, recipeName, recipeID):
    if request.method == 'DELETE':
        udao = UserDAO()
        valid_key = udao.check_user_session_key(request.cookies.get("user"), request.cookies.get("session_key"))

        if valid_key:
            fdao = FavouriteDAO()
            result = "Y" if fdao.delete_favourite(request.cookies.get("user"), recipeID) else "N"
            return result

    return "N"

'''
Allows users to change their current settings, if email auth is enabled have to
enter a code that is sent to the email linked to the account.

GET --:--
signedIn : To decide what the header should include in it.
user :     To add a link to the header for the users account and 
           potential avatar for user in the future.
alert :    Show alert when changing details and entering auth code.
userobj :  Complete User object for the Users settings.

POST --:--
If the input code is equal to the one sent to the email the users is
granted access to the settings page.
'''
@app.route("/account/<user>/settings", methods=['GET', 'POST'])
def account_settings(user):
    if request.method == 'GET':
        udao = UserDAO()
        valid_key = udao.check_user_session_key(user, request.cookies.get("session_key"))

        if valid_key:
            alertParam = request.args.get("alert")
            alert = None

            if alertParam:
                alertData = urllib.parse.unquote(alertParam)
                alertData = alertData.split("|")
                alert = Alert(alertData[0], alertData[1], alertData[2])
            
            u = udao.get_user(user)

            if u.email_auth == 1 and u.can_edit_settings == 0 and not alertParam:
                eh = EmailHandler(u.email)
                code = eh.send_settings_code()
                if code:
                    udao.set_user_settings_code(u.id, code)

            return render_template("settings.html",
                                    signedIn = request.cookies.get("signedIn"),
                                    user = request.cookies.get("user"),
                                    alert = alert,
                                    userobj = u)
        else:
            return "Not Your Page to Edit"
    elif request.method == 'POST':
        inputted_code = request.form['email_auth']
        udao = UserDAO()
        actual_code = udao.get_user_settings_code(user)

        if inputted_code == actual_code:
            udao.allow_edit_settings(user)
            return redirect(f"/account/{user}/settings")
        return redirect(f"/account/{user}/settings?alert=Incorrect Code!|Try inputting the code again.|alert-fail")

'''
Changes the users password if they supply the correct password for the account.
'''
@app.route("/account/<user>/settings/changepassword", methods=['POST'])
def change_password(user):
    if request.method == 'POST':
        ldao = LogDAO()
        udao = UserDAO()
        valid_key = udao.check_user_session_key(user, request.cookies.get("session_key"))

        if valid_key:
            cur_password = request.form['current_pass']
            new_password = request.form['new_pass']

            creds_correct = udao.check_users_password_matches(user, cur_password)
            if not creds_correct:
                ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_PASSWORD_CHANGE, 0)
                return redirect(f"/account/{user}/settings?alert=Password change failed!|The current password you entered was incorrect.|alert-fail")
            
            udao.update_password(user, new_password)
            ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_PASSWORD_CHANGE, 1)
            return redirect(f"/account/{user}/settings?alert=Password changed!|Password has been changed to new password.|alert-suc")
        
        ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_PASSWORD_CHANGE, 0)
        return redirect(f"/account/{user}/settings?alert=Password change failed!|Something with your details is incorrect.|alert-fail")

'''
Activates email authentication for a given account if the password for the account is correct.
'''
@app.route("/account/<user>/settings/enableemailauth", methods=['POST'])
def change_email_auth(user):
    if request.method == 'POST':
        ldao = LogDAO()
        udao = UserDAO()
        valid_key = udao.check_user_session_key(user, request.cookies.get("session_key"))

        if valid_key:
            email = request.form['email']
            cur_password = request.form['email_pass']

            creds_correct = udao.check_users_password_matches(user, cur_password)

            if not creds_correct:
                ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_EMAIL_AUTH_ENABLE, 0)
                return redirect(f"/account/{user}/settings?alert=Email authentication change failed!|The password you entered is incorrect.|alert-fail")
    
            udao.enable_email_auth(user, email)
            ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_EMAIL_AUTH_ENABLE, 1)
            return redirect(f"/account/{user}/settings?alert=Email authentication updated!|Successfully changed the status of your email authentication.|alert-suc")

    ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_EMAIL_AUTH_ENABLE, 0)
    return redirect(f"/account/{user}/settings?alert=Email authentication change failed!|Something with your details is incorrect.|alert-fail")

'''
Changes a user email if they have the correct password.
'''
@app.route("/account/<user>/settings/changeemail", methods=['POST'])
def change_email(user):
    if request.method == 'POST':
        ldao = LogDAO()
        udao = UserDAO()
        valid_key = udao.check_user_session_key(request.cookies.get("user"), request.cookies.get("session_key"))

        if valid_key:
            email = request.form['email']
            cur_password = request.form['email_pass']

            creds_correct = udao.check_users_password_matches(user, cur_password)

            if not creds_correct:
                ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_EMAIL_AUTH_CHANGE, 0)
                return redirect(f"/account/{user}/settings?alert=Email change failed!|The password you entered is incorrect.|alert-fail")

            udao.change_email(user, email)
            ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_EMAIL_AUTH_CHANGE, 1)
            return redirect(f"/account/{user}/settings?alert=Email updated!|Successfully changed email linked to your account.|alert-suc")

        ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_EMAIL_AUTH_CHANGE, 0)
        return redirect(f"/account/{user}/settings?alert=Email authentication change failed!|Something with your details is incorrect.|alert-fail")

'''
Set a users background for account page only.
'''
@app.route("/account/<user>/settings/changebackground", methods=['POST'])
def set_background(user):
    if request.method == 'POST':
        ldao = LogDAO()
        file = request.files['bgr']

        if file.filename.endswith(".jpg") | file.filename.endswith(".png") | file.filename.endswith(".svg") | file.filename.endswith(".jpeg"):
            pass
        else:
            ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_USER_BGR_CHANGE, 0)
            return redirect(f"/account/{user}/settings?alert=Background update failed!|Unsupported image type uploaded.|alert-fail")

        file_path = f"static/images/{user}/background.{file.filename.split('.')[-1]}"

        if not os.path.isdir(f"static/images/{user}"):
            os.mkdir(f"static/images/{user}")

        file.save(file_path)
        udao = UserDAO()
        udao.update_user_background(user, "/"+ file_path)
        ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_USER_BGR_CHANGE, 1)
        return redirect(f"/account/{user}/settings?alert=Background updated!|Successfully updated your background image.|alert-suc")

'''
Delete users account, recipes, favourites and all other attached data will be deleted
by a Job Scheduler at the end of each day to tidy database.
'''
@app.route("/account/<user>/delete", methods=['GET'])
def delete_user(user):
    if request.method == 'GET':
        ldao = LogDAO()
        udao = UserDAO()
        valid_key = udao.check_user_session_key(user, request.cookies.get("session_key"))

        if valid_key:
            udao.delete_user(user)
            resp = make_response(redirect("/"))
            resp.delete_cookie("signedIn")
            resp.delete_cookie("user")
            resp.delete_cookie("session_key")
            return resp
    
        ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_DEL_ACCOUNT, 0)
        return redirect(f"/account/{user}/settings?alert=Account Delete Failed|Unable to delete your account.|alert-fail")

'''
Reset a users password.

GET --:--
email : Accessed via XHR request and used to send an email to the specifed email.
code : code that was sent in email, usually navigated to through link in email.

POST --:--
Resets password based on the given code.
'''
@app.route("/resetpassword", methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':

        email = request.args.get("email")
        code = request.args.get("code")

        if email:
            eh = EmailHandler(email)
            code = eh.send_reset_link()
            udao = UserDAO()
            udao.update_password_reset_link(email, code)
        elif code:
            return render_template("resetpassword.html",
                                    signedIn = request.cookies.get("signedIn"),
                                    code = code)

        return render_template("resetpassword.html",
                                signedIn = request.cookies.get("signedIn"),
                                code = None)
    elif request.method == 'POST':
        password = request.form['pass']
        code = request.args.get("code")
        udao = UserDAO()
        ldao = LogDAO()
        success = udao.reset_password(code, password)

        if success:
            ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_PASSWORD_RESET, 1)
            return redirect("/?alert=Successfully changed password!|Password has been changed for the specified account, sign in with your new details|alert-suc")
        
        ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_PASSWORD_RESET, 1)
        return redirect("/?alert=Password change unsuccessful!|Some of the details you input must have been inccorect.|alert-fail")

'''
Subscribe to a specific users page.
Accessed via XHR request however a creator could put their subscribe link
in a description as well.
'''
@app.route("/account/<user>/subscribe", methods=['GET'])
def subscribe(user):
    if request.method == 'GET':
        udao = UserDAO()
        valid_key = udao.check_user_session_key(request.cookies.get("user"), request.cookies.get("session_key"))

        if valid_key:
            sdao = SubscribeDAO()
            sdao.subscribe(request.cookies.get("user"), user)
    
    return redirect(f"/account/{user}")

'''
Unsubscribe from a specific users page.
'''
@app.route("/account/<user>/unsubscribe", methods=['GET'])
def unsubscribe(user):
    if request.method == 'GET':
        udao = UserDAO()
        valid_key = udao.check_user_session_key(request.cookies.get("user"), request.cookies.get("session_key"))

        if valid_key:
            sdao = SubscribeDAO()
            sdao.unsubscribe(request.cookies.get("user"), user)
    
    return redirect(f"/account/{user}")

'''
Get all recipes for a user based on their subscriptions.
Got through XHR request and displayed in the 'Subscribed' tab of the account page.
'''
@app.route("/account/<user>/subscribed")
def subscribed(user):
    sdao = SubscribeDAO()
    subbed_ids = tuple([x[0] for x in sdao.get_subscribed_pages_for_user(user)])
    print(subbed_ids)

    rdao = RecipeDAO()
    recipe_ids = rdao.get_subscribed_recipes(subbed_ids)
    recipes = ""
    for id in recipe_ids:
        recipe = rdao.get_recipe_by_id(id) 
        if recipe:
            recipes = recipes + f"{recipe.name}|{recipe.description}|{recipe.creator}|{recipe.id}|||"
    return recipes

'''
Adds a new comment to a recipe, done through XHR request.
'''
@app.route("/account/<user>/<recipeName>/addcomment", methods=['GET'])
def addComment(user, recipeName):
    if request.method == 'GET':
        ldao = LogDAO()
        udao = UserDAO()
        valid_key = udao.check_user_session_key(request.cookies.get("user"), request.cookies.get("session_key"))

        if valid_key:
            comment = request.args.get("comment")

            if (comment):
                cdao = CommentDAO()
                cdao.add_comment(request.cookies.get("user"), user, recipeName, comment)
                ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_ADD_COMMENT, 1)
                return "Y"

        ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_ADD_COMMENT, 1)        
        return "N"

'''
Removes an exisitng comment from a recipe, done through XHR request.
'''
@app.route("/account/<user>/<recipeName>/removecomment", methods=['GET'])
def removeComment(user, recipeName):
    if request.method == 'GET':
        ldao = LogDAO()
        udao = UserDAO()
        valid_key = udao.check_user_session_key(request.cookies.get("user"), request.cookies.get("session_key"))

        if valid_key:
            cdao = CommentDAO()
            result = cdao.remove_comment(request.cookies.get("user"), user, recipeName)

            if result:
                ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_DEL_COMMENT, 1)
                return "Y"

        ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_DEL_COMMENT, 0)
        return "N"

'''
Edits an existing comment on a recipe, done through XHR request.
'''
@app.route("/account/<user>/<recipeName>/editcomment", methods=['GET'])
def editComment(user, recipeName):
    if request.method == 'GET':
        ldao = LogDAO()
        udao = UserDAO()
        valid_key = udao.check_user_session_key(request.cookies.get("user"), request.cookies.get("session_key"))

        if valid_key:
            comment = request.args.get("comment")

            if comment:
                cdao = CommentDAO()
                result = cdao.edit_comment(request.cookies.get("user"), user, recipeName, comment)
                if result:
                    ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_EDIT_COMMENT, 1)
                    return "Y"
                    
        ldao.add_log(request, request.cookies.get("user"), ldao.REQUEST_EDIT_COMMENT, 0)
        return "N"

'''
Adds, edits and removes rating, hard work done in CommentsDAO, done through XHR request.
'''
@app.route("/account/<user>/<recipeName>/addrating", methods=['GET'])
def addRating(user, recipeName):
    if request.method == 'GET':
        udao = UserDAO();
        valid_key = udao.check_user_session_key(request.cookies.get("user"), request.cookies.get("session_key"))

        if valid_key:
            comment_id = request.args.get("cid")
            rating = request.args.get("r")
            if comment_id and rating:
                cdao = CommentDAO()
                result = cdao.add_comment_rating(request.cookies.get("user"), comment_id, int(rating))
                return str(result)
        return "N"

@app.route("/logs", methods=['GET'])
def logs():
    if request.method == 'GET':
        udao = UserDAO()
        admin = udao.check_admin(request.cookies.get("user"), request.cookies.get("session_key"))

        if admin: 
            ldao = LogDAO()
            logs = ldao.get_logs(None, None, None, None, None)

            return render_template("logs.html",
                                    logs = logs,
                                    signedIn = request.cookies.get("signedIn"),
                                    user = request.cookies.get("user"))
        return "ACCESS DENIED"

@app.route("/logs/filter", methods=['GET'])
def logFilter():
    if request.method == 'GET':
        udao = UserDAO()
        admin = udao.check_admin(request.cookies.get("user"), request.cookies.get("session_key"))

        if admin:
            ret_data = ""
            ldao = LogDAO()
            _type = request.args.get("type")
            status  = request.args.get("status")
            url = request.args.get("url")
            ip = request.args.get("ip")
            user_agent = request.args.get("user-agent")

            logs = ldao.get_logs(_type, status, url, ip, user_agent)

            for log in logs:
                ret_data += f"""
                            <tr>
                                <td>{log.id}</td>
                                <td>{log.user_id}</td>
                                <td>{log.type}</td>
                                <td>{log.ip}</td>
                                <td>{log.port}</td>
                                <td>{log.url}</td>
                                <td>{log.date}</td>
                                <td>{log.status}</td>
                                <td>{log.user_agent}</td>
                                <td>{log.host}</td>
                            </tr>
                            """
            
            return ret_data
        return "N"

@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html")

if __name__ == "__main__":
    app.run(debug=True)