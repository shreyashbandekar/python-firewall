import subprocess
import ipaddress
from datetime import datetime

def log_event(action, ip, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("firewall.log", "a") as log_file:
        log_file.write(f"{timestamp} | {action} | {ip} | {status}\n")




def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def block_ip(ip):
    rule_name = f"PYFW_BLOCK_{ip}"

    check_command = (
        f'netsh advfirewall firewall show rule '
        f'name="{rule_name}"'
    )

    check_result = subprocess.run(
        check_command,
        capture_output=True,
        text=True,
        shell=True
    )

    if "No rules match" not in check_result.stdout:
        print(f"[!] IP {ip} is already blocked.")
        return

    command = (
        f'netsh advfirewall firewall add rule '
        f'name="{rule_name}" '
        f'dir=in '
        f'action=block '
        f'remoteip={ip}'
    )

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        shell=True
    )

    if result.returncode == 0:
        print(f"[+] IP {ip} blocked successfully.")
        log_event("BLOCK", ip, "SUCCESS")
    else:
        print(f"[!] Failed to block IP {ip}.")
        print(result.stdout.strip())
        log_event("BLOCK", ip, "FAILED")
    
def unblock_ip(ip):
    rule_name = f"PYFW_BLOCK_{ip}"

    command = (
        f'netsh advfirewall firewall delete rule '
        f'name="{rule_name}"'
    )

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        shell=True
    )

    if "No rules match" in result.stdout:
        print(f"[!] No firewall rule found for IP {ip}.")
    elif result.returncode == 0:
        print(f"[-] IP {ip} unblocked successfully.")
        log_event("UNBLOCK", ip, "SUCCESS")
    else:
        print(f"[!] Failed to unblock IP {ip}.")
        log_event("UNBLOCK", ip, "FAILED")


def check_ip(ip):
    rule_name = f"PYFW_BLOCK_{ip}"

    command = (
        f'netsh advfirewall firewall show rule '
        f'name="{rule_name}"'
    )

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        shell=True
    )

    if "No rules match" in result.stdout:
        print(f"[-] IP {ip} is not blocked.")
    else:
        print(f"[+] IP {ip} is currently blocked.")
def main():
    while True:
        print("\n================================")
        print("       PYTHON FIREWALL")
        print("          v1.0")
        print("================================")
        print("--------------------------------")
        print("1. Block IP")
        print("2. Unblock IP")
        print("3. Check IP Status")
        print("4. Exit")
        print("--------------------------------")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            ip = input("Enter IP to block: ").strip()

            try:
                ipaddress.ip_address(ip)
                block_ip(ip)
            except ValueError:
                print("[!] Invalid IP address.")

        elif choice == "2":
            ip = input("Enter IP to unblock: ").strip()

            try:
                ipaddress.ip_address(ip)
                unblock_ip(ip)
            except ValueError:
                print("[!] Invalid IP address.")

        elif choice == "3":
            ip = input("Enter IP to check: ").strip()

            try:
                ipaddress.ip_address(ip)
                check_ip(ip)
            except ValueError:
                print("[!] Invalid IP address.")

        elif choice == "4":
            print("\n[+] Exiting Python Firewall...")
            break

        else:
            print(f"[!] Invalid choice: {choice}")

if __name__ == "__main__":
    main()