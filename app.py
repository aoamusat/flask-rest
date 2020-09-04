from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from  werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets, jwt, uuid
from models import User
from helpers import token_required


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)    #   generate secret key

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# creates SQLALCHEMY object 
db = SQLAlchemy(app)

@app.route('/', methods=['GET'])
def home():
    return "Home"


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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3400, debug=True)
    pass