"""hashcat straight dictionary attack (mode -a 0)."""
import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from rich.console import Console

from hashCrack.functions import (
    define_default_parameters, define_logs, run_hashcat, validate_hashfile,
)
from hashCrack.linux_inputs import (
    define_wordlist, define_session, define_status, define_hashmode,
    define_workload, define_device, define_force,
)

console = Console()
parameters = define_default_parameters()
OS_NAME = "Linux"


def build_command(session, hashmode, wordlist_path, wordlist, workload,
                  status_timer, device, hash_file, plaintext_path, force):
    cmd = [
        "hashcat",
        f"--session={session}",
        "-m", hashmode,
        hash_file,
        "-a", "0",
        "-w", workload,
        "--outfile-format=2",
        "-o", plaintext_path,
        f"{wordlist_path}/{wordlist}",
        "-d", device,
        "--potfile-disable",
    ]
    if status_timer.lower() == "y":
        cmd += ["--status", "--status-timer=2"]
    if force:
        cmd.append("--force")
    return cmd


def main():
    parser = argparse.ArgumentParser(description="Wordlist attack (hashcat -a 0).")
    parser.add_argument("hash_file", help="Path to the hash file")
    parser.add_argument("--force", action="store_true", help="Pass --force to hashcat")
    args = parser.parse_args()

    hash_file = validate_hashfile(args.hash_file)
    session = define_session()
    wordlist_path, wordlist = define_wordlist()
    if wordlist_path is None:
        sys.exit(1)
    hashmode = define_hashmode()
    status_timer = define_status()
    workload = define_workload()
    device = define_device()
    force = True if args.force else define_force(default=False)

    plaintext_path, _status_path, _log_dir = define_logs(session)
    cmd = build_command(session, hashmode, wordlist_path, wordlist, workload,
                        status_timer, device, hash_file, plaintext_path, force)

    console.print(f"[magenta]Restore:[/] {parameters['default_restorepath']}/{session}")
    run_hashcat(cmd, session, save_kwargs=dict(
        wordlist_path=wordlist_path,
        wordlist=wordlist,
        hash_file=hash_file,
        attack_type="wordlist",
        hashmode=hashmode,
        workload=workload,
        device=device,
        force=force,
        os_name=OS_NAME,
    ))


if __name__ == "__main__":
    main()
