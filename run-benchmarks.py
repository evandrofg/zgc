import subprocess
import os
import psutil
import threading
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

java_executable = "./build/macosx-aarch64-server-release/jdk/bin/java"
#java_executable = "java"
dacapo_jar = "../dacapo-23.11-chopin/dacapo-23.11-chopin.jar"
results_dir = "./results"
dacapo_thread_count = 4
dacapo_iterations = 1

# GC options dictionary
gc_options = {
    'memb': "-XX:+UseZGC -Xmemb -Xgco10"
}

benchmarks = [
    "spring",
    "spring"
]

os.makedirs(results_dir, exist_ok=True)

def monitor_cpu_usage(benchmark, gc_option, instance_id, stop_event):
    cpu_log_name = f"./{results_dir}/{gc_option}-{benchmark}-{instance_id}-cpu-usage.log"
    with open(cpu_log_name, "w") as log_file:
        while not stop_event.is_set():
            cpu_usage = psutil.cpu_percent()
            log_file.write(f"{cpu_usage}\n")
            log_file.flush()
            sleep(1)

def run_benchmark(benchmark, gc_option, instance_id):
    print(f"Started: {benchmark} with GC option: {gc_option} (Instance {instance_id})")
    log_name = f"{gc_option}-{benchmark}-{instance_id}-log.log"
    gc_log_name = f"{gc_option}-{benchmark}-{instance_id}-log-gc.log"
    zgc_opts = gc_options[gc_option]
    command = f"{java_executable} -XX:+PrintGCDetails -Xloggc:{results_dir}/{gc_log_name} -XX:+UnlockExperimentalVMOptions {zgc_opts} -jar {dacapo_jar} -n {dacapo_iterations} -t {dacapo_thread_count} {benchmark}"
    
    # Start CPU usage monitoring
    stop_event = threading.Event()
    cpu_thread = threading.Thread(target=monitor_cpu_usage, args=(benchmark, gc_option, instance_id, stop_event))
    cpu_thread.start()
    
    with open(f"{results_dir}/{log_name}", "w") as output_file:
        print("Running ", command)
        subprocess.run(command, shell=True, stdout=output_file, stderr=subprocess.STDOUT)
    
    # Stop CPU monitoring
    stop_event.set()
    cpu_thread.join()
    
    print(f"Completed: {benchmark} with GC option: {gc_option} (Instance {instance_id})")
    sleep(5)  # Idle time between benchmark runs

if __name__ == '__main__':
    os.makedirs(results_dir, exist_ok=True)
    for gc_option in gc_options:
        with ThreadPoolExecutor() as executor:
            futures = []
            for i, benchmark in enumerate(benchmarks):
                futures.append(executor.submit(run_benchmark, benchmark, gc_option, i))
            for future in as_completed(futures):
                future.result()  # This will re-raise any exceptions that occurred in the thread
