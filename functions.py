import os
import sys
import time
import random
import subprocess
from datetime import datetime
from termcolor import colored

default_scripts = os.path.expanduser("~/hashCrack")
default_windows_scripts = f"/c/Users/{os.getenv('USER')}/source/repos/ente0v1/hashCrack/scripts/windows"

def define_default_parameters():
    return {
        "default_hashcat": ".",
        "default_status_timer": "y",
        "default_workload": "4",
        "default_os": "Linux",
        "default_restorepath": os.path.expanduser("~/.local/share/hashcat/sessions"),
        "default_session": datetime.now().strftime("%Y-%m-%d"),
        "default_wordlists": "wordlists",
        "default_masks": "masks",
        "default_rules": "rules",
        "default_wordlist": "rockyou.txt",
        "default_mask": "?d?d?d?d",
        "default_rule": "T0XlCv2.rule",
        "default_min_length": "4",
        "default_max_length": "16",
        "default_hashmode": "22000",
        "default_device": "2"
    }

def define_windows_parameters():
    return {
        "default_hashcat": ".",
        "default_status_timer": "y",
        "default_workload": "4",
        "default_os": "Windows",
        "default_restorepath": os.path.expanduser("~/hashcat/sessions"),
        "default_session": datetime.now().strftime("%Y-%m-%d"),
        "default_wordlists": f"/c/Users/{os.getenv('USER')}/wordlists",
        "default_masks": "masks",
        "default_rules": "rules",
        "default_wordlist": "rockyou.txt",
        "default_mask": "?d?d?d?d",
        "default_rule": "T0XlCv2.rule",
        "default_min_length": "4",
        "default_max_length": "16",
        "default_hashmode": "22000",
        "default_device": "2"
    }

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_menu(default_os):
    ascii_art = """
888                        888       .d8888b.                           888     
888                        888      d88P  Y88b                          888     
888                        888      888    888                          888     
88888b.   8888b.  .d8888b  88888b.  888        888d888 8888b.   .d8888b 888  888
888 "88b     "88b 88K      888 "88b 888        888P"      "88b d88P"    888 .88P
888  888 .d888888 "Y8888b. 888  888 888    888 888    .d888888 888      888888K 
888  888 888  888      X88 888  888 Y88b  d88P 888    888  888 Y88b.    888 "88b
888  888 "Y888888  88888P' 888  888  "Y8888P"  888    "Y888888  "Y8888P 888  888
    """
    print(colored(ascii_art, 'cyan'))
    print(colored("="*80, 'cyan'))
    print(colored(f"   Welcome to hashCrack! - Menu Options for {default_os}", 'cyan', attrs=['bold']))
    print(colored("="*80, 'cyan'))
    options = [
        f"{colored('[1]', 'blue', attrs=['bold'])} Crack with Wordlist          {colored('[EASY]', 'blue', attrs=['bold'])}",
        f"{colored('[2]', 'green', attrs=['bold'])} Crack with Association       {colored('[MEDIUM]', 'green', attrs=['bold'])}",
        f"{colored('[3]', 'yellow', attrs=['bold'])} Crack with Brute-Force       {colored('[HARD]', 'yellow', attrs=['bold'])}",
        f"{colored('[4]', 'red', attrs=['bold'])} Crack with Combinator        {colored('[ADVANCED]', 'red', attrs=['bold'])}",
        f"\n{colored('[5]', 'magenta', attrs=['bold'])} Clear Hashcat Potfile        {colored('[UTILITY]', 'magenta', attrs=['bold'])}"
    ]
    print("\n   " + "\n   ".join(options))
    print(colored("\n" + "="*80, 'magenta'))
    print(f"   {colored('Press X to switch to Windows' if default_os == 'Linux' else 'Press X to switch to Linux', 'magenta', attrs=['bold'])}.")
    print(colored("="*80, 'magenta'))

    user_option = input(colored("\nEnter option (1-5, X to switch OS, Q to quit): ", 'cyan', attrs=['bold'])).strip().lower()

    if user_option == 'x':
        default_os = "Linux" if default_os == "Windows" else "Windows"
        print(f"System switched to {default_os}")
        time.sleep(1)

    elif user_option == 'q':
        print("Exiting program...")
        sys.exit(0) 

    elif user_option == '5':
        if default_os == 'Linux':
            os.system("sudo rm ~/.local/share/hashcat/hashcat.potfile")
            print(colored("[+] Hashcat potfile cleared for Linux.", 'green'))
        elif default_os == 'Windows':
            os.system("del %userprofile%\\hashcat\\hashcat.potfile")
            print(colored("[+] Hashcat potfile cleared for Windows.", 'green'))
        time.sleep(1)

    return user_option, default_os


