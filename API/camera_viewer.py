import cv2
import multiprocessing
from API.shared_state import CameraFactory
from flask import Flask, Response, render_template_string
import eventlet
import eventlet.wsgi

class CameraViewerHandler:
    def __init__(self):
        self.server_thread = None
        self.processor_thread = None
        self.shared_state = None
        self.latest_frames = {}  # Dictionary to hold the latest frames for each camera
        self.stop_event = multiprocessing.Event()  # Event to control the frame generation thread

    def start_server(self, app, shared_state: multiprocessing.managers.SyncManager.dict):
        print("Starting server")
        self.shared_state = shared_state

        # Start frame generation in a separate thread
        self.processor_thread = eventlet.spawn(self.frame_generator)
        # Use eventlet's WSGI server for async operation
        self.server_thread = eventlet.spawn(self.run_server, app)
        print("Server thread started")

    def frame_generator(self):
        while not self.stop_event.is_set():
            for camera_key in self.shared_state.keys():
                if '_camera' in camera_key:
                    with CameraFactory(camera_key, self.shared_state, read_only=True) as state:
                        _, buffer = cv2.imencode('.jpg', state.value)
                        self.latest_frames[camera_key] = buffer.tobytes()
            eventlet.sleep(0.005)  # Sleep to control frame generation frequency

    def generate_frames(self, camera_key):
        # Yield the latest frame as a byte stream in multipart format
        while not self.stop_event.is_set():
            frame = self.latest_frames.get(camera_key)
            if frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            eventlet.sleep(0.005)  # Sleep to avoid tight loop

    def run_server(self, app: Flask):
        @app.route('/video_feed/<camera_key>')
        def video_feed(camera_key):
            return Response(self.generate_frames(camera_key),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
        
        @app.route('/')
        def index():
            camera_list = [key for key in self.shared_state.keys() if '_camera' in key]
            checkboxes_html = ''.join(
                f'<input type="checkbox" class="camera-checkbox" value="{camera}" checked>{camera}<br>' for camera in camera_list
            )
            return render_template_string(f'''
            <html>
            <head>
                <title>Live Stream</title>
                <script type="text/javascript">
                    function updateCameras() {{
                        const checkboxes = document.querySelectorAll('.camera-checkbox');
                        const selectedCameras = Array.from(checkboxes)
                                                      .filter(checkbox => checkbox.checked)
                                                      .map(checkbox => checkbox.value);
                        const grid = document.getElementById('camera_grid');

                        const existingImages = grid.getElementsByTagName('img');
                        selectedCameras.forEach((camera, index) => {{
                            let img;
                            if (index < existingImages.length) {{
                                img = existingImages[index];
                                img.src = '/video_feed/' + camera + '?' + new Date().getTime();
                            }} else {{
                                img = document.createElement('img');
                                img.src = '/video_feed/' + camera + '?' + new Date().getTime();
                                img.width = 360; 
                                img.style.margin = '10px'; 
                                grid.appendChild(img); 
                            }}
                        }});

                        while (existingImages.length > selectedCameras.length) {{
                            grid.removeChild(existingImages[existingImages.length - 1]);
                        }}
                    }}

                    window.onload = function() {{
                        const checkboxes = document.querySelectorAll('.camera-checkbox');
                        checkboxes.forEach(checkbox => {{
                            checkbox.addEventListener('change', updateCameras);
                        }});
                        updateCameras(); 
                    }};
                </script>
                <style>
                    #camera_grid {{
                        display: flex;
                        flex-wrap: wrap;
                    }}
                </style>
            </head>
            <body>
                <div>{checkboxes_html}</div>
                <h2>Live Camera Feed</h2>
                <div id="camera_grid"></div>
            </body>
            </html>
            ''')

        print("Running server")
        eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5002)), app)

    def shutdown(self):
        print("Shutting down")
        self.stop_event.set()  # Signal the frame generation thread to stop
        if self.server_thread:
            self.server_thread.kill()
        if self.processor_thread:
            self.processor_thread.kill()
        print("Shutdown complete")
