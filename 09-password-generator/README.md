
# 🔐 Password Generator & Strength Analyzer | Python Security Project

A menu-driven Python security application that generates random passwords, creates memorable passphrases, analyzes password strength, detects common vulnerabilities, estimates brute-force resistance, and exports password batches.

Built as part of a first-semester Python programming fundamentals collection, this project introduces practical concepts in cryptographic randomness, information theory, string analysis, pattern detection, file handling, and defensive programming.

---

## 📌 Project Overview

Many beginner password generators use Python's `random` module and evaluate password strength using only character length.

This project takes a more security-focused approach by using Python's built-in `secrets` module for password generation and mathematical models to evaluate password characteristics.

It combines three main capabilities:

1. **Password Generation:** Creates random passwords and memorable multi-word passphrases.
2. **Security Analysis:** Evaluates password length, character diversity, entropy estimates, and common predictable patterns.
3. **Password Provisioning:** Generates password batches and stores security-related metadata without intentionally retaining plaintext passwords in the metadata vault.

The application is designed as an educational security tool, not a replacement for a professional password manager or enterprise identity management platform.

---

## ✨ Features

### 🔑 1. Cryptographically Secure Password Generation

Uses Python's built-in `secrets` module instead of the standard `random` module.

- Generates passwords using configurable character sets.
- Supports uppercase letters, lowercase letters, digits, and symbols.
- Ensures at least one character from each selected character category.
- Shuffles generated characters to avoid predictable category ordering.
- Supports ambiguous-character exclusion for easier reading.

**Optional ambiguous characters:**

- `l` — lowercase L
- `1` — digit one
- `I` — uppercase i
- `0` — digit zero
- `O` — uppercase o

### 🧠 2. Memorable Passphrase Generator

Generates multi-word passphrases designed to be easier to remember.

Example:

```text
Quantum-Battery-Summit-Orbit-42
```

Passphrases combine multiple words and optional additional characters or digits, depending on the implementation.

Their security depends heavily on the size and selection method of the underlying word list.

### 📊 3. Mathematical Password Entropy Analysis

The application uses two different entropy models to estimate password strength.

**A. Shannon Entropy**

Measures the diversity of characters in a password based on their observed frequency.

\[
H=-\sum_{i=1}^{n}P(x_i)\log_2P(x_i)
\]

The estimated total Shannon information is:

\[
H_{\text{total}}=H\times L
\]

Where:

- \(P(x_i)\) = observed probability of character \(x_i\)
- \(L\) = password length
- \(H\) = empirical entropy per character

**B. Character Pool Entropy**

Estimates the size of the theoretical search space when characters are independently and uniformly selected from a known pool.

\[
H_{\text{pool}}=L\times\log_2(N)
\]

Where:

- \(L\) = password length
- \(N\) = number of possible characters in the pool

**Important:** These are estimates, not guaranteed measures of real-world password security. Shannon entropy based on character frequencies does not account for all language patterns, while pool entropy assumes independent, uniform selection. Password structure and generation methods can significantly affect actual resistance to guessing.

### 🛡️ 4. Password Vulnerability Detection

Analyzes password strings for common weaknesses.

**Dictionary word detection**
- Identifies common words and predictable password fragments.
- Flags potentially vulnerable terms such as `admin` and `password`.

**Keyboard pattern detection**
- Detects predictable keyboard sequences such as:
  - `qwerty`
  - `asdfgh`

**Sequential pattern detection**
- Identifies incremental sequences such as:
  - `1234`
  - `abcd`

**Repeated character detection**
- Identifies repeated character patterns such as:
  - `aaaa`
  - `1111`

**Character diversity analysis**
- Checks the presence of uppercase letters, lowercase letters, digits, and symbols.

### 📋 5. NIST-Informed Security Checks

The analyzer includes checks inspired by the NIST Digital Identity Guidelines (SP 800-63B).

Depending on the implementation, these may include:

- Password length evaluation.
- Common or compromised password detection.
- Predictable pattern identification.
- Basic password quality warnings.

The project uses simplified local heuristics. It is not a complete NIST compliance auditor.

