"""Core helpers for hashCrack: menu, logging, sessions and subprocess dispatch.

Logs are stored under ~/.hashCrack/logs/<session>/ as:
    plaintext.txt   hashcat's captured plaintext (raw)
    status.json     structured run metadata (written by save_logs)
    command.txt     exact hashcat invocation (for replay)
"""
from __future__ import annotations

import os
import sys
import time
import json
import glob
import shlex
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from importlib import resources

from termcolor import colored
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box

try:
    import pkg_resources
except ImportError:
    pkg_resources = None

console = Console()

HASHCRACK_HOME = Path.home() / ".hashCrack"
LOGS_DIR = HASHCRACK_HOME / "logs"

ASCII_ART = [
    r" ▄  █ ██      ▄▄▄▄▄    ▄  █ ▄█▄    █▄▄▄▄ ██   ▄█▄    █  █▀",
    r"█   █ █ █    █     ▀▄ █   █ █▀ ▀▄  █  ▄▀ █ █  █▀ ▀▄  █▄█  ",
    r"██▀▀█ █▄▄█ ▄  ▀▀▀▀▄   ██▀▀█ █   ▀  █▀▀▌  █▄▄█ █   ▀  █▀▄  ",
    r"█   █ █  █  ▀▄▄▄▄▀    █   █ █▄  ▄▀ █  █  █  █ █▄  ▄▀ █  █ ",
    r"   █     █               █  ▀███▀    █      █ ▀███▀    █  ",
    r"  ▀     █               ▀           ▀      █          ▀   ",
    r"       ▀                                  ▀               ",
]


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
        "default_device": "1",
        "default_force": False,
    }


def define_windows_parameters():
    return {
        "default_hashcat": ".",
        "default_status_timer": "y",
        "default_workload": "3",
        "default_os": "Windows",
        "default_restorepath": os.path.expanduser("~/hashcat/sessions"),
        "default_session": datetime.now().strftime("%Y-%m-%d"),
        "default_wordlists": f"/c/Users/{os.getenv('USER', os.getenv('USERNAME', ''))}/wordlists",
        "default_masks": "masks",
        "default_rules": "rules",
        "default_wordlist": "rockyou.txt",
        "default_mask": "?d?d?d?d?d?d?d?d",
        "default_rule": "T0XlCv2.rule",
        "default_min_length": "8",
        "default_max_length": "16",
        "default_hashmode": "22000",
        "default_device": "1",
        "default_force": False,
    }


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_hashcrack_title():
    """Render the ASCII logo centered, in blue."""
    banner = Text()
    for line in ASCII_ART:
        banner.append(line + "\n", style="bold blue")
    banner.append("For more information: https://github.com/ente0/hashCrack\n", style="dim")
    console.print(Align.center(banner))


def define_logs(session):
    """Ensure the session log dir exists and return (plaintext, status_json, log_dir) paths."""
    log_dir = LOGS_DIR / session
    log_dir.mkdir(parents=True, exist_ok=True)
    plaintext = log_dir / "plaintext.txt"
    status = log_dir / "status.json"
    return str(plaintext), str(status), str(log_dir)


def _read_status_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def collect_found_plaintexts():
    """Scan status.json files and return a list of cracked sessions."""
    if not LOGS_DIR.exists():
        return []
    results = []
    for status_path in sorted(LOGS_DIR.glob("*/status.json")):
        data = _read_status_json(str(status_path))
        if not data or not data.get("plaintext"):
            continue
        attack = data.get("attack") or {}
        results.append({
            "session": data.get("session") or status_path.parent.name,
            "plaintext": data["plaintext"],
            "path": str(status_path.parent),
            "attack": attack.get("type"),
            "hashmode": attack.get("hashmode"),
            "wordlist": attack.get("wordlist"),
            "rule": attack.get("rule"),
            "mask": attack.get("mask"),
        })
    return results


def count_sessions():
    if not LOGS_DIR.exists():
        return 0
    return sum(1 for _ in LOGS_DIR.glob("*/status.json"))


def update_terminal_title(default_os, found_plaintexts):
    if found_plaintexts:
        parts = [f"{p['plaintext']} ({p['session']})" for p in found_plaintexts]
        title = "hashCrack - " + " | ".join(parts)
    else:
        title = "hashCrack"
    if default_os == "Windows":
        os.system(f"title {title}")
    else:
        print(f"\033]0;{title}\007", end="", flush=True)


def get_potfile_info():
    candidates = [
        Path.home() / ".local/share/hashcat/hashcat.potfile",
        Path.home() / ".hashcat/hashcat.potfile",
    ]
    for p in candidates:
        if p.exists():
            return p, p.stat().st_size
    return None, 0


