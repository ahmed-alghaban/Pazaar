from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import artist
from flask import flash,request
import os
from werkzeug.utils import secure_filename
from flask_app import app

class Merch:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.artist_id = data['artist_id']
        self.img = data['img']
        self.price = data['price']
        self.artist = None
        self.artist_by_merch = []

    @classmethod
    def get_merch(cls):
        
        query = "SELECT * FROM merchandises JOIN artists ON artists.id = merchandises.artist_id "
        merch_row = connectToMySQL('Pazaar').query_db(query)
        merch_data = []

        for merch in merch_row : 
            merchs = cls(merch)
            artist_data = {
                "id" : merch['artists.id'],
                "name" : merch['name'],
                "email" : merch['email'],
                'password' : "",
                "created_at" : merch['artists.created_at'],
                "updated_at" : merch['artists.updated_at'],
            }
            merchs.artist = artist.Artists(artist_data)
            merch_data.append(merchs)

        return merch_data
    
    @classmethod
    def save_merch(cls,data):
        query = "INSERT INTO merchandises(title,artist_id,img,price) Values(%(title)s,%(artist_id)s,%(file_name)s,%(price)s)"
        return connectToMySQL('Pazaar').query_db(query,data)
    
    @classmethod
    def one_merch(cls,data):
        query = "SELECT * FROM merchandises WHERE id =%(id)s"
        merch = connectToMySQL('Pazaar').query_db(query,data)
        return cls(merch[0]) if merch else None
    
    @classmethod
    def edit_merch(cls,data):
        query ="UPDATE merchandises set title = %(title)s ,img =%(file_name)s , price = %(price)s WHERE id=%(id)s"
        return connectToMySQL('Pazaar').query_db(query,data)
    
    @classmethod
    def destroy_merch(cls,data):
        query = "DELETE FROM merchandises WHERE id=%(id)s"
        return connectToMySQL('Pazaar').query_db(query,data)
    
    @classmethod
    def artist_merch(cls,data):
          query = "SELECT * FROM merchandises  WHERE artist_id = %(id)s "
          result = connectToMySQL("Pazaar").query_db(query,data)
          merch_row = []
          for merch in result:
            merch_row.append(cls(merch))
          return merch_row
          
        
    @staticmethod
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @staticmethod
    def file_upload(file):
        if file and Merch.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    @staticmethod
    def merch_validation(merch,file):
        price = request.form.get('price', type=float)
        isValid = True
        if len(merch['title'])  == 0:
            flash("must be at least one character")
            isValid = False
        if price is None or price < 1:
           flash("Price must be a number greater than or equal to 1")
           isValid = False
        if file.filename == '':
            flash('No selected file')
            isValid = False
        return isValid