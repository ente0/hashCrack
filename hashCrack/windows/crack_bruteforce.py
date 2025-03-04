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
    define_mask, define_length, define_session, define_status, define_hashmode, define_workload, define_device, define_hashcat
)
parameters = define_windows_parameters()

def run_hashcat(session, hashmode, mask, workload, status_timer, min_length, max_length, hash_file, hashcat_path, device):
    temp_output = tempfile.mktemp()
    plaintext_path = define_logs(session)

    hashcat_command = [
        f"{hashcat_path}/hashcat.exe",
        f"--session={session}",
        "-m", hashmode,
        hash_file,
        "-a", "3",
        "-w", workload,
        "--outfile-format=2",
        "-o", plaintext_path,
        f"\"{mask}\"",
        "-d", device,
        "--potfile-disable"
    ]

    hashcat_command.append(f"--increment")
    hashcat_command.append(f"--increment-min={min_length}")
    hashcat_command.append(f"--increment-max={max_length}")

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
        save_logs(session, mask)
    else:
        print(colored("[!] Hashcat did not find the plaintext.", "red"))
        time.sleep(2)

    os.remove(temp_output)

def main():
    hash_file = define_hashfile()
    session = define_session()
    use_mask_file, mask_path, mask = define_mask()
    hashmode = define_hashmode()
    hashcat_path = define_hashcat()
    status_timer = define_status()
    min_length, max_length = define_length()
    hashcat_path = define_hashcat()
    workload = define_workload()
    device = define_device()
    plaintext_path, status_file_path, log_dir = define_logs(session)

    print(colored("\n[+] Running Hashcat command...", "blue"))
    print(colored(f"[*] Restore >>", "magenta") + f" {hashcat_path}/{session}")
    print(colored(f"[*] Command >>", "magenta") + f" {hashcat_path}/hashcat.exe --session={session} --increment --increment-min={min_length} --increment-max={max_length} -m {hashmode} {hash_file} -a 3 -w {workload} --outfile-format=2 -o {plaintext_path} \"{mask}\" -d {device} --potfile-disable")

    run_hashcat(session, hashmode, mask, workload, status_timer, min_length, max_length, hash_file, hashcat_path, device)

if __name__ == "__main__":
    main()
