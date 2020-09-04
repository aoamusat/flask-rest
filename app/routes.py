from flask import request, flash, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets, jwt, uuid, os
from app import app, db
from app.models import User
from app.helpers import token_required


@app.route('/register', methods =['POST']) 
def register(): 
    # fetch the request payload
    data = request.get_json() 
   
    # gets name, email and password 
    name, email = data.get('name'), data.get('email') 
    password = data.get('password') 
   
    # checking for existing user 
    user = User.query.filter_by(email = email).first() 
    if not user: 
        user = User( 
            api_key = str(uuid.uuid4()), 
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


@app.route('/login', methods =['POST']) 
def login(): 
	# get user payload
	data = request.get_json() 

	if not data or not data.get('email') or not data.get('password'): 
		# returns 401 if any email or / and password is missing 
		return make_response( 
			jsonify({'message':"Verification failed!"}), 
			401, 
			{'WWW-Authenticate' : 'Basic realm ="Login required !!"'} 
		) 

	user = User.query.filter_by(email = data.get('email')).first() 

	if not user: 
		# returns 404 if user does not exist 
		return make_response( 
			jsonify({'message':"User Not Found!"}), 
			404, 
			{'WWW-Authenticate' : 'Basic realm ="Login required !!"'} 
		) 

	if check_password_hash(user.password, data.get('password')): 
		# generates the JWT Token using api_key and secret key
		token = jwt.encode({ 
			'api_key': user.public_key, 
			'exp' : datetime.utcnow() + timedelta(minutes = 30) 
		}, app.config['SECRET_KEY']) 

		return make_response(jsonify({'access_token' : token.decode('UTF-8')}), 201) 
	
    # returns 403 if password is wrong 
	return make_response( 
        jsonify({'message':"Invalid Email/Password"}), 
        403, 
        {'WWW-Authenticate' : 'Basic realm ="Invalid login details!!"'} 
    )


@app.route('/posts', methods=['GET'])
@token_required
def posts():
    post_list = [
        "dasdasda",
        "asdasdasdas"
    ]

    return make_response( 
        jsonify({'message':"OK!", 'posts': post_list}), 200
    ) 