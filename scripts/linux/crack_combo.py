import os
import sys
import subprocess
import tempfile
import time
import argparse

from datetime import datetime
from termcolor import colored

from hashCrack.functions import (
    list_sessions, save_logs, restore_session, define_default_parameters, define_hashfile
)

parameters = define_default_parameters()

def run_hashcat_with_path(session, hashmode, wordlist_path, wordlist, mask_path, mask, min_length, max_length, workload, status_timer, hashcat_path, device, hash_file):
    temp_output = tempfile.mktemp()

    hashcat_command = [
        "hashcat",
        f"--session={session}",
        "-m", hashmode,
        hash_file,
        "-a", "6",
        "-w", workload,
        "--outfile-format=2", "-o", "plaintext.txt",
        f"{wordlist_path}/{wordlist}",
        f"{mask_path}/{mask}",
        "-d", device
    ]

    if status_timer.lower() == "y":
        hashcat_command.append("--status")
        hashcat_command.append("--status-timer=2")

    hashcat_command.append("--increment")
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
        save_logs(session, wordlist_path, wordlist, mask_path, mask)
    else:
        print(colored("[!] Hashcat did not find the plaintext.", "red"))
        time.sleep(2)

def run_hashcat(session, hashmode, wordlist_path, wordlist, mask, workload, status_timer, min_length, max_length, device, hash_file):
    temp_output = tempfile.mktemp()

    hashcat_command = [
        "hashcat", 
        f"--session={session}", 
        "-m", hashmode, 
        hash_file,
        "-a", "6", 
        "-w", workload, 
        "--outfile-format=2", 
        "-o", "plaintext.txt", 
        f"{wordlist_path}/{wordlist}", 
        f"\"{mask}\"",
        "-d", device
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
        save_logs(session, wordlist_path, wordlist, mask, mask_path=None)
    else:
        print(colored("[!] Hashcat did not find the plaintext.", "red"))
        time.sleep(2)

    os.remove(temp_output)

def execute_hashcat(session, hashmode, wordlist_path, wordlist, mask, min_length, max_length, workload, status_timer, device, use_mask_file, hash_file, mask_path=None):
    if use_mask_file:
        print(colored(f"[*] Restore >>", "magenta") + f" {parameters['default_restorepath']}/{session}")
        print(colored(f"[*] Command >>", "magenta") + f" hashcat --session={session} --increment --increment-min={min_length} --increment-max={max_length} -m {hashmode} {hash_file} -a 6 -w {workload} --outfile-format=2 -o plaintext.txt {wordlist_path}/{wordlist} {mask_path}/{mask} -d {device}")
        run_hashcat_with_path(session, hashmode, wordlist_path, wordlist, mask_path, mask, min_length, max_length, workload, status_timer, device)
    else:
        print(colored(f"[*] Restore >>", "magenta") + f" {parameters['default_restorepath']}/{session}")
        print(colored(f"[*] Command >>", "magenta") + f" hashcat --session={session} --increment --increment-min={min_length} --increment-max={max_length} -m {hashmode} {hash_file} -a 6 -w {workload} --outfile-format=2 -o plaintext.txt {wordlist_path}/{wordlist} \"{mask}\" -d {device}")
        run_hashcat(session, hashmode, wordlist_path, wordlist, mask, min_length, max_length, workload, status_timer, device)

def main():
    hash_file = define_hashfile()

    list_sessions(parameters["default_restorepath"])
    
    restore_file_input = input(colored("[+] ","green") + f"Restore? (Enter restore file name or leave empty): ")
    restore_file = restore_file_input or parameters["default_restorepath"]
    
    restore_session(restore_file, parameters["default_restorepath"])

    session_input = input(colored("[+] ","green") + f"Enter session name (default '{parameters['default_session']}'): ")
    session = session_input or parameters["default_session"]
    
    wordlist_path_input = input(colored("[+] ","green") + f"Enter Wordlists Path (default '{parameters['default_wordlists']}'): ")
    wordlist_path = wordlist_path_input or parameters["default_wordlists"]

    print(colored("[+] ","green") + f"Available Wordlists in {wordlist_path}: ")
    try:
        wordlist_files = os.listdir(wordlist_path)
        if not wordlist_files:
            print(colored("[!] Error: No wordlists found.", "red"))
        else:
            for wordlist_file in wordlist_files:
                print(colored("[-]", "yellow") + f" {wordlist_file}") 
    except FileNotFoundError:
        print(colored(f"[!] Error: The directory {wordlist_path} does not exist.", "red"))
        return

    wordlist_input = input(colored("[+] ","green") + f"Enter Wordlist (default '{parameters['default_wordlist']}'): ")
    wordlist = wordlist_input or parameters["default_wordlist"]
    
    use_mask_file = input(colored("[+] ", "green") + "Do you want to use a mask file? [y/n]: ").strip().lower()

    if use_mask_file == 'y':
        mask_path_input = input(colored("[+] ", "green") + f"Enter Masks Path (default '{parameters['default_masks']}'): ")
        mask_path = mask_path_input or parameters["default_masks"]

        print(colored("[+] ", "green") + f"Available Masks in {mask_path}: ")
        try:
            mask_files = os.listdir(mask_path)
            if not mask_files:
                print(colored("[!] Error: No masks found.", "red"))
            else:
                for mask_file in mask_files:
                    print(colored("[-] ", "yellow") + f"{mask_file}")
        except FileNotFoundError:
            print(colored(f"[!] Error: The directory {mask_path} does not exist.", "red"))
            return

        mask_input = input(colored("[+] ", "green") + f"Enter Mask (default '{parameters['default_mask']}'): ")
        mask = mask_input or parameters["default_mask"]
    else:
        mask = input(colored("[+] ", "green") + "Enter manual mask (e.g., '?a?a?a?a?a?a'): ")

        if not mask:
            print(colored("[!] Error: No mask entered. Using default mask.", "red"))
            mask = parameters["default_mask"]

    status_timer_input = input(colored("[+] ","green") + f"Use status timer? (default '{parameters['default_status_timer']}') [y/n]: ")
    status_timer = status_timer_input or parameters["default_status_timer"]

    min_length_input = input(colored("[+] ","green") + f"Enter Minimum Length (default '{parameters['default_min_length']}'): ")
    min_length = min_length_input or parameters["default_min_length"]
    
    max_length_input = input(colored("[+] ","green") + f"Enter Maximum Length (default '{parameters['default_max_length']}'): ")
    max_length = max_length_input or parameters["default_max_length"]
    
    hashmode_input = input(colored("[+] ","green") + f"Enter hash attack mode (default '{parameters['default_hashmode']}'): ")
    hashmode = hashmode_input or parameters["default_hashmode"]
    
    workload_input = input(colored("[+] ","green") + f"Enter workload (default '{parameters['default_workload']}') [1-4]: ")
    workload = workload_input or parameters["default_workload"]

    device_input = input(colored("[+] ", "green") + f"Enter device (default '{parameters['default_device']}'): ")
    device = device_input or parameters["default_device"]

    print(colored("[+] Running Hashcat command...", "blue"))
    
    execute_hashcat(session, hashmode, wordlist_path, wordlist, mask, min_length, max_length, workload, status_timer, device, use_mask_file, hash_file, mask_path=None)

if __name__ == "__main__":
    main()
