from flask import Flask, render_template, request, make_response, redirect
from UserDAO import UserDAO
from RecipeDAO import RecipeDAO
from FavouriteDAO import FavouriteDAO
from User import User
from Alert import Alert
from Recipe import Recipe
import urllib.parse

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

        if not user:
            resp = make_response(redirect("/signup/?alert=Username is Already Taken|Try another username and sign up again.|alert-fail"))
            return resp
        else:
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
@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dao = UserDAO()
        user = dao.login_user(username, password)
        
        if user == None:
            return redirect("/?alert=Sign In Failed!|Make sure the details you entered are correct and try again.|alert-fail")
        else:
            resp = make_response(redirect("/?alert=Sign In Success|Start creating and browsing awesome recipes.|alert-suc"))
            resp.set_cookie("signedIn", "true")
            resp.set_cookie("user", user.username)
            resp.set_cookie("session_key", user.sessionKey)
            return resp

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

        if valid_session_key:
            allowEdit = True

        return render_template("account.html", signedIn = request.cookies.get("signedIn"),
                                               user = request.cookies.get("user"),
                                               recipes = recipes,
                                               allowEdit = allowEdit)

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
        
        if not recipe:
            return render_template("errors/recipe_not_found.html")

        return render_template("recipe.html", signedIn = request.cookies.get("signedIn"),
                                               user = request.cookies.get("user"),
                                               recipe = recipe,
                                               favourite = favourited)

'''
Delete recipe.

Uses users session key cookie and user cookie to determine whether or not the request
is valid. Could be used for API purposes in the future. Done through XHR request in JS.

If return Y the recipe is visibliy deleted from the users page.
'''
@app.route("/account/<user>/<recipeName>/delete", methods=['DELETE'])
def recipe_delete(user, recipeName):
    if request.method == "DELETE":
        udao = UserDAO()
        valid_key = udao.check_user_session_key(request.cookies.get("user"), request.cookies.get("session_key"))

        if valid_key: 
            dao = RecipeDAO()
            dao.delete_recipe(user, recipeName.replace("-", " "))
            return "Y"
        else: 
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
        udao = UserDAO()
        valid_key = udao.check_user_session_key(request.cookies.get("user"), request.cookies.get("session_key"))

        if valid_key:
            desc = request.args.get("desc")
            ingredients = request.args.get("ingredients")
            dao = RecipeDAO()
            dao.add_recipe(user, recipeName, desc, ingredients)
            return "Y"  
        else:
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
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html")

if __name__ == "__main__":
    app.run(debug=True)