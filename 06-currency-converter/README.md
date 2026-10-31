
# 💱 Foreign Exchange (Forex) & Multi-Currency Converter

A feature-rich, menu-driven Python CLI foreign exchange application designed to perform multi-currency conversions, calculate cross-exchange rates, apply transaction fees, manage custom exchange rates, and maintain persistent conversion records.

Part of the **10 Beginner Python Projects – First Semester Collection**, this project demonstrates practical applications of dictionaries, nested data structures, mathematical operations, functions, loops, JSON and CSV file handling, and input validation through a simulated foreign exchange management system.

---

## 📌 Project Overview

Basic currency converters often rely on simple multiplication using a limited number of predefined exchange rates.

This project takes a more flexible approach by implementing a multi-currency conversion engine that uses USD as a common base currency to calculate cross-exchange rates dynamically.

Users can convert between supported currencies, select different transaction service tiers, compare equivalent values across multiple currencies, modify exchange rates, add custom currencies, and maintain a persistent transaction history.

The application also generates printable conversion receipts and maintains audit logs for important operations.

It is designed for educational purposes and demonstrates how fundamental Python programming concepts can be combined to develop a practical financial calculation and currency management application.

---

## ✨ Features

### 🌐 Multi-Currency Conversion Engine

- **USD-Based Mathematical Triangulation:** Uses USD as a common base currency to calculate exchange rates between supported currencies.
- **Dynamic Cross-Rate Calculation:** Converts between any two registered currencies without requiring individually hardcoded conversion pairs.
- **Inverse Exchange Rates:** Calculates reverse conversion rates automatically.
- **Currency Metadata:** Maintains currency codes, names, symbols, regions, and exchange rates.
- **Flexible Currency Selection:** Supports conversions between all registered currencies.

### 💸 Transaction Service & Fee Management

Supports three processing tiers:

- **Standard Transfer:** Applies a 1.0% processing spread fee.
- **Express Remittance:** Applies a 2.5% priority network fee.
- **VIP / Institutional Transfer:** Applies a 0.0% service fee.

The application calculates the gross converted amount, applicable service fee, and final net payout.

### 📊 Multi-Currency Batch Portfolio Conversion

- Converts a single base amount into multiple registered currencies.
- Displays equivalent values across the supported currency list.
- Presents exchange rates and converted amounts in a formatted table.
- Provides a consolidated multi-currency comparison.

### ⚙️ Custom Exchange Rate Management

Implements basic CRUD-style exchange rate management.

- **View:** Display all registered currencies and their exchange rates.
- **Update:** Modify existing currency exchange rates.
- **Create:** Add new currencies with custom codes, names, symbols, regions, and rates.
- **Persistent Configuration:** Saves custom exchange rates in `custom_rates.json`.
- **Session Persistence:** Retains supported configuration changes across application restarts.

### 🧾 Automated Conversion Receipt Generation

- Generates individual printable conversion receipts.
- Assigns unique transaction identifiers.
- Records transaction timestamps.
- Displays source and target currencies.
- Includes effective exchange rates and service fees.
- Shows gross converted values and final net payouts.
- Saves receipts as `.txt` files in a dedicated directory.

### 💾 Persistent CSV Transaction Ledger

- Stores conversion history in `fx_data/conversion_history.csv`.
- Records transaction IDs, timestamps, source amounts, exchange rates, service fees, and net payouts.
- Maintains transaction information across application sessions.

### 📝 Audit Logging

- Tracks exchange rate modifications.
- Records currency management operations.
- Logs batch conversion activities.
- Maintains chronological system activity in `fx_data/fx_audit_log.txt`.

### 🛡️ Input Validation & Error Handling

- Handles uppercase and lowercase currency codes.
- Rejects unsupported currency codes.
- Validates positive numerical conversion amounts.
- Handles invalid input types and empty values.
- Prevents invalid exchange rate configurations.

---

## 📊 Default Currency Matrix

The application includes the following illustrative exchange rates, expressed as the value of each currency relative to 1 USD.

