

<p align="center">
  <img src="https://github.com/user-attachments/assets/acdddcac-41ad-4c89-a9b9-34a4d7a1f814"/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/ente0/hashCrack">
  <img src="https://img.shields.io/badge/language-python-green" alt="Language: Python">
  
  <img src="https://img.shields.io/badge/dependencies-python--pip--hashcat--termcolor-green" alt="Dependencies">
  
  <a href="https://github.com/ente0/hashCrack/releases">
    <img src="https://img.shields.io/badge/release-v1.4.3-blue" alt="PyPI Version">
  </a>
</p>

<div align="center">
  
# hashCrack: Hashcat made Easy

### **A Python-based wrapper for [Hashcat](https://hashcat.net/hashcat/), offering a simplified menu interface for password cracking tasks. This tool enables users to conduct various attack types through an intuitive, menu-driven interface.**

</div>

> [!CAUTION]
> This tool is provided "as-is," without any express or implied warranties. The author assumes no responsibility for any damages, losses, or consequences arising from the use of this tool. It is specifically designed for penetration testing purposes, and should only be used in legal and authorized environments, such as with explicit permission from the system owner. Unauthorized use or misuse of this tool, in violation of applicable laws, is strictly prohibited. Users are strongly advised to comply with all relevant local, national, and international laws and obtain proper authorization before performing any security assessments.

---

## Features
- Multiple attack modes: wordlists, rules, brute-force, and hybrid attacks.
- An interactive menu for selecting and configuring cracking options.
- Session restoration support for interrupted sessions.
- Designed for compatibility across Linux and Windows environments.

## Installation & Setup

### Requirements

