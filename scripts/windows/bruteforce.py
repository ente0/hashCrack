import os
import subprocess
import tempfile
import time
from datetime import datetime
from termcolor import colored
from functions import (
    list_sessions, save_logs, save_settings, restore_session, define_windows_parameters
)

parameters = define_windows_parameters()

def run_hashcat(session, hashmode, mask, workload, status_timer, hashcat_path):
    temp_output = tempfile.mktemp()

    hashcat_command = [
        f"{hashcat_path}/hashcat.exe",
        f"--session={session}",
        "-m", hashmode,
        "hash.txt", "-a", "3", 
        f"-w {workload}",
        "--outfile-format=2", "-o", "plaintext.txt", 
        mask
    ]

    if status_timer.lower() == "y":
        hashcat_command.extend(["--status", "--status-timer=2"])

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

    session_input = input(colored(f"Enter session name (default '{parameters['default_session']}'): ", "magenta"))
    session = session_input or parameters["default_session"]

    mask_input = input(colored(f"Enter Mask (default '{parameters['default_mask']}'): ", "magenta"))
    mask = mask_input or parameters["default_mask"]

    status_timer_input = input(colored("Use status timer? (y/n): ", "magenta"))
    status_timer = status_timer_input or parameters["default_status_timer"]

    min_length_input = input(colored(f"Enter Minimum Length (default '{parameters['default_min_length']}'): ", "magenta"))
    min_length = min_length_input or parameters["default_min_length"]

    max_length_input = input(colored(f"Enter Maximum Length (default '{parameters['default_max_length']}'): ", "magenta"))
    max_length = max_length_input or parameters["default_max_length"]

    hashcat_path_input = input(colored(f"Enter Hashcat Path (default '{parameters['default_hashcat']}'): ", "red"))
    hashcat_path = hashcat_path_input or parameters["default_hashcat"]

    hashmode_input = input(colored(f"Enter hash attack mode (default '{parameters['default_hashmode']}'): ", "magenta"))
    hashmode = hashmode_input or parameters["default_hashmode"]

    workload_input = input(colored(f"Enter workload (default '{parameters['default_workload']}') [1-4]: ", "magenta"))
    workload = workload_input or parameters["default_workload"]

    print(colored(f"Restore >> {hashcat_path}/{session}", "green"))
    print(colored(f"Command >> {hashcat_path}/hashcat.exe --session={session} --increment --increment-min={min_length} --increment-max={max_length} -m {hashmode} hash.txt -a 3 -w {workload} --outfile-format=2 -o plaintext.txt {mask}", "green"))

    run_hashcat(session, hashmode, mask, workload, status_timer, hashcat_path)

if __name__ == "__main__":
    main()
