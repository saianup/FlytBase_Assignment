import csv
import random

def generate_3d_drone_data(num_drones, output_file="simulated_drones_3d.csv"):
    
    # Function to generate simple 3D drone data with random waypoints and time intervals
    random.seed(1)
    # Seed for reproducibility

    with open(output_file, mode='w', newline='') as file:
        # Open the CSV file for writing
        writer = csv.writer(file)
        # Write the header row
        writer.writerow([
            "drone_id",
            "waypoint_1", "waypoint_2", "waypoint_3", "waypoint_4",
            "time_start", "time_end"
        ])

        for drone_id in range(1, num_drones + 1):
            
            # Generate 4 random integer 3D waypoints in [0, 20]
            waypoints = []
            for _ in range(4):
                x = random.randint(0, 20)
                y = random.randint(0, 20)
                z = random.randint(0, 20)
                waypoints.append(f"[{x}, {y}, {z}]")
            
            # Generate random start and end times
            # Ensure end time is greater than start time
            time_start = random.randint(0, 30)
            time_end = random.randint(time_start + 10, 50)

            # Write the drone data to the CSV file
            # Each drone has 4 waypoints and a time interval
            writer.writerow([
                f"drone_{drone_id}",
                *waypoints,
                time_start,
                time_end
            ])

    print(f" Simulated data for {num_drones} drones saved to {output_file}")

if __name__ == "__main__":
    n = int(input("Enter number of simulated drones: "))
    generate_3d_drone_data(n)
