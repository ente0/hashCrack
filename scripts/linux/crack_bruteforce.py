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

def run_hashcat(session, hashmode, wordlist_path, wordlist, mask, workload, status_timer, min_length, max_length):
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
        f"{wordlist_path}/{wordlist}", 
        mask
    ]
    
    if status_timer.lower() == "y":
        hashcat_command.append("--status")
        hashcat_command.append("--status-timer=2")
    
    hashcat_command.append(f"--increment")
    hashcat_command.append(f"--increment-min={min_length}")
    hashcat_command.append(f"--increment-max={max_length}")

    with open(temp_output, 'w') as output_file:
        try:
            subprocess.run(hashcat_command, check=True, stdout=output_file, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            print(colored("[!] Error while executing hashcat.", "red"))
            return

    with open(temp_output, 'r') as file:
        hashcat_output = file.read()

    print(hashcat_output)

    if "Cracked" in hashcat_output:
        print(colored("[+] Hashcat found the plaintext! Saving logs...", "green"))
        time.sleep(2)
        save_logs(session)
        save_settings(session)
    else:
        print(colored("[!] Hashcat did not find the plaintext.", "red"))
        time.sleep(2)

    os.remove(temp_output)

def main():
    list_sessions(parameters["default_restorepath"])
    
    restore_file_input = input(colored(("[+]","green") + f"Restore? (Enter restore file name or leave empty): "))
    restore_file = restore_file_input or parameters["default_restorepath"]
    
    restore_session(restore_file, parameters["default_restorepath"])

    session_input = input(colored(("[+]","green") + f"Enter session name (default '{parameters['default_session']}'): "))
    session = session_input or parameters["default_session"]
    
    mask_path_input = input(colored(("[+]","green") + f"Enter Masks Path (default '{parameters['default_masks']}'): "))
    mask_path = mask_path_input or parameters["default_masks"]

    print(colored(("[+]","green") + f"Available Masks in {mask_path}: "))
    try:
        mask_files = os.listdir(mask_path)
        if not mask_files:
            print(colored("[!] Error: No masks found.", "red"))
        else:
            for mask_file in mask_files:
                print(colored("[-]", "yellow") + f" {mask_file}") 
    except FileNotFoundError:
        print(colored(f"[!] Error: The directory {mask_path} does not exist.", "red"))
        return
    
    mask_input = input(colored(("[+]","green") + f"Enter Mask (default '{parameters['default_mask']}'): "))
    mask = mask_input or parameters["default_mask"]
    
    status_timer_input = input(colored(("[+]","green") + f"Use status timer? (default '{parameters['default_status_timer']}') [y/n]: "))
    status_timer = status_timer_input or parameters["default_status_timer"]

    min_length_input = input(colored(("[+]","green") + f"Enter Minimum Length (default '{parameters['default_min_length']}'): "))
    min_length = min_length_input or parameters["default_min_length"]
    
    max_length_input = input(colored(("[+]","green") + f"Enter Maximum Length (default '{parameters['default_max_length']}'): "))
    max_length = max_length_input or parameters["default_max_length"]
    
    hashmode_input = input(colored(("[+]","green") + f"Enter hash attack mode (default '{parameters['default_hashmode']}'): "))
    hashmode = hashmode_input or parameters["default_hashmode"]
    
    workload_input = input(colored(("[+]","green") + f"Enter workload (default '{parameters['default_workload']}') [1-4]: "))
    workload = workload_input or parameters["default_workload"]

    print(colored("[+] Running Hashcat command...", "blue"))
    print(colored(f"[*] Restore >>", "magenta") + f" {parameters['default_restorepath']}/{session}")
    print(colored(f"[*] Command >>", "magenta") + f" hashcat --session={session} --increment --increment-min={min_length} --increment-max={max_length} -m {hashmode} hash.txt -a 3 -w {workload} --outfile-format=2 -o plaintext.txt {mask}")
    
    run_hashcat(session, hashmode, mask, workload, status_timer, min_length, max_length)

if __name__ == "__main__":
    main()
