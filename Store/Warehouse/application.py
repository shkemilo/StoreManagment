import http
import logging
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required

from Commons.exceptions import BadRequestException
from Commons.role_checker import role_check
from Store.Warehouse.configuration import Configuration
from Store.Warehouse.warehouse_controller import WarehouseController


application = Flask(__name__)
application.config.from_object(Configuration)

jwt = JWTManager(application)
application.logger.setLevel(logging.INFO)


@application.route('/')
def index():
    return 'Hello from the Warehouse Service!'


@application.route("/update", methods=["POST"])
@jwt_required()
@role_check(role="worker")
def update():
    file = request.files['file']

    try:
        WarehouseController.update(file)
    except BadRequestException as ex:
        return jsonify(message=str(ex)), http.HTTPStatus.BAD_REQUEST
    
    return http.HTTPStatus.OK


if (__name__ == "__main__"):
    application.run(debug=True, host="0.0.0.0", port=5003)
