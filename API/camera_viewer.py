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

    def start_server(self, app, shared_state: multiprocessing.managers.SyncManager.dict):
        print("Starting server")
        self.shared_state = shared_state
        
        # Use eventlet's WSGI server for async operation
        self.server_thread = eventlet.spawn(self.run_server, app)
        print("Server thread started")

    def start_queue_processor(self, queue):
        print("Starting queue processor thread")
        self.processor_thread = eventlet.spawn(self.process_queue, queue)
        print("Queue processor thread started")

    def generate_frames(self, camera_key):
        with CameraFactory(camera_key, self.shared_state, read_only=True) as state:
            _, buffer = cv2.imencode('.jpg', state.value)
            frame = buffer.tobytes()

            # Yield the frame as a byte stream in multipart format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def run_server(self, app: Flask):
        @app.route('/video_feed/<camera_key>')
        def video_feed(camera_key):
            # Route to serve the video stream for a specific camera
            return Response(self.generate_frames(camera_key),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
        
        @app.route('/')
        def index():

            camera_list = [key for key in self.shared_state.keys() if '_camera' in key]

            # Generate checkboxes for each camera
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

                        // Check the number of existing images
                        const existingImages = grid.getElementsByTagName('img');

                        // Update or create images based on the selected cameras
                        selectedCameras.forEach((camera, index) => {{
                            let img;

                            // If an image element already exists, update its src
                            if (index < existingImages.length) {{
                                img = existingImages[index];
                                img.src = '/video_feed/' + camera + '?' + new Date().getTime(); // Update src with new timestamp
                            }} else {{
                                // If no existing image, create a new one
                                img = document.createElement('img');
                                img.src = '/video_feed/' + camera + '?' + new Date().getTime(); // Add timestamp to URL to bypass cache
                                img.width = 360;  // Adjust width as needed
                                img.style.margin = '10px';  // Spacing between images
                                grid.appendChild(img); // Append the new image to the grid
                            }}
                        }});

                        // Remove any extra images if there are more existing images than selected cameras
                        while (existingImages.length > selectedCameras.length) {{
                            grid.removeChild(existingImages[existingImages.length - 1]);
                        }}
                    }}

                    // Call updateCameras on checkbox change
                    window.onload = function() {{
                        const checkboxes = document.querySelectorAll('.camera-checkbox');
                        checkboxes.forEach(checkbox => {{
                            checkbox.addEventListener('change', updateCameras);
                        }});
                        updateCameras();  // Initialize grid with selected cameras

                        // Set an interval to refresh camera images every second
                        setInterval(updateCameras, 200); // Refresh every second
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
                <h1>Select Cameras to View</h1>
                <div>
                    {checkboxes_html}
                </div>
                <h2>Live Camera Feed</h2>
                <div id="camera_grid"></div>
            </body>
            </html>
            ''')

        print("Running server")
        # Use eventlet's WSGI server to run the Flask app
        eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5002)), app)

    def shutdown(self):
        print("Shutting down")
        # Graceful shutdown logic here
        if self.server_thread:
            self.server_thread.kill()
        if self.processor_thread:
            self.processor_thread.kill()

        print("Shutdown complete")
