import subprocess
import sys

def check_dependency(command, tool_name):
    try:
        result = subprocess.run(["which", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"{tool_name} is installed.")
        else:
            print(f"{tool_name} is NOT installed. Please install {tool_name}.")
    except FileNotFoundError:
        print(f"{tool_name} is NOT installed. Please install {tool_name}.")

def main():
    print("Checking system dependencies...\n")
    
    check_dependency("hashcat", "Hashcat")
    check_dependency("aircrack-ng", "Aircrack-ng")
    check_dependency("hcxtools", "hcxtools")
    check_dependency("hcxdumptool", "hcxdumptool")
    

if __name__ == "__main__":
    main()
