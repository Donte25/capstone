from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.hash_password(password)

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def save(self):
        db.session.add(self)
        db.session.commit()


class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anime_name = db.Column(db.String, unique=True, nullable=False)
    genre = db.Column(db.String, nullable=False)
    episodes = db.Column(db.String, nullable=False)
    
    def __init__(self, name, genre):
        self.name = name
        self.genre = genre
        
    def save(self):
        db.session.add(self)
        db.session.commit()

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id'))

    def __init__(self, username, anime_name):
        self.username = username
        self.anime_name = anime_name
        
    
# class Message(db.Model):
#     def __init__(self):
    
# class Selection(db.Model):
#     def __init__(self):

# class Genre(db.Model):
#     def __init__(self):

