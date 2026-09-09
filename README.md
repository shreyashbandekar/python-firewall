# 🛡️ Python Firewall

A lightweight Python-based Windows Firewall management tool for blocking, unblocking, and checking the status of IP addresses through the Windows Firewall.

**Current Version:** `v1.0`

---

## 📌 Overview

Python Firewall is a command-line security utility written in Python that provides a simple interface for managing Windows Firewall rules.

The application uses Python's `subprocess` module to interact with the Windows `netsh` firewall command and the `ipaddress` module to validate IP addresses before making firewall changes.

This project is designed as a practical cybersecurity project for learning and demonstrating:

- Windows Firewall administration
- Network security fundamentals
- IP address validation
- Firewall rule management
- Python system administration
- Command-line security tooling
- Git and GitHub workflows

---

## ✨ Features

- 🔒 Block an IP address
- 🔓 Unblock an IP address
- 🔎 Check IP blocking status
- ✅ IPv4 and IPv6 address validation
- 🛑 Prevent duplicate firewall rules
- ⚠️ Graceful handling of missing firewall rules
- 🖥️ Uses the native Windows Firewall
- 💻 Interactive command-line interface
- 🏷️ Consistent firewall rule naming
- 📝 Clear success and error messages

---

## 🏷️ Firewall Rule Naming

Firewall rules created by the application use the following naming convention:

`PYFW_BLOCK_<IP>`

Example:

`PYFW_BLOCK_203.0.113.50`

This makes rules created by the application easy to identify and manage.

---

## 🖥️ Application Menu

When the application starts, it displays:

    =================================
           PYTHON FIREWALL
              v1.0
    =================================
    --------------------------------
    1. Block IP
    2. Unblock IP
    3. Check IP Status
    4. Exit
    --------------------------------
    Enter your choice:

---

## 🔒 Block an IP

Select option `1` and provide the IP address you want to block.

Example:

    Enter your choice: 1
    Enter IP to block: 203.0.113.50

    [+] IP 203.0.113.50 blocked successfully.

The application creates a Windows Firewall rule named:

    PYFW_BLOCK_203.0.113.50

---

## 🔎 Check IP Status

Select option `3` to determine whether an IP is currently blocked by a firewall rule created by the application.

Example:

    Enter your choice: 3
    Enter IP to check: 203.0.113.50

    [+] IP 203.0.113.50 is currently blocked.

If the IP is not blocked:

    [-] IP 203.0.113.50 is not blocked.

---

## 🔓 Unblock an IP

Select option `2` to remove the firewall rule created for an IP.

Example:

    Enter your choice: 2
    Enter IP to unblock: 203.0.113.50

    [-] IP 203.0.113.50 unblocked successfully.

If no matching firewall rule exists:

    [!] No firewall rule found for IP 203.0.113.50.

---

## ⚙️ How It Works

The application follows a simple workflow:

    User
      │
      ▼
    Python CLI
      │
      ▼
    Validate IP Address
      │
      ▼
    Check Firewall Rule
      │
      ▼
    Windows Firewall
      │
      ▼
    netsh advfirewall
      │
      ▼
    Block / Unblock / Check

### Block Workflow

    User enters IP
          ↓
    Validate IP address
          ↓
    Check if rule already exists
          ↓
    Create firewall rule
          ↓
    Windows Firewall blocks inbound traffic

### Unblock Workflow

    User enters IP
          ↓
    Validate IP address
          ↓
    Find corresponding firewall rule
          ↓
    Delete firewall rule
          ↓
    Rule is removed

### Status Workflow

    User enters IP
          ↓
    Validate IP address
          ↓
    Search for corresponding firewall rule
          ↓
    Report current status

---

## 🧰 Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Application logic |
| `subprocess` | Execute Windows firewall commands |
| `ipaddress` | Validate IPv4 and IPv6 addresses |
| `netsh` | Interface with Windows Firewall |
| Windows Defender Firewall | Network traffic filtering |
| Git | Version control |
| GitHub | Source code hosting |

