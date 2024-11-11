import os
import sys
import subprocess
import tempfile
import time
from datetime import datetime
from termcolor import colored

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from functions import (
    list_sessions, save_logs, save_settings, restore_session, define_default_parameters
)

parameters = define_default_parameters()

def run_hashcat(session, hashmode, mask, workload, status_timer):
    temp_output = tempfile.mktemp()

    hashcat_command = [
        "hashcat", 
        f"--session={session}", 
        f"-m {hashmode}", 
        "hash.txt", 
        "-a 3", 
        f"-w {workload}", 
        "--outfile-format=2", 
        "-o", "plaintext.txt", 
        mask
    ]
    
    if status_timer.lower() == "y":
        hashcat_command.append("--status")
        hashcat_command.append("--status-timer=2")
    
    with open(temp_output, 'w') as output_file:
        try:
            subprocess.run(hashcat_command, check=True, stdout=output_file, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            print(colored("Error while executing hashcat.", "red"))
            return

    with open(temp_output, 'r') as file:
        hashcat_output = file.read()

    print(hashcat_output)

    if "Cracked" in hashcat_output:
        print(colored("Hashcat found the plaintext! Saving logs...", "green"))
        time.sleep(2)
        save_logs(session)
        save_settings(session)
    else:
        print(colored("Hashcat did not find the plaintext.", "red"))
        time.sleep(2)

    os.remove(temp_output)

def main():
    list_sessions(parameters["default_restorepath"])
    restore_file_input = input(colored(f"\nRestore? (Enter restore file name or leave empty, default '{parameters['restore_file_input']}'): ", "red"))
    restore_session(restore_file_input, parameters["default_restorepath"])

    session_input = input(colored(f"Enter session name (default '{parameters['default_session']}'): ", "magenta"))
    session = session_input or parameters["default_session"]
    
    mask_path_input = input(colored(f"Enter Masks Path (default '{parameters['default_masks']}'): ", "red"))
    masks_path = mask_path_input or parameters["default_masks"]
    
    print(colored(f"Available Masks in {masks_path}: ", "magenta"))
    for mask_file in os.listdir(masks_path):
        print(mask_file)
    
    mask_input = input(colored(f"Enter Mask (default '{parameters['default_mask']}'): ", "magenta"))
    mask = mask_input or parameters["default_mask"]
    
    status_timer_input = input(colored(f"Use status timer? (y/n, default '{parameters['default_status_timer']}'): ", "magenta"))

    min_length_input = input(colored(f"Enter Minimum Length (default '{parameters['default_min_length']}'): ", "magenta"))
    min_length = min_length_input or parameters["default_min_length"]
    
    max_length_input = input(colored(f"Enter Maximum Length (default '{parameters['default_max_length']}'): ", "magenta"))
    max_length = max_length_input or parameters["default_max_length"]
    
    hashmode_input = input(colored(f"Enter hash attack mode (default '{parameters['default_hashmode']}'): ", "magenta"))
    hashmode = hashmode_input or parameters["default_hashmode"]
    
    workload_input = input(colored(f"Enter workload (default '{parameters['default_workload']}') [1-4]: ", "magenta"))
    workload = workload_input or parameters["default_workload"]

    print(colored("Running Hashcat command...", "green"))
    run_hashcat(session, hashmode, mask, workload, status_timer_input)

if __name__ == "__main__":
    main()
