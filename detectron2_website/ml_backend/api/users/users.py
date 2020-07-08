from flask import Blueprint, g
from flask import request
from flask import jsonify, abort
from flask_cors import CORS

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from itsdangerous import BadSignature, SignatureExpired

from api import mongo, auth
from .usermodel import User

users = Blueprint('users', __name__)
CORS(users)


    
@users.route("", methods=["GET"])
def index():
    return jsonify({"successful": True})


@users.route('', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if username is None or password is None:
        res = jsonify({
            "successful": False,
            "message": "The username or password was not provided"
        })
        return (res, 400)
    
    user = User.register(username, password)

    if not(user):
        res = jsonify({
            "successful": False, 
            "message": "User already exists"
        })
        return (res, 400)

    token = user.generate_auth_token(600).decode('ascii')
    res = jsonify({
        "successful": True,
        "username": user.username,
        "token": token,
        "duration": 600
    })

    res.set_cookie('token', token)
    return res


@users.route("/signin", methods=["GET"])
@auth.login_required
def get_token():
    token = g.user.generate_auth_token(600)
    res = jsonify({
        "successful": True, 
        "token": token.decode('ascii'), 
        "duration": 600
    })
    res.set_cookie('token', token, httponly=True)
    return res



@users.route("/gettestresource", methods=["GET"])
@auth.login_required
def get_test_resource():
    res = jsonify({
        "successful": True
    })
    return res




