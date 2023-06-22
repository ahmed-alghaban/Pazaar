from flask_app import app
from flask_app.models.artist import Artists
from flask import redirect,render_template,session,request,flash
from flask_app.models.merch import Merch

@app.route("/artist_merch")
def artist_merch():
    if not 'id' in session or not session['type'] == 'artist':
        return redirect("/")
    data = {
            "id" : session['id']
        }
    return render_template("artist_merch.html",merchs = Merch.artist_merch(data))