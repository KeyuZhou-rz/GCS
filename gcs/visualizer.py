import pyvista as pv
import time
import numpy as np
from pathlib import Path
from core import Drone

plotter = pv.Plotter(window_size=[1280,720])
plotter.set_background('black', top='blue')
plotter.add_light(pv.Light(position=(0,0,20), light_type='scene light'))

ground = pv.Plane(i_size=50, j_size=50)
plotter.add_mesh(ground, color='green', opacity=0.5)

drone_mesh = pv.read('plane.obj')
drone_actor = plotter.add_mesh(drone_mesh,color="white",style="surface")
drone_para = Drone()

# 非阻塞地打开窗口 — 不同 pyvista 版本使用不同参数，先尝试 interactive 参数，失败再用 block
try:
    plotter.show(interactive=False, auto_close=False)
except TypeError:
    try:
        plotter.show(block=False, auto_close=False)
    except TypeError:
        plotter.show(auto_close=False)  # 最后兜底

# 获取底层 vtk actor（不同 pyvista 版本 wrapper 名称不同）
vtk_actor = getattr(drone_actor, "actor", drone_actor)

try:
    for i in range(20000):
        drone_para.update_position([i * 0.1, 0.0, 5.0])  # x, y, z
        drone_para.update_orientation([0.0, 0.0, i * 2.0])# roll, pitch, yaw (deg)

        # 使用 VTK 接口设置位置与姿态
        vtk_actor.SetPosition(drone_para.get_position())
        vtk_actor.SetOrientation(drone_para.get_orientation())

        # 强制渲染
        plotter.render()
        time.sleep(0.02)
except KeyboardInterrupt:
    pass
finally:
    plotter.close()