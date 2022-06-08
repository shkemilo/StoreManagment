import http
import logging
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required

from Commons.role_checker import role_check
from Store.Admin.admin_controller import AdminController
from Store.Admin.configuration import Configuration
from Store.Commons.models import database


application = Flask(__name__)
application.config.from_object(Configuration)
application.logger.setLevel(logging.INFO)

jwt = JWTManager(application)


@application.route('/')
def index():
    return 'Hello from the Admin Service!'


@application.route('/productStatistics', methods=['GET'])
@jwt_required()
@role_check(role="admin")
def productStatistics():
    result = AdminController.productStatistics()

    return jsonify(statistics=result), http.HTTPStatus.OK


@application.route('/categoryStatistics', methods=['GET'])
@jwt_required()
@role_check(role="admin")
def categoryStatistics():
    result = AdminController.categoryStatistics()

    return jsonify(statistics=result), http.HTTPStatus.OK


if (__name__ == "__main__"):
    application.logger.info("Admin service is starting")

    database.init_app(application)

    application.run(debug=True, host="0.0.0.0", port=5006)
