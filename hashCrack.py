import os
import time
import sys
from functions import (
    define_default_parameters, define_windows_parameters, clear_screen, show_menu1, show_menu2, handle_option
)

define_windows_parameters()
define_default_parameters()

default_os = "Linux"

def get_hash_file():
    """Funzione per chiedere all'utente di fornire un percorso del file hash"""
    hash_file_input = input("Enter the path to the hash file (default 'hash.txt'): ")
    hash_file = hash_file_input or "hash.txt"  # Se non viene fornito un percorso, usa 'hash.txt' come default
    return hash_file

while True:
    clear_screen()
    user_option, default_os = show_menu1(default_os)

    if user_option in ['1', '2', '3', '4']:
        hash_file = get_hash_file()  
        handle_option(user_option, default_os, hash_file) 
