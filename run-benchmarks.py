import subprocess
import os

java_executable = "./build/macosx-aarch64-server-release/jdk/bin/java"
dacapo_jar = "../dacapo-23.11-chopin/dacapo-23.11-chopin.jar"

base_command = f"{java_executable} -Xloggc:../logs/{{log_name}} -XX:+UnlockExperimentalVMOptions -XX:+UseZGC -{{xgco}} -jar {dacapo_jar} -s large {{benchmark}}"

xgco_params = ["Xgco1", "Xgco5", "Xgco15", "Xgco20"]

# Benchmarks to run
#benchmarks = [
#    "avrora", "batik", "biojava", "cassandra", "eclipse", "fop", "graphchi", 
#    "h2", "h2o", "jme", "jython", "kafka", "luindex", "lusearch", "pmd", 
#    "spring", "sunflow", "tomcat", "tradebeans", "tradesoap", "xalan", "zxing"
#]
benchmarks = ["xalan"]

os.makedirs("../logs", exist_ok=True)

for benchmark in benchmarks:
    for xgco in xgco_params:
        log_name = f"{benchmark}-{xgco}-log.log"
        gc_log_name = f"{benchmark}-{xgco}-log-gc.log"
        
        command = base_command.format(log_name=gc_log_name, xgco=xgco, benchmark=benchmark)
        
        with open(f"../logs/{log_name}", "w") as output_file:
            subprocess.run(command, shell=True, stdout=output_file, stderr=subprocess.STDOUT)

        print(f"Completed: {benchmark} with {xgco}")
