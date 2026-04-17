"""hashCrack — entry point.

By default launches the Textual TUI. Pass --classic for the legacy rich-based
menu, or --attack <type> for a fully non-interactive run that dispatches to
the matching crack_*.py script.
"""
from __future__ import annotations

import argparse
import os
import platform
import sys
import time
import traceback

from rich.console import Console

from hashCrack.functions import (
    clean_hashcat_cache, clear_screen, handle_option, show_menu,
    validate_hashfile,
)

console = Console()

ATTACK_CHOICES = ["wordlist", "rule", "bruteforce", "combo"]
_ATTACK_TO_OPTION = {
    "wordlist":   "1",
    "rule":       "2",
    "bruteforce": "3",
    "combo":      "4",
}


def _running_under_pipx() -> bool:
    exe = sys.executable
    venv = os.environ.get("VIRTUAL_ENV", "")
    return "pipx" in exe or "pipx" in venv


def _auto_os() -> str:
    return "Windows" if platform.system().lower().startswith("win") else "Linux"


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="hashcrack",
        description="Interactive Textual TUI around hashcat: wordlist, rule, brute-force and combinator attacks.",
    )
    p.add_argument("hash_file", help="Path to the file containing the hash(es) to crack")
    p.add_argument("--os", choices=["linux", "windows"], default=_auto_os().lower(),
                   help="Target hashcat binary flavour (default: auto-detect)")
    p.add_argument("--force", action="store_true",
                   help="Default --force to ON in forms / CLI invocations (opt-in)")
    p.add_argument("--attack", choices=ATTACK_CHOICES,
                   help="Skip the TUI and run the named attack interactively")
    p.add_argument("--classic", action="store_true",
                   help="Use the legacy rich-based text menu instead of the Textual TUI")
    return p


def _run_classic_menu(hash_file: str, default_os: str, force_default: bool) -> None:
    """Legacy rich-based menu loop — kept as a fallback when Textual is unusable."""
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
            if option in ("1", "2", "3", "4", "5"):
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
    """Non-interactive single-attack dispatch: execs the matching crack_*.py script."""
    import subprocess
    from hashCrack.functions import get_package_script_path
    script_map = {
        "wordlist":   "crack_wordlist.py",
        "rule":       "crack_rule.py",
        "bruteforce": "crack_bruteforce.py",
        "combo":      "crack_combo.py",
    }
    script_path = get_package_script_path(script_map[attack], default_os.lower())
    python_cmd = "python3" if default_os == "Linux" else "python"
    cmd = [python_cmd, str(script_path), hash_file]
    if force:
        cmd.append("--force")
    return subprocess.run(cmd).returncode


def main() -> None:
    if not _running_under_pipx():
        console.print(
            "[bold red]Error:[/] hashcrack must be installed with pipx, not pip.\n\n"
            "  [bold]Install:[/]\n"
            "    [cyan]pipx install git+https://github.com/ente0/hashCrack[/]\n"
            "  or locally:\n"
            "    [cyan]pipx install .[/]"
        )
        sys.exit(1)
    args = _build_parser().parse_args()
    default_os = "Windows" if args.os == "windows" else "Linux"
    hash_file = validate_hashfile(args.hash_file)

    try:
        if args.attack:
            sys.exit(_run_attack_cli(args.attack, hash_file, default_os, args.force))

        if args.classic:
            _run_classic_menu(hash_file, default_os, args.force)
            return

        # Default: Textual TUI
        try:
            from hashCrack.tui import launch as tui_launch
        except ImportError as e:
            console.print(f"[yellow]Textual unavailable ({e}); falling back to classic menu.[/]")
            _run_classic_menu(hash_file, default_os, args.force)
            return
        tui_launch(hash_file=hash_file, os_name=default_os, force_default=args.force)

    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting safely...[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/]")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
