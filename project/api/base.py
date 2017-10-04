from apistar import http
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
        cursor = db.user.find({'username': data.__getitem__('username'), 'password': data.__getitem__('password')}, {"group": 1})
        if cursor.count() == 1:
            return cursor[0].__getitem__('group')
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