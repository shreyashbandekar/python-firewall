# 🛡️ Python Firewall

A lightweight Windows Firewall management utility written in Python for blocking, unblocking, checking, and auditing IP-based firewall rules.

**Current Version:** `v2.0`

---

## 📌 Overview

Python Firewall provides a simple command-line interface for managing selected Windows Defender Firewall rules through `netsh advfirewall`.

The tool is designed as a practical cybersecurity project for learning and demonstrating:

- Windows Firewall administration
- IP address validation
- Firewall rule management
- Python system administration
- Security-focused CLI design
- Event logging
- Automated testing
- GitHub Actions CI

The application only manages rules created with the `PYFW_BLOCK_` prefix.

---

## ✨ Features

- 🔒 Block IPv4 and IPv6 addresses
- 🔓 Unblock managed IP rules
- 🔎 Check IP blocking status
- 📋 List Python Firewall rules
- 📝 CSV event logging
- 🛑 Duplicate-rule protection
- ⚠️ Safe handling of missing rules
- ✅ IPv4 and IPv6 validation
- 🔐 Administrator privilege enforcement by Windows
- 🛡️ Safe `subprocess` argument handling without `shell=True`
- 🧪 Automated unit tests
- ⚙️ GitHub Actions CI

---

## 🖥️ CLI

```text
================================
       PYTHON FIREWALL
          v2.0
================================
1. Block IP
2. Unblock IP
3. Check IP Status
4. List Firewall Rules
5. View Event Logs
6. Exit
--------------------------------
Enter your choice:

```
## 🔒 Block an IP

Select option `1` and enter a valid IPv4 or IPv6 address.

    Enter your choice: 1
    Enter IP to block: 203.0.113.50

    [+] IP 203.0.113.50 blocked successfully.

The tool creates a managed Windows Firewall rule using the naming format:

`PYFW_BLOCK_<IP>`

For example:

`PYFW_BLOCK_203.0.113.50`

---

## 🔓 Unblock an IP

Select option `2`:

    Enter your choice: 2
    Enter IP to unblock: 203.0.113.50

    [-] IP 203.0.113.50 unblocked successfully.

If no matching managed rule exists, the tool reports that the IP is not currently blocked.

---

## 🔎 Check IP Status

Select option `3`:

    Enter your choice: 3
    Enter IP to check: 203.0.113.50

    [+] IP 203.0.113.50 is currently blocked.

The status check only considers firewall rules created by this tool.

## 📋 List Firewall Rules

Select option `4` to display firewall rules created by Python Firewall.

    Enter your choice: 4

    Python Firewall Rules
    ---------------------
    Rule Name: PYFW_BLOCK_203.0.113.50

Only rules using the `PYFW_BLOCK_` prefix are displayed.

---

## 📝 Event Logging

Select option `5` to view the local firewall event log.

    Enter your choice: 5

The tool records:

- Timestamp
- Action
- IP address
- Result status

Example:

    timestamp | action | ip | status
    2026-09-20 18:10:22 | BLOCK | 203.0.113.50 | SUCCESS
    2026-09-20 18:11:05 | CHECK | 203.0.113.50 | BLOCKED
    2026-09-20 18:12:14 | UNBLOCK | 203.0.113.50 | SUCCESS

The log is stored locally as:

`firewall_events.csv`

This file is ignored by Git and is not committed to the repository.

## ⚙️ How It Works

Python Firewall acts as a lightweight interface around Windows Defender Firewall.

The workflow is:

1. Validate the supplied IP address.
2. Generate a unique managed rule name using `PYFW_BLOCK_`.
3. Query Windows Firewall for an existing matching rule.
4. Create or remove the rule using `netsh advfirewall`.
5. Report the operation result.
6. Record the event in `firewall_events.csv`.

The tool uses Python `subprocess` module to execute Windows Firewall commands with explicit argument lists.

---

## 🛡️ Security Design

The project follows several basic security principles:

- Uses `ipaddress` for IP validation.
- Uses list-based `subprocess` arguments.
- Does not use `shell=True`.
- Only manages rules created with the `PYFW_BLOCK_` prefix.
- Handles duplicate rules safely.
- Handles missing rules safely.
- Records successful and failed operations.
- Relies on Windows for administrator privilege enforcement.
- Uses a local CSV file for event auditing.

The tool does not attempt to bypass Windows security controls or elevate privileges automatically.

## 👤 Administrator Privileges

Windows Defender Firewall requires administrator privileges for rule-management operations.

Run PowerShell or Command Prompt as **Administrator** before using the block and unblock functions.

