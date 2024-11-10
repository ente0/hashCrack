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

def run_hashcat(session, hashmode, wordlist_path, wordlist, mask_path, mask, min_length, max_length, workload, status_timer, hashcat_path):
    temp_output = tempfile.mktemp()

    hashcat_command = [
        f"{hashcat_path}/hashcat.exe",
        f"--session={session}",
        "-m", hashmode,
        "hash.txt", "-a", "6",
        f"-w {workload}",
        "--outfile-format=2", "-o", "plaintext.txt",
        f"{wordlist_path}/{wordlist}",
        mask
    ]

    if status_timer.lower() == "y":
        hashcat_command.extend(["--status", "--status-timer=2"])

    try:
        with open(temp_output, 'w') as output_file:
            subprocess.run(hashcat_command, check=True, stdout=output_file, stderr=subprocess.STDOUT)

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

    except subprocess.CalledProcessError:
        print(colored("Error while executing hashcat.", "red"))
    finally:
        os.remove(temp_output)

def main():
    list_sessions()

    restore_file_input = input(colored("\nRestore? (Enter restore file name or leave empty): ", "red"))
    restore_session(restore_file_input)

    session_input = input(colored(f"Enter session name (default '{parameters['default_session']}'): ", "magenta"))
    session = session_input or parameters["default_session"]

    wordlist_path_input = input(colored(f"Enter Wordlist Path (default '{parameters['default_wordlists']}'): ", "red"))
    wordlist_path = wordlist_path_input or parameters["default_wordlists"]

    print(colored(f"Available Wordlists in {wordlist_path}:", "magenta"))
    for f in os.listdir(wordlist_path):
        print(f)
    
    wordlist_input = input(colored(f"Enter Wordlist (default '{parameters['default_wordlist']}'): ", "magenta"))
    wordlist = wordlist_input or parameters["default_wordlist"]

    mask_path_input = input(colored(f"Enter Masks Path (default '{parameters['default_masks']}'): ", "red"))
    mask_path = mask_path_input or parameters["default_masks"]

    print(colored(f"Available Masks in {mask_path}:", "magenta"))
    for f in os.listdir(mask_path):
        print(f)
    
    mask_input = input(colored(f"Enter Mask (default '{parameters['default_mask']}'): ", "magenta"))
    mask = mask_input or parameters["default_mask"]

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

    status_timer_input = input(colored("Use status timer? (y/n): ", "magenta"))
    status_timer = status_timer_input or parameters["default_status_timer"]

    print(colored(f"Restore >> {hashcat_path}/{session}", "green"))
    print(colored(f"Command >> {os.path.join(hashcat_path, 'hashcat.exe')} --session={session} --increment --increment-min={min_length} --increment-max={max_length} -m {hashmode} hash.txt -a 6 -w {workload} --outfile-format=2 -o plaintext.txt {os.path.join(wordlist_path, wordlist)} {os.path.join(mask_path, mask)}", "green"))

    run_hashcat(session, hashmode, wordlist_path, wordlist, mask_path, mask, min_length, max_length, workload, status_timer, hashcat_path)

if __name__ == "__main__":
    main()
