import time
import socket
from pymavlink import mavutil
import json

# mavlink connection
mavlink_string = 'COM3'
mavlink_baud_rate = 115200
master = mavutil.mavlink_connection(mavlink_string, baud=mavlink_baud_rate)

# udp connection
UDP_IP = '127.0.0.1'
UDP_PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

print('等待udp心跳包')
master.wait_heartbeat()
print('飞控已链接，现在开始udp转发')

# 请求数据流，确保飞控按频率发送常见消息
try:
    master.mav.request_data_stream_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_ALL,
        5,  # 5 Hz
        1   # start
    )
    print("已发送 request_data_stream_send，请等待...")
except Exception as e:
    print("发送 request_data_stream_send 时出错：", e)

# === 诊断阶段：在接下来的 15 秒内打印任意收到的消息类型（不做过滤），以确认飞控是否发送 MAVLink 消息 ===
print('进入诊断阶段：在 15 秒内打印所有收到的消息类型（无过滤）...')
diag_start = time.time()
any_msg = False
while time.time() - diag_start < 15:
    msg = master.recv_match(blocking=True, timeout=2)
    if not msg:
        print('[DIAG] 在2秒内未收到消息')
        continue
    any_msg = True
    try:
        print(f"[DIAG] 收到消息类型: {msg.get_type()}")
    except Exception:
        print(f"[DIAG] 收到消息 (无法读取类型): {msg}")

if not any_msg:
    print('[DIAG] 未检测到任何 MAVLink 消息；请检查物理连接/串口/固件是否在该接口发送 MAVLink。')

# 诊断阶段结束，进入常规转发循环
print('诊断阶段结束，回到常规 udp 转发循环')

try:
    while True:
        # 使用超时避免无限阻塞，便于检测没有消息的情况
        msg = master.recv_match(type=['ATTITUDE','GLOBAL_POSITION_INT','VIBRATION','SYS_STATUS'], blocking=True, timeout=5)
        if not msg:
            print("[DEBUG] 在 5 秒内未收到匹配消息，可能需要检查数据流订阅或飞控是否发送该类型。", flush=True)
            continue

        # 打印原始消息类型与内容，便于确认字段名
        try:
            print(f"[DEBUG] 收到消息: type={msg.get_type()} repr={repr(msg)}", flush=True)
        except Exception:
            print(f"[DEBUG] 收到消息但无法打印完整内容: {msg}", flush=True)

        data_to_send = {}
        msg_type = msg.get_type()
        data_to_send['type'] = msg_type

        if msg_type == 'ATTITUDE':
            data_to_send['roll'] = msg.roll
            data_to_send['pitch'] = msg.pitch
            data_to_send['yaw'] = msg.yaw
            
        elif msg_type == 'GLOBAL_POSITION_INT':
            data_to_send['lat'] = msg.lat
            data_to_send['lon'] = msg.lon
            data_to_send['relative_alt'] = msg.relative_alt
            
        elif msg_type == 'VIBRATION':
            data_to_send['vibration_x'] = msg.vibration_x
            data_to_send['vibration_y'] = msg.vibration_y
            data_to_send['vibration_z'] = msg.vibration_z
            
        elif msg_type == 'SYS_STATUS':
            data_to_send['voltage_battery'] = msg.voltage_battery
            data_to_send['current_battery'] = msg.current_battery
            data_to_send['battery_remaining'] = msg.battery_remaining
        
        # 将字典转换为JSON字符串，并编码为字节流
        message_bytes = json.dumps(data_to_send).encode('utf-8')
        
        # 通过UDP发送
        sock.sendto(message_bytes, (UDP_IP, UDP_PORT))
        
        print(f"已发送 {msg_type} 数据") # 打印日志，方便调试
        
        # 控制发送频率，避免过于频繁
        time.sleep(0.2) # 50Hz

except KeyboardInterrupt:
    print("服务已停止。")
    sock.close()