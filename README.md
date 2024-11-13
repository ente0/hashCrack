# hashCrack: A Hashcat Wrapper

<p align="center">
  <video src="https://github.com/user-attachments/assets/ea69ed0f-e870-4a32-90cd-6a3972eb71cb" />
</p>


## Description

A Python-based wrapper for [Hashcat](https://hashcat.net/hashcat/), offering a simplified, user-friendly interface for password cracking tasks. hashCrack enables you to use different attack methods—wordlists, rules, brute-force, and hybrid attacks—through a guided menu interface. ![GitHub License](https://img.shields.io/github/license/ente0v1/hashCrack)


## Disclaimer

This tool is provided without warranties, and the author is not liable for any damage resulting from its usage. Use responsibly and in compliance with all applicable laws.

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
  sudo apt update && sudo apt install hashcat aircrack-ng hcxtools hcxdumptool python3 python3-pip git
  ```
- **Fedora**:
  ```bash
  sudo dnf install hashcat aircrack-ng hcxtools hcxdumptool python3 python3-pip git
  ```
- **Arch Linux/Manjaro**:
  ```bash
  sudo pacman -S hashcat aircrack-ng hcxtools hcxdumptool python python-pip git
  ```

#### Windows:
- **OS**: Windows 10 or later
- **Programs**:
  - **Hashcat**: Download the Windows version from [hashcat.net](https://hashcat.net/hashcat/)
  - **Python**: Install from [python.org](https://www.python.org/downloads/)
  - **Optional**: For a Linux-like environment, set up [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install)

#### Additional Resources:
- Recommended wordlists, rules, and masks can be found in repositories like [SecLists](https://github.com/danielmiessler/SecLists) and [wpa2-wordlists](https://github.com/kennyn510/wpa2-wordlists.git). It’s advised to keep these resources in `hashCrack` under `wordlists`, `rules`, and `masks` folders for better compatibility.

---

### Cloning and Running hashCrack
1. **Clone the repository**:
   ```bash
   git clone --depth 1 https://github.com/ente0v1/hashCrack.git
   cd hashCrack
   ```
2. **Download default wordlists and rules**:
   ```bash
   git clone https://github.com/ente0v1/hashcat-defaults
   git lfs install
   git pull
   cd ..
   cp -rf hashcat-defaults/* .
   sudo rm -r hashcat-defaults
   ```
3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Place the hash**:
   ```bash
   mv hash.txt hashCrack
   ```
4. **Run hashCrack**:
   ```bash
   python hashCrack.py
   ```
To verify and check for any missing dependencies, execute the `check_dependencies.py` script. Run the following command:
```
python check_dependencies.py
```
If you encounter any issues with installing dependencies, such as permission errors or system-wide installation restrictions, you can either create a virtual environment or install the dependencies as root.

### If `pip install -r requirements.txt` fails

Creating a Python virtual environment is optional but recommended if you run into issues with installing dependencies system-wide. Here's how you can set up a virtual environment:

1. **Install Python and pip** (if you haven't already):

   - On Arch Linux:
     ```
     sudo pacman -S python python-pip
     ```

   - On Debian/Ubuntu-based distributions:
     ```
     sudo apt install python3 python3-pip
     ```

   - On Fedora:
     ```
     sudo dnf install python3 python3-pip
     ```

   - On Windows, Python and pip can be installed from the official [Python website](https://www.python.org/downloads/).

2. **Create and activate a virtual environment**:
   - Run the following commands to create a virtual environment named `venv`:
     ```
     python -m venv venv
     ```

   - **Activate the virtual environment**:
     - On Linux:
       ```
       source venv/bin/activate
       ```

     - On Windows:
       ```
       .\venv\Scripts\activate
       ```

3. **Install dependencies**:
   After activating the virtual environment, install the required Python packages using `pip`:
    ```
    pip install -r requirements.txt
    ```

## Usage Overview

### Capturing WPA2 Hashes
To capture WPA2 hashes, follow [this guide on the 4-way handshake](https://notes.networklessons.com/security-wpa-4-way-handshake) and see this [video](https://www.youtube.com/watch?v=WfYxrLaqlN8) to see it actually works. Capture scripts are provided in the `scripts` folder.

### Cracking the Hash
1. Rename the hash file to `hash.txt` and place it in the `hashCrack` directory.
2. Start cracking with:
   ```bash
   python hashCrack.py
   ```
3. The cracking results will be stored in `logs`, specifically in `status.txt`.

### Attack Modes
hashCrack supports the following attack modes:
| # | Mode                 | Description                                                                                   |
|---|-----------------------|-----------------------------------------------------------------------------------------------|
| 0 | Straight             | Uses a wordlist directly to attempt cracks                                                    |
| 1 | Combination          | Combines two dictionaries to produce candidate passwords                                      |
| 3 | Brute-force          | Attempts every possible password combination based on a specified character set               |
| 6 | Hybrid Wordlist + Mask | Uses a wordlist combined with a mask to generate variations                                 |
| 7 | Hybrid Mask + Wordlist | Uses a mask combined with a wordlist for generating password candidates                     |
| 9 | Association          | For specific hash types where known data is combined with brute-force attempts                |

---

## Menu Options

The main menu provides easy access to various cracking methods:
| Option | Description                | Script |
|--------|----------------------------|--------|
| 1      | Crack with Wordlist        | Executes crack-wordlist script |
| 2      | Crack with Rules           | Executes crack-rule script     |
| 3      | Crack with Brute-Force     | Executes crack-bruteforce script |
| 4      | Crack with Combinator      | Executes crack-combo script     |
| Q      | Quit                       | Saves settings and logs, then exits |

### Example Commands
```bash
hashcat -a 0 -m 400 example400.hash example.dict              # Wordlist
hashcat -a 0 -m 0 example0.hash example.dict -r best64.rule   # Wordlist + Rules
hashcat -a 3 -m 0 example0.hash ?a?a?a?a?a?a                  # Brute-Force
hashcat -a 1 -m 0 example0.hash example.dict example.dict     # Combination
hashcat -a 9 -m 500 example500.hash 1word.dict -r best64.rule # Association
```


## Script Walkthrough

The main hashCrack script consists of:
1. **Initialization**: Loads default parameters and reusable functions.
2. **User Prompts**: Gathers inputs from the user such as wordlist location, session names, and attack type.
3. **Command Construction**: Constructs the Hashcat command based on user inputs and specified attack mode.
4. **Execution**: Runs the cracking session with or without status timers.
5. **Logging**: Saves session settings and logs the results for future reference.

---

## Useful Wordlist Manipulation Commands

Here are some bash commands for common wordlist operations:
- **Remove duplicates**:
  ```bash
  awk '!(count[$0]++)' old.txt > new.txt
  ```
- **Sort by length**:
  ```bash
  awk '{print length, $0}' old.txt | sort -n | cut -d " " -f2- > new.txt
  ```
- **Sort alphabetically**:
  ```bash
  sort old.txt | uniq > new.txt
  ```
- **Merge multiple files**:
  ```bash
  cat file1.txt file2.txt > combined.txt
  ```
- **Remove blank lines**:
  ```bash
  egrep -v "^[[:space:]]*$" old.txt > new.txt
  ```

---

## Help
For more resources, consider the following repositories:
- [wpa2-wordlists](https://github.com/kennyn510/wpa2-wordlists.git)
- [paroleitaliane](https://github.com/napolux/paroleitaliane)
- [SecLists](https://github.com/danielmiessler/SecLists)
- [hashcat-rules](https://github.com/Unic0rn28/hashcat-rules)

For more details on Hashcat’s attack modes and usage, consult the [Hashcat Wiki](https://hashcat.net/wiki/), [Radiotap Introduction](https://www.radiotap.org/), or [Aircrack-ng Guide](https://wiki.aircrack-ng.org/doku.php?id=airodump-ng).
