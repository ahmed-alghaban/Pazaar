from flask_app import app
from flask_app.models.user import Users
from flask_app.models.artist import Artists
from flask import redirect,render_template,session,request,flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/register")
def render_register():
    return render_template("register.html")

@app.route("/create_user" ,methods =['POST'])
def create_user():
    id = ''
    password = bcrypt.generate_password_hash(request.form['password']) 
    data = {
        "name" : request.form['name'],
        "email" : request.form['email'],
        "password": password
    }
    if not Users.user_validation(data) or not Artists.user_validation(data):
        return redirect("/")  
      
    if request.form['type'] == "artist":
        id = Artists.save(data)
        session['id'] = id
        session['type'] = "artist"
    else:
       id = Users.save(data)
       session['id'] = id
       session['type'] = 'customer'
    return redirect("/")

@app.route("/login/form")
def render_login():
    return render_template("login.html")

@app.route("/login", methods = ['POST'])
def login():
    user = Users.get_by_email(request.form['email']) if request.form['type'] == 'customer' else Artists.get_by_email(request.form['email'])
    if not user or not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("invalid credentials")
        return redirect("/login/form")

    session['id'] = user.id 
    session['type'] = 'artist' if request.form['type'] == 'artist' else 'customer'
    return redirect("/") if session['type'] == 'customer' else redirect('/artist_merch')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")