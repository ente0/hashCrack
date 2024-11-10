import subprocess

interface = input("Interface: ")
mac = input("MAC: ")
channel = input("Channel: ")

subprocess.run(["sudo", "airodump-ng", "-w", "eapol", "--output-format", "pcap", "-c", channel, "--bssid", mac, interface])
