from flask_app import app
from flask_app.models.merch import Merch
from flask import redirect,render_template,session,request,flash , url_for
from flask_app.models.artist import Artists
from flask_app.models.order import Orders
from flask_app.models.user import Users
import os

@app.route('/orders')
def render_orders():
    status = ["proccessing","in delivery"," done"]
    if 'id' not in session :
        return redirect("/") 
    return render_template("orders.html",orders = Users.artist_order({"artist_id" : session['id']}), status = status)
@app.route("/place_order_in_cart/<int:merch_id>")
def place_order_in_cart(merch_id):
    if 'id' not in session :
        return redirect("/") 
    data = {
        "user_id" : session['id'],
        "merchandise_id" : merch_id
    }
    Orders.place_merch_in_cart(data)
    session['cart'] = True
    return redirect("/")
@app.route("/cart")
def cart():
    if 'id' not in session and not session['type'] == 'customer' :
        return redirect("/") 
    data = {
        "user_id" : session['id']
    }
    return render_template("cart.html",orders = Users.users_merch(data))
@app.route("/place_order/<int:id>") 
def place_order(id):
    if 'id' not in session :
        return redirect("/") 
    Orders.new_order({"user_id":session['id'],"artist_id":id})
    session['cart'] = False
    return redirect ("/")

@app.route("/delete_from_cart/<int:id>" ,methods = ['POST'])
def delete_from_cart(id):
    if 'id' not in session :
        return redirect("/") 
    Orders.delete_from_cart({"cart_order_id":id})
    return redirect("/cart")
@app.route("/update_status/<int:id>",methods = ['POST'])
def update_status(id):
  if 'id' not in session :
        return redirect("/") 
  data = {
      "status" : request.form['status'],
      "id" : id
  } 
  Orders.update_status(data) 
  return redirect("/orders")

