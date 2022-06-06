import logging
import threading
from flask import Flask

from Store.Daemon.configuration import Configuration
from Store.Daemon.daemon_controller import DaemonController


application = Flask(__name__)
application.config.from_object(Configuration)
application.logger.setLevel(logging.INFO)

@application.route('/')
def index():
    return 'Hello from the Daemon Service!'

if (__name__ == "__main__"):
    application.run(debug=True, host="0.0.0.0", port=5004)

    productConsumerThread = threading.Thread(name="product_consumer", target=DaemonController.consumeProducts)
    productConsumerThread.setDaemon(True)
    productConsumerThread.start()