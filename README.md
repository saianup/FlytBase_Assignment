# FlytBase_Assignment
This repository was created for the submission of the source code and video explanation as part of the FlytBase Robotics Assignment.

# UAV Strategic Deconfliction in Shared Airspace

## Overview

This project implements a strategic deconfliction system for drones operating in shared airspace. The system checks if a primary drone's planned waypoint mission is safe to execute, considering the simulated flight paths of multiple other drones. It performs both spatial and temporal conflict checks and provides clear explanations and visualizations of any detected conflicts.

## Features

- **Spatial Check:** Ensures the primary drone's path does not come within a defined safety buffer of any other drone's trajectory.
- **Temporal Check:** Ensures no other drone is present in the same spatial area during overlapping time segments.
- **Conflict Explanation:** Reports the location(s), time(s), and drone(s) involved in any detected conflict.
- **Visualization:** Animates all drone trajectories in 3D, showing the evolution of positions over time.
- **User Interface:** Accepts manual input for the primary drone's mission (waypoints and time window).
- **Extensible:** Easily adaptable for more drones or different safety thresholds.

## Requirements

- Python 3.7+
- matplotlib

## Setup

1. Clone this repository or download the code files.
2. Ensure you have `matplotlib` installed:
    ```
    pip install matplotlib
    ```
3. Place your drone schedule CSV file (e.g., `simulated_drones_3d.csv`) in the same directory as the code.

## Usage

1. Run the main script:
    ```
    python main.py
    ```
2. Enter the primary drone's waypoints and time window when prompted. The waypoints to be entered with spaces (Example: 2 4 7), and then the start time and end time to be entered.
3. The system will:
    - Print all drone trajectories.
    - Perform and report spatial and temporal checks.
    - Animate the trajectories in 3D.

## CSV Format

The CSV file should have the following columns:

| drone_id | waypoint_1 | waypoint_2 | waypoint_3 | waypoint_4 | time_start | time_end |
|----------|------------|------------|------------|------------|------------|----------|
| drone_1  | [x, y, z]  | [x, y, z]  | [x, y, z]  | [x, y, z]  | int        | int      |

## Example

```
drone_id,waypoint_1,waypoint_2,waypoint_3,waypoint_4,time_start,time_end
drone_1,[4, 18, 2],[8, 3, 15],[14, 15, 20],[12, 6, 3],15,25
drone_2,[12, 13, 19],[0, 14, 8],[7, 18, 3],[10, 0, 0],0,44
...
```

## Notes

- The safety threshold for conflict detection is set to 1.5 meters by default.
- The animation runs from global time 0 to 50 seconds.
- The code is modular and can be extended for more advanced features or larger datasets.

## License

MIT License
