import matplotlib.pyplot as plt
import sys
import re
import os

# Function to determine and parse GC log data using appropriate patterns
def parse_gc_log_data(file_path):
    times = []  # To hold the time stamps in seconds
    soft_max_capacities = []
    pattern = re.compile(r'\[(\d+\.\d+)s\].*GC\(\d+\) Soft Max Capacity: (\d+)M', re.IGNORECASE)
    
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
def plot_data(gc_times_data, gc_capacities_data, cpu_times_data, cpu_usages_data, benchmark_name, save_plots, log_dir):
    # Plotting GC data
    plt.figure(figsize=(12, 7))
    for times, capacities, label in zip(gc_times_data, gc_capacities_data, labels):
        plt.plot(times, capacities, marker='o', linestyle='-', label=f"{label} GC", linewidth=1.0)
    plt.title(f'Soft Max Capacity Change Over Time for {benchmark_name}')
    plt.xlabel('Time in Seconds')
    plt.ylabel('Soft Max Capacity')
    plt.legend()
    plt.grid(True)
    if save_plots:
        plot_file = os.path.join(log_dir, 'plots', f'{benchmark_name}_gc.png')
        plt.savefig(plot_file)
        print(f"Plot saved to {plot_file}")
    else:
        plt.show()

    # Plotting CPU data
    plt.figure(figsize=(12, 7))
    for times, usages, label in zip(cpu_times_data, cpu_usages_data, labels):
        plt.plot(times, usages, marker='o', linestyle='-', label=f"{label} CPU", linewidth=1.0)
    plt.title(f'CPU Usage Over Time for {benchmark_name}')
    plt.xlabel('Time in Seconds')
    plt.ylabel('CPU Usage (%)')
    plt.legend()
    plt.grid(True)
    if save_plots:
        plot_file = os.path.join(log_dir, 'plots', f'{benchmark_name}_cpu.png')
        plt.savefig(plot_file)
        print(f"Plot saved to {plot_file}")
    else:
        plt.show()

# Main script execution
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python plot_data.py <benchmark_name> <path_to_log_dir> <save_plots>")
        sys.exit(1)
    
    benchmark_name = sys.argv[1]
    log_dir = sys.argv[2]
    save_plots = len(sys.argv) >= 4 and sys.argv[3].lower() == 'true'
    
    plots_dir = os.path.join(log_dir, 'plots')
    if save_plots and not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    labels = ['memb', 'gco20', 'gco2', 'zgc']
    #labels = ['zgc']
    gc_times_data = []
    gc_capacities_data = []
    cpu_times_data = []
    cpu_usages_data = []

    for label in labels:
        gc_file_path = os.path.join(log_dir, f"{label}-{benchmark_name}-log-gc.log")
        cpu_file_path = os.path.join(log_dir, f"{label}-{benchmark_name}-cpu-usage.log")
        
        if os.path.exists(gc_file_path):
            times, capacities = parse_gc_log_data(gc_file_path)
            gc_times_data.append(times)
            gc_capacities_data.append(capacities)
        else:
            print(f"No GC log file found for {label}")

        if os.path.exists(cpu_file_path):
            times, usages = parse_cpu_log_data(cpu_file_path)
            cpu_times_data.append(times)
            cpu_usages_data.append(usages)
        else:
            print(f"No CPU log file found for {label}")

    if gc_times_data and cpu_times_data:
        plot_data(gc_times_data, gc_capacities_data, cpu_times_data, cpu_usages_data, benchmark_name, save_plots, log_dir)
    else:
        print("No valid data to plot.")
