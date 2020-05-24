from flask import Flask, render_template, request, make_response, redirect
from UserDAO import UserDAO
from RecipeDAO import RecipeDAO
from User import User
from Alert import Alert
import urllib.parse

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
    else:          
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

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dao = UserDAO()
        valid = dao.signup_user(username, password)

        if not valid:
            resp = make_response(redirect("/signup/?alert=Username is Already Taken|Try another username and sign up again.|alert-fail"))
            return resp
        else:
            resp = make_response(redirect("/?alert=Sign Up Success|Start creating and browsing awesome recipes.|alert-suc"))
            resp.set_cookie("signedIn", "true")
            resp.set_cookie("user", username)
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

@app.route("/signout", methods=['GET'])
def signout():
    if request.method == 'GET':
        resp = make_response(redirect("/"))
        resp.set_cookie("signedIn", "false")
        resp.delete_cookie("user")
        return resp

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
            return resp

@app.route("/searchResult", methods=['GET'])
def searchResult():
    if request.method == 'GET':
        param = request.args.get("s")

        if(param):
            param = urllib.parse.unquote(param)
            dao = RecipeDAO()
            result = dao.get_searched_recipe(str(param))
            print(result)
        return("|".join(result))

@app.route("/account/<user>", methods=['GET'])
def account(user):
    if request.method == 'GET':
        return render_template("account.html", signedIn = request.cookies.get("signedIn"),
                                               user = request.cookies.get("user"))

if __name__ == "__main__":
    app.run(debug=True)