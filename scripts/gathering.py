import subprocess

interface = input("Interface: ")

subprocess.run(["sudo", "airmon-ng", "check", "kill"])
subprocess.run(["sudo", "airodump-ng", interface])
