import http
from functools import wraps
from flask import Response
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def role_check(role):
    def innerRole(function):
        @wraps(function)
        def decorator(*arguments, **keywordArguments):
            verify_jwt_in_request()
            claims = get_jwt()
            if (("roles" in claims) and (role in claims["roles"])):
                return function(*arguments, **keywordArguments)
            else:
                return Response("User not authorized for this request.", status=http.HTTPStatus.UNAUTHORIZED)

        return decorator

    return innerRole
