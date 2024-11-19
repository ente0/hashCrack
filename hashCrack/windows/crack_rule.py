import os
import sys
import subprocess
import tempfile
import time
import argparse

from datetime import datetime
from termcolor import colored

from hashCrack.functions import (
    list_sessions, save_logs, restore_session, define_windows_parameters, define_hashfile, define_logs
)

parameters = define_windows_parameters()

def run_hashcat(session, hashmode, wordlist_path, wordlist, rule_path, rule, workload, status_timer, hashcat_path, device, hash_file):
    temp_output = tempfile.mktemp()
    plaintext_path = define_logs(session)

    hashcat_command = [
        f"{hashcat_path}/hashcat.exe",
        f"--session={session}", 
        "-m", hashmode, 
        hash_file,
        "-a", "0", 
        "-w", workload, 
        "--outfile-format=2", 
        "-o", plaintext_path, 
        f"{wordlist_path}/{wordlist}", 
        "-r", f"{rule_path}/{rule}",
        "-d", device,
        "--potfile-disable"
    ]

    if status_timer.lower() == "y":
        hashcat_command.extend(["--status", "--status-timer=2"])

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
        save_logs(session, wordlist_path, wordlist, rule_path, rule)
    else:
        print(colored("[!] Hashcat did not find the plaintext.", "red"))
        time.sleep(2)

    os.remove(temp_output)

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

    rule_path_input = input(colored("[+] ","green") + f"Enter Rules Path (default '{parameters['default_rules']}'): ")
    rule_path = rule_path_input or parameters["default_rules"]

    print(colored("[+] ","green") + f"Available Rules in {rule_path}: ")
    try:
        rule_files = os.listdir(rule_path)
        if not rule_files:
            print(colored("[!] Error: No rules found.", "red"))
        else:
            for rule_file in rule_files:
                print(colored("[-]", "yellow") + f" {rule_file}") 
    except FileNotFoundError:
        print(colored(f"[!] Error: The directory {rule_path} does not exist.", "red"))
        return

    rule_input = input(colored("[+] ","green") + f"Enter Rule (default '{parameters['default_rule']}'): ")
    rule = rule_input or parameters["default_rule"]

    status_timer_input = input(colored("[+] ","green") + f"Use status timer? (default '{parameters['default_status_timer']}') [y/n]: ")
    status_timer = status_timer_input or parameters["default_status_timer"]

    hashcat_path_input = input(colored("[+] ","green") + f"Enter Hashcat Path (default '{parameters['default_hashcat']}'): ")
    hashcat_path = hashcat_path_input or parameters["default_hashcat"]

    hashmode_input = input(colored("[+] ","green") + f"Enter hash attack mode (default '{parameters['default_hashmode']}'): ")
    hashmode = hashmode_input or parameters["default_hashmode"]

    workload_input = input(colored("[+] ","green") + f"Enter workload (default '{parameters['default_workload']}') [1-4]: ")
    workload = workload_input or parameters["default_workload"]

    device_input = input(colored("[+] ", "green") + f"Enter device (default '{parameters['default_device']}'): ")
    device = device_input or parameters["default_device"]

    plaintext_path, status_file_path, log_dir = define_logs(session)

    print(colored("[+] Running Hashcat command...", "blue"))
    print(colored(f"[*] Restore >>", "magenta") + f" {hashcat_path}/{session}")
    print(colored(f"[*] Command >>", "magenta") + f" {hashcat_path}/hashcat.exe --session={session} -m {hashmode} {hash_file} -a 0 -w {workload} --outfile-format=2 -o {plaintext_path} {wordlist_path}/{wordlist} -r {rule_path}/{rule} -d {device} --potfile-disable")

    run_hashcat(session, hashmode, wordlist_path, wordlist, rule_path, rule, workload, status_timer, hashcat_path, device, hash_file)

if __name__ == "__main__":
    main()
