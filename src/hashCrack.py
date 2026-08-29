"""hashCrack command-line entry point."""

from __future__ import annotations

import argparse
import platform
import subprocess
import sys
import time
import traceback

from rich.console import Console

from functions import (
    clean_hashcat_cache,
    clear_screen,
    get_package_script_path,
    handle_option,
    show_menu,
    validate_hashfile,
)

console = Console()
ATTACK_CHOICES = ("wordlist", "rule", "bruteforce", "combo")


def _auto_os() -> str:
    return "Windows" if platform.system().lower().startswith("win") else "Linux"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hashcrack",
        description=(
            "Interactive Textual TUI around Hashcat: wordlist, rule, "
            "brute-force and combinator attacks."
        ),
    )
    parser.add_argument("hash_file", help="Path to the file containing hashes to crack")
    parser.add_argument(
        "--os",
        choices=("linux", "windows"),
        default=_auto_os().lower(),
        help="Hashcat binary flavour (default: host OS)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Default the Hashcat --force option to enabled",
    )
    parser.add_argument(
        "--attack",
        choices=ATTACK_CHOICES,
        help="Skip the TUI and open the selected attack workflow",
    )
    parser.add_argument(
        "--classic",
        action="store_true",
        help="Use the legacy rich-rendered menu instead of Textual",
    )
    return parser


def _run_classic_menu(hash_file: str, default_os: str, force_default: bool) -> None:
    """Run the legacy rich-rendered menu without invoking a command shell."""
    extra_args = ["--force"] if force_default else []
    while True:
        try:
            clear_screen()
            option = show_menu(default_os, hash_file)
            if option == "x":
                default_os = "Linux" if default_os == "Windows" else "Windows"
                console.print(f"[green]Switched to {default_os}[/]")
                time.sleep(0.8)
                continue
            if option == "6":
                clean_hashcat_cache(verbose=True)
                time.sleep(0.8)
                continue
            if option == "q":
                console.print("[green]Goodbye![/]")
                return
            if option in {"1", "2", "3", "4", "5"}:
                validate_hashfile(hash_file)
                handle_option(option, default_os, hash_file, extra_args=extra_args)
            else:
                console.print(f"[red]Invalid option: {option}[/]")
                time.sleep(0.8)
        except KeyboardInterrupt:
            answer = console.input("\n[yellow]Exit hashCrack? [y/n]: [/]").strip().lower()
            if answer == "y":
                return


def _run_attack_cli(attack: str, hash_file: str, default_os: str, force: bool) -> int:
    """Dispatch one attack script through the current Python interpreter."""
    script_map = {
        "wordlist": "crack_wordlist.py",
        "rule": "crack_rule.py",
        "bruteforce": "crack_bruteforce.py",
        "combo": "crack_combo.py",
    }
    script_path = get_package_script_path(script_map[attack], default_os.lower())
    command = [sys.executable, str(script_path), hash_file]
    if force:
        command.append("--force")
    return subprocess.run(command, check=False).returncode


def main() -> None:
    args = _build_parser().parse_args()
    default_os = "Windows" if args.os == "windows" else "Linux"

    try:
        hash_file = validate_hashfile(args.hash_file)
        if args.attack:
            raise SystemExit(
                _run_attack_cli(args.attack, hash_file, default_os, args.force)
            )
        if args.classic:
            _run_classic_menu(hash_file, default_os, args.force)
            return

        try:
            from tui import launch as tui_launch
        except ImportError as exc:
            console.print(
                f"[yellow]Textual unavailable ({exc}); falling back to classic menu.[/]"
            )
            _run_classic_menu(hash_file, default_os, args.force)
            return
        tui_launch(hash_file=hash_file, os_name=default_os, force_default=args.force)
    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting safely...[/]")
        raise SystemExit(0) from None
    except Exception as exc:
        console.print(f"[red]Fatal error: {exc}[/]")
        traceback.print_exc()
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
