import os
import time
import sys
from functions import (
    define_default_parameters, define_windows_parameters, clear_screen, show_menu, handle_option)

define_windows_parameters()
define_default_parameters()

default_os = "Linux"

while True:
    clear_screen()
    user_option, default_os = show_menu(default_os)

    if user_option in ['1', '2', '3', '4']:
        handle_option(user_option, default_os)
