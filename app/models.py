from app import db


class User(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True) 
    api_key = db.Column(db.String(64), unique = True) 
    name = db.Column(db.String(100)) 
    email = db.Column(db.String(70), unique = True) 
    password = db.Column(db.String(80))