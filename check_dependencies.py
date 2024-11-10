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

def create_requirements_file():
    with open("requirements.txt", "w") as req_file:
        req_file.write("psutil\n")

    print("\nrequirements.txt has been created. You can install dependencies using:\n")
    print("pip install -r requirements.txt")

def main():
    print("Checking system dependencies...\n")
    
    check_dependency("hashcat", "Hashcat")
    check_dependency("aircrack-ng", "Aircrack-ng")
    check_dependency("hcxtools", "hcxtools")
    check_dependency("hcxdumptool", "hcxdumptool")
    
    create_requirements_file()

if __name__ == "__main__":
    main()
