import subprocess
import sys
import os
import ctypes
from colorama import Fore, Style, init
from tqdm import tqdm
import getpass

# Initialize colorama
init()

def check_admin():
    """Check if the script is run as an administrator."""
    try:
        is_admin = os.name == 'nt' and ctypes.windll.shell32.IsUserAnAdmin() != 0
        if not is_admin:
            print(f"{Fore.RED}[x] This script must be run as an administrator!{Style.RESET_ALL}")
            sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}[x] Error checking admin rights: {e}{Style.RESET_ALL}")
        sys.exit(1)

def install_requirements():
    """Check and install required packages."""
    try:
        # Check and install colorama
        try:
            import colorama
        except ImportError:
            print(f"{Fore.YELLOW}[!] Installing colorama...{Style.RESET_ALL}")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'colorama'])
            print(f"{Fore.GREEN}[✓] Colorama installed.{Style.RESET_ALL}")

        # Check and install tqdm
        try:
            import tqdm
        except ImportError:
            print(f"{Fore.YELLOW}[!] Installing tqdm...{Style.RESET_ALL}")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tqdm'])
            print(f"{Fore.GREEN}[✓] Tqdm installed.{Style.RESET_ALL}")

        # Check if nmap is installed
        if os.name == 'nt':
            nmap_path = r"C:\Program Files (x86)\Nmap\nmap.exe"
            if not os.path.exists(nmap_path):
                print(f"{Fore.YELLOW}[!] Nmap not found. Installing Nmap...{Style.RESET_ALL}")
                subprocess.check_call(["winget", "install", "--id", "Insecure.Nmap", "--source", "winget"])
                print(f"{Fore.GREEN}[✓] Nmap installed at {nmap_path}.{Style.RESET_ALL}")
        else:
            # For Linux or macOS, check if nmap is installed
            result = subprocess.run(["which", "nmap"], capture_output=True, text=True)
            if not result.stdout.strip():
                print(f"{Fore.RED}[x] Nmap not found. Please install it manually.{Style.RESET_ALL}")
                sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}[x] An error occurred during installation: {e}{Style.RESET_ALL}")
        sys.exit(1)

def run_nmap(target_ip, ports):
    """Run nmap command with the provided target IP and ports."""
    try:
        command = f"nmap -p {ports} -T4 -A -v {target_ip}"
        print(f"{Fore.YELLOW}[~] Running command: {command}{Style.RESET_ALL}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"{Fore.RED}[x] Error running nmap: {result.stderr}{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}[x] An error occurred: {e}{Style.RESET_ALL}\n")
        return None

def check_ports(output):
    """Check if the scanned ports are open in the nmap output."""
    if "21/tcp open" in output or "22/tcp open" in output:
        return True
    return False

def test_ftp_sftp(website, ports, username, password):
    """Test FTP/SFTP connections based on open ports."""
    try:
        import paramiko
    except ImportError:
        print(f"{Fore.RED}[x] Paramiko module is required but not installed. Exiting.{Style.RESET_ALL}")
        sys.exit(1)

    # Test FTP (port 21)
    if "21/tcp open" in ports:
        try:
            print(f"{Fore.YELLOW}[21] Testing FTP {website} on port 21...{Style.RESET_ALL}")
            import ftplib
            ftp = ftplib.FTP()
            ftp.connect(website, 21)
            ftp.login(username, password)
            print(f"{Fore.GREEN}[!-FOUND-!] FTP Successful!{Style.RESET_ALL}")
            ftp.quit()
        except Exception as e:
            print(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")

    # Test SFTP (port 22)
    if "22/tcp open" in ports:
        if input(f"[!] Run SFTP Test for {website} [y/n]: ").strip().lower() == 'y':
            try:
                print(f"{Fore.YELLOW}[22] Testing SFTP {website} on port 22...{Style.RESET_ALL}")
                transport = paramiko.Transport((website, 22))
                transport.connect(username=username, password=password)
                sftp = paramiko.SFTPClient.from_transport(transport)
                print(f"{Fore.GREEN}[!-FOUND-!] SFTP Successful!{Style.RESET_ALL}")
                sftp.close()
                transport.close()
            except Exception as e:
                print(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")

def main():
    # Check if the script is run as an administrator
    check_admin()

    # Check and install requirements
    install_requirements()

    # Initialize variables
    websites_file = None
    ports = None
    username = None
    password = None

    while True:
        print(r"""
    /$$$$$$$$                           
    | $$_____/                           
    | $$     /$$$$$$  /$$   /$$ /$$   /$$
    | $$$$$ /$$__  $$|  $$ /$$/| $$  | $$
    | $$__/| $$  \ $$ \  $$$$/ | $$  | $$
    | $$   | $$  | $$  >$$  $$ | $$  | $$
    | $$   |  $$$$$$/ /$$/\  $$|  $$$$$$$
    |__/    \______/ |__/  \__/ \____  $$
                                /$$  | $$
                            |  $$$$$$/
                                \______/
        """)
        # Display options
        print(f"{Fore.CYAN}Select an option:{Style.RESET_ALL}")
        print(f"1. Set website file path/name")
        print(f"2. Set port for scanning")
        print(f"3. Set username for FTP/SFTP (optional)")
        print(f"4. Set password for FTP/SFTP (optional)")
        print(f"5. Run the scan")
        
        option = input(f"\n{Fore.YELLOW}Enter your choice (1-5): {Style.RESET_ALL}")

        if option == '1':
            websites_file = input("\nEnter website file path/name: ").strip()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif option == '2':
            ports = input("Enter ports for scanning (e.g., 21,22): ").strip()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif option == '3':
            username = input("Enter username for FTP/SFTP (optional): ").strip()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif option == '4':
            password = getpass.getpass("Enter password for FTP/SFTP (optional): ").strip()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif option == '5':
            if not websites_file:
                websites_file = input("\nEnter website file path/name: ").strip()
            if not ports:
                ports = input("Enter ports for scanning (e.g., 21,22): ").strip()

            if websites_file and ports:
                print("\nStarting scan...")
                try:
                    with open(websites_file, 'r') as file:
                        websites = file.readlines()

                    open_ports_websites = []

                    # Using tqdm to display a progress bar while scanning
                    for website in tqdm(websites, desc="Scanning Websites"):
                        website = website.strip()
                        if not website:
                            continue
                        print(f"\n{Fore.YELLOW}[!] Scanning {website}...{Style.RESET_ALL}")
                        nmap_output = run_nmap(website, ports)
                        if nmap_output and check_ports(nmap_output):
                            open_ports_websites.append(website)
                            print(f"{Fore.GREEN}[!-Found-!] Port {ports} open on {website}{Style.RESET_ALL}")
                            if username or password:
                                test_ftp_sftp(website, nmap_output, username, password)
                        else:
                            print(f"{Fore.RED}[x] No open ports found on {website}{Style.RESET_ALL}")

                    if open_ports_websites:
                        print(f"{Fore.GREEN}[✓] Open ports found on the following websites:{Style.RESET_ALL}")
                        for site in open_ports_websites:
                            print(f" - {site}")
                    else:
                        print(f"{Fore.RED}[x] No open ports found on any websites.{Style.RESET_ALL}")

                except Exception as e:
                    print(f"{Fore.RED}[x] An error occurred: {e}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[x] Please set the website file path and ports before running the scan.{Style.RESET_ALL}")

            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print(f"{Fore.RED}[x] Invalid option. Please enter a number between 1 and 5.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
