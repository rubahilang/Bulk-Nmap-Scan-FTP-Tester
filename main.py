import subprocess
import sys

def run_nmap(target_ip):
    try:
        # Run the nmap command with the given target IP
        command = f"nmap -p 21,22 -T4 -A -v {target_ip}"
        print(f"Running command: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"Error running nmap: {result.stderr}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def check_ports(output):
    # Check if ports 21 or 22 are open in the nmap output
    if "21/tcp open" in output or "22/tcp open" in output:
        return True
    return False

def main(websites_file):
    try:
        with open(websites_file, 'r') as file:
            websites = file.readlines()

        open_ports_websites = []

        for website in websites:
            website = website.strip()
            if not website:
                continue
            print(f"Scanning {website}...")
            nmap_output = run_nmap(website)
            if nmap_output and check_ports(nmap_output):
                open_ports_websites.append(website)
                print(f"Port 21 or 22 open on {website}")

        # Save results to a file
        with open("websites_with_open_ports.txt", 'w') as file:
            for website in open_ports_websites:
                file.write(f"{website}\n")

        print(f"Results saved to 'websites_with_open_ports.txt'")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <websites_file>")
        sys.exit(1)

    websites_file = sys.argv[1]
    main(websites_file)
