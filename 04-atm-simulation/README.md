
# 🏧 Digital ATM Simulation & Automated Teller Management System

A feature-rich, menu-driven Python CLI application that simulates real-world Automated Teller Machine operations, including secure PIN authentication, cash withdrawals, deposits, account transfers, transaction history, and automated receipt generation.

Part of the **10 Beginner Python Projects – First Semester Collection**, this project demonstrates practical applications of loops, conditional statements, functions, dictionaries, CSV file handling, exception handling, and basic cryptographic operations through an interactive banking simulation.

---

## 📌 Project Overview

An Automated Teller Machine (ATM) is a transaction-driven system that must maintain accurate account balances, validate customer authentication, manage cash availability, and record financial transactions.

This project simulates a multi-user digital banking terminal through an interactive console application.

Users can authenticate using a card number and PIN, withdraw and deposit money, transfer funds between accounts, view mini-statements, and generate transaction receipts.

The application also simulates ATM vault cash management, security lockouts, transaction validation, and persistent banking records using CSV and text files.

It is designed for educational purposes and demonstrates how fundamental Python programming concepts can be combined to create a practical financial management simulation.

---

## ✨ Features

### 🔐 Secure PIN Authentication

- **SHA-256 PIN Hashing:** Stores PIN credentials as SHA-256 hashes rather than plaintext PINs.
- **Card-Based Authentication:** Users access their accounts using a registered card number and PIN.
- **Three-Attempt Security Lockout:** Locks an account after three consecutive incorrect PIN attempts.
- **Persistent Account Status:** Maintains account security status across application sessions.
- **Session Management:** Separates authentication from active banking operations.

### 💵 Cash Withdrawal & Denomination Dispenser

- **Transaction Limits:** Enforces minimum withdrawals of PKR 500 and maximum withdrawals of PKR 50,000 per transaction.
- **Denomination Validation:** Accepts withdrawal amounts in multiples of PKR 500.
- **Automated Bill Calculation:** Calculates the required combination of PKR 5,000, PKR 1,000, and PKR 500 notes.
- **Vault Cash Verification:** Checks available ATM cash reserves before processing withdrawals.
- **Balance Validation:** Prevents withdrawals exceeding the available account balance.

### 💰 Automated Cash Deposits

- Allows customers to deposit money into their accounts.
- Updates account balances after successful deposits.
- Replenishes the simulated ATM physical cash vault.
- Maintains transaction records.

### 🔄 Peer-to-Peer Account Transfers

- Supports transfers between registered accounts.
- Validates sender and recipient account information.
- Updates both account balances.
- Prevents transfers exceeding the sender's available balance.

### 📊 Mini-Statement & Transaction History

- Tracks financial transactions across application sessions.
- Displays transaction types, amounts, timestamps, and account balances.
- Provides a tabular mini-statement for account activity.

### 🧾 Automated Receipt Generation

- Generates printable transaction receipts in `.txt` format.
- Assigns transaction identifiers.
- Masks card numbers in receipt output.
- Includes transaction timestamps and closing account balances.
- Saves receipts in a dedicated `receipts/` directory.

### 🛡️ Security & Audit Logging

- Records successful and failed authentication attempts.
- Logs account lockouts and banking activities.
- Tracks withdrawals, deposits, and transfers.
- Maintains chronological system activity records in `atm_audit_log.txt`.

### 💾 Persistent Account Database

- Stores account information in `atm_data/accounts_db.csv`.
- Maintains card numbers, account holder names, account types, balances, and security statuses.
- Automatically initializes demo accounts when required.
- Preserves account information between application sessions.

---

## 💳 Seeded Demo Accounts

On the first launch, the application initializes the following illustrative test accounts:

| Card Number | Account Holder | Default PIN | Initial Balance | Account Type |
|:---:|---|:---:|---:|:---:|
| **1001** | Ali Ahmed | `1234` | PKR 85,000.00 | Current |
| **1002** | Fatima Zahra | `4321` | PKR 142,000.00 | Savings |
| **1003** | Usman Tariq | `7890` | PKR 25,000.00 | Current |
| **1004** | Ayesha Khan | `0000` | PKR 500.00 | Savings |

> **Important:** These are demonstration accounts for educational testing only. The application is a banking simulation, not a production banking system.

---

## 📚 Python Concepts Demonstrated

