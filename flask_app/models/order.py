from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import artist,user,merch
from flask import flash

class Orders:
    def __init__ (self,data):
         self.id = data['id']
         self.inCart = data['inCart']
         self.status = data['status']
         self.user_id = data['user_id']
         self.created_at = data['created_at']
         self.updated_at = data['updated_at']
         self.total = data['total']
         self.artist_id = data['artist_id']
         self.order_merch = []
         self.artists_order =[]


    @classmethod
    def new_order(cls,data):
         query = """
         INSERT INTO orders(user_id,artist_id)
         VALUES(%(user_id)s,%(artist_id)s)
         """
         return connectToMySQL('Pazaar').query_db(query,data)
    
    @classmethod
    def place_merch_in_cart(cls,data):
         query = "INSERT INTO user_has_merchandises (user_id,merchandise_id)VALUES(%(user_id)s,%(merchandise_id)s)"      
         return connectToMySQL('Pazaar').query_db(query,data)
    
    @classmethod
    def artist_order(cls,data):
        query = """
      SELECT * FROM orders
      JOIN users ON users.id = orders.user_id
        LEFT JOIN  user_has_merchandises ON user_has_merchandises.user_id = orders.user_id 
        LEFT JOIN merchandises ON merchandises.id = user_has_merchandises.merchandise_id
        WHERE merchandises.artist_id = %(id)s
        """
        merchs_by_user = connectToMySQL('Pazaar').query_db(query,data)
        if merchs_by_user:
            merchs = cls(merchs_by_user[0])
            for item in merchs_by_user:
                merch_data = {
                    "id" : item['merchandises.id'],
                    "title" :item['title'],
                    "created_at" : item['merchandises.created_at'],
                    "updated_at" : item['merchandises.updated_at'],
                    "artist_id" : item['artist_id'],
                    "img" : item['img'],
                    "price" : item['price']
                }
                artist_data = {
                    "id" : item['users.id'],
                    "name" : item['name'],
                    "email" : item['email'],
                    'password' : "",
                    "created_at" : item['users.created_at'],
                    "updated_at" : item['users.updated_at'],
                }   
               
                merch_obj = merch.Merch(merch_data)
                merch_obj.artist_by_merch.append(user.Users(artist_data))
                merchs.artists_order.append(merch_obj)
            return merchs
        return None
    
    @classmethod 
    def delete_from_cart(cls,data):
         query = "DELETE FROM user_has_merchandises WHERE Merchandise_id = %(cart_order_id)s"
         return connectToMySQL('Pazaar').query_db(query,data)
    
    @classmethod
    def update_status(cls,data) : 
         query = "UPDATE orders SET status = %(status)s WHERE id =%(id)s"
         return connectToMySQL('Pazaar').query_db(query,data)
    
    @classmethod
    def one_order(cls,data):
         query = "SELECT * FROM orders WHERE id = %(id)s"
         result =  connectToMySQL('Pazaar').query_db(query,data)
         return cls(result[0]) if result else None