Example:

    PS C:\Users\shrey\Desktop\Codes\python-firewall> python firewall.py

If the program is started without sufficient privileges, Windows may reject firewall rule changes with an elevation error.

Python Firewall does not attempt to bypass or automatically elevate Windows privileges.

---

## 🧰 Technologies

- **Python 3**
- **Windows Defender Firewall**
- **`netsh advfirewall`**
- **`ipaddress`**
- **`subprocess`**
- **CSV logging**
- **pytest**
- **GitHub Actions**

---

## 📋 Requirements

- Windows 10 or Windows 11
- Python 3.9+
- Administrator privileges for firewall rule changes
- PowerShell or Command Prompt

No third-party runtime packages are required.

## 🚀 Installation

Clone the repository:

    git clone https://github.com/shreyashbandekar/python-firewall.git

    cd python-firewall

Run the application:

    python firewall.py

Run the automated tests:

    python -m pytest -v

No additional runtime dependencies are required.

---

## 🧪 Testing

The project includes automated tests covering:

- IP address validation
- Blocking IP addresses
- Duplicate block handling
- Unblocking IP addresses
- Missing firewall rules
- IP status checks
- Firewall rule listing
- CSV event logging
- Missing log handling
- Safe subprocess command construction

Run:

    python -m pytest -v

The current test suite contains **13 automated tests**.

## 🔍 Manual Verification

The application was manually tested against a real Windows Defender Firewall environment.

Verified operations include:

- Application startup and exit
- Invalid IP rejection
- Checking an unblocked IP
- Blocking an IP with administrator privileges
- Checking a blocked IP
- Listing managed firewall rules
- Handling duplicate block requests
- Unblocking an IP
- Confirming an IP is no longer blocked
- Handling an unblock request when no rule exists
- Viewing generated event logs
- Handling an empty rule list

The test IP used during verification was:

`203.0.113.50`

This address belongs to the documentation-only TEST-NET-3 range and was used strictly for controlled testing.

## 📁 Project Structure

    python-firewall/
    ├── firewall.py
    ├── test_firewall.py
    ├── firewall_events.csv
    ├── README.md
    ├── FIREWALL_RESEARCH.md
    ├── LICENSE
    ├── .gitignore
    └── .github/
        └── workflows/
            └── python-ci.yml

`firewall_events.csv` is generated locally during use and is excluded from Git.

---

## 🔐 Security Considerations

This project is intended for defensive administration and cybersecurity learning.

Important considerations:

- Firewall changes affect the host system.
- Administrator privileges are required for rule changes.
- Incorrect firewall rules can affect network connectivity.
- Only use the tool on systems you own or are authorized to administer.
- The application does not bypass Windows security controls.
- Event logs are stored locally and may contain IP addresses.

## 📚 Research

A detailed technical research report for this project is available in:

`FIREWALL_RESEARCH.md`

The report covers:

- Windows Defender Firewall architecture
- Firewall profiles
- Inbound and outbound traffic
- Firewall rule behavior
- IP-based filtering
- Ports and protocols
- `netsh advfirewall`
- PowerShell firewall management
- Firewall logging
- Testing methodology
- Security considerations
- Python automation limitations

The research report is intended to provide the technical background behind the implementation and its security decisions.

---

## 🗺️ Roadmap

Future improvements may include:

- Better administrator privilege detection
- Rule export and import
- More detailed firewall rule inspection
- Additional logging options
- Improved CLI argument support
- Extended automated test coverage

These features are intentionally outside the current minimum scope.

## 🤝 Contributing

Contributions, improvements, and security-focused suggestions are welcome.

Before submitting changes:

1. Keep the implementation focused and readable.
2. Add or update automated tests where appropriate.
3. Verify the application on Windows.
4. Run the complete test suite.
5. Update the documentation when behavior changes.

---

## 📄 License

This project is licensed under the MIT License.

See the `LICENSE` file for the full license text.

## 🆘 Support

If you encounter an issue:

1. Check that Python is installed and available in your PATH.
2. Run the automated tests with `python -m pytest -v`.
3. Verify that PowerShell or Command Prompt is running with administrator privileges when modifying firewall rules.
4. Check the generated `firewall_events.csv` for operation results.
5. Open an issue in the GitHub repository with the relevant error message and environment details.

---

## 👨‍💻 Author

**Shreyash Bandekar**

Cybersecurity | SOC Analysis | Security Engineering

GitHub: `https://github.com/shreyashbandekar`

---

⭐ If this project was useful for learning Windows Firewall automation, consider starring the repository.

---
