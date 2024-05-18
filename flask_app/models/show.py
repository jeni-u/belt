from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash,request
from flask_app.models.user import User

class Show:
    db="users_shows_schema"
    def __init__(self,data):
        self.id=data['id']
        self.title = data['title']
        self.network=data['network']
        self.release_date=data['release_date']
        self.description=data['description']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']


    @classmethod
    def createShow(cls, data):
        query = 'INSERT INTO shows ( title, network, release_date, description, user_id) VALUES (%(title)s, %(network)s, %(release_date)s, %(description)s, %(user_id)s)';
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def getAllShows(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL(cls.db).query_db(query)
        shows = []
        if results:
            for show in results:
                shows.append(show)
        return shows
    
    @classmethod
    def get_show_by_id(cls, show_id):
        query = "SELECT * FROM shows WHERE id = %(show_id)s;"
        data = {
            'show_id': show_id
            }
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def delete_show(cls, data):
        query = "DELETE FROM shows WHERE id= %(show_id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    

    @classmethod
    def update_show(cls, data):
        query = "UPDATE shows set title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    

    @classmethod
    def delete_show(cls, data):

        query_remove_likes = 'DELETE FROM likes WHERE show_id = %(show_id)s;'
        connectToMySQL(cls.db).query_db(query_remove_likes, data)
        

        query_delete_show = 'DELETE FROM shows WHERE id = %(show_id)s;'
        return connectToMySQL(cls.db).query_db(query_delete_show, data)

    @classmethod
    def allUsers(cls, data):
        query = 'SELECT user_id FROM likes WHERE show_id = %(show_id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        usersWhoLiked = []
        if results:
            for user in results:
                usersWhoLiked.append(user['user_id'])
        return usersWhoLiked

    @classmethod
    def has_liked(cls, data):
        query = 'SELECT * FROM likes WHERE user_id = %(user_id)s AND show_id = %(show_id)s;'
        result = connectToMySQL(cls.db).query_db(query, data)
        return len(result) > 0

    @classmethod
    def like(cls, data):
        query = 'INSERT INTO likes (user_id, show_id) VALUES (%(user_id)s, %(show_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def allUsers(cls, data):
        query = 'SELECT user_id FROM likes WHERE show_id = %(show_id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        usersWhoLiked = []
        if results:
            for user in results:
                usersWhoLiked.append(user['user_id'])
        return usersWhoLiked
    
    @classmethod
    def get_likes_count(cls, data):
        query = 'SELECT COUNT(*) AS likes_count FROM likes WHERE show_id = %(show_id)s;'
        result = connectToMySQL(cls.db).query_db(query, data)
        return result[0]['likes_count']
    
    @classmethod
    def removeLike(cls,data):
        query = 'DELETE FROM likes WHERE show_id = %(show_id)s and user_id = %(user_id)s';
        return connectToMySQL(cls.db).query_db(query, data)


    @staticmethod
    def validate_show(data):
        is_valid = True
        if len(data['title']) < 3:
            flash("Title should be at least 3 characters!", 'title')
            is_valid = False
        if len(data['network']) < 3:
            flash("Network should be at least 3 characters!", 'network')
            is_valid = False
        if not data['release_date']:
            flash("You need to give a release date!", 'releaseDate')
            is_valid = False
        if not data['description']:
            flash("Give a description about the show!", 'description')
            is_valid = False
        return is_valid
    