def save_logs(
    session,
    *,
    wordlist_path=None,
    wordlist=None,
    mask_path=None,
    mask=None,
    rule_path=None,
    rule=None,
    hash_file=None,
    attack_type=None,
    command=None,
    hashmode=None,
    workload=None,
    device=None,
    force=False,
    os_name=None,
    min_length=None,
    max_length=None,
    silent=False,
):
    """Persist structured status + display a summary. Keyword-only to avoid positional bugs."""
    plaintext_file, status_file, log_dir = define_logs(session)

    plaintext = None
    if os.path.exists(plaintext_file) and os.path.getsize(plaintext_file) > 0:
        with open(plaintext_file, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line:
                    plaintext = line
                    break

    hash_content = None
    if hash_file and os.path.exists(hash_file):
        try:
            with open(hash_file, "r", encoding="utf-8", errors="replace") as f:
                hash_content = f.read().strip()
        except Exception:
            hash_content = None

    def _join(parent, name):
        if parent and name:
            return str(Path(parent) / name)
        return name or None

    status = {
        "session": session,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "cracked" if plaintext else "not_cracked",
        "attack": {
            "type": attack_type,
            "hashmode": hashmode,
            "wordlist": _join(wordlist_path, wordlist),
            "rule": _join(rule_path, rule),
            "mask": _join(mask_path, mask) if mask_path else mask,
            "min_length": min_length,
            "max_length": max_length,
        },
        "system": {
            "os": os_name,
            "device": device,
            "workload": workload,
            "force": bool(force),
        },
        "hash_file": {
            "path": hash_file,
            "size": os.path.getsize(hash_file) if hash_file and os.path.exists(hash_file) else None,
            "content": hash_content,
        },
        "plaintext": plaintext,
        "command": command,
    }

    with open(status_file, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)

    if command:
        with open(os.path.join(log_dir, "command.txt"), "w", encoding="utf-8") as f:
            f.write(command + "\n")

    if not silent:
        console.print(Panel.fit(
            f"[bold]Session:[/] {session}\n"
            f"[bold]Status :[/] {'[green]CRACKED[/]' if plaintext else '[red]NOT CRACKED[/]'}\n"
            f"[bold]Result :[/] {plaintext or 'N/A'}\n"
            f"[bold]Logs   :[/] {log_dir}",
            title="Run summary",
            border_style="green" if plaintext else "red",
        ))


def display_plaintext_status():
    found = collect_found_plaintexts()
    if not found:
        console.print(Panel.fit("[yellow]No plaintexts found in status files.[/]", border_style="yellow"))
        return
    t = Table(title="Found plaintexts", box=box.ROUNDED, show_lines=False, header_style="bold green")
    t.add_column("Session", style="cyan")
    t.add_column("Plaintext", style="bold yellow")
    t.add_column("Attack", style="magenta")
    t.add_column("Wordlist", style="green", overflow="fold")
    t.add_column("Rule", style="blue", overflow="fold")
    t.add_column("Mask", style="red", overflow="fold")
    for p in found:
        t.add_row(
            p["session"],
            p["plaintext"],
            p.get("attack") or "-",
            str(p.get("wordlist") or "-"),
            str(p.get("rule") or "-"),
            str(p.get("mask") or "-"),
        )
    console.print(t)


def _hash_file_panel(hash_file):
    if hash_file and os.path.isfile(hash_file) and os.path.getsize(hash_file) > 0:
        try:
            with open(hash_file, "r", encoding="utf-8", errors="replace") as f:
                preview = f.readline().strip()
            preview = preview[:60] + "..." if len(preview) > 60 else preview
            text = (
                f"[green]✓[/] [bold]{os.path.basename(hash_file)}[/]  "
                f"[dim]({os.path.getsize(hash_file)} B)[/]\n"
                f"[dim]path:[/]    {hash_file}\n"
                f"[dim]preview:[/] {preview}"
            )
            return Panel(text, title="Hash file", border_style="green")
        except Exception as e:
            return Panel(f"[yellow]{hash_file}[/] loaded but unreadable: {e}",
                         title="Hash file", border_style="yellow")
    if hash_file:
        return Panel(f"[red]✕ {hash_file}: file not found or empty[/]",
                     title="Hash file", border_style="red")
    return Panel("[red]✕ No hash file loaded[/]", title="Hash file", border_style="red")


def show_menu(default_os, hash_file=None):
    """Render the dashboard menu and return the user's selection."""
    found = collect_found_plaintexts()
    update_terminal_title(default_os, found)

    print_hashcrack_title()

    potfile_path, potfile_size = get_potfile_info()
    sessions_count = count_sessions()

    stats = Table.grid(padding=(0, 3), expand=True)
    for _ in range(4):
        stats.add_column(justify="center")
    stats.add_row(
        f"[bold cyan]OS[/]\n{default_os}",
        f"[bold cyan]Potfile[/]\n" + (f"{potfile_size:,} B" if potfile_path else "[dim]none[/]"),
        f"[bold cyan]Sessions[/]\n{sessions_count}",
        f"[bold cyan]Cracked[/]\n{len(found)}",
    )
    console.print(Panel(stats, title="[bold]hashCrack[/] — dashboard", border_style="cyan"))
    console.print(_hash_file_panel(hash_file))

    if found:
        ft = Table(box=box.SIMPLE, show_header=True, header_style="bold green")
        ft.add_column("#", justify="right", width=3)
        ft.add_column("Session", style="cyan")
        ft.add_column("Plaintext", style="bold yellow")
        ft.add_column("Attack", style="magenta")
        for i, p in enumerate(found, 1):
            ft.add_row(str(i), p["session"], p["plaintext"], p.get("attack") or "-")
        console.print(Panel(ft, title="Recent cracks", border_style="green"))

    attacks = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan", title="Attack modes")
    attacks.add_column("#", style="bold cyan", width=3, justify="center")
    attacks.add_column("Mode", style="white")
    attacks.add_column("Hashcat invocation", style="dim")
    attacks.add_column("Level", justify="right")
    attacks.add_row("1", "Wordlist",             "-a 0 <wordlist>",              "[blue]EASY[/]")
    attacks.add_row("2", "Wordlist + Rules",     "-a 0 <wordlist> -r <rule>",    "[green]MEDIUM[/]")
    attacks.add_row("3", "Brute-Force (mask)",   "-a 3 <mask> --increment",      "[yellow]HARD[/]")
    attacks.add_row("4", "Combinator",           "-a 6 <wordlist> <mask>",       "[red]ADVANCED[/]")
    attacks.add_row("5", "Plaintext status",     "Inspect cracked sessions",     "")
    console.print(attacks)

    utils = Table(box=box.ROUNDED, show_header=False)
    utils.add_column(style="bold magenta", width=3, justify="center")
    utils.add_column(style="white")
    utils.add_column(style="dim")
    utils.add_row("6", "Clear potfile",  "Delete hashcat potfile(s)")
    utils.add_row("X", "Switch OS",      f"Currently {default_os} → {'Windows' if default_os=='Linux' else 'Linux'}")
    utils.add_row("Q", "Quit",           "Exit hashCrack")
    console.print(Panel(utils, title="Utilities & system", border_style="magenta"))

    return console.input("[bold cyan]>[/] Enter option: ").strip().lower()


def handle_option(option, default_os, hash_file, extra_args=None):
    """Dispatch a menu selection to the matching attack script."""
    script_map = {
        "1": "crack_wordlist.py",
        "2": "crack_rule.py",
        "3": "crack_bruteforce.py",
        "4": "crack_combo.py",
    }
    clear_screen()

    if option == "5":
        display_plaintext_status()
        console.input("\n[cyan]Press Enter to return to the menu...[/]")
        return

    script_name = script_map.get(option)
    if not script_name:
        console.print(f"[red]Invalid option: {option}[/]")
        return

    script_type = "windows" if default_os == "Windows" else "linux"
    try:
        script_path = get_package_script_path(script_name, script_type)
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/]")
        return

    python_cmd = "python3" if default_os == "Linux" else "python"
    cmd = [python_cmd, str(script_path), hash_file]
    if extra_args:
        cmd.extend(extra_args)

    console.print(f"[green]Executing:[/] {' '.join(shlex.quote(c) for c in cmd)}")
    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        console.print("\n[yellow]Attack interrupted by user.[/]")
    console.input("\n[cyan]Press Enter to return to the menu...[/]")