For reference, NIST guidance emphasizes password length, screening against commonly used or compromised passwords, and rate limiting. It does not require arbitrary character-composition rules such as mandatory uppercase letters, digits, and symbols.

### ⚡ 6. Brute-Force Resistance Estimator

Estimates theoretical guessing time using a configurable attacker speed.

**Default simulation assumption:**

\[
10^{11}\text{ guesses per second}
\]

The theoretical search-space estimate is:

\[
T=\frac{2^H}{R}
\]

Where:

- \(T\) = estimated time in seconds
- \(H\) = estimated entropy in bits
- \(R\) = assumed guesses per second

The application converts the estimated time into readable units such as seconds, days, years, or longer periods.

*This is a simplified theoretical model. Actual cracking speeds depend on password structure, hashing algorithms, hardware, attack strategies, and whether attackers can exploit patterns instead of searching the entire theoretical keyspace.*

### 📦 7. Bulk Password Generation & Export

- Generates batches of passwords.
- Supports configurable batch sizes, from 5 to 100.
- Exports generated credentials to formatted text files.
- Stores exported files in the `exports/` directory.

**Security note:** Exported files contain plaintext credentials. Protect them carefully, restrict file permissions, and securely dispose of them when no longer required.

### 🗃️ 8. Password Vault Metadata

Maintains a CSV-based metadata record containing information such as:

- Password length.
- Entropy estimates.
- Security evaluation status.
- Generation or analysis timestamps.

The metadata vault is designed not to store plaintext passwords.

### 📝 9. Security Audit Logging

Maintains a record of application activities, such as:

- Password generation operations.
- Bulk export events.
- Password analysis.
- Security evaluation results.

---

## 📐 Password Strength Reference

The following table provides illustrative entropy categories, not official NIST security classifications.

| Estimated Entropy | Illustrative Rating |
|---|---|
| Below 30 bits | Very Weak |
| 30–44 bits | Weak |
| 45–59 bits | Moderate |
| 60–79 bits | Strong |
| 80+ bits | Very Strong |

**Important:** A high theoretical entropy score does not guarantee security. A predictable password can be vulnerable even when it contains multiple character types.

For real-world credentials, prioritize long, randomly generated passwords or passphrases and avoid reusing passwords across services.

---

## 🛠️ Technologies Used

- **Python 3.8+**
- `secrets` — Cryptographically secure random generation.
- `math` — Entropy and logarithmic calculations.
- `string` — Character sets.
- `csv` — Metadata storage.
- `os` — File and directory management.
- `datetime` — Timestamp recording.

No third-party Python packages are required.

---

## 📂 Project Structure

```text
09-password-generator/
│
├── main.py
├── README.md
│
├── sec_data/
│   ├── password_vault.csv
│   └── security_audit.txt
│
└── exports/
    └── Bulk_Passwords_YYYY-MM-DD_HHMMSS.txt
```

**Note:** The `sec_data/` and `exports/` directories and their files are generated automatically when the application runs.

---

## 🚀 Getting Started

### 1. Prerequisites

Install Python 3.8 or later.

Verify your installation:

```bash
python --version
```

### 2. Clone the Repository

```bash
git clone https://github.com/rabeeanaseer/python-fundamentals-projects.git
```

### 3. Navigate to the Project Directory

```bash
cd python-fundamentals-projects/09-password-generator
```

### 4. Run the Application

```bash
python main.py
```

---

## 🖥️ Interactive Console Interface

The application provides a menu-driven interface for password generation, bulk provisioning, security analysis, and metadata review.

```text
=================================================================
   🔐 ADVANCED PASSWORD GENERATOR & ENTROPY ANALYZER
=================================================================
  --- Password Generation & Provisioning ---
  [1] Generate Secure Password or Memorable Passphrase
  [2] Bulk Password Generation & Export to Text File

  --- Security Analysis & Vulnerability Auditing ---
  [3] Analyze Password Strength (Entropy & Security Checks)
  [4] View Password Vault Historical Metadata
  [5] View Security Audit Logs
  [6] Exit System
=================================================================
```

---

## 🔬 Sample Password Security Audit

Example output from the password analysis feature:

