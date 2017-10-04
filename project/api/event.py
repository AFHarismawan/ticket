from apistar import http
from apistar import Response
from project.config import db
from project.api.base import check_token, format_json, error
from jsonschema import validate, ValidationError


schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "required": True},
        "venue": {"type": "string", "required": True},
        "detail": {"type": "string", "required": True},
        "layoutImage": {"type": "string", "required": True},
        "promoImage": {"type": "string", "required": True},
        "promoVideo": {"type": "string", "required": True},
        "lat": {"type": "number", "required": True},
        "lng": {"type": "number", "required": True},
        "dateStart": {"type": "string", "required": True},
        "dateEnd": {"type": "string", "required": True},
        "ticket": {
            "type": "array",
            "required": True,
            "items": {
                "type": "object",
                "required": True,
                "properties": {
                    "category": {"type": "string", "required": True},
                    "price": {"type": "number", "required": True}
                }
            }
        }
    }
}


def add_event(authorization: http.Header, data: http.RequestData) -> Response:
    cred = check_token(authorization)
    if cred == True:
        try: 
            validate(data, schema)
            db.event.insert(data)
            return Response(format_json(True, "Success"), status=200, headers={})
        except ValidationError:
            return error(400, {'error': 'wrong json schema'})
    return cred


def get_event(authorization: http.Header) -> Response:
    cred = check_token(authorization)
    if cred == True:
        return Response(format_json(True, 'Success'), status=200, headers={})
    return cred