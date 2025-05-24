import os
import sys
import time
import subprocess
import shutil
import argparse
from importlib import resources
from pathlib import Path
import pkg_resources 
from pathlib import Path
from datetime import datetime
from termcolor import colored

default_scripts = os.path.expanduser("~/hashCrack")
default_windows_scripts = f"/c/Users/{os.getenv('USER')}/source/repos/ente0/hashCrack/scripts/windows"

def define_default_parameters():
    return {
        "default_hashcat": ".",
        "default_status_timer": "y",
        "default_workload": "3",
        "default_os": "Linux",
        "default_restorepath": os.path.expanduser("~/.local/share/hashcat/sessions"),
        "default_session": datetime.now().strftime("%Y-%m-%d"),
        "default_wordlists": "/usr/share/wordlists",
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



def print_hashcrack_title():
    """
    Print centered hashCrack ASCII art logo in blue color.
    This function is used by the menu to display the program title.
    """
    terminal_width = shutil.get_terminal_size().columns
    ascii_art = [
r" ▄  █ ██      ▄▄▄▄▄    ▄  █ ▄█▄    █▄▄▄▄ ██   ▄█▄    █  █▀",
r"█   █ █ █    █     ▀▄ █   █ █▀ ▀▄  █  ▄▀ █ █  █▀ ▀▄  █▄█  ",
r"██▀▀█ █▄▄█ ▄  ▀▀▀▀▄   ██▀▀█ █   ▀  █▀▀▌  █▄▄█ █   ▀  █▀▄  ",
r"█   █ █  █  ▀▄▄▄▄▀    █   █ █▄  ▄▀ █  █  █  █ █▄  ▄▀ █  █ ",
r"   █     █               █  ▀███▀    █      █ ▀███▀    █  ",
r"  ▀     █               ▀           ▀      █          ▀   ",
r"       ▀                                  ▀               ",
"",
"For more information, visit: https://github.com/ente0/hashCrack"
    ]
    print("\n")
    for line in ascii_art:
        padding = (terminal_width - len(line)) // 2 if len(line) < terminal_width else 0
        print(colored(" " * padding + line, 'blue'))
    print("\n")

def monitor_plaintext_status(default_os="Linux"):
    """
    Monitor plaintext status files and update terminal title with findings.
    This function checks .hashCrack/logs directory for status files and displays
    plaintext results in the terminal title.
    
    Parameters:
        default_os (str): Current operating system ('Linux' or 'Windows')
    """
    import os
    import glob
    from pathlib import Path
    
    home_dir = os.path.expanduser("~")
    logs_dir = os.path.join(home_dir, ".hashCrack", "logs")
    
    if not os.path.exists(logs_dir):
        print(colored(f"[!] Logs directory not found: {logs_dir}", "yellow"))
        return []
    
    status_files = glob.glob(os.path.join(logs_dir, "**", "status.txt"), recursive=True)
    found_plaintexts = []
    
    for status_file in status_files:
        session_dir = os.path.dirname(status_file)
        session_name = os.path.basename(session_dir)
        
        try:
            with open(status_file, "r") as f:
                status_content = f.read()
                
                plaintext_line = next((line for line in status_content.split('\n') 
                                      if line.startswith("Plaintext:")), None)
                
                if plaintext_line and "N/A" not in plaintext_line:
                    plaintext = plaintext_line.replace("Plaintext:", "").strip()
                    
                    if plaintext:
                        found_plaintexts.append({
                            "plaintext": plaintext,
                            "session": session_name,
                            "path": session_dir
                        })
        except Exception as e:
            print(colored(f"[!] Error reading status file {status_file}: {e}", "red"))
    
    if found_plaintexts:
        if default_os == "Windows":
            title_parts = []
            for found in found_plaintexts:
                title_part = f"{found['plaintext']} ({found['session']})"
                title_parts.append(title_part)
            
            title_text = "hashCrack - " + " | ".join(title_parts)
            os.system(f'title {title_text}')
        else:
            title_parts = []
            for found in found_plaintexts:
                title_part = f"{found['plaintext']} ({found['session']})"
                title_parts.append(title_part)
            
            title_text = "hashCrack - " + " | ".join(title_parts)
            print(f"\033]0;{title_text}\007", end="", flush=True)
        
        return found_plaintexts
    else:
        if default_os == "Windows":
            os.system('title hashCrack - No plaintexts found')
        else:
            print("\033]0;hashCrack - No plaintexts found\007", end="", flush=True)
        
        return []

def display_plaintext_status():
    """
    Display a summary of found plaintexts in the terminal.
    This function calls monitor_plaintext_status() and prints the results.
    """
    found_plaintexts = monitor_plaintext_status()
    
    if found_plaintexts:
        terminal_width = shutil.get_terminal_size().columns
        separator = "=" * terminal_width
        
        print(colored(separator, 'green'))
        print(colored(" Plaintexts:", 'green', attrs=['bold']))
        print(colored(separator, 'green'))
        
        for idx, found in enumerate(found_plaintexts, 1):
            print(colored(f" [{idx}] Plaintext:", 'cyan', attrs=['bold']), colored(found['plaintext'], 'yellow'))
            print(colored(f"     Session:", 'cyan'), found['session'])
            print(colored(f"     Path:", 'cyan'), found['path'])
            print()
    else:
        print(colored("\n No plaintexts found in status files.", 'yellow'))

def print_hashcrack_title():
    """
    Print centered hashCrack ASCII art logo in blue color.
    This function is used by the menu to display the program title.
    """
    terminal_width = shutil.get_terminal_size().columns
    ascii_art = [
r" ▄  █ ██      ▄▄▄▄▄    ▄  █ ▄█▄    █▄▄▄▄ ██   ▄█▄    █  █▀",
r"█   █ █ █    █     ▀▄ █   █ █▀ ▀▄  █  ▄▀ █ █  █▀ ▀▄  █▄█  ",
r"██▀▀█ █▄▄█ ▄  ▀▀▀▀▄   ██▀▀█ █   ▀  █▀▀▌  █▄▄█ █   ▀  █▀▄  ",
r"█   █ █  █  ▀▄▄▄▄▀    █   █ █▄  ▄▀ █  █  █  █ █▄  ▄▀ █  █ ",
r"   █     █               █  ▀███▀    █      █ ▀███▀    █  ",
r"  ▀     █               ▀           ▀      █          ▀   ",
r"       ▀                                  ▀               ",
"",
"For more information, visit: https://github.com/ente0/hashCrack"
    ]
    print("\n")
    for line in ascii_art:
        padding = (terminal_width - len(line)) // 2 if len(line) < terminal_width else 0
        print(colored(" " * padding + line, 'blue'))
    print("\n")

def monitor_plaintext_status(default_os="Linux"):
    """
    Monitor plaintext status files and update terminal title with findings.
    This function checks .hashCrack/logs directory for status files and displays
    plaintext results in the terminal title.
    
    Parameters:
        default_os (str): Current operating system ('Linux' or 'Windows')
    
    Returns:
        list: List of found plaintexts with associated information
    """
    import os
    import glob
    from pathlib import Path
    
    home_dir = os.path.expanduser("~")
    logs_dir = os.path.join(home_dir, ".hashCrack", "logs")
    
    if not os.path.exists(logs_dir):
        return []
    
    status_files = glob.glob(os.path.join(logs_dir, "**", "status.txt"), recursive=True)
    found_plaintexts = []
    
    for status_file in status_files:
        session_dir = os.path.dirname(status_file)
        session_name = os.path.basename(session_dir)
        
        try:
            with open(status_file, "r") as f:
                status_content = f.read()
                
                plaintext_line = next((line for line in status_content.split('\n') 
                                      if line.startswith("Plaintext:")), None)
                
                hash_line = next((line for line in status_content.split('\n')
                                 if line.startswith("Hash:")), None)
                hash_value = hash_line.replace("Hash:", "").strip() if hash_line else "N/A"
                
                wordlist_line = next((line for line in status_content.split('\n')
                                    if line.startswith("Wordlist:")), None)
                wordlist = wordlist_line.replace("Wordlist:", "").strip() if wordlist_line else "N/A"
                
                rule_line = next((line for line in status_content.split('\n')
                                if line.startswith("Rule:")), None)
                rule = rule_line.replace("Rule:", "").strip() if rule_line else "N/A"
                
                mask_line = next((line for line in status_content.split('\n')
                                if line.startswith("Mask:")), None)
                mask = mask_line.replace("Mask:", "").strip() if mask_line else "N/A"
                
                if plaintext_line and "N/A" not in plaintext_line:
                    plaintext = plaintext_line.replace("Plaintext:", "").strip()
                    
                    if plaintext:
                        found_plaintexts.append({
                            "plaintext": plaintext,
                            "session": session_name,
                            "path": session_dir,
                            "hash": hash_value[:20] + "..." if len(hash_value) > 23 else hash_value,
                            "wordlist": wordlist,
                            "rule": rule,
                            "mask": mask
                        })
        except Exception as e:
            continue
    
    if found_plaintexts:
        if default_os == "Windows":
            title_parts = []
            for found in found_plaintexts:
                title_part = f"{found['plaintext']} ({found['session']})"
                title_parts.append(title_part)
            
            title_text = "hashCrack - " + " | ".join(title_parts)
            os.system(f'title {title_text}')
        else:
            title_parts = []
            for found in found_plaintexts:
                title_part = f"{found['plaintext']} ({found['session']})"
                title_parts.append(title_part)
            
            title_text = "hashCrack - " + " | ".join(title_parts)
            print(f"\033]0;{title_text}\007", end="", flush=True)
    else:
        if default_os == "Windows":
            os.system('title hashCrack')
        else:
            print("\033]0;hashCrack\007", end="", flush=True)
    
    return found_plaintexts

def display_plaintext_status():
    """
    Display a summary of found plaintexts in the terminal.
    This function calls monitor_plaintext_status() and prints the results.
    """
    import shutil
    from termcolor import colored
    
    found_plaintexts = monitor_plaintext_status()
    
    if found_plaintexts:
        terminal_width = shutil.get_terminal_size().columns
        separator = "=" * terminal_width
        
        print(colored(separator, 'green'))
        print(colored(" FOUND KEYS", 'green', attrs=['bold']))
        print(colored(separator, 'green'))
        
        for idx, found in enumerate(found_plaintexts, 1):
            print(colored(f" → {found['plaintext']} ", 'yellow', attrs=['bold']) + 
                  colored(f"(Session: {found['session']})", 'cyan'))
            
            if 'path' in found:
                print(colored(f"     Path: ", 'cyan') + found['path'])
                
            if 'hash' in found and found['hash'] != "N/A":
                print(colored(f"     Hash: ", 'cyan') + found['hash'])
                
            if 'wordlist' in found and found['wordlist'] != "N/A":
                print(colored(f"     Wordlist: ", 'cyan') + found['wordlist'])
                
            if 'rule' in found and found['rule'] != "N/A":
                print(colored(f"     Rule: ", 'cyan') + found['rule'])
                
            if 'mask' in found and found['mask'] != "N/A":
                print(colored(f"     Mask: ", 'cyan') + found['mask'])
                
            print()
    else:
        print(colored("\n No plaintexts found in status files.", 'yellow'))

def show_menu(default_os):
    """
    Display the main menu for hashCrack with OS-specific options.
    Difficulty levels are right-aligned at the exact terminal edge.
    
    Parameters:
        default_os (str): Current operating system ('Linux' or 'Windows')
    
    Returns:
        str: User's menu selection
    """
    terminal_width = shutil.get_terminal_size().columns
    separator = "=" * terminal_width
    dash_separator = "-" * terminal_width
    
    found_plaintexts = monitor_plaintext_status(default_os)
    
    print_hashcrack_title()
    print(colored(separator, 'cyan'))
    print(colored(f" Welcome to hashCrack! - Menu Options for {default_os}", 'cyan', attrs=['bold']))
    
    if found_plaintexts:
        print(colored(" [✓] Plaintexts:", 'green', attrs=['bold']))
        for found in found_plaintexts:
            print(colored(f"  → {found['plaintext']} ", 'yellow', attrs=['bold']) + 
                  colored(f"(Session: {found['session']})", 'green'))
    
    print(colored(separator, 'cyan'))
    
    menu_options = [
        ("Crack with Wordlist", "[EASY]", 'blue'),
        ("Crack with Association (wordlist + rule)", "[MEDIUM]", 'green'),
        ("Crack with Brute-Force (mask)", "[HARD]", 'yellow'),
        ("Crack with Combinator (wordlist + mask)", "[ADVANCED]", 'red'),
        ("Display Plaintext Status","",None)
    ]
    
    print()
    for idx, (option_text, difficulty, diff_color) in enumerate(menu_options, 1):
        option_start = f" {colored(f'[{idx}]', 'cyan', attrs=['bold'])} {option_text}"
        
        visible_length = len(f" [{idx}] {option_text}")
        spaces = terminal_width - visible_length - len(difficulty)
        
        print(f"{option_start}{' ' * spaces}{colored(difficulty, diff_color, attrs=['bold'])}")
    
    print(colored(dash_separator, 'cyan'))
    
    utility_options = [
        ("Clear Hashcat Potfile", "[UTILITY]", 'magenta'),
    ]
    
    for idx, (option_text, tag, color) in enumerate(utility_options):
        utility_start = f" {colored(f'[{idx}]', color, attrs=['bold'])} {option_text}"
        
        visible_utility_length = len(f" [{idx}] {option_text}")
        utility_spaces = terminal_width - visible_utility_length - len(tag)
        
        print(f"{utility_start}{' ' * utility_spaces}{colored(tag, color, attrs=['bold'])}")
    
    print(colored("\n" + separator, 'magenta'))
    print(f" {colored('Press X to switch to Windows' if default_os == 'Linux' else 'Press X to switch to Linux', 'magenta', attrs=['bold'])}.")
    print(colored(separator, 'magenta'))
    
    user_option = input(colored("\nEnter option (0-5, X to switch OS, Q to quit): ", 'cyan', attrs=['bold'])).strip().lower()
    return user_option
def handle_option(option, default_os, hash_file):
    """
    Unified function to handle menu options for the hashcat cracking tool.
    Supports cleaning cache, displaying status, and executing cracking scripts.
    """
    script_map = {
        "1": "crack_wordlist.py",
        "2": "crack_rule.py", 
        "3": "crack_bruteforce.py",
        "4": "crack_combo.py"
    }
    os.system('cls' if os.name == 'nt' else 'clear')

    print("...", flush=True)
    
    if option.lower() == "q":
        print(colored("Done! Exiting...", 'yellow'))
        sys.exit(0)
    
    if option == "0":
        if clean_hashcat_cache():
            print(colored("[+] Hashcat potfile cleaned successfully.", 'green'))
        else:
            print(colored("[!] Failed to clean hashcat potfile.", 'red'))
        input(colored("\nPress Enter to return to the menu...", 'cyan'))
        return
    
    elif option == "5":
        display_plaintext_status()
        input(colored("\nPress Enter to return to the menu...", 'cyan'))
        return
    
    script_name = script_map.get(option)
    if not script_name:
        print(colored("Invalid option. Please try again.", 'red'))
        return
    
    try:
        script_type = "windows" if default_os == "Windows" else "linux"
        script_path = get_package_script_path(script_name, script_type)
        print(colored(f'Executing {script_path}', 'green'))
        python_cmd = "python3" if default_os == "Linux" else "python"
        os.system(f'{python_cmd} "{script_path}" "{hash_file}"')
    except FileNotFoundError as e:
        print(colored(f"Error: {e}", 'red'))
    except Exception as e:
        print(colored(f"Unexpected error: {e}", 'red'))
    
    input("Press Enter to return to the menu...")

def animate_text(text, delay):
    for i in range(len(text) + 1):
        clear_screen()
        print(text[:i], end="", flush=True)
        time.sleep(delay)

def get_package_script_path(script_name: str, os_type: str) -> Path:
    try:
        package_path = resources.files(f'hashCrack.{os_type.lower()}') / script_name
        
        if not package_path.exists():
            raise FileNotFoundError(f"Script {script_name} not found in package")
        
        return package_path
    except (ImportError, AttributeError):
        package_path = pkg_resources.resource_filename('hashCrack', f'{os_type.lower()}/{script_name}')
        
        if not os.path.exists(package_path):
            raise FileNotFoundError(f"Script {script_name} not found in package")
        
        return Path(package_path)

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

def define_logs(session):
    home_dir = os.path.expanduser("~")
    log_dir = os.path.join(home_dir, ".hashCrack", "logs", session)
    os.makedirs(log_dir, exist_ok=True)
    original_plaintext_path = "plaintext.txt"
    plaintext_path = os.path.join(log_dir, "plaintext.txt")
    status_file_path = os.path.join(log_dir, "status.txt")
    return plaintext_path, status_file_path, log_dir

def save_logs(session, wordlist_path=None, wordlist=None, mask_path=None, mask=None, rule_path=None, rule=None, hash_file=None):
    plaintext_path, status_file_path, log_dir = define_logs(session)

    if not hash_file:
        hash_file = define_hashfile()

    with open(status_file_path, "w") as f:
        f.write(f"Session: {session}\n")

        if wordlist and wordlist_path:
            f.write(f"Wordlist: {os.path.join(wordlist_path, wordlist)}\n")
        else:
            f.write("Wordlist: N/A\n")

        if mask_path and mask:
            f.write(f"Mask File: {os.path.join(mask_path, mask)}\n")
        else:
            f.write(f"Mask: {mask if mask else 'N/A'}\n")

        if rule_path and rule:
            f.write(f"Rule: {os.path.join(rule_path, rule)}\n")
        elif rule:
            f.write(f"Rule: {rule}\n")
        else:
            f.write("Rule: N/A\n")

        if hash_file and os.path.exists(hash_file):
            try:
                with open(hash_file, "r") as hash_file_obj:
                    f.write(f"Hash: {hash_file_obj.read().strip()}\n")
            except Exception as e:
                print(f"[!] Error reading hash file: {e}")
                f.write("Hash: N/A\n")
        else:
            print("[!] Warning: Hash file not provided or doesn't exist.")
            f.write("Hash: N/A\n")

        if os.path.exists(plaintext_path):
            with open(plaintext_path, 'r') as plaintext_file:
                plaintext = plaintext_file.read().strip()
        else:
            plaintext = "N/A"

        f.write(f"Plaintext: {plaintext}\n")

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
    restore_file = restore_file_input.strip() or default_restorepath

    if restore_file.strip() == default_restorepath and not os.path.isfile(restore_file):
        return

    if not os.path.isabs(restore_file):
        restore_file = os.path.join(default_restorepath, restore_file)

    if not os.path.isfile(restore_file):
        print(colored(f"[!] Error: Restore file '{restore_file}' not found.", 'red'))
        return

    session = os.path.basename(restore_file).replace(".restore", "")
    print(colored(f"[+] Restoring session >> {restore_file}", 'blue'))

    cmd = f"hashcat --session={session} --restore"
    print(colored(f"[*] Executing: {cmd}", "blue"))
    os.system(cmd)


def define_hashfile():
    parser = argparse.ArgumentParser(description="A tool for cracking hashes using Hashcat.")
    parser.add_argument("hash_file", help="Path to the file containing the hash to crack")
    args = parser.parse_args()

    if not os.path.isfile(args.hash_file):
        print(colored(f"[!] Error: The file '{args.hash_file}' does not exist.", 'red'))
        time.sleep(2)
        sys.exit(1)

    if os.stat(args.hash_file).st_size == 0:
        print(colored(f"[!] Error: The file '{args.hash_file}' is empty.", 'red'))
        time.sleep(2)
        sys.exit(1)

    return args.hash_file

def clean_hashcat_cache():
    try:
        potfile_paths = [
            Path.home() / '.local/share/hashcat/hashcat.potfile',
            Path.home() / '.hashcat/hashcat.potfile',
            #Path('/root/.hashcat/hashcat.potfile'),
            #Path('/root/.local/share/hashcat/hashcat.potfile'),
            Path.home() / 'venv/lib/python3.12/site-packages/hashcat/hashcat/hashcat.potfile'
        ]
        
        for potfile in potfile_paths:
            if potfile.exists():
                potfile.unlink()
                print(colored(f"[+] Removed existing potfile: {potfile}", 'green'))
    
        return True
    except Exception as e:
        print(colored(f"[!] Error cleaning hashcat cache: {e}", 'red'))
        return False

def get_unique_session_name(session_name, log_path="~/.hashCrack/logs/"):
    expanded_path = os.path.expanduser(log_path)
    
    counter = 0
    while True:
        if counter == 0:
            unique_name = session_name
        else:
            unique_name = f"{session_name}_{counter}"
            
        full_path = os.path.join(expanded_path, unique_name)
            
        if not os.path.isdir(full_path):
            return unique_name
            
        counter += 1