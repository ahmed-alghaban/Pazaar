from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash,request
from flask_app.models import order,merch,artist
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Users:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.order_collection =[]
        self.order_by_user = None
        self.merchs = None
        self.artists = None
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        user_data = connectToMySQL("Pazaar").query_db(query)
        user_row = []
        for user in user_data:
            user_row.append(cls(user))
        return user_row
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        user_data_with_id = connectToMySQL("Pazaar").query_db(query,data)
        return cls(user_data_with_id[0]) if user_data_with_id else None
    
    @classmethod 
    def save(cls,data):
        query = "INSERT INTO users(name,email,password) VALUES(%(name)s,%(email)s,%(password)s)"
        return connectToMySQL("Pazaar").query_db(query,data)

    @classmethod 
    def get_by_email(cls,email):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('Pazaar').query_db(query,{"email" :email})
        return cls(result[0]) if result else None
    
    @classmethod
    def users_merch(cls,data):
         query = """SELECT * FROM users 
         LEFT JOIN user_has_merchandises ON user_has_merchandises.user_id = users.id
         LEFT JOIN merchandises ON merchandises.id = user_has_merchandises.merchandise_id
         JOIN artists ON artists.id = merchandises.artist_id
        WHERE users.id = %(user_id)s
         """
         user_data = connectToMySQL("Pazaar").query_db(query,data)
         user_row = []
         for submited_order in user_data:
            orders = cls(submited_order)
            merch_data = {
                    "id" : submited_order['merchandises.id'],
                    "title" :submited_order['title'],
                    "created_at" : submited_order['merchandises.created_at'],
                    "updated_at" : submited_order['merchandises.updated_at'],
                    "artist_id" : submited_order['artist_id'],
                    "img" : submited_order['img'],
                    "price" : submited_order['price']
                }
            artist_data = {
                    "id" : submited_order['artists.id'],
                    "name" : submited_order['name'],
                    "email" : submited_order['email'],
                    'password' : "",
                    "created_at" : submited_order['artists.created_at'],
                    "updated_at" : submited_order['artists.updated_at'],
                }
            orders.artists = artist.Artists(artist_data)
            orders.merchs = merch.Merch(merch_data)
            user_row.append(orders)
         return user_row
    
    @classmethod
    def artist_order(cls,data):
         query = """SELECT * FROM users 
         JOIN orders ON orders.user_id = users.id
         JOIN artists ON artists.id = orders.artist_id
         LEFT JOIN user_has_merchandises ON user_has_merchandises.user_id = users.id
         LEFT JOIN merchandises ON merchandises.id = user_has_merchandises.merchandise_id
        WHERE artists.id = %(artist_id)s
         """
         user_data = connectToMySQL("Pazaar").query_db(query,data)
         user_row = []
         for submited_order in user_data:
            orders = cls(submited_order)
            order_data ={
                    "id" : submited_order['orders.id'],
                    "created_at" : submited_order['orders.created_at'],
                    "updated_at" : submited_order['orders.updated_at'],
                    "status" : submited_order['status'],
                    "artist_id" : submited_order["artist_id"],
                    "user_id" : submited_order['user_id'],
                    "inCart" :  submited_order['inCart'],
                    "total" : submited_order['total']
                }
            merch_data = {
                    "id" : submited_order['merchandises.id'],
                    "title" :submited_order['title'],
                    "created_at" : submited_order['merchandises.created_at'],
                    "updated_at" : submited_order['merchandises.updated_at'],
                    "artist_id" : submited_order['merchandises.artist_id'],
                    "img" : submited_order['img'],
                    "price" : submited_order['price']
                }
            artist_data = {
                    "id" : submited_order['artists.id'],
                    "name" : submited_order['name'],
                    "email" : submited_order['email'],
                    'password' : "",
                    "created_at" : submited_order['artists.created_at'],
                    "updated_at" : submited_order['artists.updated_at'],
                }
            orders.order_by_user = order.Orders(order_data)
            orders.artists = artist.Artists(artist_data)
            orders.merchs = merch.Merch(merch_data)
            user_row.append(orders)
         return user_row

    @staticmethod
    def user_validation(user):
        is_valid = True
        if len(user['name']) < 2 :
            flash ("name must be at least 2 charecters")
            is_valid = False

        if len(user['password']) < 8 or len(user['password']) == 0:
            flash("password must be at least 8 charecters")
            is_valid = False
            
        if  request.form['confirm'] != request.form['password']:
            flash("passwords are not matching")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid 