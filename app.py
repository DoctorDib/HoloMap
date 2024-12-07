from multiprocessing import Queue
from Common.ModuleSharedState import ModuleSharedState
from Common.Modules_Handler import Modules_MultiProcess
from config import Config
from flask import Flask, jsonify, request
from flask_cors import CORS
from gevent import monkey, sleep

import eventlet
import eventlet.wsgi
import os, multiprocessing

# COMMON
from Common.Classes.instance import Instance
# PAGE IMPORTS
from API.Settings.routes import settings_routes_app, settings_get
from API.Calibration.routes import create_calibration_route
# Sockets
from API.socket import SocketIOHandler
from API.shared_state import DynamicFactory, ModuleSharedStateFactory, SharedState
# Debugging tools
# from Modules.Health.Plugins.HeartBeat_DebugOnly import HeartBeat_DebugOnly

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

    @app.route("/initialise-debugger", methods=['POST'])
    def initialise_debugger():
        
        interested_keys = ['PcStats', '_module']
        data = {}
        modules = {}
        keys = manager.keys()
        for key in keys:
            if any(interested_key in key for interested_key in interested_keys):
                
                value = manager[key]
                if (isinstance(value, ModuleSharedState)):
                    # Custom as I want to return module json data
                    modules[key] = value.to_json()
                else:
                    data[key] = manager[key]
                    
        return {
            "debug_mode": manager["debug_mode"],
            "start_time": manager["start_time"],
            "heartbeat": data,
            "modules": modules,
        }
        
    @app.route('/get/<cameras>', methods=['GET'])
    def get_cameras(cameras):
        active_cameras = cameras.split(",")
        
        camera_states = {}
        for active_camera in active_cameras:
            camera_states[active_camera] = manager[active_camera]
        
        return jsonify(camera_states)
    
    @app.route('/get/camera_keys', methods=['GET'])
    def get_camera_keys():
        camera_keys = []
        # Fetch all states with '_camera'
        camera_keys = []
        for key, _ in manager.items():
            if key.endswith('_camera_base64'):
                camera_keys.append(key)
        return jsonify(camera_keys)

    # Route to dynamically read a specific key from shared state
    @app.route('/read_state/<key>', methods=['GET'])
    def read_state(key):
        try:
            with DynamicFactory(key, manager, read_only=True) as state:
                if (state.value is None):
                    return jsonify({"message": f"Key '{key}' not found"}), 404
                else:
                    return jsonify({ "data": state.value, }), 200    
        except Exception as e:
            return jsonify({"message": str(e)}), 400
    
    @app.route('/list_state_keys', methods=['GET'])
    def list_state_keys():
        try:
            return jsonify({ "keys": manager.keys() }), 200    
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    # Route to dynamically write to a specific key in shared state
    @app.route('/write_state/<key>', methods=['POST'])
    def write_state(key):
        try:
            data = request.json
            with DynamicFactory(key, manager, read_only=False) as state:
                state.value = data['value']
                return jsonify({"message": f"Key '{key}' updated successfully"}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400


    # MODULE STATES
    @app.route('/get/modules', methods=['GET'])
    def get_modules():
        try:
            interested_keys = ['_module']
            
            modules = {}
            keys = manager.keys()
            for key in keys:
                if any(interested_key in key for interested_key in interested_keys):
                    value = manager[key]
                    if (isinstance(value, ModuleSharedState)):
                        # Custom as I want to return module json data
                        modules[key] = value.to_json()
                        
            return jsonify({ "modules": modules }), 200    
        except Exception as e:
            return jsonify({"message": str(e)}), 400
        
    @app.route('/get/module/<key>', methods=['GET'])
    def get_module(key):
        try:
            with ModuleSharedStateFactory(key, manager, read_only=True) as state:
                if (state.value is not None):
                    data = state.value.to_json()
                    return { key: data }, 200    
                else:
                    return jsonify({ "success": False }), 400    
        except Exception as e:
            return jsonify({"message": str(e)}), 400
        
    @app.route('/set/module/<key>', methods=['POST'])
    def set_module_value(key):
        try:
            data = request.json
            command = data['value']
            
            with ModuleSharedStateFactory(key, manager, read_only=False) as state:
                match (command):
                    case "initialise":
                        state.value.initialise()
                    case "stop":
                        state.value.stop()
                    case "pause":
                        state.value.pause()
                    case "play":
                        state.value.play()
                    case "reload":
                        state.value.reload()
                    case '_':
                        return jsonify({"message": f"{command} is not a valid command for {key}"}), 400
                        
                return jsonify({"message": f"Key '{key}' updated successfully"}), 200
                
        except Exception as e:
            return jsonify({"message": str(e)}), 400
        
        
    # CAMERAS
    @app.route('/camera_list')
    def camera_list():
        # Return the camera list as JSON
        camera_list = [key for key in manager.keys() if '_camera' in key]
        return jsonify(camera_list)

    return app

def run_server(manager):
    monkey.patch_all()

    try:
        # Prepping database
        MainInstance = Instance()
        MainInstance.initialise()

        managers = SharedState(manager)

        # Setting debug mode globally
        debug_mode = bool(Config().get_int("DEBUG_MODE"))
        managers.set_state("debug_mode", debug_mode)

        app = create_flask_app(managers.get_shared_state())

        output = Queue(maxsize=30)

        socketio_handler = SocketIOHandler()
        socketio_handler.start_server(app)
        socketio_handler.start_queue_processor(output)
        
        base_folder_path = os.path.dirname(os.path.abspath(__file__))
        main_module_processor = Modules_MultiProcess(base_folder_path, "Main.main.{0}_Module", "main", 0, output=output, shared_state=managers.get_shared_state())
        main_module_processor.initialise()
        
        # API Server
        eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
        
        try:
            while(True):
                print("A")
                sleep(1)
        except KeyboardInterrupt:
            print('interrupted!')
    except KeyboardInterrupt:
        pass
    finally:
        MainInstance.shutdown()
        # modules.shutdown()
        # print("Shutting down the modules")
        # modules.shutdown()
        # print("Closing instance")
        # # MainInstance.close_instance()
        # print("Shutting down application - Good bye")
        # # MainInstance.shutdown()
        #camera_handler.shutdown()?????

        # socketio_handler.shutdown()


if __name__ == "__main__":
    print("\n\n==========================================================================\n")
    print("Main Instance of C.A.S.I\n")
    print("==========================================================================\n")
    manager = multiprocessing.Manager()
    run_server(manager)

