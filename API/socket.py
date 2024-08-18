import json
from flask import Flask
from flask_socketio import SocketIO
import eventlet
import eventlet.wsgi
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

class SocketIOHandler:
    def __init__(self):
        self.server_thread = None
        self.processor_thread = None
        self.socketio = None

    def start_server(self, app):
        print("Starting server")
        self.socketio = SocketIO(app, cors_allowed_origins="*")  # Initialize Socket.IO with CORS
        
        # Use eventlet's WSGI server for async operation
        self.server_thread = eventlet.spawn(self.run_server, app)
        print("Server thread started")

    def start_queue_processor(self, queue):
        print("Starting queue processor thread")
        self.processor_thread = eventlet.spawn(self.process_queue, queue)
        print("Queue processor thread started")

    def run_server(self, app: Flask):
        print("Running server")
        # Use eventlet's WSGI server to run the Flask app
        eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5001)), app)

    def process_queue(self, queue):
        print("Queue processor started")
        while True:
            if not queue.empty():
                data = queue.get(timeout=5)

                self.socketio.emit("set_data", json.dumps(data, cls=NumpyEncoder ))
                if data is None:
                    print("Stopping queue processor")
                    break
            else:
                # Sleep for a short time to prevent busy-waiting
                eventlet.sleep(0.25)  

    def shutdown(self):
        print("Shutting down")
        # Graceful shutdown logic here
        if self.server_thread:
            self.server_thread.kill()
        if self.processor_thread:
            self.processor_thread.kill()

        print("Shutdown complete")
