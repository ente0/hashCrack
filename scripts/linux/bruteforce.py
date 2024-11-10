import os
import subprocess
import tempfile
import time
from datetime import datetime
from termcolor import colored
from functions import (
    list_sessions, save_logs, save_settings, restore_session, define_default_parameters
)

define_default_parameters()

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
    list_sessions()
    restore_file_input = input(colored("\nRestore? (Enter restore file name or leave empty): ", "red"))
    restore_session(restore_file_input)

    session_input = input(colored("Enter session name (default '{}'): ".format(default_session), "magenta"))
    session = session_input or default_session
    
    mask_path_input = input(colored("Enter Masks Path (default '{}'): ".format(default_masks), "red"))
    masks_path = mask_path_input or default_masks
    
    print(colored("Available Masks in {}: ".format(masks_path), "magenta"))
    for mask_file in os.listdir(masks_path):
        print(mask_file)
    
    mask_input = input(colored("Enter Mask (default '{}'): ".format(default_mask), "magenta"))
    mask = mask_input or default_mask
    
    status_timer_input = input(colored("Use status timer? (y/n): ", "magenta"))

    min_length_input = input(colored("Enter Minimum Length (default '{}'): ".format(default_min_length), "magenta"))
    min_length = min_length_input or default_min_length
    
    max_length_input = input(colored("Enter Maximum Length (default '{}'): ".format(default_max_length), "magenta"))
    max_length = max_length_input or default_max_length
    
    hashmode_input = input(colored("Enter hash attack mode (default '{}'): ".format(default_hashmode), "magenta"))
    hashmode = hashmode_input or default_hashmode
    
    workload_input = input(colored("Enter workload (default '{}') [1-4]: ".format(default_workload), "magenta"))
    workload = workload_input or default_workload

    print(colored("Running Hashcat command...", "green"))
    run_hashcat(session, hashmode, mask, workload, status_timer_input)

if __name__ == "__main__":
    main()