| Code | Currency Name | Symbol | Region | Rate / 1 USD |
|:---:|---|:---:|---|---:|
| **USD** | United States Dollar | `$` | North America | 1.0000 |
| **PKR** | Pakistani Rupee | `₨` | South Asia | 278.5000 |
| **EUR** | Euro | `€` | European Union | 0.9200 |
| **GBP** | British Pound Sterling | `£` | United Kingdom | 0.7900 |
| **AED** | UAE Dirham | `د.إ` | Middle East | 3.6700 |
| **SAR** | Saudi Riyal | `﷼` | Middle East | 3.7500 |
| **JPY** | Japanese Yen | `¥` | East Asia | 154.2000 |
| **CNY** | Chinese Yuan | `¥` | East Asia | 7.2400 |
| **CAD** | Canadian Dollar | `C$` | North America | 1.3800 |
| **AUD** | Australian Dollar | `A$` | Oceania | 1.5200 |
| **INR** | Indian Rupee | `₹` | South Asia | 83.9000 |
| **TRY** | Turkish Lira | `₺` | Eurasia | 34.2500 |

> **Important:** These are illustrative static exchange rates for educational purposes. They are not live market rates and should not be used for actual financial transactions.

---

## 🧮 Exchange Rate Calculation

The application uses USD as a common base currency to calculate cross-exchange rates.

### Cross-Rate Formula

\[
\text{Cross Rate} =
\frac{\text{Target Rate (vs USD)}}{\text{Source Rate (vs USD)}}
\]

### Conversion Formula

\[
\text{Gross Amount} =
\text{Source Amount} \times \text{Cross Rate}
\]

### Service Fee Calculation

\[
\text{Service Fee} =
\text{Gross Amount} \times \text{Fee Percentage}
\]

### Final Net Payout

\[
\text{Net Payout} =
\text{Gross Amount} - \text{Service Fee}
\]

### Example: USD to PKR

Given:

- Source Amount: 100 USD
- USD to PKR Rate: 278.50
- Service Fee: 1%

Calculation:

\[
100 \times 278.50 = 27,850
\]

\[
27,850 \times 0.01 = 278.50
\]

\[
27,850 - 278.50 = 27,571.50
\]

**Final Net Payout: PKR 27,571.50**

---

## 📚 Python Concepts Demonstrated

This project demonstrates how fundamental Python concepts can be applied to a currency conversion and financial calculation system.

| Python Concept | Application |
|---|---|
| Variables & Data Types | Managing amounts, rates, and transaction fees |
| User Input & Output | Interactive currency conversion interface |
| Conditional Statements | Processing service tiers and validating currencies |
| Loops | Repeated conversions and menu navigation |
| Functions | Modular conversion and transaction operations |
| Dictionaries | Managing currency codes, symbols, and exchange rates |
| Nested Dictionaries | Organizing structured currency metadata |
| Arithmetic Operations | Calculating conversions, fees, and payouts |
| JSON Module | Persisting custom exchange rate configurations |
| CSV Module | Maintaining transaction records |
| File Handling | Saving receipts and audit logs |
| DateTime Module | Generating transaction timestamps |
| OS Module | Managing storage directories |
| Exception Handling | Handling invalid inputs and configuration errors |

---

## 📂 Project Structure

```text id="f3x9qp"
06-currency-converter/
│
├── main.py                     # Main currency conversion application
├── README.md                   # Project documentation
│
├── fx_data/                    # Automatically created storage directory
│   ├── conversion_history.csv  # Persistent transaction records
│   ├── custom_rates.json       # User-modified exchange rates
│   └── fx_audit_log.txt        # System activity and rate change logs
│
└── receipts/                   # Automatically created receipt directory
    ├── FX_Receipt_FX-1001.txt
    └── FX_Receipt_FX-1002.txt
```

**Note:** The `fx_data/` and `receipts/` directories and their files are generated automatically when the application performs relevant operations. They may not exist before the first execution.

---

## ⚙️ Getting Started

### 1. Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher.
- Visual Studio Code, PyCharm, or Python IDLE.
- A terminal or command prompt.

Verify your Python installation:

```bash id="v5p2qa"
python --version
```

### 2. Navigate to the Project Directory

If you have already cloned the main repository:

```bash id="k2z8mw"
cd python-fundamentals-projects/06-currency-converter
```

### 3. Run the Application

Execute the Python script:

```bash id="p4x7nc"
python main.py
```

No external packages or `pip install` commands are required.

---

## 🖥️ Sample Console Output

### Single Currency Conversion with Fee Breakdown

