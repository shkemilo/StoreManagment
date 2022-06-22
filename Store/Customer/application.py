import http
import logging
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt

from Commons.exceptions import BadRequestException
from Commons.role_checker import role_check
from Store.Commons.models import database
from Store.Customer.configuration import Configuration
from Store.Customer.customer_controller import CustomerController


application = Flask(__name__)
application.config.from_object(Configuration)
application.logger.setLevel(logging.INFO)

jwt = JWTManager(application)


@application.route('/')
def index():
    return 'Hello from the Customer Service!'


@application.route('/search', methods=['GET'])
@jwt_required()
@role_check(role="customer")
def search():
    productName = request.args.get('name', None)
    categoryName = request.args.get('category', None)

    result = CustomerController.search(productName, categoryName)

    return jsonify(result), http.HTTPStatus.OK


@application.route('/order', methods=['POST'])
@jwt_required()
@role_check(role="customer")
def order():
    requests = request.json.get("requests", "")
    customerEmail = get_jwt()['email']

    result = None
    try:
        result = CustomerController.order(customerEmail, requests)
    except BadRequestException as ex:
        return jsonify(message=str(ex)), http.HTTPStatus.BAD_REQUEST

    return jsonify(id=result), http.HTTPStatus.OK


@application.route('/status', methods=['GET'])
@jwt_required()
@role_check(role="customer")
def status():
    customerEmail = get_jwt()['email']

    result = CustomerController.status(customerEmail)

    return jsonify(orders=result), http.HTTPStatus.OK


if (__name__ == "__main__"):
    application.logger.info("Customer service is starting")

    database.init_app(application)

    application.run(debug=True, host="0.0.0.0", port=5005)
