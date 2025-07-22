import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation  
import math

def waypoint_tuple(str):
    
    # Convert a string representation of a waypoint to a tuple of integers
    
    return tuple(map(int, str.strip('[]').split(',')))

def linear_trajectory(waypoints, t_start, t_end, dt=1):
    
    num_seg = len(waypoints) - 1
    segment_time = (t_end - t_start) / num_seg  
    trajectory = []

    for t in range(t_start, t_end + 1, dt):
        
        seg_idx = min(int((t - t_start) // segment_time), num_seg - 1)
        
        # Find the segment start time for position interpolation 
        
        seg_t_start = t_start + seg_idx * segment_time
        alpha = (t - seg_t_start) / segment_time if segment_time > 0 else 0

        x1, y1, z1 = waypoints[seg_idx]
        x2, y2, z2 = waypoints[seg_idx + 1]

        # Interpolate position , this is a linear interpolation with parametric equation
        
        x = round(x1 + alpha * (x2 - x1), 1)
        y = round(y1 + alpha * (y2 - y1), 1)
        z = round(z1 + alpha * (z2 - z1), 1)

        trajectory.append((t, x, y, z))

    return trajectory

def trajectories(manual_waypoints, manual_t_start, manual_t_end):
    
    # Creating a dictionary to hold all drone trajectories
    # including the manual drone trajectory
    all_trajectories = {}

    # Pregenerated drone waypoints from assignment.py stored in CSV 
    
    csv_filename = "simulated_drones_3d.csv"
    try:
        with open(csv_filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                drone_id = row['drone_id']
                waypoints = [
                    waypoint_tuple(row['waypoint_1']),
                    waypoint_tuple(row['waypoint_2']),
                    waypoint_tuple(row['waypoint_3']),
                    waypoint_tuple(row['waypoint_4'])
                ]
                t_start = int(row['time_start'])
                t_end = int(row['time_end'])
                traj = linear_trajectory(waypoints, t_start, t_end)
                all_trajectories[drone_id] = traj
    except FileNotFoundError:
        print(f"CSV file '{csv_filename}' not found")

    # Add manual drone
    all_trajectories["manual_drone"] = linear_trajectory(manual_waypoints, manual_t_start, manual_t_end)

    return all_trajectories

# Animate the trajectories of all drones in 3D space
def animate_trajectories(all_trajs):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    drone_ids = list(all_trajs.keys())
    colors = plt.cm.tab10.colors

    # Find each drone's time range
    drone_time_ranges = {}
    for drone_id, traj in all_trajs.items():
        times = [pt[0] for pt in traj]
        drone_time_ranges[drone_id] = (times[0], times[-1])

    scatters = []
    for i, drone_id in enumerate(drone_ids):
        sc = ax.scatter([], [], [], color=colors[i % len(colors)], label=drone_id, s=40)
        scatters.append(sc)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.legend()

    ax.set_xlim([0, 20])
    ax.set_ylim([0, 20])
    ax.set_zlim([0, 20])

    global_time_start = 0
    global_time_end = 50
    frames = list(range(global_time_start, global_time_end + 1))

    def update(frame):
        for i, drone_id in enumerate(drone_ids):
            traj = all_trajs[drone_id]
            t0, t1 = drone_time_ranges[drone_id]
            # If before drone's start time, stay at first point
            if frame < t0:
                _, x, y, z = traj[0]
            # If after drone's end time, stay at last point
            elif frame > t1:
                _, x, y, z = traj[-1]
            else:
                # Find the closest time index in the trajectory
                idx = frame - t0
                _, x, y, z = traj[idx]
            scatters[i]._offsets3d = ([x], [y], [z])
        ax.set_title(f"Global Time: {frame} s")
        return scatters

    ani = FuncAnimation(fig, update, frames=frames, interval=500, blit=False)
    plt.show()
    
    
# Perform spatial checks on the trajectories

def spatial_check(all_trajs, threshold=1.5):
    
    # Checks if manual drone position overlaps with other drones irrespective of time
    # If any drone is within the threshold distance, it reports a violation
    
    manual_traj = all_trajs["manual_drone"]
    for other_id, other_traj in all_trajs.items():
        if other_id == "manual_drone":
            continue
        for _, mx, my, mz in manual_traj:
            for _, ox, oy, oz in other_traj:
                dist = math.sqrt((mx - ox)**2 + (my - oy)**2 + (mz - oz)**2)
                if dist < threshold:
                    print(f"Spatial violation: manual_drone and {other_id} are within {dist:.2f} meters.")
                    return False
    print("Spatial check passed: No overlap within threshold.")
    return True

# Perform temporal checks on the trajectories

def temporal_check(all_trajs, threshold=1.5):
    
    # Checks if manual drone's trajectory overlaps with other drones at the same time
    # If any drone is within the threshold distance at the same time, it reports a violation
    # This is a stricter check than spatial, as it considers both time and space
    
    manual_traj = all_trajs["manual_drone"]
    manual_dict = {t: (x, y, z) for t, x, y, z in manual_traj}
    for other_id, other_traj in all_trajs.items():
        if other_id == "manual_drone":
            continue
        for t, ox, oy, oz in other_traj:
            if t in manual_dict:
                mx, my, mz = manual_dict[t]
                dist = math.sqrt((mx - ox)**2 + (my - oy)**2 + (mz - oz)**2)
                if dist < threshold:
                    print(f"Temporal violation at t={t}: manual_drone and {other_id} are within {dist:.2f} meters.")
                    return False
    print("Temporal check passed: No overlap within threshold.")
    return True
    
    
# Function to get user input for waypoints and time intervals

def user_input():
    print("Enter 4 waypoints (x y z) each:")

    waypoints = []
    for i in range(4):
        coords = input(f"Waypoint {i+1} (x y z): ").strip().split()
        if len(coords) != 3:
            print("Invalid input! Please enter 3 integers separated by spaces.")
            return
        x, y, z = map(int, coords)
        waypoints.append((x, y, z))

    try:
        t_start = int(input("Enter start time (in seconds): ").strip())
        t_end = int(input("Enter end time (in seconds): ").strip())
    except ValueError:
        print("Invalid time input")
        return
    
    print("Waypoints:")
    
    # Print the waypoints and time intervals entered by the user
    for i, wp in enumerate(waypoints, 1):
        print(f"  Waypoint {i}: {wp}")
    print(f"Start Time: {t_start}")
    print(f"End Time: {t_end}")

    all_trajs = trajectories(waypoints, t_start, t_end)
    
    # Print all drone trajectories including the manual drone
    print("\nAll drone trajectories:")
    for drone_id, traj in all_trajs.items():
        print(f"\nDrone: {drone_id}")
        for pt in traj:
            print(pt)
            
    # Calling of spatial check
    print("\nSpatial Check:")
    spatial_check(all_trajs)
    
    # Calling of temporal check
    print("\nTemporal Check:")
    temporal_check(all_trajs)
    
    # Animate the trajectories
    print("\nAnimating trajectories:")        
    animate_trajectories(all_trajs)

if __name__ == "__main__":
    user_input()