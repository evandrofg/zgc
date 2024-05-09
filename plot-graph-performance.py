import matplotlib.pyplot as plt
import re
import os
import sys
import numpy as np  # Import numpy for numerical operations

# Function to parse simple tail latency data from a log file
def parse_latency_data_from_file(file_path):
    pattern = re.compile(r"(\d+(\.\d+)?%) (\d+) usec")
    labels = []
    values = []
    
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            simple_latency_section = re.search(r"DaCapo simple tail latency:(.+?)(?=^=====|\Z)", data, re.MULTILINE | re.DOTALL)
            if simple_latency_section:
                matches = pattern.findall(simple_latency_section.group(0))
                if matches:
                    labels = [match[0] for match in matches]
                    values = [int(match[2]) for match in matches]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    
    return labels, values

# Function to plot latency data for multiple files
def plot_combined_latency_data(all_labels, all_values, all_titles, save_plots, results_dir):
    plt.figure(figsize=(14, 8))
    unique_labels = sorted(set(label for labels in all_labels for label in labels), key=lambda x: float(x.strip('%')))
    num_labels = len(unique_labels)
    width = 0.8 / len(all_titles)  # Divide the space for each bar
    x = np.arange(num_labels)  # the label locations
    
    for i, (labels, values, title) in enumerate(zip(all_labels, all_values, all_titles)):
        aligned_values = [values[labels.index(label)] if label in labels else 0 for label in unique_labels]
        plt.bar(x + i * width, aligned_values, width, label=f'{title}')

    plt.xlabel('Percentiles')
    plt.ylabel('Latency (usec)')
    plt.title('Combined Simple Tail Latency Metrics Across Different Benchmarks')
    plt.xticks(x + width * (len(all_titles) - 1) / 2, unique_labels)
    plt.legend(title="File/Benchmark")
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    if save_plots:
        plot_file = os.path.join(results_dir, 'plots', 'combined_latency_plot.png')
        plt.savefig(plot_file)
        print(f"Plot saved to {plot_file}")
    else:
        plt.show()

# Main script execution
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python plot_latency.py <benchmark_name> <path_to_results_dir> <save_plots>")
        sys.exit(1)
    
    benchmark_name = sys.argv[1]
    results_dir = sys.argv[2]
    save_plots = sys.argv[3].lower() == 'true'
    plots_dir = os.path.join(results_dir, 'plots')

    if save_plots and not os.path.exists(results_dir):
        os.makedirs(plots_dir)

    all_files = os.listdir(results_dir)
    all_labels = []
    all_values = []
    all_titles = []

    for file_name in all_files:
        if "log" in file_name and benchmark_name in file_name:
            full_path = os.path.join(results_dir, file_name)
            labels, values = parse_latency_data_from_file(full_path)
            if labels and values:
                all_labels.append(labels)
                all_values.append(values)
                all_titles.append(file_name.replace('.log', ''))

    if all_labels and all_values:
        plot_combined_latency_data(all_labels, all_values, all_titles, save_plots, results_dir)
    else:
        print("No valid data to plot.")
