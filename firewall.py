import csv
import ipaddress
import subprocess
from datetime import datetime

RULE_PREFIX = "PYFW_BLOCK_"
LOG_FILE = "firewall_events.csv"


def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def run_netsh(args):
    return subprocess.run(
        ["netsh", "advfirewall", "firewall", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def log_csv_event(action, ip, status):
    file_exists = False

    try:
        with open(LOG_FILE, "r", newline="", encoding="utf-8"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        if not file_exists:
            writer.writerow(["timestamp", "action", "ip", "status"])

        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                action,
                ip,
                status,
            ]
        )


def view_logs():
    try:
        with open(LOG_FILE, "r", newline="", encoding="utf-8") as csv_file:
            for row in csv.reader(csv_file):
                print(" | ".join(row))
    except FileNotFoundError:
        print("[!] No firewall event log found.")


def block_ip(ip):
    rule_name = f"{RULE_PREFIX}{ip}"

    check = run_netsh(
        ["show", "rule", f"name={rule_name}"]
    )

    if "No rules match" not in check.stdout:
        print(f"[!] IP {ip} is already blocked.")
        log_csv_event("BLOCK", ip, "ALREADY_BLOCKED")
        return "ALREADY_BLOCKED"

    result = run_netsh(
        [
            "add",
            "rule",
            f"name={rule_name}",
            "dir=in",
            "action=block",
            f"remoteip={ip}",
        ]
    )

    if result.returncode == 0:
        print(f"[+] IP {ip} blocked successfully.")
        log_csv_event("BLOCK", ip, "SUCCESS")
        return "SUCCESS"

    print(f"[!] Failed to block IP {ip}.")
    if result.stderr.strip():
        print(result.stderr.strip())
    log_csv_event("BLOCK", ip, "FAILED")
    return "FAILED"


def unblock_ip(ip):
    rule_name = f"{RULE_PREFIX}{ip}"

    result = run_netsh(
        ["delete", "rule", f"name={rule_name}"]
    )

    if "No rules match" in result.stdout:
        print(f"[!] No firewall rule found for IP {ip}.")
        log_csv_event("UNBLOCK", ip, "NOT_BLOCKED")
        return "NOT_BLOCKED"

    if result.returncode == 0:
        print(f"[-] IP {ip} unblocked successfully.")
        log_csv_event("UNBLOCK", ip, "SUCCESS")
        return "SUCCESS"

    print(f"[!] Failed to unblock IP {ip}.")
    if result.stderr.strip():
        print(result.stderr.strip())
    log_csv_event("UNBLOCK", ip, "FAILED")
    return "FAILED"


def check_ip(ip):
    rule_name = f"{RULE_PREFIX}{ip}"

    result = run_netsh(
        ["show", "rule", f"name={rule_name}"]
    )

    if "No rules match" in result.stdout:
        print(f"[-] IP {ip} is not blocked.")
        log_csv_event("CHECK", ip, "NOT_BLOCKED")
        return "NOT_BLOCKED"

    print(f"[+] IP {ip} is currently blocked.")
    log_csv_event("CHECK", ip, "BLOCKED")
    return "BLOCKED"


def list_rules():
    result = run_netsh(["show", "rule", "name=all"])

    if result.returncode != 0:
        print("[!] Failed to retrieve firewall rules.")
        return

    lines = result.stdout.splitlines()
    rules = []

    for line in lines:
        line = line.strip()
        if line.startswith("Rule Name:") and RULE_PREFIX in line:
            rules.append(line)

    if not rules:
        print("[!] No Python Firewall rules found.")
        return

    print("\nPython Firewall Rules")
    print("---------------------")
    for rule in rules:
        print(rule)


def get_ip(prompt):
    ip = input(prompt).strip()

    if not is_valid_ip(ip):
        print("[!] Invalid IP address.")
        return None

    return ip


def main():
    while True:
        print("\n================================")
        print("       PYTHON FIREWALL")
        print("          v2.0")
        print("================================")
        print("1. Block IP")
        print("2. Unblock IP")
        print("3. Check IP Status")
        print("4. List Firewall Rules")
        print("5. View Event Logs")
        print("6. Exit")
        print("--------------------------------")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            ip = get_ip("Enter IP to block: ")
            if ip:
                block_ip(ip)

        elif choice == "2":
            ip = get_ip("Enter IP to unblock: ")
            if ip:
                unblock_ip(ip)

        elif choice == "3":
            ip = get_ip("Enter IP to check: ")
            if ip:
                check_ip(ip)

        elif choice == "4":
            list_rules()

        elif choice == "5":
            view_logs()

        elif choice == "6":
            print("\n[+] Exiting Python Firewall...")
            break

        else:
            print(f"[!] Invalid choice: {choice}")


if __name__ == "__main__":
    main()
