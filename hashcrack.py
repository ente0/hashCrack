import os
import time
import sys
from functions import (
    define_default_parameters, define_windows_parameters, clear_screen, show_title, show_menu, handle_option)

define_windows_parameters()
define_default_parameters()

default_os = "Windows"

while True:
    clear_screen()
    show_title()
    show_menu(default_os)
    
    user_option = input("Enter option (1-4, or Q to quit): ").strip()

    if user_option.lower() == 'x':
        default_os = "Linux" if default_os == "Windows" else "Windows"
        print(f"System switched to {default_os}")
    
    elif user_option.lower() == 'q':
        print("Exiting program...")
        break

    else:
        handle_option(user_option, default_os)
    
    if user_option == "hashcat_option_identifier":
        input("Hashcat has finished. Press any key to continue...")

    print(f"User option: {user_option}")
