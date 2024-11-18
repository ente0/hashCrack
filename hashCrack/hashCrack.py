import os
import time
import sys
import argparse
from hashCrack.functions import (
    define_default_parameters, define_windows_parameters, clear_screen, show_menu1, show_menu2, handle_option, define_hashfile
)

define_windows_parameters()
define_default_parameters()

global default_os

def main():
    while True:
        default_os = "Linux"
        clear_screen()
        user_option, default_os = show_menu1(default_os)
        
        hash_file=define_hashfile()
        
        if not os.path.isfile(hash_file):
            print(f"[!] Error: The file '{hash_file}' does not exist.")
            time.sleep(2)
            continue

        if user_option in ['1', '2', '3', '4']:
            try:
                handle_option(user_option, default_os, hash_file)
            except Exception as e:
                print(f"[!] Error occurred while processing: {e}")
                time.sleep(2)

if __name__ == "__main__":
    main()

