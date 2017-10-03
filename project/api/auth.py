from apistar import http
from pymongo.errors import DuplicateKeyError
from apistar import Response
from project.config import db, key
from project.api.base import auth, error, format_json, encode_token
import hashlib

def register(username, password, firstName, lastName, address, city, group) -> Response:
    try:
        if len(username) < 6:
            raise ValueError('username is too short')

        if len(password) < 6:
            raise ValueError('password is too short')

        db.user.insert({
            'username': username, 
            'password': password, 
            'firstName': firstName, 
            'lastName': lastName,
            'address': address,
            'city': city,
            'group': int(group)
        })
    except DuplicateKeyError:
        return error(400, {'error': 'username already exists'})
    except ValueError as e:
        return error(400, {'error': 'check your input parameters'})
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