def run_hashcat(cmd, session, *, save_kwargs):
    """Execute hashcat, tee output to hashcat.log, then persist structured status."""
    _plaintext_file, _status_file, log_dir = define_logs(session)
    hashcat_log = os.path.join(log_dir, "hashcat.log")
    pretty_cmd = " ".join(shlex.quote(c) for c in cmd)
    console.print(Panel(pretty_cmd, title="Hashcat command", border_style="blue"))

    proc = None
    try:
        with open(hashcat_log, "w", encoding="utf-8") as logf:
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1,
            )
            assert proc.stdout is not None
            for line in proc.stdout:
                print(line, end="")
                logf.write(line)
            proc.wait()
    except FileNotFoundError:
        console.print("[red]Error: 'hashcat' binary not found in PATH.[/]")
        return
    except KeyboardInterrupt:
        console.print("\n[yellow]Attack interrupted by user.[/]")
        if proc is not None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

    save_logs(session, command=pretty_cmd, **save_kwargs)


def animate_text(text, delay):
    for i in range(len(text) + 1):
        clear_screen()
        print(text[:i], end="", flush=True)
        time.sleep(delay)


def get_package_script_path(script_name, os_type):
    try:
        package_path = resources.files(f"hashCrack.{os_type.lower()}") / script_name
        if not package_path.is_file():
            raise FileNotFoundError(f"Script {script_name} not found in package")
        return package_path
    except (ImportError, AttributeError, TypeError):
        if pkg_resources is None:
            raise FileNotFoundError(f"Cannot locate {script_name}")
        package_path = pkg_resources.resource_filename("hashCrack", f"{os_type.lower()}/{script_name}")
        if not os.path.exists(package_path):
            raise FileNotFoundError(f"Script {script_name} not found in package")
        return Path(package_path)


