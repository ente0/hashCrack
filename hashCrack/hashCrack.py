import os
import time
import sys
import subprocess
from termcolor import colored
from hashCrack.functions import (
    define_default_parameters, define_windows_parameters, clear_screen, 
    show_menu1, show_menu2, handle_option, define_hashfile, verify_hash_crackable, clean_hashcat_cache
)

def main():
    define_windows_parameters()
    define_default_parameters()
    
    default_os = "Linux" 
    
    while True:
        try:
            clear_screen()

            user_option = show_menu1(default_os)
            
            if user_option == 'x':
                default_os = "Linux" if default_os == "Windows" else "Windows"
                clear_screen() 
                print(f"System switched to {default_os}")
                time.sleep(1)
                continue 
            
            if user_option == '0':
                if default_os == 'Linux':
                    clean_hashcat_cache()
                    print(colored("[+] Hashcat potfile cleared on Linux.", 'green'))
                elif default_os == 'Windows':
                    os.system("del %userprofile%\\hashcat\\hashcat.potfile")
                    print(colored("[+] Hashcat potfile cleared on Windows.", 'green'))
                time.sleep(1)
                continue 

            hash_file = define_hashfile()
            if not os.path.isfile(hash_file):
                print(colored(f"[!] Error: The file '{hash_file}' does not exist.", 'red'))
                time.sleep(2)
                continue
                
            if user_option in ['1', '2', '3', '4']:
                if not verify_hash_crackable(hash_file):
                    print(colored("[!] Hash might already be cracked or there was an error.", 'yellow'))
                    input("Press Enter to continue...")
                    continue
                    
                try:
                    handle_option(user_option, default_os, hash_file)
                except KeyboardInterrupt:
                    print(colored("\n[!] Operation cancelled by user", 'yellow'))
                    time.sleep(1)
                except Exception as e:
                    print(colored(f"[!] Error occurred while processing: {e}", 'red'))
                    time.sleep(2)
            
            elif user_option.lower() == 'q':
                clear_screen()
                print(colored("Goodbye!", 'green'))
                sys.exit(0)
            else:
                pass
                
        except KeyboardInterrupt:
            clear_screen()
            print(colored("\nExiting safely...", 'yellow'))
            sys.exit(0)
        except Exception as e:
            print(colored(f"[!] Unexpected error: {e}", 'red'))
            time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print(colored("\nExiting safely...", 'yellow'))
        sys.exit(0)
