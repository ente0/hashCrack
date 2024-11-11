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
        "-a 6", 
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
    restore_file_input = input(colored("Restore? (Enter restore file name or leave empty): ", "red"))
    restore_session(
        parameters["restore_file_input"], 
        parameters["default_restorepath"], 
        parameters["default_hashmode"], 
        parameters["workload"], 
        parameters["default_wordlists"],    
        parameters["default_wordlist"]
    )

    session_input = input(colored("Enter session name (default '{}'): ".format(parameters["default_session"]), "magenta"))
    session = session_input or parameters["default_session"]
    
    wordlist_path_input = input(colored("Enter Wordlists Path (default '{}'): ".format(parameters["default_wordlists"]), "red"))
    wordlist_path = wordlist_path_input or parameters["default_wordlists"]

    print(colored("Available Wordlists in {}: ".format(wordlist_path), "magenta"))
    for wordlist_file in os.listdir(wordlist_path):
        print(wordlist_file)
    
    wordlist_input = input(colored("Enter Wordlist (default '{}'): ".format(parameters["default_wordlist"]), "magenta"))
    wordlist = wordlist_input or parameters["default_wordlist"]
    
    mask_path_input = input(colored("Enter Masks Path (default '{}'): ".format(parameters["default_masks"]), "red"))
    masks_path = mask_path_input or parameters["default_masks"]

    print(colored("Available Masks in {}: ".format(masks_path), "magenta"))
    for mask_file in os.listdir(masks_path):
        print(mask_file)
    
    mask_input = input(colored("Enter Mask (default '{}'): ".format(parameters["default_mask"]), "magenta"))
    mask = mask_input or parameters["default_mask"]

    min_length_input = input(colored("Enter Minimum Length (default '{}'): ".format(parameters["default_min_length"]), "magenta"))
    min_length = min_length_input or parameters["default_min_length"]
    
    max_length_input = input(colored("Enter Maximum Length (default '{}'): ".format(parameters["default_max_length"]), "magenta"))
    max_length = max_length_input or parameters["default_max_length"]

    status_timer_input = input(colored("Use status timer? (default '{}') [y/n]: ".format(parameters["default_status_timer"]), "magenta"))
    status_timer = status_timer_input or parameters["default_status_timer"]

    hashmode_input = input(colored("Enter hash attack mode (default '{}'): ".format(parameters["default_hashmode"]), "magenta"))
    hashmode = hashmode_input or parameters["default_hashmode"]
    
    workload_input = input(colored("Enter workload (default '{}') [1-4]: ".format(parameters["default_workload"]), "magenta"))
    workload = workload_input or parameters["default_workload"]

    print(colored("Running Hashcat command...", "green"))
    run_hashcat(session, hashmode, wordlist_path, wordlist, mask, workload, status_timer, min_length, max_length)

if __name__ == "__main__":
    main()