This project demonstrates how fundamental Python programming concepts can be applied to a financial transaction system.

| Python Concept | Application |
|---|---|
| Variables & Data Types | Managing balances, PINs, and transaction amounts |
| User Input & Output | Interactive ATM interface |
| Conditional Statements | Authentication and transaction validation |
| While Loops | Continuous ATM operation and banking sessions |
| Functions | Modular transaction processing |
| Lists | Managing transaction histories and denominations |
| Dictionaries | Organizing account information |
| Nested Dictionaries | Managing structured banking records |
| File Handling | Persistent account and transaction storage |
| CSV Module | Maintaining customer account databases |
| Exception Handling | Handling invalid inputs and transaction errors |
| OS Module | Managing data and receipt directories |
| Hashlib Module | SHA-256 PIN hashing |
| DateTime Module | Generating transaction timestamps |
| String Formatting | Producing receipts and account statements |

---

## 💳 Transaction Rules & Limits

### Cash Withdrawal Rules

| Parameter | Limit |
|---|---:|
| Minimum Withdrawal | PKR 500 |
| Maximum Withdrawal | PKR 50,000 |
| Allowed Withdrawal Multiple | PKR 500 |
| Maximum Incorrect PIN Attempts | 3 |

### Supported Cash Denominations

| Note Denomination | Usage |
|---|---|
| PKR 5,000 | Large-value cash dispensing |
| PKR 1,000 | Medium-value cash dispensing |
| PKR 500 | Small-value cash dispensing |

### Security Rules

- Customers must provide a valid registered card number.
- PIN authentication is required before accessing banking services.
- Three consecutive incorrect PIN attempts trigger an account lockout.
- Locked accounts cannot access banking operations until reset.
- Transaction validation prevents invalid or unauthorized balance changes.

---

## 📂 Project Structure

```text id="c7m4px"
04-atm-simulation/
│
├── main.py                     # Main ATM application
├── README.md                   # Project documentation
│
├── atm_data/                   # Automatically created storage directory
│   ├── accounts_db.csv         # Account database and PIN hashes
│   └── atm_audit_log.txt       # Security and transaction logs
│
└── receipts/                   # Automatically created receipt directory
    ├── Receipt_TXN-1001.txt
    └── Receipt_TXN-1002.txt
```

**Note:** The `atm_data/` and `receipts/` directories and their files are generated automatically when the application performs relevant operations. They may not exist before the first execution.

---

## ⚙️ Getting Started

### 1. Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher.
- Visual Studio Code, PyCharm, or Python IDLE.
- A terminal or command prompt.

Verify your Python installation:

```bash id="g8pw2a"
python --version
```

### 2. Navigate to the Project Directory

If you have already cloned the main repository:

```bash id="k9mz1v"
cd python-fundamentals-projects/04-atm-simulation
```

### 3. Run the Application

Execute the Python script:

```bash id="e6qx9w"
python main.py
```

No external packages or `pip install` commands are required.

---

## 🖥️ Sample Terminal Interface

### Standby & Authentication

```text id="a9k4ps"
############################################################
       🏛️  NATIONAL VIRTUAL ATM MACHINE (STANDBY)
############################################################
  [1] Insert Card / Start Banking Session
  [2] View ATM Physical Vault Status (Admin)
  [3] View Hardware Audit Trail Logs (Admin)
  [4] Power Down Simulator
############################################################

Select Terminal Action (1-4): 1

=================================================================
💳 SECURE CARD INSERTION & USER AUTHENTICATION
=================================================================
Insert Card (Enter 4-Digit Card Number): 1001
Enter 4-Digit Secret PIN (3 attempt(s) remaining): 1234

[✓] Welcome, Ali Ahmed!
```

### Cash Withdrawal & Denomination Breakdown

```text id="x4y2bz"
============================================================
💵 DISPENSE CASH WITHDRAWAL
============================================================
 Daily Per-Txn Limit : PKR 50,000.00
 Minimum Withdrawal  : PKR 500.00
 Allowed Multiples   : Multiples of PKR 500 only
------------------------------------------------------------
Enter amount to withdraw (PKR): 16500

============================================================
  [✓] PLEASE COLLECT YOUR CASH FROM DISPENSER:
      • PKR 5,000 Notes : 3
      • PKR 1,000 Notes : 1
      • PKR 500 Notes   : 1
  Remaining Account Balance: PKR 68,500.00
============================================================
```

