from email.utils import parseaddr
import json
from operator import and_
from flask import Flask, Response, jsonify, request
from Authentication.src.authentication.authentication_controller import AuthenticationController
from commons.models import database, User, UserRole
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

    result = AuthenticationController.register(
        forename=forename, surname=surname,
        email=email, password=password,
        isCustomer=isCustomer)

    return Response(result[1], http.HTTPStatus.OK if result[0] else http.HTTPStatus.BAD_REQUEST)


jwt = JWTManager(application)


@application.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    emailEmpty = len(email) == 0
    passwordEmpty = len(password) == 0

    if (emailEmpty or passwordEmpty):
        return Response("All fields required!", status=400)

    user = User.query.filter(
        and_(User.email == email, User.password == password)).first()

    if (not user):
        return Response("Invalid credentials!", status=400)

    additionalClaims = {
        "forename": user.forename,
        "surname": user.surname,
        "roles": [str(role) for role in user.roles]
    }

    accessToken = create_access_token(
        identity=user.email, additional_claims=additionalClaims)
    refreshToken = create_refresh_token(
        identity=user.email, additional_claims=additionalClaims)

    return jsonify(accessToken=accessToken, refreshToken=refreshToken)


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

    return Response(create_access_token(identity=identity, additional_claims=additionalClaims), status=200)


if (__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5002)
