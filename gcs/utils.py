from pymavlink import mavutil
import time
from core import Drone
import numpy as np

def connect_to_drone(connection_string):
    print(f"正在连接到无人机: {connection_string}")
    try:
        master = mavutil.mavlink_connection(connection_string)
        master.wait_heartbeat()
        print("心跳包已接收！无人机已连接。")
        return master
    except Exception as e:
        print(f"连接失败: {e}")
        return None

def mavlink_data_receiver(master, drone_state):
    print("MAVLink数据接收线程已启动。")
    while True:
        try:
            msg = master.recv_match()
            if not msg:
                continue

            # 调用解析函数更新状态
            parse_mavlink_message(msg, drone_state)

        except Exception as e:
            print(f"数据接收时发生错误: {e}")
            time.sleep(1) # 发生错误时稍作等待


def parse_mavlink_message(msg, drone_state):
    """
    解析收到的MAVLink消息，并用其更新DroneState对象。
    这部分将物理参数映射到具体的MAVLink消息和字段 [cite: 66]。
    """
    msg_type = msg.get_type()
    if msg_type == 'ATTITUDE':
        # 更新姿态信息：横滚角、俯仰角、偏航角
        # 注意：np.array需要一个列表或元组作为输入
        state_update = np.array([msg.roll, msg.pitch, msg.yaw])
        # 更新传入的drone_state实例，而不是Drone类
        drone_state.update_orientation(state_update)

    elif msg_type == 'GLOBAL_POSITION_INT':
        # 更新位置和速度
        state_update = {
            "lat": msg.lat / 1e7,
            "lon": msg.lon / 1e7,
            "alt": msg.alt / 1000.0,
            "vx": msg.vx / 100.0,          # 北向速度 (m/s) [cite: 68]
            "vy": msg.vy / 100.0,          # 东向速度 (m/s) [cite: 68]
        }
        # 更新传入的drone_state实例
        drone_state.update_position_and_speed(state_update)

    elif msg_type == 'VFR_HUD':
        # 更新油门百分比等信息 [cite: 68]
        state_update = {
            "throttle": msg.throttle  # 油门百分比 (%) [cite: 68]
        }
        # 更新传入的drone_state实例
        drone_state.update_hud(state_update)

    elif msg_type == 'SYS_STATUS':
        # 更新电池电压和电流信息 [cite: 68]
        state_update = {
            "voltage_battery": msg.voltage_battery / 1000.0, # 伏特 (V) [cite: 68]
            "current_battery": msg.current_battery / 100.0   # 安培 (A) [cite: 68]
        }
        # 更新传入的drone_state实例
        drone_state.update_battery(state_update)

