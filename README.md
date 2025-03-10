<p align="center">
  <img src="https://github.com/user-attachments/assets/0c5fcac9-f8d7-4a7b-be44-b0b8757df9a5"/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/ente0/hashCrack" alt="License">
  <img src="https://img.shields.io/badge/language-python-green" alt="Language: Python">
  <img src="https://img.shields.io/badge/dependencies-hashcat-blue" alt="Dependencies">
  <img src="https://img.shields.io/badge/release-v1.4.15-green" alt="Version">
</p>

<div align="center">
  
# hashCrack: Hashcat made Easy
### **A sophisticated Python-based wrapper for Hashcat. The tool provides a streamlined approach to various attack modes, making advanced password recovery more accessible.**

</div>


> [!CAUTION]
> This tool is strictly for authorized security testing and educational purposes. Always obtain explicit permission before conducting any network assessments.

## 🚀 Key Features

- 🔐 Multiple Attack Modes
  - Wordlist attacks
  - Rule-based cracking
  - Brute-force strategies
  - Hybrid attack combinations

- 🖥️ Cross-Platform Compatibility
  - Optimized for Linux environments
  - Experimental Windows support via WSL

- 📊 Intelligent Interface
  - Interactive menu system
  - Session restoration
  - Comprehensive logging

## 💻 System Requirements

### 🐧 Recommended: Linux Environment
- **Distributions**: 
  - Kali Linux
  - Ubuntu
  - Debian
  - Fedora
  - Arch Linux

### 🪟 Windows Support: Proceed with Caution
- **Current Status**: Experimental
- **Recommended Approach**: 
  - Use Windows Subsystem for Linux (WSL)
  - Prefer native Linux installation

> [!WARNING]
> Windows support is not fully tested. Strong recommendation to use WSL or a Linux environment for optimal performance.

## 🔧 Dependencies Installation

### Linux Installation
```bash
# Kali/Debian/Ubuntu
sudo apt update && sudo apt install hashcat python3 python3-pip python3-termcolor pipx

# Fedora
sudo dnf install hashcat python3 python3-pip python3-termcolor python3-pipx

# Arch Linux/Manjaro
sudo pacman -S hashcat python python-pip python-termcolor python-pipx
```

### Windows Installation
1. Install [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install)
2. Follow Linux installation instructions within WSL


## 📦 Installation & Usage

### Install via pip
```bash
pipx install hashcrack-tool
```

> [!IMPORTANT]
> Ensure `~/.local/bin` is in your PATH variable.

### Running hashCrack
```bash
# Run hashCrack with hash file
hashcrack hashfile
```

### Upgrading
```bash
pipx upgrade hashcrack-tool
```

## 🛠 Optional Setup

### Download Default Wordlists
```bash
git clone https://github.com/ente0/hashcat-defaults
```

## 🎬 Demo Walkthrough
<p align="center">
  <video src="https://github.com/user-attachments/assets/bcfc0ecd-6cde-436d-87df-4fb2ed1d90d0" />
</p>
    
> [!TIP]
> Cracking results are automatically stored in `~/.hashCrack/logs/session/status.txt`

## 🎮 Menu Options

| Option | Description | Function |
|--------|-------------|----------|
| 1 (Mode 0) | Wordlist Crack | Dictionary-based attack |
| 2 (Mode 9) | Rule-based Crack | Advanced dictionary mutations |
| 3 (Mode 3) | Brute-Force Crack | Exhaustive password generation |
| 4 (Mode 6) | Hybrid Crack | Wordlist + mask attack |
| 0 | Clear Potfile | Reset previous cracking results |
| X | OS Menu Switch | Update OS-specific settings |
| Q | Quit | Exit the program |

### Example Hashcat Commands
```bash
# Wordlist Attack
hashcat -a 0 -m 400 example400.hash example.dict

# Wordlist with Rules
hashcat -a 0 -m 0 example0.hash example.dict -r best64.rule

# Brute-Force
hashcat -a 3 -m 0 example0.hash ?a?a?a?a?a?a

# Combination Attack
hashcat -a 1 -m 0 example0.hash example.dict example.dict
```

## 📚 Recommended Resources

#### Wordlists & Dictionaries
- 📖 [SecLists](https://github.com/danielmiessler/SecLists)
- 🌐 [WPA2 Wordlists](https://github.com/kennyn510/wpa2-wordlists)
- 🇮🇹 [Parole Italiane](https://github.com/napolux/paroleitaliane)

#### Hashcat Tools & Rules
- 🔧 [Hashcat Defaults](https://github.com/ente0v1/hashcat-defaults)
- 📏 [Hashcat Rules](https://github.com/Unic0rn28/hashcat-rules)

### 🎓 Learning Resources

#### WPA2 Handshake Capture
- [4-Way Handshake Guide](https://notes.networklessons.com/security-wpa-4-way-handshake)
- [Practical Attack Demonstration](https://www.youtube.com/watch?v=WfYxrLaqlN8)

#### Technical Documentation
- [Hashcat Wiki](https://hashcat.net/wiki/)
- [Radiotap Introduction](https://www.radiotap.org/)
- [Aircrack-ng Guide](https://wiki.aircrack-ng.org/doku.php?id=airodump-ng)

## 📝 License
Licensed under the project's original license. See LICENSE file for details.

## 🤝 Support and Contributions

- 🐛 [Report Issues](https://github.com/ente0/hashCrack/issues)
- 📧 Contact: [enteo.dev@protonmail.com](mailto:enteo.dev@protonmail.com)

> [!IMPORTANT]
> Always use these resources and tools responsibly and ethically. Respect legal and privacy boundaries.
