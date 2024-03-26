
import subprocess
import aux.variables as variables
from aux.ping_wrapper import PingWrapperThread
import pingparsing
from aux.ping_wrapper import parse_hping_output
import json
import os
import multiprocessing
import threading
from datetime import datetime
import shlex
import pandas

def create_process_group():
    os.setpgrp()

def start_iperf_client(target_ip, number_of_streams):
    
    command = f"iperf3 -t 5 -c {target_ip} -P {number_of_streams} -J > "\
    f"/tmp/{variables.E2E_SINGLE_UE_THROUGHPUT_AND_LATENCY}"

    # Run the command as a background process
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    print(f"Started Iperf3 client process with {number_of_streams} streams...")
    # Optional: Print the process ID (PID) if needed
    print("Process ID:", process.pid)        
    return process

def start_iperf_server():
    # Command to start the iperf3 server
    command = "iperf3 -s"

    # Run the command as a background process
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        preexec_fn=create_process_group
    )
    print(f"Started Iperf3 server process...")
    # Optional: Print the process ID (PID) if needed
    print("Process ID:", process.pid)        
    return process
    
def process_iperf_results(data):

    throughput_mbps = data['end']['sum_sent']['bits_per_second'] / 1000000
    
    mean_rtts_ms = []
    for stream in  data['end']["streams"]:
        mean_rtts_ms.append(stream["sender"]["mean_rtt"] * 0.001)

    mean_rtt_ms = sum(mean_rtts_ms)/len(mean_rtts_ms)

    return throughput_mbps, mean_rtt_ms


# todo: needs to be updated
def start_ping(target_ip, runs):
    
    for run in range(runs):
        command = f"ping -c 5 {target_ip} | grep time= | "\
            "awk '{print $7}' | cut -d'=' -f2 > "\
            f"/tmp/{variables.E2E_SINGLE_UE_LATENCY_BASE_NAME}_{i}.json"
        
        # Run the command as a background process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

    print(f"Started {runs} ping client processes ...")

def compute_max_hops(target):
    max_hops=30
    for ttl in range(1, max_hops + 1):
        print(f"TTL: {ttl}")
        response = os.system(f"ping -c 3 -t {ttl} {target} > /dev/null")
        if response == 0:
            print(f"Reached {target} with {ttl} hops!")
            with open(
                f'/tmp/{variables.MAX_HOPS_RESULTS}',
                'w'
            ) as json_file:
                json.dump(
                    {
                        target: {
                            "hops_until_target": ttl
                        }
                    },
                    json_file
                )
            return
        print(
            f"Could not reach {target} with {ttl} hops. Will try with "
            f"{ttl + 1} hops..."
        )
    
    # Finally, create an output file for the unsuccessful test cases
    with open(
        f'/tmp/{variables.MAX_HOPS_RESULTS}',
        'w'
    ) as json_file:
        json.dump(
            {
                target: {
                    "hops_until_target": -1
                }
            },
            json_file
        )


def start_max_hops_computing(target):
    print(f"Will compute the number of hops until the target {target}...")
    # Run the command as a background process
    process = multiprocessing.Process(
        target=compute_max_hops,
        args=(target,)
    )
    process.start()
    print("Started the hops computation process...")
    # Optional: Print the process ID (PID) if needed
    print("Process ID:", process.pid)
    return process





def start_netstat_command(output_file):
    
    print("HEllo")
    
    if os.system(f"netstat --version > /dev/null") == 0:
        base_command = "netstat -an | grep \"ESTABLISHED\""
    elif os.system(f"ss --version > /dev/null") == 0:
        base_command = "ss -t state established"
    else:
        return None
            
    # Command to start the netsat connections monitoring loop
    # The monitoring will run for 300 seconds and then stop.
    # This process can also be killed by invoking the /stop endpoint
    command = "start_time=$(date +%s); while true; do current_time=$(date " \
        "+%s); elapsed_time=$((current_time - start_time)); if " \
        f"[ $elapsed_time -ge 300 ]; then break; fi; {base_command} " \
        "| wc -l >> " \
        f"{output_file}; sleep 1; done"

    # Run the command as a background process
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        preexec_fn=create_process_group
    )
    print("Started Netstat Monitoring Loop process...")
    # Optional: Print the process ID (PID) if needed
    print("Process ID:", process.pid)
    return process

def on_timeout_stop_driveu(process, timeout):
    print(f"[{datetime.now()}]  Stop DriveU process after running duration of {timeout} seconds")
    process.terminate()

def start_driveu_streamer(target_ip, test_duration):
    print(f"[{datetime.now()}] Starting DriveU Streamer process ...")

    command = f"./build/Fake streamer --relay-ip {target_ip}"

    # Run the command as a background process
    try:
        process = subprocess.Popen(
            shlex.split(command),
            cwd="/opt/driveu/fake",
            close_fds=True,
            stdout=None,
            stderr=None
        )
    except Exception as e:
        print(f"Failed DriveU streamer process with: {e}")
    # Set up timer to kill the process after timeout
    timer_thread = threading.Timer(interval=test_duration, function=on_timeout_stop_driveu, args=(process, test_duration))
    timer_thread.start()

    print(f"[{datetime.now()}] Started DriveU Streamer process ...")
    # Optional: Print the process ID (PID) if needed
    print("Process ID:", process.pid)
    return process

def start_driveu_server():
    print(f"Starting DriveU server process...")

    # Command to start the DriveU server
    command = "./build/Fake server"

    try:
        # Run the command as a background process
        process = subprocess.Popen(
            shlex.split(command),
            cwd="/opt/driveu/fake",
            close_fds=True,
            stdout=None,
            stderr=None
        )
    except Exception as e:
        print(f"Failed DriveU server process with: {e}")

    print(f"Started DriveU server process...")
    # Optional: Print the process ID (PID) if needed
    print("Process ID:", process.pid)
    return process


def fixLastLine(frameLogPath):
    replacement = ']'

    with open(frameLogPath, 'r') as file:
        lines = file.readlines()

    second_to_last_line_index = -2
    last_line_index = -1
    if len(lines) > 1:
        lines[last_line_index] = replacement
        lines[second_to_last_line_index] = lines[second_to_last_line_index].rstrip(', \n') + '\n'
        # Write the modified lines back to the file
        with open(frameLogPath, 'w') as file:
            file.writelines(lines)

def process_driveu_results():
    frameLogPath = '/tmp/miyadijsonlogs/framelog.json'
    US_IN_MS = 1000
    KB_TO_MB = 1000

    try:
        dataFrame = pandas.read_json(frameLogPath)
    except:
        fixLastLine(frameLogPath)
        try:
            dataFrame = pandas.read_json(frameLogPath)
        except Exception as e:
            error_msg = f"Failed to parse DriveU results with: {e}"
            print(f"{error_msg}")
            return False, 0, 0, error_msg

    return True, dataFrame['b'].mean()/KB_TO_MB, dataFrame['l'].mean()/US_IN_MS, ""
