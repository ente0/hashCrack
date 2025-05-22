import os
import time
import sys
import subprocess
import traceback
from termcolor import colored
from hashCrack.functions import (
    define_default_parameters, define_windows_parameters, clear_screen,
    show_menu, handle_option, define_hashfile, clean_hashcat_cache
)

def check_file_exists(file_path):
    """Check if a file exists and has content."""
    if not os.path.isfile(file_path):
        print(colored(f"[!] Error: The file '{file_path}' does not exist.", 'red'))
        input("Press Enter to return to the menu...")
        return False
    if os.stat(file_path).st_size == 0:
        print(colored(f"[!] Error: The file '{file_path}' is empty.", 'red'))
        input("Press Enter to return to the menu...")
        return False
    return True

def windows_clean_potfile():
    """Clean hashcat potfile on Windows with error handling."""
    try:
        result = os.system("del %userprofile%\\hashcat\\hashcat.potfile")
        if result != 0:
            print(colored("[!] Warning: Potential error clearing hashcat potfile on Windows.", 'yellow'))
            return False
        return True
    except Exception as e:
        print(colored(f"[!] Error clearing hashcat potfile on Windows: {e}", 'red'))
        return False

def main():
    try:
        define_windows_parameters()
        define_default_parameters()
        default_os = "Linux"
        
        while True:
            try:
                clear_screen()
                user_option = show_menu(default_os)
                
                if user_option == 'x':
                    default_os = "Linux" if default_os == "Windows" else "Windows"
                    clear_screen()
                    print(f"System switched to {default_os}")
                    time.sleep(1)
                    continue
                
                if user_option == '0':
                    if default_os == 'Linux':
                        try:
                            clean_hashcat_cache()
                            print(colored("[+] Hashcat potfile cleared on Linux.", 'green'))
                        except Exception as e:
                            print(colored(f"[!] Error clearing hashcat potfile: {e}", 'red'))
                    elif default_os == 'Windows':
                        if windows_clean_potfile():
                            print(colored("[+] Hashcat potfile cleared on Windows.", 'green'))
                    time.sleep(1)
                    continue
                
                if user_option.lower() == 'q':
                    print(colored("Goodbye!", 'green'))
                    sys.exit(0)
                
                if user_option in ['1', '2', '3', '4', '5']:
                    try:
                        hash_file = define_hashfile()
                        
                        try:
                            check_file_exists(hash_file)
                        except (FileNotFoundError, ValueError) as e:
                            print(colored(f"[!] Error: {e}", 'red'))
                            time.sleep(2)
                            continue
                        
                        handle_option(user_option, default_os, hash_file)
                        
                    except KeyboardInterrupt:
                        print(colored("\n[!] Operation cancelled by user", 'yellow'))
                        time.sleep(1)
                    except Exception as e:
                        error_details = traceback.format_exc()
                        print(colored(f"[!] Error occurred while processing: {e}", 'red'))
                        with open('error_log.txt', 'a') as log_file:
                            log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error: {e}\n")
                            log_file.write(f"Details: {error_details}\n\n")
                        print(colored("[i] Error details logged to error_log.txt", 'blue'))
                        time.sleep(2)
                else:
                    if user_option.lower() != 'q' and user_option not in ['0', 'x']:
                        print(colored(f"[!] Invalid option: {user_option}", 'red'))
                        time.sleep(1)
                        
            except KeyboardInterrupt:
                answer = input(colored("\n[?] Do you want to exit the program? (y/n): ", 'yellow'))
                if answer.lower() == 'y':
                    print(colored("Exiting safely...", 'green'))
                    sys.exit(0)
                
    except Exception as e:
        print(colored(f"[!] Critical error in main program: {e}", 'red'))
        traceback.print_exc()
        time.sleep(3)
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\nExiting safely...", 'yellow'))
        sys.exit(0)
    except Exception as e:
        print(colored(f"\n[!] Fatal error: {e}", 'red'))
        sys.exit(1)