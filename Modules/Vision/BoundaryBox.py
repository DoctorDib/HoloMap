import cv2
import cv2.typing as ty
import numpy as np

class BoundaryBox():
    
    def __init__(self):
        self.line_thickess: int = 3

    def __init__(self, top_left: ty.Point = None, top_right: ty.Point = None, bottom_right: ty.Point = None, bottom_left: ty.Point = None):
        # Constants
        self.line_thickess: int = 3

        self.top_left: ty.Point = top_left
        self.top_right: ty.Point = top_right
        self.bottom_right: ty.Point = bottom_right
        self.bottom_left: ty.Point = bottom_left

    def is_in_boundary(self, x: int, y: int) -> bool:
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
    
    def draw_boundary(self, img: cv2.typing.MatLike) -> cv2.typing.MatLike:
        # top of boundary
        if (self.top_left is not None and self.top_right is not None):
            img = cv2.line(img, self.top_left, self.top_right, (0, 0, 255), self.line_thickess)
        # right side of boundary
        if (self.top_right is not None and self.bottom_right is not None):
            img = cv2.line(img, self.top_right, self.bottom_right, (0, 0, 255), self.line_thickess)
        # bottom of boundary
        if (self.bottom_right is not None and self.bottom_left is not None):
            img = cv2.line(img, self.bottom_right, self.bottom_left, (0, 0, 255), self.line_thickess)
        # left side of boundary
        if (self.bottom_left is not None and self.top_left is not None):
            img = cv2.line(img, self.bottom_left, self.top_left, (0, 0, 255), self.line_thickess)

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

    def get_points_arr(self) -> list[int]:
        return [self.top_left, self.top_right, self.bottom_right, self.bottom_left]
    
    def set_points_arr(self, points: list[int]):
        self.top_left = points[0]
        self.top_right = points[1]
        self.bottom_right = points[2]
        self.bottom_left = points[3]
