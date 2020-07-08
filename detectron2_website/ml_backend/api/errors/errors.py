from flask import Blueprint
from flask import jsonify
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import Unauthorized

errorhandler = Blueprint('error_handlers', __name__)

@errorhandler.app_errorhandler(401)
def handle_unauthorised(e):
    return jsonify({
        "successful": False,
        "message": "unauthorised access"
    }), 401


@errorhandler.app_errorhandler(Exception)
def generic_handler(e):
    return jsonify({
        "successful": False,
        "message": "a problem occurred"
    }), e.code