# PyVista Drone Simulation

## Overview
This project is a drone simulation visualization using PyVista, a powerful library for 3D visualization in Python. The main script sets up a 3D plot with a ground plane and a drone model, updating the drone's position and orientation in real-time.

## Installation
To set up the project, you need to install the required dependencies. You can do this using pip. First, ensure you have Python installed, then run:

```
pip install -r requirements.txt
```

## Usage
To run the drone simulation, execute the following command in your terminal:

```
python src/pyvista_demo.py
```

This will open a window displaying the simulation. The drone will move forward and rotate around its Z-axis.

## Project Structure
- `pyvista_demo.py`: Main code for visualizing the drone simulation.
- `core.py`: Core functionalities related to the drone simulation.
- `utils.py`: Utility functions for data processing and configuration management.
- `plane.obj`: 3D model of the plane used in the visualization.
- `tests/test_demo.py`: Unit tests for the project functionalities.
- `requirements.txt`: Lists the required Python dependencies.
- `pyproject.toml`: Project configuration file.
- `.gitignore`: Specifies files to be ignored by Git.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.