from apistar import http
from apistar import Response
from project.api.base import check_token, format_json

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