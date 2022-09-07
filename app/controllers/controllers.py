from app import app
from flask import request, session, redirect, render_template, flash
from app.config.config import urls
from app.models.database import DbConnection

DbConnector = DbConnection()

@app.route(urls['index'])
def get_index():
    if "loggedin" in session:
        return render_template("index.html", username=session["username"])
    return redirect("login.html")

@app.route(urls['login'], methods=['GET', 'POST'])
def login():
    if "loggedin" in session:
        return redirect("/")
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = DbConnector.check_user(username)
        if account:
            password_rs = account['password']
            if password == password_rs:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                return redirect("/")
            else:
                flash('Incorrect User/Password')
        else:
            flash('Incorrect User/Password')
    return render_template('login.html')

@app.route(urls['register'], methods=['GET', 'POST'])
def register(): 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = DbConnector.check_user(username)
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        else:
            DbConnector.insert_user(username, password)
            flash('You have successfully registered!')
            return redirect("login.html")
    elif request.method == 'POST':
        flash('Please fill out the form!')
    return render_template("register.html")

@app.route(urls['logout'])
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect("login.html")

@app.route(urls['create'], methods = ['POST', 'GET'])
def get_create():
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            DbConnector.insert_user(username, password)
            return redirect('create.html')
        except:
            flash('¡Ah ocurrido un error!')
            return redirect('create.html')
    if request.method == "GET":
        return render_template('create.html')

@app.route(urls['read'], methods = ['GET'])
def get_read():
    rows = DbConnector.concat_read()
    return render_template('read.html', data=rows)

@app.route(urls['update'], methods = ['POST', 'GET'])
def get_update():
    if request.method == "GET":
        rows = DbConnector.concat_update()
        return render_template('update.html', data=rows)
    if request.method == "POST":
        try:
            id = request.form["id"]
            username = request.form["username"]
            password = request.form["password"]
            DbConnector.update_user(id, username, password)
            return redirect('update.html')
        except:
            flash('¡Ah ocurrido un error!')
            return redirect('update.html')

@app.route(urls['delete'], methods = ['POST', 'GET'])
def get_delete():
    if request.method == "GET":
        rows = DbConnector.concat_delete()
        return render_template('delete.html', data=rows)
    if request.method == "POST":
        try:
            id = request.form["id"]
            DbConnector.delete_user(id)
            return redirect('delete.html')
        except:
            flash('¡Ah ocurrido un error!')
            return redirect('delete.html')
