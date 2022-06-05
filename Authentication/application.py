import logging
from time import sleep
from flask import Flask, Response, jsonify, request
from authentication_controller import AuthenticationController
from Commons.exceptions import BadRequestException
from Commons.role_checker import role_check
from Authentication.models import database
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
from Authentication.configuration import Configuration
import http
from sqlalchemy_utils import database_exists, create_database
from database_init import init_db

application = Flask(__name__)
application.config.from_object(Configuration)

application.logger.setLevel(logging.INFO)


@application.route('/')
def index():
    return 'Hello from the Authentication Service'


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
@role_check(role="admin")
def delete():
    email = request.json.get("email", "")

    try:
        AuthenticationController.delete(email=email)
    except BadRequestException as ex:
        return jsonify(message=str(ex)), http.HTTPStatus.BAD_REQUEST

    return Response(status=http.HTTPStatus.OK)


if (__name__ == "__main__"):
    done = False
    initRequired = True
    while(not done):
        try:
            if (not database_exists(application.config["SQLALCHEMY_DATABASE_URI"])):
                create_database(application.config["SQLALCHEMY_DATABASE_URI"])
            else:
                initRequired = False

            done = True
        except Exception as ex:
            application.logger.info(
                "Database didn't respond. Try again in 1 sec.")
            sleep(1)

    application.logger.info("Authorization service is starting")
    database.init_app(application)

    if(initRequired):
        application.logger.info(
            "Database was found empty. Initalization process starting")
        init_db(application)

    application.run(debug=True, host="0.0.0.0", port=5002)
