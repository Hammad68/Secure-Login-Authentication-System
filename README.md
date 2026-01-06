# Secure Login & Authentication System

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Security](https://img.shields.io/badge/Security-MFA%20%7C%20Bcrypt-green.svg)](#)

A robust terminal-based authentication system demonstrating secure credential handling, multi-factor authentication (MFA), and defensive programming. This project applies real-world security practices in a Python-based educational context.

---

## ⚡ Key Features

* **Secure Hashing:** Uses `bcrypt` with adaptive salting to prevent credential theft.
* **MFA Integration:** TOTP-based 2FA with QR code support for Google Authenticator.
* **Smart Security Policy:** Enforces high-entropy passwords and blocks common leaks.
* **Brute-Force Shield:** Automatic account lockouts and cooldown timers.
* **Audit Trails:** Complete logging of all login attempts and system changes.
* **Attack Simulation:** Built-in module for testing hash resilience against cracking.
---

## 📂 Project Structure

```text
.
├── components/          # Core auth and MFA logic
├── bruteforce/          # Protection and lockout mechanisms
├── auditing/            # Security event logging
├── attackSimulation/    # Offline cracking simulation tools
├── data/                # Local JSON storage (User DB)
├── qrcodes/             # Generated QR codes for MFA setup
├── verification.py      # MFA and credential verification logic
├── registration.py      # User onboarding and policy enforcement
├── accountControl.py    # Account management and status handling
├── Project_Logbook.pdf  # Development journey and documentation
├── requirements.txt     # List of dependencies
├── README.md            # Project documentation
└── main.py              # System entry point

```

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.x |
| **Hashing** | Bcrypt |
| **MFA/TOTP** | PyOTP / qrcode |
| **Storage** | JSON-based Local Storage |
| **Interface** | Terminal (CLI) |

---

## 🚀 Getting Started

### Installation
Ensure you have Python 3 installed, then clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the System
To launch the terminal interface, run:

```Bash
python main.py
```

## ⚖ Ethical Considerations
- All testing and simulations are performed locally on test accounts only.

- No real user data or external systems were involved in this project.

- The attack simulation exists purely for educational and defensive analysis.

## 👤 Author
- Hammad Ahmed 
- Computer Science Student 
- Focus: Secure Authentication & Software Security