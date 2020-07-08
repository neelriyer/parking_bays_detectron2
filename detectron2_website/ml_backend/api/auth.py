from flask import request, g, abort
from api import auth 
from api.users.usermodel import User

@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)

    if not user:
        cookie_token = request.cookies.get('token')
        if cookie_token:
            user = User.verify_auth_token(request.cookies.get('token'))
    if not user:
        user = User.verify_user(username_or_token, password)
    
    if not user:
        return False
    
    g.user = user
    return True

@auth.error_handler
def auth_error():
    abort(401)