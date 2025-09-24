import pyvista as pv
import time
import numpy as np

plotter = pv.Plotter(window_size=[1280,720])
plotter.set_background('black',top='blue')
plotter.add_light(pv.Light(position=(0,0,20),light_type='scene light'))

ground = pv.Plane(i_size=50,j_size=50)
plotter.add_mesh(ground,color='green',opacity=0.5)

drone_mesh = pv.read('plane.obj')
drone_actor = plotter.add_mesh(drone_mesh,color="white",style="surface")

plotter.show(interactive=True,auto_close=False)

for i in range(20000):
    # 模拟从数据线程获取的最新状态
    new_position = (i * 0.1, 0, 5) # 向前移动
    # 绕Z轴旋转 (Yaw)
    new_orientation = (0, 0, i * 2) # (roll, pitch, yaw) in degrees

    # 核心：直接修改actor的属性
    drone_actor.Setposition(new_position)
    drone_actor.SetOrientation(new_orientation)

    # 刷新渲染器
    plotter.render()
    time.sleep(0.02) # 控制更新频率


'''
#--position accquire
while True:
    new_pos = 
    new_orientation = #(roll,pitch,yaw)
    drone_actor.position = new_pos
    drone_actor.orientation = new_orientation

    plotter.update()
    time.sleep(0.2)

    if KeyboardInterrupt:
        plotter.close()
'''



