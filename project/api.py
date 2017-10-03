from apistar import http
from pymongo.errors import DuplicateKeyError
from apistar import Response
from project.config import db, key
import base64
import hashlib
import jwt


def auth(authorization):
    if authorization is None:
        return error(401, {'error': 'unauthorized'})
    scheme, token = authorization.split()
    if scheme.lower() == 'basic':
        return base64.b64decode(token).decode('utf-8')
    elif scheme.lower() == 'bearer':
        return token
    return error(401, {'error': 'unauthorized'})


def check_token(authorization):
    cred = auth(authorization)
    try:
        data = decode_token(cred)
        cursor = db.user.find({'username': data.__getitem__('username'), 'password': data.__getitem__('password')})
        if cursor.count() == 1:
            return True
    except jwt.DecodeError:
        return error(401, {'error': 'unauthorized'})
    return error(401, {'error': 'wrong credential'})


def error(status, data):
    return Response(format_json(False, data), status=status, headers={})


def format_json(sts, msg):
    return {'status': sts, 'message': msg}


def encode_token(data):
    return jwt.encode(data, hashlib.sha1(key.encode('utf-8')).hexdigest(), algorithm='HS256').decode('utf-8')


def decode_token(encoded):
    return jwt.decode(encoded, hashlib.sha1(key.encode('utf-8')).hexdigest(), algorithms=['HS256'])


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


def event(authorization: http.Header) -> Response:
    cred = check_token(authorization)
    if cred == True:
        return Response(format_json(True, 'Success'), status=200, headers={})
    return cred


def event(authorization: http.Header) -> Response:
    cred = check_token(authorization)
    if cred == True:
        return Response(format_json(True, 'Success'), status=200, headers={})
    return cred
