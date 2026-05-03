"""Interactive prompts for Linux attack scripts."""
import os
from termcolor import colored

from hashCrack.functions import (
    list_sessions, restore_session, define_default_parameters, get_unique_session_name
)

parameters = define_default_parameters()


def _walk_tree(root_path, color_dir="yellow", color_file="yellow"):
    for root, _dirs, files in os.walk(root_path):
        level = root.replace(root_path, "").count(os.sep)
        indent = "    " * level
        print(f"{indent}{colored('[*]', color_dir)} {os.path.basename(root) or root}")
        for f in files:
            print(f"{indent}    {colored('[-]', color_file)} {f}")


def define_wordlist():
    wordlist_path_input = input(colored("[+] ", "green") + f"Enter Wordlists Path (default '{parameters['default_wordlists']}'): ")
    wordlist_path = wordlist_path_input or parameters["default_wordlists"]

    print(colored("[+] ", "green") + f"Available Wordlists in {wordlist_path}:")
    if not os.path.exists(wordlist_path):
        print(colored(f"[!] Error: The directory {wordlist_path} does not exist.", "red"))
        return None, None
    _walk_tree(wordlist_path)

    wordlist_input = input(colored("[+] ", "green") + f"Enter Wordlist (default '{parameters['default_wordlist']}'): ")
    wordlist = wordlist_input or parameters["default_wordlist"]
    print(f"Wordlist: {colored(f'{wordlist_path}/{wordlist}', 'blue')}")
    return wordlist_path, wordlist


def define_rule():
    rule_path_input = input(colored("[+] ", "green") + f"Enter Rules Path (default '{parameters['default_rules']}'): ")
    rule_path = rule_path_input or parameters["default_rules"]

    print(colored("[+] ", "green") + f"Available Rules in {rule_path}:")
    if not os.path.exists(rule_path):
        print(colored(f"[!] Error: The directory {rule_path} does not exist.", "red"))
        return rule_path, parameters["default_rule"]
    _walk_tree(rule_path)

    rule_input = input(colored("[+] ", "green") + f"Enter Rule (default '{parameters['default_rule']}'): ")
    rule = rule_input or parameters["default_rule"]
    print(f"Rule: {colored(f'{rule}', 'blue')}")
    return rule_path, rule


def define_session():
    list_sessions(parameters["default_restorepath"])
    restore_file_input = input(colored("[+] ", "green") + "Restore? (Enter restore file name or leave empty): ")
    restore_session(restore_file_input, parameters["default_restorepath"])

    session_input = input(colored("[+] ", "green") + f"Enter session name (default '{parameters['default_session']}'): ")
    session = session_input or parameters["default_session"]
    new_session_name = get_unique_session_name(session)
    if new_session_name != session:
        print(colored(f"[!] Session name '{session}' already exists. Assigning new session name: '{new_session_name}'", "red"))

    session = new_session_name
    print(f"Session name: {colored(session, 'blue')}")
    return session


def define_status():
    status_timer_input = input(colored("[+] ", "green") + f"Use status timer? (default '{parameters['default_status_timer']}') [y/n]: ")
    status_timer = status_timer_input or parameters["default_status_timer"]
    print(f"Status timer: {colored(status_timer, 'blue')}")
    return status_timer


def define_hashmode():
    hashmode_input = input(colored("[+] ", "green") + f"Enter hash attack mode (default '{parameters['default_hashmode']}'): ")
    hashmode = hashmode_input or parameters["default_hashmode"]
    print(f"Hashmode: {colored(hashmode, 'blue')}")
    return hashmode


def define_workload():
    workload_input = input(colored("[+] ", "green") + f"Enter workload (default '{parameters['default_workload']}') [1-4]: ")
    workload = workload_input or parameters["default_workload"]
    print(f"Workload: {colored(workload, 'blue')}")
    return workload


def define_device():
    device_input = input(colored("[+] ", "green") + f"Enter device (default '{parameters['default_device']}'): ")
    device = device_input or parameters["default_device"]
    print(f"OpenCL device: {colored(device, 'blue')}")
    return device


def define_force(default=False):
    """Ask whether to pass --force to hashcat. Opt-in; defaults to off because
    --force hides real driver/OpenCL issues that are usually worth diagnosing."""
    suggested = "y" if default else "n"
    answer = input(colored("[+] ", "green") + f"Add --force to hashcat? [y/n] (default '{suggested}'): ").strip().lower()
    if not answer:
        answer = suggested
    use_force = answer == "y"
    print(f"Force: {colored('yes' if use_force else 'no', 'blue')}")
    return use_force


def define_mask():
    use_mask_file = input(colored("[+] ", "green") + "Do you want to use a mask file? [y/n]: ").strip().lower()
    mask_path = None

    if use_mask_file == "y":
        mask_path_input = input(colored("[+] ", "green") + f"Enter Masks Path (default '{parameters['default_masks']}'): ")
        mask_path = mask_path_input or parameters["default_masks"]

        print(colored("[+] ", "green") + f"Available Masks in {mask_path}:")
        try:
            mask_files = os.listdir(mask_path)
            if not mask_files:
                print(colored("[!] Error: No masks found.", "red"))
            else:
                for mask_file in mask_files:
                    print(colored("[-] ", "yellow") + f"{mask_file}")
        except FileNotFoundError:
            print(colored(f"[!] Error: The directory {mask_path} does not exist.", "red"))
            return use_mask_file, None, parameters["default_mask"]

        mask_input = input(colored("[+] ", "green") + f"Enter Mask (default '{parameters['default_mask']}'): ")
        mask = mask_input or parameters["default_mask"]
    else:
        mask = input(colored("[+] ", "green") + "Enter manual mask (e.g., '?a?a?a?a?a?a'): ")
        if not mask:
            print(colored("[!] No mask entered. Using default mask.", "yellow"))
            mask = parameters["default_mask"]

    if mask_path:
        print(f"Mask: {colored(f'{mask_path}/{mask}', 'blue')}")
    else:
        print(f"Mask: {colored(mask, 'blue')}")
    return use_mask_file, mask_path, mask


def define_length():
    min_length_input = input(colored("[+] ", "green") + f"Enter Minimum Length (default '{parameters['default_min_length']}'): ")
    min_length = min_length_input or parameters["default_min_length"]

    max_length_input = input(colored("[+] ", "green") + f"Enter Maximum Length (default '{parameters['default_max_length']}'): ")
    max_length = max_length_input or parameters["default_max_length"]
    print(f"Minimum length: {colored(min_length, 'blue')}")
    print(f"Maximum length: {colored(max_length, 'blue')}")
    return min_length, max_length
