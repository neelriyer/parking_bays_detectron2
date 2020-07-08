from flask import current_app, g
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from itsdangerous import BadSignature, SignatureExpired

from api import mongo, auth
import uuid


class User(UserMixin):

    def __init__(self, username, password_hash, _id=None):
        self.username = username
        self.password_hash = password_hash
        self._id = uuid.uuid4().hex if _id is None else _id

    def get_id(self):
        return self._id

    def save(self):
        mongo.db.users.insert({
            "username": self.username,
            "password_hash": self.password_hash,
            "_id": self._id
        })

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps({'_id': self._id})
    
    @classmethod
    def get_by_username(cls, username):
        data = mongo.db.users.find_one({"username": username})

        if data is not None:
            return cls(**data)
        
        return None
    
    @classmethod
    def get_by_id(cls, id):
        data = mongo.db.users.find_one({"_id": id})

        if data is not None:
            return cls(**data)
        
        return None

    @classmethod
    def register(cls, username, password):
        user = cls.get_by_username(username)

        if user is None:
            password_hash = generate_password_hash(password)
            new_user = cls(username, password_hash)
            new_user.save()
            return new_user

        return False

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except SignatureExpired:
            return False    
        except BadSignature:
            return False

        return User.get_by_id(data['_id'])

    @staticmethod
    def verify_user(username, password):
        user = User.get_by_username(username)
        if user is not None:
            if check_password_hash(user.password_hash, password):
                return user
        return False

    

    