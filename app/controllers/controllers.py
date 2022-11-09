from app import app
from flask import render_template, request, redirect, flash
from app.config.config import urls
from app.models.database import DbConnection

DbConnector = DbConnection()

@app.route(urls['index'], methods = ['GET'])
def get_index():
    return render_template('index.html')

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
