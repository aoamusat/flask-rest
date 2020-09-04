from flask import request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets, jwt, uuid, os
from app import app, db
from app.models import User
from app.helpers import token_required


@app.route('/test', methods=['GET'])
def home():
    data = request.get_json()
    return jsonify(data.get('name'))

@app.route('/register', methods =['POST']) 
def register(): 
    # creates a dictionary of the form data 
    data = request.get_json() 
   
    # gets name, email and password 
    name, email = data.get('name'), data.get('email') 
    password = data.get('password') 
   
    # checking for existing user 
    user = User.query.filter_by(email = email).first() 
    if not user: 
        user = User( 
            public_id = str(uuid.uuid4()), 
            name = name, 
            email = email, 
            password = generate_password_hash(password) 
        )

        # insert user 
        db.session.add(user) 
        db.session.commit()
        return (jsonify({'message': "User created"}), 201) 
    else: 
        # returns 202 if user already exists 
        return jsonify({'message': 'User already exists. Please Log in.'}), 202