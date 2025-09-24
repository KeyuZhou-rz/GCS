import numpy as np
import threading
class Drone:
    def __init__(self, position=(0, 0, 0), orientation=(0, 0, 0)):
        self.lock = threading.Lock()
        self.position = np.array(position)
        self.orientation = np.array(orientation)
        # 遥测属性在此补充
        self.lat = 0.0
        self.lon = 0.0
        self.ground_speed = np.array([0.0, 0.0]) # vx, vy
        self.throttle = 0
        self.voltage = 0.0
        self.current = 0.0

    def update_position_and_speed(self, pos_data):
        with self.lock:
            self.lat = pos_data["lat"]
            self.lon = pos_data["lon"]
            # 我们只用高度(alt)来更新可视化中的z轴
            self.position[2] = pos_data["alt"] 
            self.ground_speed = np.array([pos_data["vx"], pos_data["vy"]])
    
    def update_orientation(self, new_orientation):
        with self.lock:
            # Pymavlink的姿态是弧度，PyVista的SetOrientation是角度，需要转换
            self.orientation = np.rad2deg(new_orientation)

    def update_hud(self, hud_data):
        with self.lock:
            self.throttle = hud_data["throttle"]

    def update_battery(self, battery_data):
        with self.lock:
            self.voltage = battery_data["voltage_battery"]
            self.current = battery_data["current_battery"]
            
    # --- 获取数据的方法 ---
    def get_position(self):
        with self.lock:
            return self.position
    
    def get_orientation(self):
        with self.lock:
            return self.orientation