```text
======================================================================
🛡️ PASSWORD STRENGTH & ENTROPY EVALUATOR
======================================================================
Enter password to analyze: ***********

----------------------------------------------------------------------
                   SECURITY AUDIT SUMMARY
----------------------------------------------------------------------
 Evaluated String      : *********5!
 String Length         : 11 characters
 Shannon Entropy       : 36.52 bits
 Key-Space Entropy     : 72.27 bits
 Estimated Guess Time  : 1.6 years
 Overall Rating        : STRONG (Theoretical Estimate)
 Security Check Status : WARNINGS DETECTED
----------------------------------------------------------------------

  🌟 Positive Security Attributes:
     [+] High Character Diversity: Uses all four character categories.

  ⚠️ Security Vulnerabilities & Pattern Flags:
     [-] Shorter than the recommended length configured by this tool.
     [-] Dictionary Word Detected: Contains the common term 'admin'.
     [-] Sequential Pattern: Contains a predictable sequence.

======================================================================
```

*Illustrative output only. Actual entropy, estimated guessing time, and security warnings depend on the application's implementation and configured assumptions.*

---

## 🧠 Python Concepts Demonstrated

This project provides practical experience with:

- Variables, data types, and operators.
- Conditional statements and loops.
- Functions and modular programming.
- Strings and character manipulation.
- Lists, sets, and dictionaries.
- Cryptographically secure random generation.
- Mathematical entropy calculations.
- Logarithmic functions.
- Pattern matching and string analysis.
- Input validation and exception handling.
- CSV file handling.
- Directory and file management.
- Timestamp generation.
- Basic security concepts.

---

## 🎯 Learning Outcomes

After exploring this project, beginners should understand how to:

1. Generate random values using Python's `secrets` module.
2. Understand the difference between `random` and cryptographically secure randomness.
3. Build configurable password generators.
4. Create memorable multi-word passphrases.
5. Calculate theoretical password entropy.
6. Detect common password patterns and weaknesses.
7. Estimate theoretical brute-force search time.
8. Store application metadata using CSV files.
9. Generate and export batches of credentials.
10. Apply basic security principles when designing Python applications.

---

## 🔍 Suggested Improvements

Extend the application with additional security features:

- Argon2id or bcrypt-based password hashing.
- Have I Been Pwned API integration for compromised-password screening.
- Configurable password policies.
- A graphical interface using Tkinter or Streamlit.
- Encrypted export files.
- Secure deletion workflows for temporary credential files.
- More comprehensive dictionary and keyboard-pattern detection.
- Password strength visualizations.
- Unit tests for entropy and password-generation algorithms.
- A passphrase generator using a larger, curated word list.

---

## 🔐 Security Considerations

This project is an educational password-generation and analysis tool.

- Do not use generated passwords in production systems without reviewing the implementation.
- Do not store plaintext credentials in the metadata vault.
- Treat exported password files as sensitive information.
- Do not interpret theoretical entropy as a guarantee of security.
- Do not use this application as a substitute for a trusted password manager.
- Avoid entering real passwords into third-party or untrusted password analyzers.

---

## 📺 Video Tutorial

Follow the project walkthrough to understand password generation, entropy calculations, vulnerability detection, and the application's internal workflow.

**YouTube:** [Watch the Project Tutorial](ADD_YOUTUBE_VIDEO_LINK)

---

## 🌐 Learning Resources

Explore more beginner-friendly programming projects and learning resources.

**Website:** [Visit My Learning Hub](ADD_WEBSITE_LINK)

**GitHub Repository:** [Python Fundamentals Projects](https://github.com/rabeeanaseer/python-fundamentals-projects)

---

## 🤝 Contributing

Suggestions, improvements, and contributions are welcome.

1. Fork the repository.
2. Create a new branch.
3. Implement your changes.
4. Submit a pull request.

---

## 📄 License

This project is intended for educational and learning purposes. Add a license file to the repository if you want to define explicit permissions for reuse and distribution.

---

## ⭐ Support

If this project helps you understand Python programming and basic security concepts, consider giving the repository a star on GitHub.

Explore the other projects in the collection and keep building!
