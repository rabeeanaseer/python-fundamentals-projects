
# 🏥 Hospital & Patient Ward Management System

A comprehensive, menu-driven Python CLI application designed to simulate hospital operations, including patient admissions, inpatient bed allocation, doctor assignments, pharmacy and laboratory billing, patient discharge, and operational analytics.

Part of the **10 Beginner Python Projects – First Semester Collection**, this project demonstrates practical applications of dictionaries, lists, functions, loops, conditional logic, input validation, and persistent file handling through a real-world hospital management simulation.

---

## 📌 Project Overview

Hospital operations involve coordinating patient information, room availability, physician assignments, medication orders, diagnostic investigations, and billing.

This project simulates a lightweight Hospital Information System (HIS) through an interactive terminal application.

Users can admit patients, allocate available rooms, assign consulting doctors, add pharmacy and laboratory charges, process patient discharges, generate itemized invoices, and analyze hospital operations.

The application maintains patient records using CSV storage and generates audit logs and printable discharge receipts using text files.

It is designed for educational purposes and demonstrates how fundamental Python programming concepts can be combined to develop a practical management system.

---

## ✨ Features

### 🏥 Patient Admission & Bed Management

- **Automated Patient ID Generation:** Generates unique patient identifiers in the `P26-XXXX` format.
- **Patient Registration:** Records patient demographics, contact details, and admission information.
- **Multiple Ward Categories:** Supports General Ward, Semi-Private Rooms, Private Deluxe Suites, and Intensive Care Units.
- **Real-Time Bed Tracking:** Monitors room availability and occupancy.
- **Double-Booking Prevention:** Validates room availability before assigning beds.

### 👨‍⚕️ Doctor Directory & Department Management

- Maintains a directory of consulting physicians.
- Supports multiple medical specialties, including Cardiology, Neurology, Orthopedics, Pediatrics, and General Medicine.
- Assigns doctors to admitted patients.
- Automatically calculates professional consultation fees.

### 💊 Pharmacy & Diagnostic Laboratory

- **Medication Management:** Add prescribed medications and their prices to patient bills.
- **Diagnostic Investigations:** Order standardized laboratory and diagnostic services.
- Supports CBC, Metabolic Panel, X-Ray, ECG, Ultrasound, and MRI.
- Allows custom laboratory test entries.
- Maintains itemized pharmacy and diagnostic charges.

### 🧾 Automated Discharge & Billing System

- Calculates patient length of stay using admission and discharge timestamps.
- Computes room rental charges based on ward category and duration.
- Includes professional consultation fees.
- Calculates pharmacy and diagnostic expenses.
- Applies a configurable 5% hospital service surcharge.
- Generates detailed discharge invoices.
- Automatically releases occupied beds after successful payment settlement.

### 💾 Persistent Data Storage

- **CSV Patient Database (`patients_database.csv`):** Stores patient demographics, admission details, clinical status, and billing summaries.
- **Invoice Generation:** Exports printable patient invoices into individual `.txt` files.
- **Audit Logging (`audit_log.txt`):** Records important system activities with timestamps.
- **Automatic Directory Creation:** Creates required storage directories when needed.

### 📊 Hospital Operational Analytics

- Calculates real-time ward occupancy percentages.
- Tracks total hospital revenue.
- Displays doctor caseload statistics.
- Visualizes patient distribution using terminal-based ASCII bar charts.
- Provides an overview of hospital operations.

### 🔍 Patient Search & Record Retrieval

- Search patients using Patient ID.
- Search by full name.
- Search using emergency contact number.
- Retrieve both active and discharged patient records.

### 🛡️ Input Validation & Error Handling

- Validates numerical and textual inputs.
- Prevents invalid patient and room information.
- Handles incorrect data types and empty inputs.
- Checks room availability before bed allocation.
- Uses defensive error handling to reduce unexpected application crashes.

---

## 🏥 Hospital Inventory & Tariff Schedule

### Bed & Ward Categories

The application uses the following illustrative room inventory and daily tariffs:

| Room Range | Category / Tier | Daily Tariff (PKR) | Department |
|:---:|---|---:|---|
| **101–103** | General Ward | 1,200.00 | Internal Medicine |
| **201–202** | Semi-Private Room | 3,500.00 | Post-Surgical Ward |
| **301–302** | Private Deluxe Suite | 7,500.00 | Executive Care |
| **401–402** | Intensive Care Unit (ICU) | 15,000.00 | Critical Care Unit |

### Consulting Specialists

| Doctor ID | Physician Name | Specialization | Consultation Fee |
|:---:|---|---|---:|
| **DOC-01** | Dr. Sarah Khan | Cardiology | PKR 2,500 |
| **DOC-02** | Dr. Ahmed Raza | Neurology | PKR 3,000 |
| **DOC-03** | Dr. Fatima Noor | General Medicine | PKR 1,500 |
| **DOC-04** | Dr. Bilal Siddiqui | Orthopedics | PKR 2,200 |
| **DOC-05** | Dr. Ayesha Tariq | Pediatrics | PKR 1,800 |

> **Note:** Room tariffs, physician information, and consultation fees are illustrative project data, not actual hospital pricing or medical service information.

---

## 📚 Python Concepts Demonstrated

This project demonstrates how fundamental Python concepts can be applied to a practical management application.

| Python Concept | Application |
|---|---|
| Variables & Data Types | Storing patient and billing information |
| User Input & Output | Interactive hospital management interface |
| Conditional Statements | Admission, room allocation, and discharge decisions |
| Loops | Repeated menu navigation and record processing |
| Functions | Modular application structure |
| Lists | Managing patient-related collections |
| Dictionaries | Patient records, doctor directories, and room inventory |
| Nested Dictionaries | Organizing structured patient and billing information |
| File Handling | Persistent data storage and invoice generation |
| CSV Module | Maintaining patient databases |
| Exception Handling | Handling invalid inputs and unexpected errors |
| DateTime Module | Calculating admission duration and timestamps |
| String Formatting | Generating invoices and aligned console reports |
| OS Module | Creating directories and managing file paths |

