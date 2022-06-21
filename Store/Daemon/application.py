import logging
import threading
from time import sleep
from flask import Flask
from sqlalchemy_utils import database_exists, create_database

from Store.Commons.models import database
from Store.Daemon.database_init import init_db
from Store.Daemon.configuration import Configuration
from Store.Daemon.daemon_controller import DaemonController


application = Flask(__name__)
application.config.from_object(Configuration)
application.logger.setLevel(logging.INFO)


@application.route('/')
def index():
    return 'Hello from the Daemon Service!'


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

    application.logger.info("Daemon service is starting")
    database.init_app(application)

    if(initRequired):
        application.logger.info(
            "Database was found empty. Initalization process starting")
        init_db(application)

    productConsumerThread = threading.Thread(
        name="product_consumer", target=DaemonController.consumeProducts, args=(application,))
    productConsumerThread.daemon = True
    productConsumerThread.start()

    application.run(debug=False, host="0.0.0.0", port=5004)
