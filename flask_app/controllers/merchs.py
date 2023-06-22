from flask_app import app
from flask_app.models.merch import Merch
from flask import redirect,render_template,session,request,flash , url_for
from flask_app.models.user import Users
from flask_app.models.order import Orders
from flask_app.models.artist import Artists

import os


@app.route("/")
def main():
    return render_template("index.html",merchs = Merch.get_merch())

@app.route("/add_merch" ,methods= ['POST'])
def add_merch():
    if not 'id' in session or not session['type'] == 'artist':
        return redirect("/")
    file = request.files['file']
    data ={
            "title" : request.form['title'],
            "price" : request.form['price'],
            "artist_id" : session['id'],
            "file_name" : file.filename
        }
    if not Merch.merch_validation(data,file):
        return redirect("/add_merch/form")
    Merch.file_upload(file)
    Merch.save_merch(data)
    return redirect("/artist_merch")
    
@app.route("/add_merch/form")
def render_add_merch():
    if not 'id' in session or not session['type'] == 'artist':
        return redirect("/")
    return render_template("add_merch.html")


@app.route("/delete_merch/<int:id>", methods = ['POST'])
def destroy_merch(id):
    if not 'id' in session or not session['type'] == 'artist':
        return redirect("/artist_merch")
    data = {
        "id" : id
    }

    Merch.destroy_merch(data)
    return redirect("/")

@app.route("/edit_merch/form/<int:id>")
def render_edit_merch(id):   
    
    if not 'id' in session or not session['type'] == 'artist':
        return redirect("/")
    data = {
    "id" : id
}

    merch = Merch.one_merch(data)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'],f'{merch.img}')
    print(file_path)
    return render_template("edit_merch.html", merch = merch,file_path = file_path)

@app.route("/edit_merch/<int:id>",methods=['POST'])
def edit_merch(id):
    if not 'id' in session or not session['type'] == 'artist':
        return redirect("/")
    file = request.files['file']
    data ={
            "id":id,
            "title" : request.form['title'],
            "price" : request.form['price'],
            "artist_id" : session['id'],
            "file_name" :file.filename
        }
    if not Merch.merch_validation(data,file):
        return redirect("/add_merch/form")
    if not 'id' in session and not session['type'] == 'artist':
        return redirect("/")
    Merch.edit_merch(data)
    return redirect("/")