---

## 🧾 Sample Generated Transaction Receipt

The following is an illustrative example of the automatically generated transaction receipt:

```text id="v8z2qa"
=======================================================
             NATIONAL DIGITAL ATM TERMINAL
               TRANSACTION RECEIPT SLIP
=======================================================
Terminal ID     : ATM-ISB-0941
Date & Time     : 2026-10-31 10:35:12
Transaction ID  : TXN-1001
Card Number     : ****-****-****-1001
Account Holder  : Ali Ahmed
Transaction     : WITHDRAWAL
Amount Involved : PKR 16,500.00
Closing Balance : PKR 68,500.00
-------------------------------------------------------
       Thank you for banking with us online!
=======================================================
```

*Sample transaction information is illustrative and demonstrates the receipt format.*

---

## ⚙️ Technical Highlights

- **SHA-256 Cryptographic Hashing:** Uses Python's built-in `hashlib` module to hash PIN credentials before storage.
- **State Machine Architecture:** Uses nested `while` loops to separate the ATM standby state, authentication process, and active banking session.
- **Defensive Input Validation:** Handles invalid values, negative amounts, incorrect data types, and transaction boundary conditions.
- **Denomination Calculation:** Uses arithmetic and division operations to determine the required combination of available banknotes.
- **Dictionary-Based Account Management:** Organizes banking information using structured key-value data.
- **Persistent CSV Storage:** Maintains customer account information across application sessions.
- **Automated Receipt Generation:** Creates timestamped transaction receipts using text file handling.
- **Security Audit Logging:** Records important authentication and transaction events.
- **Modular Programming:** Separates authentication, deposits, withdrawals, transfers, and reporting into logical operations.

---

## 🎯 Learning Outcomes

After exploring this project, beginners should be able to:

1. Build menu-driven applications using Python.
2. Manage continuous application workflows using `while` loops.
3. Organize account information using dictionaries.
4. Implement authentication and basic access control.
5. Perform arithmetic operations for financial calculations.
6. Validate transactions using conditional logic.
7. Read and write persistent records using CSV files.
8. Generate formatted transaction receipts.
9. Use Python's standard library for hashing and timestamps.
10. Understand how multiple functions work together in a banking simulation.

---

## 💡 Learning Recommendations

If you are learning Python, try the following:

- Start by understanding how account balances are stored.
- Experiment with the authentication and PIN validation process.
- Test successful and unsuccessful login attempts.
- Explore how cash denominations are calculated.
- Try different withdrawal amounts and account balances.
- Experiment with deposits and account transfers.
- Observe how CSV records change after transactions.
- Study how receipts and audit logs are generated.
- Try adding new banking features independently.

**Don't just copy the code. Understand the logic, experiment with it, and build your own version.**

---

## ⚠️ Security Disclaimer

This project is an educational ATM simulation and is not intended for real financial transactions or production banking environments.

Although it demonstrates SHA-256 PIN hashing and basic authentication controls, production banking systems require stronger credential storage approaches, secure key management, transaction integrity controls, access management, encryption, and independent security auditing.

The demonstration PINs and account balances must never be reused for real accounts.

---

## 📺 Learn Along with the Tutorial

This project is part of a collection of 10 beginner-friendly Python projects designed for first-semester university students.

- **YouTube Tutorial:** [Add Your Video Link Here]
- **Complete Python Projects Collection:** [Add Your Website Link Here]
- **Main GitHub Repository:** [Python Fundamentals Projects](https://github.com/rabeeanaseer/python-fundamentals-projects)

---

## 🤝 Contributing

Contributions and improvements are welcome!

1. Fork this repository.
2. Create a new branch for your changes.
3. Implement your improvements.
4. Test your changes.
5. Submit a pull request with a clear description.

You can also report bugs or suggest new features through the GitHub Issues section.

---

## 📜 License

This project is distributed under the MIT License. You are welcome to study, modify, and use the code for personal and educational purposes, subject to the license terms.

---

## ⭐ Support the Project

If you find this project useful:

- Give the repository a ⭐ Star.
- Share it with fellow programming students.
- Use it to strengthen your Python fundamentals.
- Contribute improvements and new ideas.

---

**Happy Coding! 🐍**

*Learn the concepts. Build the projects. Strengthen your fundamentals.*
