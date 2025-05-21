<p align="center">
  <img src="https://github.com/user-attachments/assets/0c5fcac9-f8d7-4a7b-be44-b0b8757df9a5"/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/ente0/hashCrack" alt="License">
  <img src="https://img.shields.io/badge/language-python-green" alt="Language: Python">
  <img src="https://img.shields.io/badge/dependencies-hashcat-blue" alt="Dependencies">
  <img src="https://img.shields.io/badge/release-v1.4.17-green" alt="Version">
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
> [!IMPORTANT]
> Check out which is the exact format of your hash in order to input the correct hashmode and preventing errors. These are all the hash examples: [Hashcat Wiki](https://hashcat.net/wiki/doku.php?id=example_hashes).

### Upgrading
```bash
pipx upgrade hashcrack-tool
```

## 🛠 Optional Setup

### Download Default Wordlists
```bash
git clone https://github.com/ente0/hashcat-defaults
```
Sure! Here's the **translated explanation in English** and a **cleaned-up instruction** for how to handle `$pkzip$` hashes in Hashcat:

---

### 🔧 How to Clean the Hash Format for Hashcat

If you want to crack a zip file use the following command:
> ```bash
> zip2john filename.zip > hash.txt
> ```


If you're using Hashcat with a ZIP archive hash (e.g. `$pkzip$`), make sure to **clean the hash line** correctly before use. Here's what to do:

#### ✅ **Clean the Hash Line**

From your `hash.txt`, **remove**:

* The initial filename prefix (e.g., `backup.zip:`)
* The trailing file names (after `::`), like:

  ```
  ::backup.zip:style.css, index.php:backup.zip
  ```

So, for example, given this original line:

```
backup.zip:$pkzip$2*1*1*...*$/pkzip$::backup.zip:style.css, index.php:backup.zip
```

It should be cleaned to:

```
$pkzip$2*1*1*...*$/pkzip$
```

This format ensures that Hashcat can parse the hash correctly since the "signature" (`$pkzip$`) is correct.

### 📌 Hashcat Modes for ZIP Archives

Hashcat supports different modes for ZIP archives depending on the encryption and structure. Here’s what to use:


| Hashcat Mode | Format Example                                      | Description                                                    |
| ------------ | --------------------------------------------------- | -------------------------------------------------------------- |
| `-m 13600`   | `$zip2$`                                            | WinZip legacy ZipCrypto encryption                             |
| `-m 17200`   | `$pkzip2$...*$/pkzip2$` (Compressed, single file)   | PKZIP archive, compressed single-file                          |
| `-m 17210`   | `$pkzip2$...*$/pkzip2$` (Uncompressed, single file) | PKZIP archive, uncompressed single-file                        |
| `-m 17220`   | `$pkzip2$3*...*$/pkzip2$`                           | PKZIP compressed **multi-file** archive ✅                      |
| `-m 17225`   | `$pkzip2$3*...*$/pkzip2$`                           | PKZIP **mixed** (compressed & uncompressed) multi-file archive |
| `-m 17230`   | `$pkzip2$8*...*$/pkzip2$`                           | PKZIP mixed multi-file (checksum-only entries)                 |


> 🔸 **Recommendation:**
> If your ZIP file contains more than one file inside (e.g., `style.css`, `index.php`), use:

```bash
-m 17220
```

## 🎬 Demo Walkthrough
<p align="center">
  <video src="https://github.com/user-attachments/assets/bcfc0ecd-6cde-436d-87df-4fb2ed1d90d0" />
</p>
    
> [!TIP]
> Cracking results are automatically stored in `~/.hashCrack/logs/session/status.txt`

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

This will perform a system benchmark. If it runs without errors, your Hashcat installation is likely working correctly.

5. **Segmentation Fault or Crashes**:

If you encounter a segmentation fault during execution, like the following error:

```
Counting lines in backup.zip. Please be patient...
[1] 633187 segmentation fault (core dumped)  hashcat --session=2025-05-21_2 -m 17220 backup.zip -a 0 -w 3 -o ...
```

This may be due to a **bug or compatibility issue in newer versions** of Hashcat. In such cases, try downgrading to an earlier stable version, such as **Hashcat 6.1.1**, which has resolved similar issues for others.

You can find relevant discussion and workaround suggestions in this thread:
🔗 [https://hashcat.net/forum/thread-9467.html](https://hashcat.net/forum/thread-9467.html)

To download Hashcat 6.1.1:

```bash
wget https://github.com/hashcat/hashcat/releases/download/v6.1.1/hashcat-6.1.1.7z
sudo apt install p7zip-full
7z x hashcat-6.1.1.7z
sudo mv hashcat-6.1.1 /opt/hashcat-6.1.1
sudo ln -s /opt/hashcat-6.1.1/hashcat.bin /usr/local/bin/hashcat
sudo rm hashcat-6.1.1.7z
```

---

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
## Supported Hash Modes

| ID | Hash-name | Example |
|----|------|-----------|
| 900 | MD4 | Raw Hash |
| 0 | MD5 | Raw Hash |
| 100 | SHA1 | Raw Hash |
| 1300 | SHA2-224 | Raw Hash |
| 1400 | SHA2-256 | Raw Hash |
| 10800 | SHA2-384 | Raw Hash |
| 1700 | SHA2-512 | Raw Hash |
| 17300 | SHA3-224 | Raw Hash |
| 17400 | SHA3-256 | Raw Hash |
| 17500 | SHA3-384 | Raw Hash |
| 17600 | SHA3-512 | Raw Hash |
| 6000 | RIPEMD-160 | Raw Hash |
| 600 | BLAKE2b-512 | Raw Hash |
| 11700 | GOST R 34.11-2012 (Streebog) 256-bit, big-endian | Raw Hash |
| 11800 | GOST R 34.11-2012 (Streebog) 512-bit, big-endian | Raw Hash |
| 6900 | GOST R 34.11-94 | Raw Hash |
| 17010 | GPG (AES-128/AES-256 (SHA-1($pass))) | Raw Hash |
| 5100 | Half MD5 | Raw Hash |
| 17700 | Keccak-224 | Raw Hash |
| 17800 | Keccak-256 | Raw Hash |
| 17900 | Keccak-384 | Raw Hash |
| 18000 | Keccak-512 | Raw Hash |
| 6100 | Whirlpool | Raw Hash |
| 10100 | SipHash | Raw Hash |
| 70 | md5(utf16le($pass)) | Raw Hash |
| 170 | sha1(utf16le($pass)) | Raw Hash |
| 1470 | sha256(utf16le($pass)) | Raw Hash |
| 10870 | sha384(utf16le($pass)) | Raw Hash |
| 1770 | sha512(utf16le($pass)) | Raw Hash |
| 610 | BLAKE2b-512($pass.$salt) | Raw Hash salted and/or iterated |
| 620 | BLAKE2b-512($salt.$pass) | Raw Hash salted and/or iterated |
| 10 | md5($pass.$salt) | Raw Hash salted and/or iterated |
| 20 | md5($salt.$pass) | Raw Hash salted and/or iterated |
| 3800 | md5($salt.$pass.$salt) | Raw Hash salted and/or iterated |
| 3710 | md5($salt.md5($pass)) | Raw Hash salted and/or iterated |
| 4110 | md5($salt.md5($pass.$salt)) | Raw Hash salted and/or iterated |
| 4010 | md5($salt.md5($salt.$pass)) | Raw Hash salted and/or iterated |
| 21300 | md5($salt.sha1($salt.$pass)) | Raw Hash salted and/or iterated |
| 40 | md5($salt.utf16le($pass)) | Raw Hash salted and/or iterated |
| 2600 | md5(md5($pass)) | Raw Hash salted and/or iterated |
| 3910 | md5(md5($pass).md5($salt)) | Raw Hash salted and/or iterated |
| 3500 | md5(md5(md5($pass))) | Raw Hash salted and/or iterated |
| 4400 | md5(sha1($pass)) | Raw Hash salted and/or iterated |
| 4410 | md5(sha1($pass).$salt) | Raw Hash salted and/or iterated |
| 20900 | md5(sha1($pass).md5($pass).sha1($pass)) | Raw Hash salted and/or iterated |
| 21200 | md5(sha1($salt).md5($pass)) | Raw Hash salted and/or iterated |
| 4300 | md5(strtoupper(md5($pass))) | Raw Hash salted and/or iterated |
| 30 | md5(utf16le($pass).$salt) | Raw Hash salted and/or iterated |
| 110 | sha1($pass.$salt) | Raw Hash salted and/or iterated |
| 120 | sha1($salt.$pass) | Raw Hash salted and/or iterated |
| 4900 | sha1($salt.$pass.$salt) | Raw Hash salted and/or iterated |
| 4520 | sha1($salt.sha1($pass)) | Raw Hash salted and/or iterated |
| 24300 | sha1($salt.sha1($pass.$salt)) | Raw Hash salted and/or iterated |
| 140 | sha1($salt.utf16le($pass)) | Raw Hash salted and/or iterated |
| 19300 | sha1($salt1.$pass.$salt2) | Raw Hash salted and/or iterated |
| 14400 | sha1(CX) | Raw Hash salted and/or iterated |
| 4700 | sha1(md5($pass)) | Raw Hash salted and/or iterated |
| 4710 | sha1(md5($pass).$salt) | Raw Hash salted and/or iterated |
| 21100 | sha1(md5($pass.$salt)) | Raw Hash salted and/or iterated |
| 18500 | sha1(md5(md5($pass))) | Raw Hash salted and/or iterated |
| 4500 | sha1(sha1($pass)) | Raw Hash salted and/or iterated |
| 4510 | sha1(sha1($pass).$salt) | Raw Hash salted and/or iterated |
| 5000 | sha1(sha1($salt.$pass.$salt)) | Raw Hash salted and/or iterated |
| 130 | sha1(utf16le($pass).$salt) | Raw Hash salted and/or iterated |
| 1410 | sha256($pass.$salt) | Raw Hash salted and/or iterated |
| 1420 | sha256($salt.$pass) | Raw Hash salted and/or iterated |
| 22300 | sha256($salt.$pass.$salt) | Raw Hash salted and/or iterated |
| 20720 | sha256($salt.sha256($pass)) | Raw Hash salted and/or iterated |
| 21420 | sha256($salt.sha256_bin($pass)) | Raw Hash salted and/or iterated |
| 1440 | sha256($salt.utf16le($pass)) | Raw Hash salted and/or iterated |
| 20800 | sha256(md5($pass)) | Raw Hash salted and/or iterated |
| 20710 | sha256(sha256($pass).$salt) | Raw Hash salted and/or iterated |
| 21400 | sha256(sha256_bin($pass)) | Raw Hash salted and/or iterated |
| 1430 | sha256(utf16le($pass).$salt) | Raw Hash salted and/or iterated |
| 10810 | sha384($pass.$salt) | Raw Hash salted and/or iterated |
| 10820 | sha384($salt.$pass) | Raw Hash salted and/or iterated |
| 10840 | sha384($salt.utf16le($pass)) | Raw Hash salted and/or iterated |
| 10830 | sha384(utf16le($pass).$salt) | Raw Hash salted and/or iterated |
| 1710 | sha512($pass.$salt) | Raw Hash salted and/or iterated |
| 1720 | sha512($salt.$pass) | Raw Hash salted and/or iterated |
| 1740 | sha512($salt.utf16le($pass)) | Raw Hash salted and/or iterated |
| 1730 | sha512(utf16le($pass).$salt) | Raw Hash salted and/or iterated |
| 50 | HMAC-MD5 (key = $pass) | Raw Hash authenticated |
| 60 | HMAC-MD5 (key = $salt) | Raw Hash authenticated |
| 150 | HMAC-SHA1 (key = $pass) | Raw Hash authenticated |
| 160 | HMAC-SHA1 (key = $salt) | Raw Hash authenticated |
| 1450 | HMAC-SHA256 (key = $pass) | Raw Hash authenticated |
| 1460 | HMAC-SHA256 (key = $salt) | Raw Hash authenticated |
| 1750 | HMAC-SHA512 (key = $pass) | Raw Hash authenticated |
| 1760 | HMAC-SHA512 (key = $salt) | Raw Hash authenticated |
| 11750 | HMAC-Streebog-256 (key = $pass), big-endian | Raw Hash authenticated |
| 11760 | HMAC-Streebog-256 (key = $salt), big-endian | Raw Hash authenticated |
| 11850 | HMAC-Streebog-512 (key = $pass), big-endian | Raw Hash authenticated |
| 11860 | HMAC-Streebog-512 (key = $salt), big-endian | Raw Hash authenticated |
| 28700 | Amazon AWS4-HMAC-SHA256 | Raw Hash authenticated |
| 11500 | CRC32 | Raw Checksum |
| 27900 | CRC32C | Raw Checksum |
| 28000 | CRC64Jones | Raw Checksum |
| 18700 | Java Object hashCode() | Raw Checksum |
| 25700 | MurmurHash | Raw Checksum |
| 27800 | MurmurHash3 | Raw Checksum |
| 14100 | 3DES (PT = $salt, key = $pass) | Raw Cipher, Known-plaintext attack |
| 14000 | DES (PT = $salt, key = $pass) | Raw Cipher, Known-plaintext attack |
| 26401 | AES-128-ECB NOKDF (PT = $salt, key = $pass) | Raw Cipher, Known-plaintext attack |
| 26402 | AES-192-ECB NOKDF (PT = $salt, key = $pass) | Raw Cipher, Known-plaintext attack |
| 26403 | AES-256-ECB NOKDF (PT = $salt, key = $pass) | Raw Cipher, Known-plaintext attack |
| 15400 | ChaCha20 | Raw Cipher, Known-plaintext attack |
| 14500 | Linux Kernel Crypto API (2.4) | Raw Cipher, Known-plaintext attack |
| 14900 | Skip32 (PT = $salt, key = $pass) | Raw Cipher, Known-plaintext attack |
| 11900 | PBKDF2-HMAC-MD5 | Generic KDF |
| 12000 | PBKDF2-HMAC-SHA1 | Generic KDF |
| 10900 | PBKDF2-HMAC-SHA256 | Generic KDF |
| 12100 | PBKDF2-HMAC-SHA512 | Generic KDF |
| 8900 | scrypt | Generic KDF |
| 400 | phpass | Generic KDF |
| 16100 | TACACS+ | Network Protocol |
| 11400 | SIP digest authentication (MD5) | Network Protocol |
| 5300 | IKE-PSK MD5 | Network Protocol |
| 5400 | IKE-PSK SHA1 | Network Protocol |
| 25100 | SNMPv3 HMAC-MD5-96 | Network Protocol |
| 25000 | SNMPv3 HMAC-MD5-96/HMAC-SHA1-96 | Network Protocol |
| 25200 | SNMPv3 HMAC-SHA1-96 | Network Protocol |
| 26700 | SNMPv3 HMAC-SHA224-128 | Network Protocol |
| 26800 | SNMPv3 HMAC-SHA256-192 | Network Protocol |
| 26900 | SNMPv3 HMAC-SHA384-256 | Network Protocol |
| 27300 | SNMPv3 HMAC-SHA512-384 | Network Protocol |
| 2500 | WPA-EAPOL-PBKDF2 | Network Protocol |
| 2501 | WPA-EAPOL-PMK | Network Protocol |
| 22000 | WPA-PBKDF2-PMKID+EAPOL | Network Protocol |
| 22001 | WPA-PMK-PMKID+EAPOL | Network Protocol |
| 16800 | WPA-PMKID-PBKDF2 | Network Protocol |
| 16801 | WPA-PMKID-PMK | Network Protocol |
| 7300 | IPMI2 RAKP HMAC-SHA1 | Network Protocol |
| 10200 | CRAM-MD5 | Network Protocol |
| 16500 | JWT (JSON Web Token) | Network Protocol |
| 29200 | Radmin3 | Network Protocol |
| 19600 | Kerberos 5, etype 17, TGS-REP | Network Protocol |
| 19800 | Kerberos 5, etype 17, Pre-Auth | Network Protocol |
| 28800 | Kerberos 5, etype 17, DB | Network Protocol |
| 19700 | Kerberos 5, etype 18, TGS-REP | Network Protocol |
| 19900 | Kerberos 5, etype 18, Pre-Auth | Network Protocol |
| 28900 | Kerberos 5, etype 18, DB | Network Protocol |
| 7500 | Kerberos 5, etype 23, AS-REQ Pre-Auth | Network Protocol |
| 13100 | Kerberos 5, etype 23, TGS-REP | Network Protocol |
| 18200 | Kerberos 5, etype 23, AS-REP | Network Protocol |
| 5500 | NetNTLMv1 / NetNTLMv1+ESS | Network Protocol |
| 27000 | NetNTLMv1 / NetNTLMv1+ESS (NT) | Network Protocol |
| 5600 | NetNTLMv2 | Network Protocol |
| 27100 | NetNTLMv2 (NT) | Network Protocol |
| 29100 | Flask Session Cookie ($salt.$salt.$pass) | Network Protocol |
| 4800 | iSCSI CHAP authentication, MD5(CHAP) | Network Protocol |
| 8500 | RACF | Operating System |
| 6300 | AIX {smd5} | Operating System |
| 6700 | AIX {ssha1} | Operating System |
| 6400 | AIX {ssha256} | Operating System |
| 6500 | AIX {ssha512} | Operating System |
| 3000 | LM | Operating System |
| 19000 | QNX /etc/shadow (MD5) | Operating System |
| 19100 | QNX /etc/shadow (SHA256) | Operating System |
| 19200 | QNX /etc/shadow (SHA512) | Operating System |
| 15300 | DPAPI masterkey file v1 (context 1 and 2) | Operating System |
| 15310 | DPAPI masterkey file v1 (context 3) | Operating System |
| 15900 | DPAPI masterkey file v2 (context 1 and 2) | Operating System |
| 15910 | DPAPI masterkey file v2 (context 3) | Operating System |
| 7200 | GRUB 2 | Operating System |
| 12800 | MS-AzureSync PBKDF2-HMAC-SHA256 | Operating System |
| 12400 | BSDi Crypt, Extended DES | Operating System |
| 1000 | NTLM | Operating System |
| 9900 | Radmin2 | Operating System |
| 5800 | Samsung Android Password/PIN | Operating System |
| 28100 | Windows Hello PIN/Password | Operating System |
| 13800 | Windows Phone 8+ PIN/password | Operating System |
| 2410 | Cisco-ASA MD5 | Operating System |
| 9200 | Cisco-IOS $8$ (PBKDF2-SHA256) | Operating System |
| 9300 | Cisco-IOS $9$ (scrypt) | Operating System |
| 5700 | Cisco-IOS type 4 (SHA256) | Operating System |
| 2400 | Cisco-PIX MD5 | Operating System |
| 8100 | Citrix NetScaler (SHA1) | Operating System |
| 22200 | Citrix NetScaler (SHA512) | Operating System |
| 1100 | Domain Cached Credentials (DCC), MS Cache | Operating System |
| 2100 | Domain Cached Credentials 2 (DCC2), MS Cache 2 | Operating System |
| 7000 | FortiGate (FortiOS) | Operating System |
| 26300 | FortiGate256 (FortiOS256) | Operating System |
| 125 | ArubaOS | Operating System |
| 501 | Juniper IVE | Operating System |
| 22 | Juniper NetScreen/SSG (ScreenOS) | Operating System |
| 15100 | Juniper/NetBSD sha1crypt | Operating System |
| 26500 | iPhone passcode (UID key + System Keybag) | Operating System |
| 122 | macOS v10.4, macOS v10.5, macOS v10.6 | Operating System |
| 1722 | macOS v10.7 | Operating System |
| 7100 | macOS v10.8+ (PBKDF2-SHA512) | Operating System |
| 3200 | bcrypt $2*$, Blowfish (Unix) | Operating System |
| 500 | md5crypt, MD5 (Unix), Cisco-IOS $1$ (MD5) | Operating System |
| 1500 | descrypt, DES (Unix), Traditional DES | Operating System |
| 29000 | sha1($salt.sha1(utf16le($username).':'.utf16le($pass))) | Operating System |
| 7400 | sha256crypt $5$, SHA256 (Unix) | Operating System |
| 1800 | sha512crypt $6$, SHA512 (Unix) | Operating System |
| 24600 | SQLCipher | Database Server |
| 131 | MSSQL (2000) | Database Server |
| 132 | MSSQL (2005) | Database Server |
| 1731 | MSSQL (2012, 2014) | Database Server |
| 24100 | MongoDB ServerKey SCRAM-SHA-1 | Database Server |
| 24200 | MongoDB ServerKey SCRAM-SHA-256 | Database Server |
| 12 | PostgreSQL | Database Server |
| 11100 | PostgreSQL CRAM (MD5) | Database Server |
| 28600 | PostgreSQL SCRAM-SHA-256 | Database Server |
| 3100 | Oracle H: Type (Oracle 7+) | Database Server |
| 112 | Oracle S: Type (Oracle 11+) | Database Server |
| 12300 | Oracle T: Type (Oracle 12+) | Database Server |
| 7401 | MySQL $A$ (sha256crypt) | Database Server |
| 11200 | MySQL CRAM (SHA1) | Database Server |
| 200 | MySQL323 | Database Server |
| 300 | MySQL4.1/MySQL5 | Database Server |
| 8000 | Sybase ASE | Database Server |
| 8300 | DNSSEC (NSEC3) | FTP, HTTP, SMTP, LDAP Server |
| 25900 | KNX IP Secure - Device Authentication Code | FTP, HTTP, SMTP, LDAP Server |
| 16400 | CRAM-MD5 Dovecot | FTP, HTTP, SMTP, LDAP Server |
| 1411 | SSHA-256(Base64), LDAP {SSHA256} | FTP, HTTP, SMTP, LDAP Server |
| 1711 | SSHA-512(Base64), LDAP {SSHA512} | FTP, HTTP, SMTP, LDAP Server |
| 24900 | Dahua Authentication MD5 | FTP, HTTP, SMTP, LDAP Server |
| 10901 | RedHat 389-DS LDAP (PBKDF2-HMAC-SHA256) | FTP, HTTP, SMTP, LDAP Server |
| 15000 | FileZilla Server >= 0.9.55 | FTP, HTTP, SMTP, LDAP Server |
| 12600 | ColdFusion 10+ | FTP, HTTP, SMTP, LDAP Server |
| 1600 | Apache $apr1$ MD5, md5apr1, MD5 (APR) | FTP, HTTP, SMTP, LDAP Server |
| 141 | Episerver 6.x < .NET 4 | FTP, HTTP, SMTP, LDAP Server |
| 1441 | Episerver 6.x >= .NET 4 | FTP, HTTP, SMTP, LDAP Server |
| 1421 | hMailServer | FTP, HTTP, SMTP, LDAP Server |
| 101 | nsldap, SHA-1(Base64), Netscape LDAP SHA | FTP, HTTP, SMTP, LDAP Server |
| 111 | nsldaps, SSHA-1(Base64), Netscape LDAP SSHA | FTP, HTTP, SMTP, LDAP Server |
| 7700 | SAP CODVN B (BCODE) | Enterprise Application Software (EAS) |
| 7701 | SAP CODVN B (BCODE) from RFC_READ_TABLE | Enterprise Application Software (EAS) |
| 7800 | SAP CODVN F/G (PASSCODE) | Enterprise Application Software (EAS) |
| 7801 | SAP CODVN F/G (PASSCODE) from RFC_READ_TABLE | Enterprise Application Software (EAS) |
| 10300 | SAP CODVN H (PWDSALTEDHASH) iSSHA-1 | Enterprise Application Software (EAS) |
| 133 | PeopleSoft | Enterprise Application Software (EAS) |
| 13500 | PeopleSoft PS_TOKEN | Enterprise Application Software (EAS) |
| 21500 | SolarWinds Orion | Enterprise Application Software (EAS) |
| 21501 | SolarWinds Orion v2 | Enterprise Application Software (EAS) |
| 24 | SolarWinds Serv-U | Enterprise Application Software (EAS) |
| 8600 | Lotus Notes/Domino 5 | Enterprise Application Software (EAS) |
| 8700 | Lotus Notes/Domino 6 | Enterprise Application Software (EAS) |
| 9100 | Lotus Notes/Domino 8 | Enterprise Application Software (EAS) |
| 26200 | OpenEdge Progress Encode | Enterprise Application Software (EAS) |
| 20600 | Oracle Transportation Management (SHA256) | Enterprise Application Software (EAS) |
| 4711 | Huawei sha1(md5($pass).$salt) | Enterprise Application Software (EAS) |
| 20711 | AuthMe sha256 | Enterprise Application Software (EAS) |
| 22400 | AES Crypt (SHA256) | Full-Disk Encryption (FDE) |
| 27400 | VMware VMX (PBKDF2-HMAC-SHA1 + AES-256-CBC) | Full-Disk Encryption (FDE) |
| 14600 | LUKS v1 (legacy) | Full-Disk Encryption (FDE) |
| 29541 | LUKS v1 RIPEMD-160 + AES | Full-Disk Encryption (FDE) |
| 29542 | LUKS v1 RIPEMD-160 + Serpent | Full-Disk Encryption (FDE) |
| 29543 | LUKS v1 RIPEMD-160 + Twofish | Full-Disk Encryption (FDE) |
| 29511 | LUKS v1 SHA-1 + AES | Full-Disk Encryption (FDE) |
| 29512 | LUKS v1 SHA-1 + Serpent | Full-Disk Encryption (FDE) |
| 29513 | LUKS v1 SHA-1 + Twofish | Full-Disk Encryption (FDE) |
| 29521 | LUKS v1 SHA-256 + AES | Full-Disk Encryption (FDE) |
| 29522 | LUKS v1 SHA-256 + Serpent | Full-Disk Encryption (FDE) |
| 29523 | LUKS v1 SHA-256 + Twofish | Full-Disk Encryption (FDE) |
| 29531 | LUKS v1 SHA-512 + AES | Full-Disk Encryption (FDE) |
| 29532 | LUKS v1 SHA-512 + Serpent | Full-Disk Encryption (FDE) |
| 29533 | LUKS v1 SHA-512 + Twofish | Full-Disk Encryption (FDE) |
| 13711 | VeraCrypt RIPEMD160 + XTS 512 bit (legacy) | Full-Disk Encryption (FDE) |
| 13712 | VeraCrypt RIPEMD160 + XTS 1024 bit (legacy) | Full-Disk Encryption (FDE) |
| 13713 | VeraCrypt RIPEMD160 + XTS 1536 bit (legacy) | Full-Disk Encryption (FDE) |
| 13741 | VeraCrypt RIPEMD160 + XTS 512 bit + boot-mode (legacy) | Full-Disk Encryption (FDE) |
| 13742 | VeraCrypt RIPEMD160 + XTS 1024 bit + boot-mode (legacy) | Full-Disk Encryption (FDE) |
| 13743 | VeraCrypt RIPEMD160 + XTS 1536 bit + boot-mode (legacy) | Full-Disk Encryption (FDE) |
| 29411 | VeraCrypt RIPEMD160 + XTS 512 bit | Full-Disk Encryption (FDE) |
| 29412 | VeraCrypt RIPEMD160 + XTS 1024 bit | Full-Disk Encryption (FDE) |
| 29413 | VeraCrypt RIPEMD160 + XTS 1536 bit | Full-Disk Encryption (FDE) |
| 29441 | VeraCrypt RIPEMD160 + XTS 512 bit + boot-mode | Full-Disk Encryption (FDE) |
| 29442 | VeraCrypt RIPEMD160 + XTS 1024 bit + boot-mode | Full-Disk Encryption (FDE) |
| 29443 | VeraCrypt RIPEMD160 + XTS 1536 bit + boot-mode | Full-Disk Encryption (FDE) |
| 13751 | VeraCrypt SHA256 + XTS 512 bit (legacy) | Full-Disk Encryption (FDE) |
| 13752 | VeraCrypt SHA256 + XTS 1024 bit (legacy) | Full-Disk Encryption (FDE) |
| 13753 | VeraCrypt SHA256 + XTS 1536 bit (legacy) | Full-Disk Encryption (FDE) |
| 13761 | VeraCrypt SHA256 + XTS 512 bit + boot-mode (legacy) | Full-Disk Encryption (FDE) |
| 13762 | VeraCrypt SHA256 + XTS 1024 bit + boot-mode (legacy) | Full-Disk Encryption (FDE) |
| 13763 | VeraCrypt SHA256 + XTS 1536 bit + boot-mode (legacy) | Full-Disk Encryption (FDE) |
| 29451 | VeraCrypt SHA256 + XTS 512 bit | Full-Disk Encryption (FDE) |
| 29452 | VeraCrypt SHA256 + XTS 1024 bit | Full-Disk Encryption (FDE) |
| 29453 | VeraCrypt SHA256 + XTS 1536 bit | Full-Disk Encryption (FDE) |
| 29461 | VeraCrypt SHA256 + XTS 512 bit + boot-mode | Full-Disk Encryption (FDE) |
| 29462 | VeraCrypt SHA256 + XTS 1024 bit + boot-mode | Full-Disk Encryption (FDE) |
| 29463 | VeraCrypt SHA256 + XTS 1536 bit + boot-mode | Full-Disk Encryption (FDE) |
| 13721 | VeraCrypt SHA512 + XTS 512 bit (legacy) | Full-Disk Encryption (FDE) |
| 13722 | VeraCrypt SHA512 + XTS 1024 bit (legacy) | Full-Disk Encryption (FDE) |
| 13723 | VeraCrypt SHA512 + XTS 1536 bit (legacy) | Full-Disk Encryption (FDE) |
| 29421 | VeraCrypt SHA512 + XTS 512 bit | Full-Disk Encryption (FDE) |
| 29422 | VeraCrypt SHA512 + XTS 1024 bit | Full-Disk Encryption (FDE) |
| 29423 | VeraCrypt SHA512 + XTS 1536 bit | Full-Disk Encryption (FDE) |
| 13771 | VeraCrypt Streebog-512 + XTS 512 bit (legacy) | Full-Disk Encryption (FDE) |
| 13772 | VeraCrypt Streebog-512 + XTS 1024 bit (legacy) | Full-Disk Encryption (FDE) |
| 13773 | VeraCrypt Streebog-512 + XTS 1536 bit (legacy) | Full-Disk Encryption (FDE) |
| 13781 | VeraCrypt Streebog-512 + XTS 512 bit + boot-mode (legacy) | Full-Disk Encryption (FDE) |
| 13782 | VeraCrypt Streebog-512 + XTS 1024 bit + boot-mode (legacy) | Full-Disk Encryption (FDE) |
| 13783 | VeraCrypt Streebog-512 + XTS 1536 bit + boot-mode (legacy) | Full-Disk Encryption (FDE) |
| 29471 | VeraCrypt Streebog-512 + XTS 512 bit | Full-Disk Encryption (FDE) |
| 29472 | VeraCrypt Streebog-512 + XTS 1024 bit | Full-
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
