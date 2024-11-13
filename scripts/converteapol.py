import os
import subprocess
import sys

print("\n".join(os.listdir(".")))

capture = input("Capture file: ").strip()

if not os.path.isfile(capture):
    print(f"Error: Capture file '{capture}' not found.")
    sys.exit(1)

try:
    subprocess.run(["hcxpcapngtool", "-o", "hash.hc22000", "-E", "essidlist", capture], check=True)
except subprocess.CalledProcessError:
    print("Error: hcxpcapngtool failed to process the capture file.")
    sys.exit(1)

if not os.path.isfile("essidlist"):
    print("Error: Failed to generate 'essidlist' file.")
    sys.exit(1)

with open("essidlist", "r") as f:
    ssid = f.read().strip()

os.makedirs(ssid, exist_ok=True)

os.rename("hash.hc22000", os.path.join(ssid, "hash.hc22000"))
os.rename("essidlist", os.path.join(ssid, "essidlist"))

print(f"Conversion completed successfully. Output stored in: {ssid}/")
