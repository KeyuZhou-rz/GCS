# visualizer.py
import pyvista as pv
import time
import threading
from core import Drone
import utils

# --- 1. 初始化共享的数据对象 ---
shared_drone_state = Drone()

# --- 2. PyVista场景设置 (这部分不变) ---
plotter = pv.Plotter(window_size=[1280,720])
plotter.set_background('black', top='blue')
plotter.add_light(pv.Light(position=(0,0,20), light_type='scene light'))
ground = pv.Plane(i_size=50, j_size=50)
plotter.add_mesh(ground, color='green', opacity=0.5)
drone_mesh = pv.read('plane.obj')
# 设置无人机初始姿态，使其水平
drone_mesh.rotate_x(90, inplace=True) 
drone_actor = plotter.add_mesh(drone_mesh, color="white")

# --- 3. 启动MAVLink数据接收后台线程 ---
connection_string = 'udpin:localhost:14550' # 根据你的SITL或无人机配置修改
master = utils.connect_to_drone(connection_string)

if master:
    # 创建并启动后台数据接收线程
    receiver_thread = threading.Thread(
        target=utils.mavlink_data_receiver,
        args=(master, shared_drone_state),
        daemon=True  # 设置为守护线程，主程序退出时线程也退出
    )
    receiver_thread.start()
else:
    print("无法连接到无人机，程序将只显示静态模型。")

# --- 4. 启动渲染 ---
plotter.show(interactive_update=True, auto_close=False)

# 获取底层vtk actor
vtk_actor = getattr(drone_actor, "actor", drone_actor)

# --- 5. 主渲染循环 [cite: 31] ---
try:
    while plotter.is_open:
        # 从共享对象获取最新的位置和姿态
        pos = shared_drone_state.get_position()
        orient = shared_drone_state.get_orientation()

        # 使用 VTK 接口设置位置与姿态
        vtk_actor.SetPosition(pos)
        vtk_actor.SetOrientation(orient)

        # 刷新场景
        plotter.update() # update()是刷新PyVista场景的核心函数 [cite: 32]
        time.sleep(1 / 60) # 控制刷新率，例如60 FPS

except KeyboardInterrupt:
    pass
finally:
    plotter.close()