from multiprocessing import Queue
from config import Config
from flask import Flask
from flask_cors import CORS
from gevent import monkey, sleep

import eventlet
import eventlet.wsgi
import os, multiprocessing

# COMMON
from Common.Classes.instance import Instance
from Common.ModulesHandler import Modules_MultiProcess
# PAGE IMPORTS
from API.Settings.routes import settings_routes_app, settings_get
from API.Calibration.routes import create_calibration_route
# Sockets
from API.socket import SocketIOHandler
from API.shared_state import SharedState

MainInstance : Instance = None

def create_flask_app(manager: SharedState):
    app = Flask(__name__)

    # Initiating routes
    app.register_blueprint(settings_routes_app)
    app.register_blueprint(create_calibration_route(manager))

    CORS(app)

    @app.route("/initialise", methods=['POST'])
    def initialise():
        return {
            "settings": settings_get(),
            # "calibrations": calibration_get_all(),
        }

    return app

def run_server(manager):
    monkey.patch_all()

    try:
        # Prepping database
        MainInstance = Instance()
        MainInstance.initialise()

        managers = SharedState(manager)
        # Setting debug mode globally
        managers.set_state("debug_mode", bool(Config().get_int("DEBUG_MODE")))

        app = create_flask_app(managers.get_shared_state())

        output = Queue(maxsize=30)

        socketio_handler = SocketIOHandler()
        socketio_handler.start_server(app)
        socketio_handler.start_queue_processor(output)

        # Modules system for vision
        base_folder_path = os.path.dirname(os.path.abspath(__file__)) + "/Modules"
        modules = Modules_MultiProcess(base_folder_path, "Modules.{0}.main.{0}_Module")


        modules.initialise(None, output=output, shared_state=managers.get_shared_state())

        eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)

        while(True):
            sleep(1)
    except KeyboardInterrupt:
        pass
    # finally:
        # print("Shutting down the modules")
        # modules.shutdown()
        # print("Closing instance")
        # # MainInstance.close_instance()
        # print("Shutting down application - Good bye")
        # # MainInstance.shutdown()

        # socketio_handler.shutdown()

if __name__ == "__main__":
    print("\n\n==========================================================================\n")
    print("Main Instance of C.A.S.I\n")
    print("==========================================================================\n")
    manager = multiprocessing.Manager()
    run_server(manager)