def animate_text(text, delay):
    for i in range(len(text) + 1):
        clear_screen()
        print(text[:i], end="", flush=True)
        time.sleep(delay)

def handle_option(option, default_os):
    animate_text("...", 0.1)
    
    script_map = {
        "1": "crack_wordlist.py",
        "2": "crack_rule.py",
        "3": "crack_bruteforce.py",
        "4": "crack_combo.py"
    }
    
    script_type = "windows" if default_os == "Windows" else "linux"
    script_name = script_map.get(option, None)

    if script_name:
        script_path = f"scripts/{script_type}/{script_name}"
        print(f"{colored(f'{script_path} is Executing', 'green')}")
        
        if default_os == "Linux":
            os.system(f"python3 {script_path}")
        else:
            os.system(f"python {script_path}")

        input("Press Enter to return to the menu...")

    elif option.lower() == "q":
        animate_text("Exiting...", 0.1)
        print(colored("Done! Exiting...", 'yellow'))
        exit(0)
    else:
        print(colored("Invalid option. Please try again.", 'red'))


def execute_windows_scripts():
    windows_scripts_dir = "scripts/windows"
    if os.path.isdir(windows_scripts_dir):
        for script in os.listdir(windows_scripts_dir):
            script_path = os.path.join(windows_scripts_dir, script)
            if os.path.isfile(script_path):
                print(f"Executing Windows script: {script}")
                os.system(f"python {script_path}")
    else:
        print(colored(f"Windows scripts directory not found: '{windows_scripts_dir}'", 'red'))

def save_settings(session, path_wordlists, default_wordlist, mask, rule):
    with open("status.txt", "w") as f:
        f.write(f"\nSession: {session}")
        f.write(f"\nWordlist: {path_wordlists}/{default_wordlist}")
        f.write(f"\nMask: {mask}")
        f.write(f"\nRule: {rule}")
        f.write(f"\nHash: {open('hash.txt').read()}")
        f.write(f"\nPlaintext: {open('plaintext.txt').read()}")

def list_sessions(default_restorepath):
    try:
        restore_files = [f for f in os.listdir(default_restorepath) if f.endswith('.restore')]
        if restore_files:
            print(colored("[+] Available sessions:", "green"))
            for restore_file in restore_files:
                print(colored("[-]", "yellow") + f" {restore_file}")
        else:
            print(colored("[!] No restore files found...", "red"))
    except FileNotFoundError:
        print(colored(f"[!] Error: The directory {default_restorepath} does not exist.", "red"))

def restore_session(restore_file_input, default_restorepath):
    if not restore_file_input:
        list_sessions(default_restorepath)
        restore_file_input = input(colored(f"[+] Restore? (Enter restore file name or leave empty): ", "green"))
    
    restore_file = os.path.join(default_restorepath, f"{restore_file_input}.restore")
     
    if not os.path.isfile(restore_file):
        print(colored(f"[!] Error: Restore file '{restore_file}' not found.", 'red'))
        return

    session = os.path.basename(restore_file).replace(".restore", "")
    print(colored(f"[+] Restoring session >> {restore_file}", 'blue'))

    cmd = f"hashcat --session={session} --restore"
    print(colored(f"[+] Executing: {cmd}", "blue"))
    os.system(cmd)

import os

def save_logs(session):
    os.makedirs(f"logs/{session}", exist_ok=True)

    if os.path.exists("status.txt"):
        os.rename("status.txt", f"logs/{session}/status.txt")
    else:
        print(colored("[!] Warning: 'status.txt' not found, skipping.", "red"))

    if os.path.exists("plaintext.txt"):
        os.rename("plaintext.txt", f"logs/{session}/plaintext.txt")
    else:
        print(colored("Warning: 'plaintext.txt' not found, skipping.", "red"))

