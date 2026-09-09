import subprocess
import ipaddress


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
    else:
        print(f"[!] Failed to block IP {ip}.")
        print(result.stdout.strip())
    
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
    else:
        print(f"[!] Failed to unblock IP {ip}.")


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