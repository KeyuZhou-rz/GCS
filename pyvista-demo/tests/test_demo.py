import pytest
import pyvista as pv
from src.pyvista_demo import plotter, drone_mesh

def test_drone_initialization():
    assert drone_mesh is not None, "Drone mesh should be initialized."

def test_drone_position_update():
    initial_position = (0, 0, 5)
    plotter.add_mesh(drone_mesh, color="white", style="surface")
    plotter.update()
    
    # Simulate position update
    new_position = (10, 0, 5)
    drone_mesh.SetPosition(new_position)
    plotter.render()
    
    assert drone_mesh.GetPosition() == new_position, "Drone position should be updated."

def test_drone_orientation_update():
    initial_orientation = (0, 0, 0)
    plotter.add_mesh(drone_mesh, color="white", style="surface")
    plotter.update()
    
    # Simulate orientation update
    new_orientation = (0, 0, 90)
    drone_mesh.SetOrientation(new_orientation)
    plotter.render()
    
    assert drone_mesh.GetOrientation() == new_orientation, "Drone orientation should be updated."