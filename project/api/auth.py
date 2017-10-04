from apistar import http
from pymongo.errors import DuplicateKeyError
from apistar import Response
from project.config import db
from project.api.base import auth, error, format_json, encode_token
from jsonschema import validate, ValidationError
import hashlib


schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 6, "required": True},
        "password": {"type": "string", "required": True},
        "firstName": {"type": "string", "required": True},
        "lastName": {"type": "string", "required": True},
        "address": {"type": "string", "required": True},
        "city": {"type": "string", "required": True},
        "group": {"type": "number", "required": True},
    }
}


def register(data: http.RequestData) -> Response:
    try:
        validate(data, schema)
        db.user.insert(data)
    except DuplicateKeyError:
        return error(400, {'error': 'username already exists'})
    except ValidationError:
        return error(400, {'error': 'wrong json schema'})
    return Response(format_json(True, 'Success'), status=200, headers={})


def login(authorization: http.Header) -> Response:
    cred = auth(authorization)
    try:
        username, password = cred.split(':')
    except AttributeError:
        return cred

    pwd = hashlib.sha1(password.encode('utf-8')).hexdigest()
    cursor = db.user.find({'username': username, 'password': pwd}, {'_id': False, 'username': 1, 'password': 1, 'group': 1})
    if cursor.count() == 1:
        return Response(format_json(True, {'token': encode_token(cursor[0])}), status=200, headers={})
    return error(401, {'error': 'wrong credential'})