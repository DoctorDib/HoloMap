from Main.Modules.Vision.OutlierDetection import CalibrationOutlierDetection

import cv2
import cv2.typing as ty
import numpy as np

# TODO - Update a way to store boundary boxes where ever needed and only
#        use the shared_state value when it detects changes from calibrating.

class BoundaryBox():

    def __init__(self, top_left: ty.Point = None, top_right: ty.Point = None, bottom_right: ty.Point = None, bottom_left: ty.Point = None):
        # Constants
        self.line_thickess: int = 3

        # TODO - Get an array of array of corners and the check for outliers after 
        #        each loop then average the none outliers

        self.points: list[list[tuple]] = [] # Example input: [[ (0, 0), (0, 0), (0, 0), (0, 0) ], [ (0, 0), (0, 0), (0, 0), (0, 0) ]]

        self.temp_top_left: ty.Point = top_left
        self.temp_top_right: ty.Point = top_right
        self.temp_bottom_right: ty.Point = bottom_right
        self.temp_bottom_left: ty.Point = bottom_left

        self.top_left: ty.Point = top_left
        self.top_right: ty.Point = top_right
        self.bottom_right: ty.Point = bottom_right
        self.bottom_left: ty.Point = bottom_left

        self.outlier_detection = CalibrationOutlierDetection()

    def reset(self):
        self.top_left_average = []
        self.top_right_average = []
        self.bottom_right_average = []
        self.bottom_left_average = []

        self.top_left = None
        self.top_right = None
        self.bottom_right = None
        self.bottom_left = None
        
    def get_width(self):
        return self.top_right[0] - self.top_left[0]
    
    def get_height(self):
        return self.bottom_right[1] - self.top_left[1]
        
    def is_set(self):
        return self.top_left is not None and self.top_right is not None and self.bottom_right is not None and self.bottom_left is not None

    def is_in_boundary(self, x: int, y: int) -> bool:
        if (not self.is_set()):
            return None
        
        points = [self.top_left, self.top_right, self.bottom_right, self.bottom_left]
        n = len(points)
        inside = False

        p1x, p1y = points[0][0], points[0][1]

        for i in range(n + 1):
            p2x, p2y = points[i % n][0], points[i % n][1]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside
    
    def draw_boundary(self, img: cv2.typing.MatLike, color: tuple = (0, 0, 255)) -> cv2.typing.MatLike:
        # top of boundary
        if (self.top_left is not None and self.top_right is not None):
            img = cv2.line(img, self.top_left, self.top_right, color, self.line_thickess)
        # right side of boundary
        if (self.top_right is not None and self.bottom_right is not None):
            img = cv2.line(img, self.top_right, self.bottom_right, color, self.line_thickess)
        # bottom of boundary
        if (self.bottom_right is not None and self.bottom_left is not None):
            img = cv2.line(img, self.bottom_right, self.bottom_left, color, self.line_thickess)
        # left side of boundary
        if (self.bottom_left is not None and self.top_left is not None):
            img = cv2.line(img, self.bottom_left, self.top_left, color, self.line_thickess)

        return img
    
    def has_all_points(self) -> bool:
        return self.top_left != None and self.top_right != None and self.bottom_right != None and self.bottom_left != None
   
    def get_real_coords(self, arr, image_width, image_height):
        image_box = np.array([
            [0, 0],                # top-left
            [image_width, 0],      # top-right
            [image_width, image_height],  # bottom-right
            [0, image_height]      # bottom-left
        ], dtype="float32")

        # Define the boundary box and image box as you have them
        boundary_box = np.array([
            [self.top_left[0], self.top_left[1]],      # top-left
            [self.top_right[0], self.top_right[1]],    # top-right
            [self.bottom_right[0], self.bottom_right[1]],  # bottom-right
            [self.bottom_left[0], self.bottom_left[1]] # bottom-left
        ], dtype="float32")

        # Compute the perspective transform matrix
        matrix = cv2.getPerspectiveTransform(boundary_box, image_box)
        
        # Apply the perspective transformation to the input_box
        transformed_box = cv2.perspectiveTransform(np.array([arr], dtype='float32'), matrix)
        
        # Reshape the result to match the input_box shape
        return transformed_box.reshape(-1, 2)      
    
    def get_relative_position_from_img(self, img, point):
        """
        Get the relative position of a point in a quadrilateral boundary box.

        Parameters:
        - point: Tuple (x, y) representing the point coordinates.
        - box_coords: List of tuples containing the coordinates of the boundary box corners 
                    in the order: top-left, top-right, bottom-right, bottom-left.
                    Format: [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

        Returns:
        - Tuple (relative_x, relative_y) if the point is within the boundary box,
        otherwise None.
        """
        # Get the dimensions of the input image
        height, width = img.shape[:2]

        return self.get_relative_position_from_height_width(height, width, point)
    
    def get_relative_position_from_height_width(self, height, width, point):
        """
        Get the relative position of a point in a quadrilateral boundary box.

        Parameters:
        - point: Tuple (x, y) representing the point coordinates.
        - box_coords: List of tuples containing the coordinates of the boundary box corners 
                    in the order: top-left, top-right, bottom-right, bottom-left.
                    Format: [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

        Returns:
        - Tuple (relative_x, relative_y) if the point is within the boundary box,
        otherwise None.
        """
        x, y = point

        box_coords = [(self.top_left[0], self.top_left[1]), (self.top_right[0], self.top_right[1]), (self.bottom_right[0], self.bottom_right[1]), (self.bottom_left[0], self.bottom_left[1])]
        box_coords_np = np.array(box_coords, dtype='float32')

        # Create a mask for the defined quadrilateral
        mask = np.zeros((height, width), dtype=np.uint8)  # Match mask size to image size
        cv2.fillConvexPoly(mask, box_coords_np.astype(int), 255)  # Fill the polygon

        target_pts = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype='float32')
        transform_matrix = cv2.getPerspectiveTransform(box_coords_np, target_pts)

        # Transform the point
        point_np = np.array([[x, y]], dtype='float32')
        transformed_point = cv2.perspectiveTransform(point_np[None, :], transform_matrix)[0][0]

        relative_x = int(transformed_point[0] * width)
        relative_y = int(transformed_point[1] * height) 

        return (int(relative_x), int(relative_y))

    def get_points_arr(self) -> list[int]:
        return [self.top_left, self.top_right, self.bottom_right, self.bottom_left]
    
    def set_points_arr(self, points: list[int]):
        self.top_left = points[0]
        self.top_right = points[1]
        self.bottom_right = points[2]
        self.bottom_left = points[3]


    def insert(self, index: int, position: ty.Point):
        if (index == 0):
            self.temp_top_left = position
        elif (index == 1):
            self.temp_top_right = position
        elif (index == 2):
            self.temp_bottom_right = position
        elif (index == 3):
            self.temp_bottom_left = position

    def new_round(self):
        self.points.append([self.temp_top_left, self.temp_top_right, self.temp_bottom_right, self.temp_bottom_left])

        # Resetting points
        self.temp_top_left = []
        self.temp_top_right = []
        self.temp_bottom_right = []
        self.temp_bottom_left = []

    def apply(self):
        # Remove outliers
        clean_data, _ = self.outlier_detection.detect_outliers_in_data(self.points)
        
        # Get average of points
        averaged_points = self.average_points(clean_data)

        # Reset
        self.top_left = (int(averaged_points[0][0]), int(averaged_points[0][1]))
        self.top_right = (int(averaged_points[1][0]), int(averaged_points[1][1]))
        self.bottom_right = (int(averaged_points[2][0]), int(averaged_points[2][1]))
        self.bottom_left = (int(averaged_points[3][0]), int(averaged_points[3][1]))

    def average_points(self, clean_points):
        # Convert the list of lists of tuples into a numpy array for easier manipulation
        arr = np.array(clean_points, dtype=float)
        
        # Calculate the mean along the 0th axis (average across the first dimension)
        average = np.mean(arr, axis=0)
        
        # Convert back to a list of tuples for the result
        return [tuple(point) for point in average]