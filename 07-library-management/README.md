
# 📚 Library Book Management System | Advanced Python CRUD Project

A menu-driven Library Management System built with Python that demonstrates book catalog management, member registration, book circulation, ISBN validation, inventory tracking, overdue fine calculation, and CSV-based data persistence.

This project is part of a beginner-friendly Python programming collection. It introduces practical concepts such as relational data management, nested dictionaries, input validation, file handling, date calculations, and CRUD operations.

---

## 📌 Project Overview

The Library Book Management System simulates the core operations of a university or institutional library.

Instead of storing book titles in a simple list, the application manages three interconnected data entities:

1. **Book Catalog:** Stores ISBNs, book titles, authors, categories, total copies, and available inventory.
2. **Patron Registry:** Maintains member profiles, unique IDs, and borrowing information.
3. **Circulation Records:** Tracks issued books, due dates, returns, and overdue fines.

The system helps demonstrate how separate data collections can work together to maintain consistent library records.

---

## ✨ Features

### 📖 1. Book Catalog Management

- Add new books with ISBN validation.
- Search books by title, author, category, or ISBN.
- View the available book inventory.
- Update book details, including title, author, and category.
- Add additional copies to existing inventory.
- Delete obsolete books when no active loans exist.

### 🔢 2. ISBN-10 and ISBN-13 Validation

Implements checksum algorithms to validate both standard ISBN formats.

- **ISBN-10:** Uses Modulus 11 validation, including support for `X` as the final check character.
- **ISBN-13:** Uses Modulus 10 validation with alternating weights of 1 and 3.
- Rejects invalid ISBN inputs before adding books to the catalog.

### 👥 3. Patron Management

- Register new library members.
- Generate unique member IDs using the `LIB-XXX` format.
- View registered patrons.
- Maintain member borrowing records.
- Enforce a maximum of three active book checkouts per member.

### 🔄 4. Book Circulation Management

- Issue books to registered members.
- Check available inventory before issuing a book.
- Prevent duplicate active checkouts of the same title by a member.
- Generate checkout transaction IDs.
- Record issue dates and return deadlines.
- Process book returns and update inventory.

### 💰 5. Automated Overdue Fine Calculation

- Calculate overdue days using Python's `datetime` module.
- Apply a late-return fee of **PKR 20 per overdue day**.
- Calculate fines based on the difference between the due date and actual return date.

**Fine calculation:**

```python
overdue_days = max(0, (return_date - due_date).days)
fine = overdue_days * 20
```

### 🧾 6. Transaction Slip Generation

Automatically generates printable text receipts for:

- Book checkout transactions.
- Book return transactions.

Generated slips are stored in the `slips/` directory.

### 💾 7. CSV-Based Data Persistence

The application maintains three CSV data files:

| File | Purpose |
|---|---|
| `books_catalog.csv` | Stores book catalog and inventory records |
| `patrons_registry.csv` | Stores registered library members |
| `active_loans.csv` | Stores circulation and loan records |

The application automatically creates the required data directories and initializes its data files when needed.

### 📋 8. System Audit Logging

Maintains a timestamped activity log containing events such as:

- New book registrations.
- Catalog modifications.
- Patron registrations.
- Book checkouts.
- Book returns.
- Fine settlements.

---

## 📐 ISBN Validation Algorithms

### ISBN-10 Validation — Modulus 11

For the first nine digits, multiply each digit by descending weights from 10 to 2. Add the check digit, where `X` represents 10.

The ISBN is valid when:

\[
\left(\sum_{i=1}^{9} d_i(11-i)+d_{10}\right)\bmod 11=0
\]

### ISBN-13 Validation — Modulus 10

Multiply the first twelve digits by alternating weights of 1 and 3.

The check digit is calculated as:

\[
d_{13} =
\left(10-
\left(
\sum_{i=1}^{12} d_i w_i
\right)\bmod 10
\right)\bmod 10
\]

Where:

\[
w_i =
\begin{cases}
1 & \text{if } i \text{ is odd}\\
3 & \text{if } i \text{ is even}
\end{cases}
\]

These algorithms help detect invalid ISBNs before they enter the catalog.

---

## 🛠️ Technologies Used

- **Python 3.8+**
- `os` — Directory and file management
- `csv` — Structured data storage
- `datetime` — Issue dates, due dates, and overdue calculations

No third-party Python packages are required.