def execute_windows_scripts():
    windows_scripts_dir = "scripts/windows"
    if not os.path.isdir(windows_scripts_dir):
        console.print(f"[red]Error: Windows scripts directory not found: '{windows_scripts_dir}'[/]")
        return
    for script in os.listdir(windows_scripts_dir):
        script_path = os.path.join(windows_scripts_dir, script)
        if os.path.isfile(script_path):
            console.print(f"[green]Executing Windows script:[/] {script}")
            os.system(f"python {script_path}")


def list_sessions(default_restorepath):
    try:
        restore_files = [f for f in os.listdir(default_restorepath) if f.endswith(".restore")]
    except FileNotFoundError:
        console.print(f"[red]Directory {default_restorepath} does not exist.[/]")
        return
    if not restore_files:
        console.print("[yellow]No restore files found.[/]")
        return
    console.print("[green]Available sessions:[/]")
    for restore_file in restore_files:
        console.print(f"  [yellow]-[/] {restore_file}")


def restore_session(restore_file_input, default_restorepath):
    restore_file = (restore_file_input or "").strip()
    if not restore_file:
        return
    if not os.path.isabs(restore_file):
        restore_file = os.path.join(default_restorepath, restore_file)
    if not os.path.isfile(restore_file):
        console.print(f"[red]Restore file '{restore_file}' not found.[/]")
        return
    session = os.path.basename(restore_file).replace(".restore", "")
    console.print(f"[blue]Restoring session:[/] {restore_file}")
    cmd = f"hashcat --session={session} --restore"
    console.print(f"[blue]Executing:[/] {cmd}")
    os.system(cmd)


def validate_hashfile(path):
    """Fail fast if the given path is not a readable non-empty file."""
    if not path:
        console.print("[red]Error: no hash file provided.[/]")
        sys.exit(1)
    if not os.path.isfile(path):
        console.print(f"[red]Error: '{path}' does not exist.[/]")
        sys.exit(1)
    if os.stat(path).st_size == 0:
        console.print(f"[red]Error: '{path}' is empty.[/]")
        sys.exit(1)
    return path


def define_hashfile(path=None):
    """Backwards-compatible: if path is None, parse argv[1]; either way validate."""
    if path is None:
        if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
            path = sys.argv[1]
    return validate_hashfile(path)


def clean_hashcat_cache(verbose=False):
    """Remove known hashcat potfiles. Returns (removed_paths, error_msg_or_None).
    When verbose=True also prints the outcome (used by the classic menu)."""
    potfile_paths = [
        Path.home() / ".local/share/hashcat/hashcat.potfile",
        Path.home() / ".hashcat/hashcat.potfile",
        Path.home() / "venv/lib/python3.12/site-packages/hashcat/hashcat/hashcat.potfile",
    ]
    removed = []
    try:
        for potfile in potfile_paths:
            if potfile.exists():
                potfile.unlink()
                removed.append(potfile)
        if verbose:
            if removed:
                for p in removed:
                    console.print(f"[green]Removed:[/] {p}")
            else:
                console.print("[yellow]No potfile found to remove.[/]")
        return removed, None
    except Exception as e:
        if verbose:
            console.print(f"[red]Error cleaning hashcat cache: {e}[/]")
        return removed, str(e)


def get_unique_session_name(session_name, log_path="~/.hashCrack/logs/"):
    expanded_path = os.path.expanduser(log_path)
    counter = 0
    while True:
        unique_name = session_name if counter == 0 else f"{session_name}_{counter}"
        if not os.path.isdir(os.path.join(expanded_path, unique_name)):
            return unique_name
        counter += 1
