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

def run_hashcat(session, hashmode, wordlist_path, wordlist, rule_path, rule, workload, status_timer):
    temp_output = tempfile.mktemp()

    hashcat_command = [
        "hashcat", 
        f"--session={session}", 
        f"-m {hashmode}", 
        "hash.txt", 
        "-a 0", 
        f"-w {workload}", 
        "--outfile-format=2", 
        "-o", "plaintext.txt", 
        f"{wordlist_path}/{wordlist}", 
        f"-r {rule_path}/{rule}"
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
    restore_file_input = input(colored("Restore? (Enter restore file name or leave empty): ", "red"))
    restore_session(
        parameters["restore_file_input"], 
        parameters["default_restorepath"], 
        parameters["default_hashmode"], 
        parameters["workload"], 
        parameters["default_wordlists"],    
        parameters["default_wordlist"]
    )

    session_input = input(colored(f"Enter session name (default '{parameters['default_session']}'): ", "magenta"))
    session = session_input or parameters["default_session"]

    wordlist_path_input = input(colored(f"Enter Wordlists Path (default '{parameters['default_wordlists']}'): ", "red"))
    wordlist_path = wordlist_path_input or parameters["default_wordlists"]

    print(colored(f"Available Wordlists in {wordlist_path}: ", "magenta"))
    for wordlist_file in os.listdir(wordlist_path):
        print(wordlist_file)

    wordlist_input = input(colored(f"Enter Wordlist (default '{parameters['default_wordlist']}'): ", "magenta"))
    wordlist = wordlist_input or parameters["default_wordlist"]

    rule_path_input = input(colored(f"Enter Rules Path (default '{parameters['default_rules']}'): ", "red"))
    rule_path = rule_path_input or parameters["default_rules"]

    print(colored(f"Available Rules in {rule_path}: ", "magenta"))
    for rule_file in os.listdir(rule_path):
        print(rule_file)

    rule_input = input(colored(f"Enter Rule (default '{parameters['default_rule']}'): ", "magenta"))
    rule = rule_input or parameters["default_rule"]

    hashmode_input = input(colored(f"Enter hash attack mode (default '{parameters['default_hashmode']}'): ", "magenta"))
    hashmode = hashmode_input or parameters["default_hashmode"]

    workload_input = input(colored(f"Enter workload (default '{parameters['default_workload']}') [1-4]: ", "magenta"))
    workload = workload_input or parameters["default_workload"]

    status_timer_input = input(colored(f"Use status timer? (default '{parameters['default_status_timer']}') [y/n]: ", "magenta"))
    status_timer = status_timer_input or parameters["default_status_timer"]

    print(colored(f"Restore >> {parameters['default_restorepath']}/{session}", "green"))
    print(colored(f"Command >> hashcat --session={session} -m {hashmode} hash.txt -a 0 -w {workload} --outfile-format=2 -o plaintext.txt {wordlist_path}/{wordlist} -r {rule_path}/{rule}", "green"))

    run_hashcat(session, hashmode, wordlist_path, wordlist, rule_path, rule, workload, status_timer)

if __name__ == "__main__":
    main()
