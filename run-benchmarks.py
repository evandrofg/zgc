import subprocess
import os
import psutil
import threading
from time import sleep

java_executable = "./build/macosx-aarch64-server-release/jdk/bin/java"
#java_executable = "java"
dacapo_jar = "../dacapo-23.11-chopin/dacapo-23.11-chopin.jar"
results_dir = "./results"
dacapo_thread_count = 8
dacapo_iterations = 3

# GC options dictionary
gc_options = {
    'memb': "-XX:+UseZGC -Xmemb -Xgco10",
    'gco20': "-XX:+UseZGC -Xgco20",
    'gco2': "-XX:+UseZGC -Xgco2",
    'zgc': "-XX:+UseZGC -Xgco0"
}

benchmarks = [
    "spring"
]

os.makedirs(results_dir, exist_ok=True)

def monitor_cpu_usage(benchmark, gc_option, stop_event):
    cpu_log_name = f"./{results_dir}/{gc_option}-{benchmark}-cpu-usage.log"
    with open(cpu_log_name, "w") as log_file:
        while not stop_event.is_set():
            cpu_usage = psutil.cpu_percent()
            log_file.write(f"{cpu_usage}\n")
            log_file.flush()
            sleep(1)

def run_benchmark(benchmark, gc_option):
    print(f"Started: {benchmark} with GC option: {gc_option}")
    log_name = f"{gc_option}-{benchmark}-log.log"
    gc_log_name = f"{gc_option}-{benchmark}-log-gc.log"
    zgc_opts = gc_options[gc_option]
    command = f"{java_executable} -XX:+PrintGCDetails -Xloggc:{results_dir}/{gc_log_name} -XX:+UnlockExperimentalVMOptions {zgc_opts} -jar {dacapo_jar} -s large -n {dacapo_iterations} -t {dacapo_thread_count} {benchmark}"
    
    # Start CPU usage monitoring
    stop_event = threading.Event()
    cpu_thread = threading.Thread(target=monitor_cpu_usage, args=(benchmark, gc_option, stop_event))
    cpu_thread.start()
    
    with open(f"{results_dir}/{log_name}", "w") as output_file:
        print("Running ", command)
        subprocess.run(command, shell=True, stdout=output_file, stderr=subprocess.STDOUT)
    
    # Stop CPU monitoring
    stop_event.set()
    cpu_thread.join()
    
    print(f"Completed: {benchmark} with GC option: {gc_option}")
    sleep(5)  # Idle time between benchmark runs

if __name__ == '__main__':
    os.makedirs(results_dir, exist_ok=True)
    for gc_option in gc_options:
        for benchmark in benchmarks:
            run_benchmark(benchmark, gc_option)
