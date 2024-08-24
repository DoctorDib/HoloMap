from multiprocessing import Queue
from flask import Flask
from flask_cors import CORS
from gevent import monkey, sleep
import sys, os

import eventlet
import eventlet.wsgi

# COMMON
from Common.Classes.instance import Instance
from Common.ModulesHandler import Modules_MultiProcess
# PAGE IMPORTS
from API.Settings.routes import settings_routes_app, settings_get
# Sockets
from API.socket import SocketIOHandler

dev_mode = len(sys.argv) > 1 and sys.argv[1] == "DEV"
MainInstance : Instance = None

def create_flask_app():
    app = Flask(__name__)
    
    # Initiating routes
    app.register_blueprint(settings_routes_app)

    CORS(app)

    @app.route("/initialise", methods=['POST'])
    def initialise():
        return {
            "settings": settings_get(),
        }

    return app

def run_server():
    monkey.patch_all()

    try:
        # Prepping database
        MainInstance = Instance()
        MainInstance.initialise()

        app = create_flask_app()

        output = Queue(maxsize=30)

        socketio_handler = SocketIOHandler()
        socketio_handler.start_server(app)
        socketio_handler.start_queue_processor(output)

        base_folder_path = os.path.dirname(os.path.abspath(__file__)) + "/Modules"
        modules = Modules_MultiProcess(base_folder_path, "Modules.{0}.main.{0}_Module")
        modules.initialise(None, output=output)

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
    run_server()
