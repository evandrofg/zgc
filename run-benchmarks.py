import subprocess
import os
import psutil
import threading
from concurrent.futures import ProcessPoolExecutor
from time import sleep

java_executable = "./build/macosx-aarch64-server-release/jdk/bin/java"
dacapo_jar = "../dacapo-23.11-chopin/dacapo-23.11-chopin.jar"
results_dir = "./results"

#zgc_opts = "-XX:+UseZGC -XID21 -Xmemb"
#zgc_opts = "-XX:+UseZGC -Xmemb"
zgc_opts = "-XX:+UseZGC -Xgco20"

base_command = f"{java_executable} -XX:+PrintGCDetails -Xloggc:./results/{{log_name}} -XX:+UnlockExperimentalVMOptions -XX:+UseZGC {zgc_opts} -jar {dacapo_jar} -s large {{benchmark}}"

# Update benchmarks here to run concurrently
#benchmarks = [
#    "avrora", "batik", "biojava", "cassandra", "eclipse", "fop", "graphchi", 
#    "h2", "h2o", "jme", "jython", "kafka", "luindex", "lusearch", "pmd", 
#    "spring", "sunflow", "tomcat", "tradebeans", "tradesoap", "xalan", "zxing"
#]
benchmarks = ["spring"]
timestamp = "gco"

os.makedirs("./results", exist_ok=True)

def monitor_cpu_usage(benchmark, stop_event):
    cpu_log_name = f"./results/{timestamp}-{benchmark}-cpu-usage.log"
    with open(cpu_log_name, "w") as log_file:
        while not stop_event.is_set():
            cpu_usage = psutil.cpu_percent()
            log_file.write(f"{cpu_usage}\n")
            log_file.flush()
            sleep(1)

def run_benchmark(benchmark):
    print(f"Started: {benchmark}")
    log_name = f"{timestamp}-{benchmark}-log.log"
    gc_log_name = f"{timestamp}-{benchmark}-log-gc.log"
    command = base_command.format(log_name=gc_log_name, benchmark=benchmark)

    # Start CPU usage monitoring
    stop_event = threading.Event()
    cpu_thread = threading.Thread(target=monitor_cpu_usage, args=(benchmark, stop_event))
    cpu_thread.start()
    
    with open(f"./results/{log_name}", "w") as output_file:
        print("Running ", command)
        subprocess.run(command, shell=True, stdout=output_file, stderr=subprocess.STDOUT)

    # Stop CPU monitoring
    stop_event.set()
    cpu_thread.join()
    
    print(f"Completed: {benchmark}")

if __name__ == '__main__':
    os.makedirs(results_dir, exist_ok=True)
    with ProcessPoolExecutor() as executor:
        for benchmark in benchmarks:
            executor.submit(run_benchmark, benchmark)