---

## 📂 Project Structure

```text
02-hospital-management/
│
├── main.py                     # Main application source code
├── README.md                   # Project documentation
│
├── hospital_data/              # Automatically created storage directory
│   ├── patients_database.csv   # Persistent patient records
│   └── audit_log.txt           # System activity and transaction logs
│
└── invoices/                   # Automatically created invoice directory
    ├── Invoice_P26-0001.txt
    └── Invoice_P26-0002.txt
```

**Note:** The `hospital_data/` and `invoices/` directories and their files are generated automatically when the application performs relevant operations. They may not exist before the first execution.

---

## ⚙️ Getting Started

### 1. Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher.
- Visual Studio Code, PyCharm, or Python IDLE.
- A terminal or command prompt.

Verify your Python installation:

```bash
python --version
```

### 2. Navigate to the Project Directory

If you have already cloned the main repository:

```bash
cd python-fundamentals-projects/02-hospital-management
```

### 3. Run the Application

Execute the Python script:

```bash
python main.py
```

No external packages or `pip install` commands are required.

---

## 🖥️ Interactive Console Interface

Upon launching the application, users can navigate through the following menu:

```text
=================================================================
     🏥 SHIFA CLINICAL WARD & HOSPITAL MANAGEMENT SYSTEM
=================================================================
  [1] Admit New Patient & Allocate Bed
  [2] Prescribe Medications or Lab Investigations
  [3] Process Patient Discharge & Generate Final Bill
  [4] View Real-Time Bed & Ward Occupancy Status
  [5] Search Patient Records by ID, Name, or Phone
  [6] View Hospital Executive Analytics & Doctor Caseloads
  [7] View System Audit Log
  [8] Open Saved Data & Invoice Folder Locations
  [9] Exit System
=================================================================
```

### Menu Options

| Option | Functionality |
|:---:|---|
| 1 | Register a new patient and allocate an available hospital bed. |
| 2 | Add prescribed medications or diagnostic laboratory investigations. |
| 3 | Process patient discharge and generate the final invoice. |
| 4 | View current room availability and ward occupancy. |
| 5 | Search patient records using ID, name, or contact number. |
| 6 | View hospital revenue, doctor caseloads, and operational analytics. |
| 7 | View the system audit log. |
| 8 | Open or verify saved data and invoice directory locations. |
| 9 | Exit the application. |

---

## 🧾 Sample Patient Discharge Invoice

The following is an illustrative example of the generated discharge receipt:

```text
======================================================================
           HOSPITAL CARE MANAGEMENT SYSTEM - OFFICIAL RECEIPT
======================================================================
Invoice Date : 2026-10-31 10:30:15
Patient ID   : P26-0001
Full Name    : Hamza Ali
Age / Gender : 34 yrs / Male
Contact      : 0300-1234567
Consultant   : Dr. Sarah Khan
Ward Room    : 201
Admitted     : 2026-10-28 09:15:00
Discharged   : 2026-10-31 10:30:15
Total Days   : 3
----------------------------------------------------------------------
Room Charges (3 days)                 : PKR 10500.00
Doctor Professional Services          : PKR 2500.00
Pharmacy Medications Dispensed        : PKR 1450.00
Pathology & Laboratory Investigations : PKR 3500.00
----------------------------------------------------------------------
Net Subtotal                          : PKR 17950.00
Healthcare Service Surcharge (5%)     : PKR 897.50
TOTAL SETTLED PAYMENT                 : PKR 18847.50
======================================================================
Status: PAID IN FULL - THANK YOU
```

*Sample patient information and billing figures are illustrative and intended to demonstrate the invoice format.*

---

## ⚙️ Technical Highlights

- **Dictionary-Based Data Management:** Uses key-value structures to organize patient records, doctor information, and room availability.
- **Nested Data Structures:** Demonstrates how dictionaries can represent complex patient and billing information.
- **Defensive Input Validation:** Validates integer, float, and string inputs against expected types and permitted ranges.
- **Persistent CSV Storage:** Maintains patient records across application sessions.
- **Automated Audit Trail:** Records important system events with timestamps.
- **Cross-Platform File Management:** Uses Python's built-in `os` module for directory creation and file path handling across Windows, macOS, and Linux.
- **Automated Invoice Generation:** Creates structured text-based discharge receipts.
- **Modular Programming:** Separates application operations into reusable functions and logical subroutines.

---

## 🎯 Learning Outcomes

After exploring this project, beginners should be able to:

1. Build interactive, menu-driven Python applications.
2. Use dictionaries and nested dictionaries to manage structured data.
3. Organize application logic using reusable functions.
4. Apply loops and conditional statements to real-world workflows.
5. Read and write persistent information using CSV and text files.
6. Implement basic record search and retrieval.
7. Perform calculations using dates, timestamps, and numerical values.
8. Generate formatted invoices and reports.
9. Implement input validation and exception handling.
10. Understand how different components work together in a management system.

---

## 💡 Learning Recommendations

If you are learning Python, try the following:

- Understand how patient records are stored using dictionaries.
- Experiment with different patient admission scenarios.
- Test room availability and bed allocation.
- Add different medications and laboratory charges.
- Observe how discharge bills are calculated.
- Examine how CSV records and audit logs are generated.
- Try implementing additional hospital management features independently.

**Don't just copy the code. Understand the logic, experiment with it, and build your own version.**

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
