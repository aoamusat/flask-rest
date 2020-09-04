from flask import request, jsonify
import jwt
from app import app
from app.models import User


# A decorator to check and verify access token from request header 
def token_required(f): 
    def decorator(): 
        token = None
        # check if JWT is in request header 
        if 'x-access-token' in request.headers: 
            token = request.headers['x-access-token'] 
        
        # return 401 if token is not present 
        if not token: 
            return (jsonify({'message': 'Missing access token!'}), 401)

        try: 
            # decoding the payload to extract user credentials 
            data = jwt.decode(token, app.config['SECRET_KEY']) 
            current_user = User.query.filter_by(api_key = data['api_key']).first() 
        except: 
            return jsonify({'message' : 'Invalid access token!'}), 401
        
        # returns the decorated function 
        return f() 
    
    return decorator
