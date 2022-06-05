import json
from turtle import ht
from flask import Flask, Response, jsonify, request
from authentication_controller import AuthenticationController
from authentication_exceptions import BadRequestException, NotAuthorizedException
from commons.models import database
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token, get_jwt, get_jwt_identity
from commons.configuration import Configuration
import http

application = Flask(__name__)
application.config.from_object(Configuration)


@application.route('/')
def index():
    return 'Hello from the Authentication Service'

# TODO: Encapsulate business logic into controller class


@application.route("/register", methods=["POST"])
def register():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")
    isCustomer = request.json.get("isCustomer", "")

    try:
        AuthenticationController.register(
            forename=forename, surname=surname,
            email=email, password=password,
            isCustomer=isCustomer)
    except BadRequestException as ex:
        return jsonify(message=str(ex)), http.HTTPStatus.BAD_REQUEST

    return Response(status=http.HTTPStatus.OK)


jwt = JWTManager(application)


@application.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    result = None
    try:
        result = AuthenticationController.login(email=email, password=password)
    except BadRequestException as ex:
        return jsonify(message=str(ex)), http.HTTPStatus.BAD_REQUEST

    return jsonify(result), http.HTTPStatus.OK


@application.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    refreshClaims = get_jwt()

    additionalClaims = {
        "forename": refreshClaims["forename"],
        "surname": refreshClaims["surname"],
        "roles": refreshClaims["roles"]
    }

    return Response(create_access_token(identity=identity, additional_claims=additionalClaims), status=http.HTTPStatus.OK)


@application.route("/delete", methods=["POST"])
@jwt_required()
def delete():
    accessClaims = get_jwt()
    roles = accessClaims["roles"]
    email = request.json.get("email", "")

    try:
        AuthenticationController.delete(roles=roles, email=email)
    except BadRequestException as ex:
        return jsonify(message=str(ex)), http.HTTPStatus.BAD_REQUEST
    except NotAuthorizedException as ex:
        return jsonify(message=str(ex)), http.HTTPStatus.UNAUTHORIZED
        
    
    return Response(status=http.HTTPStatus.OK)


if (__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5002)
