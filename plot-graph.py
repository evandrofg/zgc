import matplotlib.pyplot as plt
import sys
import re

# Function to read and parse GC log data, capturing the time in seconds
def parse_gc_log_data(file_path, log_type):
    times = []  # To hold the time stamps in seconds
    soft_max_capacities = []
    if log_type == "gco":
        pattern = re.compile(r'\[(\d+\.\d+)s\].*GC\(\d+\) Soft max capacity : (\d+)', re.IGNORECASE)
    elif log_type == "memb":
        pattern = re.compile(r'\[(\d+\.\d+)s\].*GC\(\d+\) Soft max capacity after MemBalancer: (\d+)', re.IGNORECASE)
    else:
        raise ValueError("Invalid log type. Use 'gco' for general GC logs or 'memb' for MemBalancer logs.")
    
    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                time_in_seconds = float(match.group(1))
                soft_max_capacity = int(match.group(2))
                times.append(time_in_seconds)
                soft_max_capacities.append(soft_max_capacity)
    return times, soft_max_capacities

# Function to read and parse CPU usage log data
def parse_cpu_log_data(file_path):
    times = []
    cpu_usages = []
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            cpu_usage = float(line.strip())
            times.append(i)  # Assuming each line is logged at 1-second intervals
            cpu_usages.append(cpu_usage)
    return times, cpu_usages

# Function to plot the data with time on the x-axis
def plot_data(times, data, title, y_label):
    plt.figure(figsize=(12, 7))
    plt.plot(times, data, marker='o', linestyle='-', color='b')
    plt.title(title)
    plt.xlabel('Time in Seconds')
    plt.ylabel(y_label)
    plt.grid(True)
    plt.show()

# Main script execution
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python plot_data.py <gc|cpu> <path_to_log_file>")
        sys.exit(1)
    
    option = sys.argv[1]
    file_path = sys.argv[2]  # Take the log file path from command line argument
    
    if option in ["gco", "memb"]:
        times, soft_max_capacities = parse_gc_log_data(file_path, option)
        plot_data(times, soft_max_capacities, 'Soft Max Capacity Change Over Time', 'Soft Max Capacity')
    elif option == "cpu":
        times, cpu_usages = parse_cpu_log_data(file_path)
        plot_data(times, cpu_usages, 'CPU Usage Over Time', 'CPU Usage (%)')
    else:
        print("Invalid option. Use 'gc', 'gco', 'memb' for GC data or 'cpu' for CPU usage data.")
        sys.exit(1)