#### Linux:
- **OS**: Any Linux distribution
- **Programs**:
  - **Hashcat**: Install from [hashcat.net](https://hashcat.net/hashcat/)
  - **Optional**: For WPA2 cracking, additional tools like [aircrack-ng](https://www.aircrack-ng.org/), [hcxtools](https://github.com/zkryss/hcxtools), and [hcxdumptool](https://github.com/fg8/hcxdumptool) are recommended.
  
**Distribution-specific Commands**:
- **Debian/Ubuntu**:
  ```bash
  sudo apt update && sudo apt install hashcat python3 python3-pip python3-termcolor pipx
  ```
- **Fedora**:
  ```bash
  sudo dnf install hashcat python3 python3-pip python3-termcolor python3-pipx
  ```
- **Arch Linux/Manjaro**:
  ```bash
  sudo pacman -S hashcat python python-pip python-termcolor python-pipx
  ```

#### Windows:
- **OS**: Windows 10 or later
- **Programs**:
  - **Hashcat**: Download the Windows version from [hashcat.net](https://hashcat.net/hashcat/)
  - **Python**: Install from [python.org](https://www.python.org/downloads/)
  - **Optional**: For a Linux-like environment, set up [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install)

> [!TIP]
> Recommended wordlists, rules, and masks can be found in repositories like [SecLists](https://github.com/danielmiessler/SecLists) and [wpa2-wordlists](https://github.com/kennyn510/wpa2-wordlists.git).
   
### Installation via pip
1. **Install hashCrack with pip**:
   You can install `hashCrack` directly from the Python Package Index (PyPI) using the following command:
   ```bash
   pipx install hashcrack-tool
   ```

> [!IMPORTANT]
> Make sure that ~/.local/bin is in the PATH variable.

2. **Running hashCrack**:
   After installation, you can run `hashCrack` by specifying the hash file you want to crack (run`source venv/bin/activate` before executing):
   ```bash
   hashcrack hashfile
   ```
3. **Upgrading hashCrack**:
   If you want to upgrade to the latest version just execute:
   ```bash
   pipx upgrade hashcrack-tool
   ```
   
<p align="center">
  <video src="https://github.com/user-attachments/assets/bcfc0ecd-6cde-436d-87df-4fb2ed1d90d0" />
</p>
    
>[!TIP]
> **(Optional) Download default wordlists and rules**:
   ```bash
   git clone https://github.com/ente0/hashcat-defaults
   ```
> [!IMPORTANT]
> The cracking results will be stored in `~/.hashCrack/logs/session`, specifically in `status.txt`.

## Latest Releases
For the latest release versions of hashCrack, visit the [hashCrack Releases](https://github.com/ente0v1/hashCrack/releases) page.

## Attack Modes
hashCrack supports the following attack modes:
| # | Mode                 | Description                                                                                   |
|---|-----------------------|-----------------------------------------------------------------------------------------------|
| 0 | Straight             | Uses a wordlist directly to attempt cracks                                                    |
| 1 | Combination          | Combines two dictionaries to produce candidate passwords                                      |
| 3 | Brute-force          | Attempts every possible password combination based on a specified character set               |
| 6 | Hybrid Wordlist + Mask | Uses a wordlist combined with a mask to generate variations                                 |
| 7 | Hybrid Mask + Wordlist | Uses a mask combined with a wordlist for generating password candidates                     |
| 9 | Association          | For specific hash types where known data is combined with brute-force attempts                |

## Menu Options
The main menu provides easy access to various cracking methods:

| Option     | Description                | Script                          |
|------------|----------------------------|---------------------------------|
| 1 (Mode 0) | Crack with Wordlist        | Executes wordlist-based cracking |
| 2 (Mode 9) | Crack with Rules           | Executes rule-based cracking |
| 3 (Mode 3) | Crack with Brute-Force     | Executes brute-force cracking |
| 4 (Mode 6) | Crack with Combinator      | Executes hybrid wordlist + mask cracking |
| 0          | Clear Hashcat Potfile      | Deletes the potfile to clear previous hash results |
| X          | Switch Current OS Menu     | Updates the menu and script settings based on the current OS |
| Q          | Quit                       | Exits the program |

### Example Commands
```bash
hashcat -a 0 -m 400 example400.hash example.dict              # Wordlist
hashcat -a 0 -m 0 example0.hash example.dict -r best64.rule   # Wordlist + Rules
hashcat -a 3 -m 0 example0.hash ?a?a?a?a?a?a                  # Brute-Force
hashcat -a 1 -m 0 example0.hash example.dict example.dict     # Combination
hashcat -a 9 -m 500 example500.hash 1word.dict -r best64.rule # Association
```
---
## Troubleshooting Hashcat Issues

If you encounter errors when running Hashcat, you can follow these steps to troubleshoot:

1. **Test Hashcat Functionality**:
   First, run a benchmark test to ensure that Hashcat is working properly:
   ```bash
   hashcat -b
   ```
   This command will perform a benchmark on your system to check Hashcat's overall functionality. If this command works without issues, Hashcat is likely properly installed.

2. **Check Available Devices**:
   To verify that Hashcat can detect your devices (such as GPUs) for cracking, use the following command:
   ```bash
   hashcat -I
   ```
   This command will list the available devices. Ensure that the correct devices are listed for use in cracking.

3. **Check for Errors in Hashcat**:
   If the cracking process fails or Hashcat doesn't seem to recognize your devices, running the above tests should help identify potential problems with your system configuration, such as missing or incompatible drivers.

4. **Permissions**:
   If you encounter permission issues (especially on Linux), consider running Hashcat with elevated privileges or configuring your user group correctly for GPU access. You can run Hashcat with `sudo` if necessary:
   ```bash
   sudo hashcat -b
   ```

---

## Script Walkthrough

The main hashCrack script consists of:
1. **Initialization**: Loads default parameters and reusable functions.
2. **User Prompts**: Gathers inputs from the user such as wordlist location, session names, and attack type.
3. **Command Construction**: Constructs the Hashcat command based on user inputs and specified attack mode.
4. **Execution**: Runs the cracking session with or without status timers.
5. **Logging**: Saves session results for future reference.

---

## Support

To report bugs, issues, or feature requests, please open a new issue on [GitHub Issues](https://github.com/ente0/hashCrack/issues).

For further questions or assistance, contact us via [email](mailto:enteo.dev@protonmail.com).

For more resources, consider the following repositories:
- [hashcat-defaults](https://github.com/ente0v1/hashcat-defaults)
- [wpa2-wordlists](https://github.com/kennyn510/wpa2-wordlists.git)
- [paroleitaliane](https://github.com/napolux/paroleitaliane)
- [SecLists](https://github.com/danielmiessler/SecLists)
- [hashcat-rules](https://github.com/Unic0rn28/hashcat-rules)

To capture WPA2 hashes, follow [this guide on the 4-way handshake](https://notes.networklessons.com/security-wpa-4-way-handshake) and see this [video](https://www.youtube.com/watch?v=WfYxrLaqlN8) to see how the attack actually works.
For more details on Hashcat’s attack modes and usage, consult the [Hashcat Wiki](https://hashcat.net/wiki/), [Radiotap Introduction](https://www.radiotap.org/), or [Aircrack-ng Guide](https://wiki.aircrack-ng.org/doku.php?id=airodump-ng).
