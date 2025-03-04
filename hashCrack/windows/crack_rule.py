import os
import sys
import subprocess
import tempfile
import time
import argparse

from datetime import datetime
from termcolor import colored

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from hashCrack.functions import (
    save_logs, define_windows_parameters, define_hashfile, define_logs
)
from hashCrack.linux_inputs import (
    define_wordlist, define_rule, define_session, define_status, define_hashmode, define_workload, define_device, define_hashcat
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
    session = define_session()
    wordlist_path, wordlist = define_wordlist()
    rule_path, rule = define_rule()
    hashmode = define_hashmode()
    status_timer = define_status()
    hashcat_path = define_hashcat()
    workload = define_workload()
    device = define_device()
    plaintext_path, status_file_path, log_dir = define_logs(session)

    print(colored("\n[+] Running Hashcat command...", "blue"))
    print(colored(f"[*] Restore >>", "magenta") + f" {hashcat_path}/{session}")
    print(colored(f"[*] Command >>", "magenta") + f" {hashcat_path}/hashcat.exe --session={session} -m {hashmode} {hash_file} -a 0 -w {workload} --outfile-format=2 -o {plaintext_path} {wordlist_path}/{wordlist} -r {rule_path}/{rule} -d {device} --potfile-disable")

    run_hashcat(session, hashmode, wordlist_path, wordlist, rule_path, rule, workload, status_timer, device, hash_file)

if __name__ == "__main__":
    main()

