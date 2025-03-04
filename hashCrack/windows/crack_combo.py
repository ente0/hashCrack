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
    define_wordlist, define_mask, define_length, define_session, define_status, define_hashmode, define_workload, define_device, define_hashcat
)
parameters = define_windows_parameters()

def run_hashcat_with_path(session, hashmode, wordlist_path, wordlist, mask_path, mask, min_length, max_length, workload, status_timer, hashcat_path, device, hash_file):
    temp_output = tempfile.mktemp()
    plaintext_path = define_logs(session)

    hashcat_command = [
        f"{hashcat_path}/hashcat.exe",
        f"--session={session}",
        "-m", hashmode,
        hash_file, 
        "-a", "6",
        "-w", workload,
        "--outfile-format=2",
        "-o", plaintext_path,
        f"{wordlist_path}/{wordlist}",
        f"{mask_path}/{mask}",
        "-d", device,
        "--potfile-disable"
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

def run_hashcat(session, hashmode, wordlist_path, wordlist, mask_path, mask, min_length, max_length, workload, status_timer, hashcat_path, device, hash_file):
    temp_output = tempfile.mktemp()
    plaintext_path = define_logs(session)

    hashcat_command = [
        f"{hashcat_path}/hashcat.exe",
        f"--session={session}", 
        "-m", hashmode, 
        hash_file, 
        "-a", "6", 
        "-w", workload, 
        "--outfile-format=2", 
        "-o", plaintext_path, 
        f"{wordlist_path}/{wordlist}", 
        f"\"{mask}\"",
        "-d", device,
        "--potfile-disable"
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
        save_logs(session, wordlist_path, wordlist, mask_path, mask)
    else:
        print(colored("[!] Hashcat did not find the plaintext.", "red"))
        time.sleep(2)

def execute_hashcat(session, hashmode, wordlist_path, wordlist, mask, min_length, max_length, workload, status_timer, hashcat_path, device, use_mask_file, hash_file, mask_path=None):
    plaintext_path, status_file_path, log_dir = define_logs(session)

    if use_mask_file:
        print(colored(f"[*] Restore >>", "magenta") + f" {hashcat_path}/{session}")
        print(colored(f"[*] Command >>", "magenta") + f" {hashcat_path}/hashcat.exe --session={session} --increment --increment-min={min_length} --increment-max={max_length} -m {hashmode} {hash_file} -a 6 -w {workload} --outfile-format=2 -o {plaintext_path} {wordlist_path}/{wordlist} {mask_path}/{mask} -d {device} --potfile-disable")
        run_hashcat_with_path(session, hashmode, wordlist_path, wordlist, mask_path, mask, min_length, max_length, workload, status_timer, hashcat_path, device, hash_file)
    else:
        print(colored(f"[*] Restore >>", "magenta") + f" {hashcat_path}/{session}")
        print(colored(f"[*] Command >>", "magenta") + f" {hashcat_path}/hashcat.exe  --session={session} --increment --increment-min={min_length} --increment-max={max_length} -m {hashmode} {hash_file} -a 6 -w {workload} --outfile-format=2 -o {plaintext_path} {wordlist_path}/{wordlist} \"{mask}\" -d {device} --potfile-disable")
        run_hashcat(session, hashmode, wordlist_path, wordlist, mask_path, mask, min_length, max_length, workload, status_timer, hashcat_path, device, hash_file)

def main():
    hash_file = define_hashfile()
    session = define_session()
    wordlist_path, wordlist = define_wordlist()
    use_mask_file, mask_path, mask = define_mask()
    status_timer = define_status()
    min_length, max_length = define_length()
    hashcat_path = define_hashcat()
    hashmode = define_hashmode()
    workload = define_workload()
    device = define_device()

    print(colored("\n[+] Running Hashcat command...", "blue"))

    execute_hashcat(session, hashmode, wordlist_path, wordlist, mask_path, mask, min_length, max_length, workload, status_timer, hashcat_path, device, use_mask_file, hash_file)

if __name__ == "__main__":
    main()