```text id="w8j3mz"
======================================================================
💱 STANDARD CURRENCY CONVERSION & REMITTANCE COUNTER
======================================================================
Enter Source Currency Code (e.g., USD, PKR, EUR): USD
Enter Target Currency Code (e.g., PKR, AED, GBP): PKR
Enter amount in USD: 100

Select Processing Service Tier:
  [1] Standard Transfer  (1.0% FX Spread Fee)
  [2] Express Remittance (2.5% Priority Network Fee)
  [3] VIP / Institutional (0.0% Zero Fee)

Select Tier (1-3): 1

----------------------------------------------------------------------
                    EXCHANGE SETTLEMENT SUMMARY
----------------------------------------------------------------------
 Transaction ID   : FX-049812
 Date & Timestamp : 2026-10-31 10:45:00
 Source Amount    : $ 100.00 USD (United States Dollar)
 Effective Rate   : 1 USD = 278.500000 PKR
 Inverted Rate    : 1 PKR = 0.003591 USD
 Gross Equivalent : ₨ 27,850.00 PKR
 Service Fee      : ₨ 278.50 PKR (1.0%)
 Net Transferred  : ₨ 27,571.50 PKR
----------------------------------------------------------------------
```

### Multi-Currency Batch Conversion

```text id="m6q2xb"
===========================================================================
🌐 MULTI-CURRENCY BATCH PORTFOLIO CONVERSION
===========================================================================
Enter Base Currency (e.g., USD, PKR): USD
Enter amount in USD: 1000

---------------------------------------------------------------------------
 Portfolio Snapshot for: $ 1,000.00 USD
---------------------------------------------------------------------------
Code  Currency Name               Rate (vs Base)    Equivalent Value
---------------------------------------------------------------------------
PKR   Pakistani Rupee             278.5000          ₨     278,500.00
EUR   Euro                        0.9200            €         920.00
GBP   British Pound Sterling      0.7900            £         790.00
AED   United Arab Emirates Dirham 3.6700            د.إ     3,670.00
SAR   Saudi Riyal                 3.7500            ﷼       3,750.00
JPY   Japanese Yen                154.2000          ¥     154,200.00
CAD   Canadian Dollar             1.3800            C$      1,380.00
===========================================================================
```

*Sample conversion values are illustrative and based on the default exchange rate matrix.*

---

## ⚙️ Technical Highlights

- **Standard Library Only:** Uses Python's built-in `json`, `csv`, `os`, and `datetime` modules. No third-party dependencies are required.
- **USD-Based Mathematical Triangulation:** Calculates cross-exchange rates using a common USD base rather than requiring individually hardcoded currency pairs.
- **Dictionary-Based Lookups:** Uses dictionaries for currency metadata and exchange rate retrieval, providing average-case O(1) lookup complexity.
- **Dynamic Exchange Rate Management:** Allows users to create and update currency configurations.
- **JSON Configuration Persistence:** Saves customized exchange rates across application sessions.
- **Persistent Transaction Ledger:** Maintains conversion history using CSV file handling.
- **Automated Receipt Generation:** Creates formatted transaction receipts using text file operations.
- **Defensive Input Validation:** Handles unsupported currencies, invalid numerical values, and unexpected user input.
- **Modular Programming:** Separates conversion calculations, fee processing, configuration management, and transaction logging into reusable functions.

---

## 🎯 Learning Outcomes

After exploring this project, beginners should be able to:

1. Organize structured data using dictionaries and nested dictionaries.
2. Perform mathematical calculations using Python.
3. Implement multi-step arithmetic formulas.
4. Build menu-driven applications using loops and conditional statements.
5. Create reusable functions for currency conversion.
6. Read and write configuration data using JSON.
7. Maintain transaction records using CSV files.
8. Generate formatted financial reports and receipts.
9. Implement input validation and exception handling.
10. Understand how mathematical logic can power a practical conversion engine.

---

## 💡 Learning Recommendations

If you are learning Python, try the following:

- Start by understanding how exchange rates are stored.
- Experiment with converting USD into different currencies.
- Understand the mathematical triangulation formula.
- Try calculating inverse exchange rates.
- Modify the service fee percentages.
- Add a new currency with a custom exchange rate.
- Observe how custom rates persist across application restarts.
- Experiment with batch currency conversions.
- Examine how transaction history and receipts are generated.
- Try implementing additional financial calculation features independently.

**Don't just copy the code. Understand the logic, experiment with it, and build your own version.**

---

## ⚠️ Financial Disclaimer

This project is an educational currency conversion simulation. It does not connect to live foreign exchange markets, banks, payment networks, or remittance providers.

Exchange rates and transaction fees are illustrative and should not be considered financial advice or used for actual financial transactions.

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
