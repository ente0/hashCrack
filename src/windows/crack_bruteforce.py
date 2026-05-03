"""hashcat brute-force (mask) attack (mode -a 3) - Windows."""
import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from rich.console import Console

from hashCrack.functions import (
    define_windows_parameters, define_logs, run_hashcat, validate_hashfile,
)
from hashCrack.windows_inputs import (
    define_mask, define_length, define_session, define_status, define_hashmode,
    define_workload, define_device, define_hashcat, define_force,
)

console = Console()
parameters = define_windows_parameters()
OS_NAME = "Windows"


def build_command(hashcat_path, session, hashmode, mask, workload, status_timer,
                  min_length, max_length, device, hash_file, plaintext_path, force):
    cmd = [
        f"{hashcat_path}/hashcat.exe",
        f"--session={session}",
        "-m", hashmode,
        hash_file,
        "-a", "3",
        "-w", workload,
        "--outfile-format=2",
        "-o", plaintext_path,
        mask,
        "-d", device,
        "--potfile-disable",
        "--increment",
        f"--increment-min={min_length}",
        f"--increment-max={max_length}",
    ]
    if status_timer.lower() == "y":
        cmd += ["--status", "--status-timer=2"]
    if force:
        cmd.append("--force")
    return cmd


def main():
    parser = argparse.ArgumentParser(description="Brute-force (mask) attack (hashcat -a 3) [Windows].")
    parser.add_argument("hash_file", help="Path to the hash file")
    parser.add_argument("--force", action="store_true", help="Pass --force to hashcat")
    args = parser.parse_args()

    hash_file = validate_hashfile(args.hash_file)
    session = define_session()
    use_mask_file, mask_path, mask = define_mask()
    hashmode = define_hashmode()
    hashcat_path = define_hashcat()
    status_timer = define_status()
    min_length, max_length = define_length()
    workload = define_workload()
    device = define_device()
    force = True if args.force else define_force(default=False)

    mask_arg = f"{mask_path}/{mask}" if (use_mask_file == "y" and mask_path) else mask

    plaintext_path, _status_path, _log_dir = define_logs(session)
    cmd = build_command(hashcat_path, session, hashmode, mask_arg, workload, status_timer,
                        min_length, max_length, device, hash_file, plaintext_path, force)

    run_hashcat(cmd, session, save_kwargs=dict(
        mask_path=mask_path if use_mask_file == "y" else None,
        mask=mask,
        hash_file=hash_file,
        attack_type="bruteforce",
        hashmode=hashmode,
        workload=workload,
        device=device,
        force=force,
        os_name=OS_NAME,
        min_length=min_length,
        max_length=max_length,
    ))


if __name__ == "__main__":
    main()