---

## 📋 Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- Administrator privileges
- Git (recommended for development)

Python:

https://www.python.org/

---

## 🚀 Installation

### Clone the Repository

    git clone https://github.com/shreyashbandekar/python-firewall.git

### Enter the Project Directory

    cd python-firewall

### Run the Application

Open PowerShell or VS Code as Administrator and run:

    python firewall.py

Administrator privileges are required because the application modifies Windows Firewall rules.

---

## 🔐 Administrator Privileges

Windows Firewall configuration requires elevated privileges.

If the application cannot create or delete firewall rules, make sure that:

- PowerShell is running as Administrator, or
- VS Code is running as Administrator.

The application does not modify Windows Firewall Group Policy settings.

---

## 🧪 Testing

The current version has been manually tested for:

- Valid IPv4 addresses
- Valid IPv6 addresses
- Invalid IP addresses
- Blocking an IP
- Blocking an already blocked IP
- Unblocking an IP
- Unblocking an IP with no existing rule
- Checking a blocked IP
- Checking an unblocked IP
- Invalid menu selections
- Exiting the application

Example test IP:

`203.0.113.50`

This address belongs to the documentation/example address space and is suitable for testing examples without targeting a real public host.

---

## 🔍 Verify Firewall Rules Manually

You can inspect a rule created by the application using:

    netsh advfirewall firewall show rule name="PYFW_BLOCK_203.0.113.50"

The command can be used to verify:

- Whether the rule exists
- Whether it is enabled
- Direction
- Profiles
- Remote IP address
- Action

---

## 📁 Project Structure

    python-firewall/
    │
    ├── firewall.py
    ├── README.md
    ├── .gitignore
    └── .git/

### Main Files

**`firewall.py`**

Contains the Python Firewall application.

**`README.md`**

Project documentation and usage instructions.

**`.gitignore`**

Prevents unnecessary Python, virtual environment, environment, and editor files from being committed.

---

## 🛡️ Security Considerations

This application directly modifies Windows Firewall configuration.

Only use this tool on systems that you own or are authorized to administer.

Incorrect firewall rules can:

- Block legitimate network traffic
- Disrupt applications
- Affect remote connectivity
- Prevent access to required services

Always verify firewall rules after making changes.

The project intentionally limits itself to firewall rules created using the `PYFW_BLOCK_<IP>` naming convention.

---

## 🎯 Learning Objectives

This project provides practical experience with several areas of cybersecurity and software development.

### Python

- Functions
- Loops
- Conditional statements
- Exception handling
- User input
- `subprocess`
- `ipaddress`

### Windows Security

- Windows Defender Firewall
- Firewall rules
- `netsh`
- Inbound traffic filtering
- Administrative privileges

### Development

- Git
- GitHub
- Version control
- Repository management
- Code organization
- Future CI automation

---

## 🗺️ Roadmap

The project will evolve through future versions.

### Planned Improvements

- [ ] Automated unit tests
- [ ] Firewall action logging
- [ ] Improved error handling
- [ ] Firewall rule listing
- [ ] Rule management and cleanup
- [ ] Configuration file support
- [ ] JSON-based logging
- [ ] Command-line arguments
- [ ] Enhanced IPv4/IPv6 handling
- [ ] GitHub Actions CI
- [ ] Automated code quality checks
- [ ] Security-focused test cases

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes
5. Commit your changes
6. Open a pull request

Please ensure that changes do not introduce unsafe or unauthorized firewall behavior.

---

## 📄 License

This project is currently intended as an educational and personal cybersecurity project.

A formal open-source license may be added in a future release.

---

## 👤 Author

**Shreyash Bandekar**

GitHub:

https://github.com/shreyashbandekar

---

## ⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

---

<div align="center">

**Python Firewall**

Built with Python 🐍 for Windows security 🛡️

</div>