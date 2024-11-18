import os
import sys
import time
import random
import subprocess
import shutil
import argparse
from datetime import datetime
from termcolor import colored

default_scripts = os.path.expanduser("~/hashCrack")
default_windows_scripts = f"/c/Users/{os.getenv('USER')}/source/repos/ente0v1/hashCrack/scripts/windows"

def define_default_parameters():
    return {
        "default_hashcat": ".",
        "default_status_timer": "y",
        "default_workload": "3",
        "default_os": "Linux",
        "default_restorepath": os.path.expanduser("~/.local/share/hashcat/sessions"),
        "default_session": datetime.now().strftime("%Y-%m-%d"),
        "default_wordlists": "wordlists",
        "default_masks": "masks",
        "default_rules": "rules",
        "default_wordlist": "rockyou.txt",
        "default_mask": "?d?d?d?d?d?d?d?d",
        "default_rule": "T0XlCv2.rule",
        "default_min_length": "8",
        "default_max_length": "16",
        "default_hashmode": "22000",
        "default_device": "1"
    }

def define_windows_parameters():
    return {
        "default_hashcat": ".",
        "default_status_timer": "y",
        "default_workload": "3",
        "default_os": "Windows",
        "default_restorepath": os.path.expanduser("~/hashcat/sessions"),
        "default_session": datetime.now().strftime("%Y-%m-%d"),
        "default_wordlists": f"/c/Users/{os.getenv('USER')}/wordlists",
        "default_masks": "masks",
        "default_rules": "rules",
        "default_wordlist": "rockyou.txt",
        "default_mask": "?d?d?d?d?d?d?d?d",
        "default_rule": "T0XlCv2.rule",
        "default_min_length": "8",
        "default_max_length": "16",
        "default_hashmode": "22000",
        "default_device": "1"
    }

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_menu1(default_os):
    ascii_art = """
888                        888       .d8888b.                           888     
888                        888      d88P  Y88b                          888     
888                        888      888    888                          888     
88888b.   8888b.  .d8888b  88888b.  888        888d888 8888b.   .d8888b 888  888
888 "88b     "88b 88K      888 "88b 888        888P"      "88b d88P"    888 .88P
888  888 .d888888 "Y8888b. 888  888 888    888 888    .d888888 888      888888K 
888  888 888  888      X88 888  888 Y88b  d88P 888    888  888 Y88b.    888 "88b
888  888 "Y888888  88888P' 888  888  "Y8888P"  888    "Y888888  "Y8888P 888  888
       
       For more information, visit: https://github.com/ente0v1/hashCrack
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
    ]
    print("\n   " + "\n   ".join(options))

    print(colored("-"*80, 'cyan')) 

    print(f"{colored('   [0]', 'magenta', attrs=['bold'])} Clear Hashcat Potfile        {colored('[UTILITY]', 'magenta', attrs=['bold'])}")

    print(colored("\n" + "="*80, 'magenta'))
    print(f"   {colored('Press X to switch to Windows' if default_os == 'Linux' else 'Press X to switch to Linux', 'magenta', attrs=['bold'])}.")
    print(colored("="*80, 'magenta'))

    user_option = input(colored("\nEnter option (0-4, X to switch OS, Q to quit): ", 'cyan', attrs=['bold'])).strip().lower()

    if user_option == 'x':
        default_os = "Linux" if default_os == "Windows" else "Windows"
        print(f"System switched to {default_os}")
        time.sleep(1)

    elif user_option == 'q':
        print("Exiting program...")
        sys.exit(0) 

    elif user_option == '0':
        if default_os == 'Linux':
            os.system("sudo rm ~/.local/share/hashcat/hashcat.potfile")
            print(colored("[+] Hashcat potfile cleared for Linux.", 'green'))
        elif default_os == 'Windows':
            os.system("del %userprofile%\\hashcat\\hashcat.potfile")
            print(colored("[+] Hashcat potfile cleared for Windows.", 'green'))
        time.sleep(1)

    return user_option, default_os

def show_menu2(default_os):
    ascii_art = r"""
