from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash,request
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Artists:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM artists"
        user_data = connectToMySQL("Pazaar").query_db(query)
        user_row = []
        for user in user_data:
            user_row.append(cls(user))
        return user_row
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM artists WHERE id = %(id)s"
        user_data_with_id = connectToMySQL("Pazaar").query_db(query,data)
        return cls(user_data_with_id[0]) if user_data_with_id else None
    
    @classmethod 
    def save(cls,data):
        query = "INSERT INTO artists(name,email,password) VALUES(%(name)s,%(email)s,%(password)s)"
        return connectToMySQL("Pazaar").query_db(query,data)

    @classmethod 
    def get_by_email(cls,email_address):
        query = "SELECT * FROM artists WHERE email = %(email_address)s"
        result = connectToMySQL('Pazaar').query_db(query,{"email_address" :email_address})
        return cls(result[0]) if result else None
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