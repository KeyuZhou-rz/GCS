import numpy as np

class Drone:
    def __init__(self, position=(0, 0, 0), orientation=(0, 0, 0)):
        self.position = np.array(position)
        self.orientation = np.array(orientation)
        # 遥测属性在此补充

    def update_position(self, new_position):
        self.position = np.array(new_position)

    def update_orientation(self, new_orientation):
        self.orientation = np.array(new_orientation)

    def get_position(self):
        return self.position
    
    def get_orientation(self):
        return self.orientation