dP                         dP       MM"'""'"YMM                            dP      
88                         88       M' .mmm. `M                            88      
88d888b. .d8888b. .d8888b. 88d888b. M  MMMMMooM 88d888b. .d8888b. .d8888b. 88  .dP 
88'  `88 88'  `88 Y8ooooo. 88'  `88 M  MMMMMMMM 88'  `88 88'  `88 88'  `"" 88888"  
88    88 88.  .88       88 88    88 M. `MMM' .M 88       88.  .88 88.  ... 88  `8b.
dP    dP `88888P8 `88888P' dP    dP MM.     .dM dP       `88888P8 `88888P' dP   `YP
                                    MMMMMMMMMMM  
         
         For more information, visit: https://github.com/ente0v1/hashCrack
    """
    print(colored(ascii_art, 'cyan'))
    print(colored("="*83, 'cyan'))
    print(colored(f"   Welcome to hashCrack! - Menu Options for {default_os}", 'cyan', attrs=['bold']))
    print(colored("="*83, 'cyan'))
    options = [
        f"{colored('[1]', 'blue', attrs=['bold'])} Crack with Wordlist          {colored('[EASY]', 'blue', attrs=['bold'])}",
        f"{colored('[2]', 'green', attrs=['bold'])} Crack with Association       {colored('[MEDIUM]', 'green', attrs=['bold'])}",
        f"{colored('[3]', 'yellow', attrs=['bold'])} Crack with Brute-Force       {colored('[HARD]', 'yellow', attrs=['bold'])}",
        f"{colored('[4]', 'red', attrs=['bold'])} Crack with Combinator        {colored('[ADVANCED]', 'red', attrs=['bold'])}",
    ]
    print("\n   " + "\n   ".join(options))

    print(colored("-"*83, 'cyan')) 

    print(f"{colored('   [0]', 'magenta', attrs=['bold'])} Clear Hashcat Potfile        {colored('[UTILITY]', 'magenta', attrs=['bold'])}")

    print(colored("\n" + "="*83, 'magenta'))
    print(f"   {colored('Press X to switch to Windows' if default_os == 'Linux' else 'Press X to switch to Linux', 'magenta', attrs=['bold'])}.")
    print(colored("="*83, 'magenta'))

    user_option = input(colored("\nEnter option (0-4, X to switch OS, Q to quit): ", 'cyan', attrs=['bold'])).strip().lower()

    if user_option == 'x':
        default_os = "Linux" if default_os == "Windows" else "Windows"
        print(f"System switched to {default_os}")
        time.sleep(1)

    elif user_option == 'q':
        print("Exiting program...")
        sys.exit(0) 

    elif user_option == '0':
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

def handle_option(option, default_os, hash_file):
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
            os.system(f"python3 {script_path} {hash_file}")
        else:
            os.system(f"python {script_path} {hash_file}")

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
                print(f"[+] Executing Windows script: {script}","green")
                os.system(f"python {script_path}")
    else:
        print(colored(f"[!] Error: Windows scripts directory not found: '{windows_scripts_dir}'", "red"))

def save_logs(session, wordlist_path=None, wordlist=None, mask_path=None, mask=None, rule_path=None, rule=None):
    home_dir = os.path.expanduser("~")
    log_dir = os.path.join(home_dir, "hashCrack", "logs", session)
    os.makedirs(log_dir, exist_ok=True)

    status_file_path = os.path.join(log_dir, "status.txt")
    
    with open(status_file_path, "w") as f:
        f.write(f"\nSession: {session}")
        
        if wordlist and wordlist_path:
            f.write(f"\nWordlist: {wordlist_path}/{wordlist}")
        else:
            f.write("\nWordlist: N/A")
        
        if mask_path and mask:
            f.write(f"\nMask File: {mask_path}/{mask}")
        else:
            f.write(f"\nMask: {mask if mask else 'N/A'}")

        if rule_path and rule:
            f.write(f"\nRule: {rule_path}/{rule}")
        elif rule:
            f.write(f"\nRule: {rule}")
        else:
            f.write("\nRule: N/A")

        try:
            with open("hash.txt", "r") as hash_file:
                f.write(f"\nHash: {hash_file.read().strip()}")
        except FileNotFoundError:
            f.write("\nHash: N/A")

        original_plaintext_path = "plaintext.txt"
        plaintext_path = os.path.join(log_dir, "plaintext.txt")
        
        if os.path.exists(original_plaintext_path):
            shutil.move(original_plaintext_path, plaintext_path)
            print(f"Moved plaintext.txt to {plaintext_path}")
        else:
            print("[!] Error: plaintext.txt not found in the root directory.")

        if os.path.exists(plaintext_path):
            with open(plaintext_path, 'r') as plaintext_file:
                plaintext = plaintext_file.read().strip()
        else:
            plaintext = "N/A"

        f.write(f"\nPlaintext: {plaintext}")

    print(f"Status saved to {status_file_path}")

    if plaintext_path and os.path.exists(plaintext_path):
        with open(plaintext_path, "r") as plaintext_file:
            print(colored("\n[*] Plaintext Output:","blue"))
            print(plaintext_file.read().strip())

    print(colored("\n[*] Status File Content:","blue"))
    with open(status_file_path, "r") as status_file:
        print(status_file.read().strip())

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
    
    restore_file = os.path.join(default_restorepath, f"{restore_file_input}")
     
    if not os.path.isfile(restore_file):
        print(colored(f"[!] Error: Restore file '{restore_file}' not found.", 'red'))
        return

    session = os.path.basename(restore_file).replace(".restore", "")
    print(colored(f"[+] Restoring session >> {restore_file}", 'blue'))

    cmd = f"hashcat --session={session} --restore"
    print(colored(f"[+] Executing: {cmd}", "blue"))
    os.system(cmd)

def define_hashfile():
    parser = argparse.ArgumentParser(description="A tool for cracking hashes using Hashcat.")
    parser.add_argument("hash_file", help="Path to the file containing the hash to crack")
    args = parser.parse_args()
    
    return args.hash_file