---

## 📂 Project Structure

```text
07-library-management/
│
├── main.py
├── README.md
│
├── library_data/
│   ├── books_catalog.csv
│   ├── patrons_registry.csv
│   ├── active_loans.csv
│   └── circulation_audit.txt
│
└── slips/
    ├── Checkout_Slip_LN-XXXXXX.txt
    └── Return_Slip_LN-XXXXXX.txt
```

**Note:** The `library_data/` and `slips/` directories and their files are generated automatically when the application runs.

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

### 3. Navigate to the Project

```bash
cd python-fundamentals-projects/07-library-management
```

### 4. Run the Application

```bash
python main.py
```

---

## 🖥️ Interactive Console Interface

The application provides a menu-driven interface for managing books, members, and circulation transactions.

```text
=================================================================
     📚 ADVANCED LIBRARY MANAGEMENT SYSTEM
=================================================================
  --- Catalog Management (Books CRUD) ---
  [1] Add New Book Title (ISBN Verified)
  [2] Search Catalog by Keyword / View All Inventory
  [3] Update Book Information / Add Copy Stock
  [4] Delete / Decommission Book Title

  --- Member & Circulation Management ---
  [5] Register New Library Patron
  [6] View All Registered Patrons
  [7] Issue Book Checkout (Generate Slip)
  [8] Process Book Return (Calculate Overdue Fines)
  [9] View Active Circulation Loans & Overdue Tracker
  [10] Exit System
=================================================================
```

---

## 🧾 Sample Checkout Slip

Example of a generated checkout receipt:

```text
============================================================
              UNIVERSITY CENTRAL LIBRARY
                BOOK CIRCULATION SLIP
============================================================
Loan ID     : LN-049812
Issue Date  : 2026-10-31
Due Date    : 2026-11-14
------------------------------------------------------------
Patron ID   : LIB-101
Member Name : Ali Ahmed
Book Title  : Clean Code
Author      : Robert C. Martin
ISBN        : 9780132350884
------------------------------------------------------------
Notice: Overdue fine is PKR 20.00/day after due date.
============================================================
```

*Sample data is illustrative.*

---

## 🧠 Python Concepts Demonstrated

This project provides practical experience with:

- Variables, data types, and operators.
- Conditional statements and loops.
- Functions and modular programming.
- Lists, dictionaries, and nested data structures.
- CRUD operations.
- ISBN checksum algorithms.
- Input validation and exception handling.
- CSV file reading and writing.
- Date and time calculations.
- Data relationships and referential integrity.
- Inventory synchronization.
- Basic audit logging.

---

## 🎯 Learning Outcomes

After exploring this project, beginners can understand how to:

1. Build a multi-feature command-line application.
2. Organize related records using dictionaries and structured data.
3. Implement Create, Read, Update, and Delete operations.
4. Validate ISBNs using mathematical algorithms.
5. Manage relationships between books, members, and loans.
6. Track inventory during checkout and return operations.
7. Calculate overdue fines using calendar dates.
8. Persist application data using CSV files.
9. Generate transaction receipts automatically.
10. Design a more structured Python application using built-in modules.

---

## 🔍 Suggested Improvements

Want to extend the project? Try implementing:

- A graphical interface using Tkinter.
- SQLite database integration.
- Admin and librarian authentication.
- Book reservation and waiting lists.
- Email reminders for approaching due dates.
- Barcode-based book identification.
- Advanced reporting and analytics.
- Configurable borrowing limits and fine rates.

---

## 📺 Video Tutorial

Follow the project walkthrough to understand the implementation, explore the code, and learn how the library management system works.

**YouTube:** [Watch the Project Tutorial](ADD_YOUTUBE_VIDEO_LINK)

---

## 🌐 Learning Resources

Explore more beginner-friendly programming projects and learning resources.

**Website:** [Visit My Learning Hub](ADD_WEBSITE_LINK)

**GitHub Repository:** [Python Fundamentals Projects](https://github.com/rabeeanaseer/python-fundamentals-projects)

---

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a new branch.
3. Make your improvements.
4. Submit a pull request.

---

## 📄 License

This project is intended for educational and learning purposes. Add a license file to the repository if you want to define explicit permissions for reuse and distribution.

---

## ⭐ Support

If this project helps you understand Python programming, consider giving the repository a star on GitHub.

Explore the other projects in the collection and keep building!
```
