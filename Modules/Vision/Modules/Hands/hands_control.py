import numpy as np

class FingerPoint():
    def __init__(self, name:str, id: int, converted_id: int, is_left: bool):
        self.name = name
        self.id = id
        self.converted_id = converted_id
        self.position = (0, 0)
        self.in_boundaries = False
        self.is_left = is_left

    def set_position(self, xy: tuple):
        self.position = xy
        return self.position

    def get_position(self):
        return self.position
    
class HandsControl():
    
    def id_convert_to(self, id: int, is_left: bool) -> int:
        ''' Landmarks have a max of 21 landmarks
        '''
        return id + (100 if is_left else 200)
    
    def id_convert_from(self, converted_id: int, is_left: bool) -> int:
        return converted_id - (100 if is_left else converted_id - 200)

    def __init__(self):
        self.points_dict = {}
        self.point_map = {}

    def register_point(self, name, id: int, is_left: bool):
        converted_id = self.id_convert_to(id, is_left)
        self.point_map[name] = converted_id
        self.points_dict[converted_id] = FingerPoint(name, id, converted_id, is_left)
        return self.points_dict
    
    def get_point(self, arg : str | int, is_left: bool):
        if isinstance(arg, str):
            # Handle string input (name)
            return self.points_dict[self.point_map[arg]]
        elif isinstance(arg, int):
            # Handle integer input (id)
            return self.points_dict[self.id_convert_to(arg, is_left)]
        else:
            raise ValueError("arg must be either a string or an integer.")
    
    def update_point_position(self, arg, is_left: bool, xy: tuple):
        if isinstance(arg, str):
            # Handle string input (name)
            point: FingerPoint = self.points_dict[self.point_map[arg]]
        elif isinstance(arg, int):
            # Handle integer input (id)
            point: FingerPoint = self.points_dict[self.id_convert_to(arg, is_left)]
        else:
            raise ValueError("arg must be either a string or an integer.")

        return point.set_position(xy)
        
    def check_distance_between_two_points(self, point1: FingerPoint, point2: FingerPoint):
        dx = point2.get_position()[0] - point1.get_position()[0]
        dy = point2.get_position()[1] - point1.get_position()[1]
        return np.sqrt(dx**2 + dy**2)
