from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class pie:
    db_name = 'pies_db'
    def __init__( self , data ):
        self.id = data['id']

        self.user_id = data['user_id']
        self.name = data['name']
        self.filling = data['filling']
        self.crust = data['crust']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_pie_by_id(cls, data):
        query = "SELECT * FROM pies LEFT JOIN users ON pies.user_id = users.id WHERE pies.id = %(pie_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    #READ
    @classmethod
    def get_all(cls):
        query = "SELECT pies.id, pies.user_id, pies.name, users.first_name, users.last_name, COUNT(votes.pies_id) as num_votes FROM pies  LEFT JOIN users ON pies.user_id = users.id LEFT JOIN votes ON pies.id = votes.pies_id GROUP BY pies.id ORDER BY num_votes DESC;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db_name).query_db(query)
        # Create an empty list to append our instances of users
        pies = []
        if results:
        # Iterate over the db results and create instances of friends with cls.
            for pie in results:
                pies.append(pie)
            return pies
        return pies
    
    @classmethod
    def get_all_Pies_By_User(cls, data):
        query = "SELECT * FROM pies WHERE pies.user_id = %(user_id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db_name).query_db(query, data)
        # Create an empty list to append our instances of users
        pies = []
        if results:
        # Iterate over the db results and create instances of friends with cls.
            for pie in results:
                pies.append(pie)
            return pies
        return pies
    #CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO pies (name, filling, crust, user_id) VALUES ( %(name)s, %(filling)s,%(crust)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE pies SET name = %(name)s, filling = %(filling)s, crust = %(crust)s WHERE pies.id = %(pie_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM pies WHERE pies.id = %(pie_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #
    @classmethod
    def like(cls, data):
        query = "INSERT INTO votes (pies_id,users_id) VALUES (%(pie_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    @classmethod
    def dislike(cls, data):
        query = "DELETE FROM votes WHERE pies_id = %(pie_id)s and users_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @staticmethod
    def validate_pie(pie):
        is_valid = True
        if len(pie['name']) <2:
            flash('Pie name should be more than 2 characters!', 'namePie')
            is_valid= False
        if len(pie['filling']) <2:
            flash('Pie filling should be more than 2 characters!', 'fillingPie')
            is_valid= False
        if len(pie['crust']) <2:
            flash('Pie crust should be more than 2 characters!', 'crustPie')
            is_valid= False
        return is_valid
        