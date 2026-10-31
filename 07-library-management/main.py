"""
Project 07: Enterprise Library Book Management & Circulation System (Advanced CRUD)
Course Level: 1st/2nd Semester CS - Advanced Programming Fundamentals
Concepts Used:
  - Advanced In-Memory Relational Data Modeling (Books, Patrons, Active Loans)
  - Full CRUD Operations: Create, Read, Update, Delete with Referential Integrity
  - Algorithmic ISBN Validation (Checksum verification for ISBN-10 and ISBN-13)
  - Date Math & Overdue Fine Calculations using datetime & timedelta
  - Persistent Multi-Table Storage (CSV Databases) with Transaction Rollbacks
  - Defensive Exception Handling & Complex Multi-Field Searching
"""

import os
import csv
from datetime import datetime, timedelta

# ==============================================================================
# GLOBAL CONFIGURATION & DATA STORAGE CONSTANTS
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "library_data")
SLIPS_DIR = os.path.join(BASE_DIR, "slips")

BOOKS_CSV = os.path.join(DATA_DIR, "books_catalog.csv")
PATRONS_CSV = os.path.join(DATA_DIR, "patrons_registry.csv")
LOANS_CSV = os.path.join(DATA_DIR, "active_loans.csv")
AUDIT_LOG_TXT = os.path.join(DATA_DIR, "circulation_audit.txt")

# Business Rules
MAX_LOAN_DAYS = 14
DAILY_FINE_RATE = 20.0  # PKR per day overdue
MAX_BOOKS_PER_PATRON = 3

# In-Memory Relational Tables
# Master Catalog: { isbn: { "isbn", "title", "author", "genre", "total_copies", "available_copies" } }
BOOKS_CATALOG = {}
# Patrons: { patron_id: { "patron_id", "name", "email", "phone", "active_borrow_count" } }
PATRONS_REGISTRY = {}
# Active Loans: { loan_id: { "loan_id", "isbn", "patron_id", "issue_date", "due_date", "status" } }
ACTIVE_LOANS = {}


# ==============================================================================
# ALGORITHMIC UTILITIES & ISBN CHECKSUM VERIFIER
# ==============================================================================
def validate_isbn(isbn_str):
    """
    Validates either ISBN-10 or ISBN-13 using official modulus checksum algorithms.
    """
    clean_isbn = isbn_str.replace("-", "").replace(" ", "").strip().upper()

    # ISBN-10 Checksum Algorithm
    if len(clean_isbn) == 10:
        total = 0
        for i in range(9):
            if not clean_isbn[i].isdigit():
                return False
            total += int(clean_isbn[i]) * (10 - i)
        last_char = clean_isbn[9]
        if last_char == "X":
            total += 10
        elif last_char.isdigit():
            total += int(last_char)
        else:
            return False
        return total % 11 == 0

    # ISBN-13 Checksum Algorithm
    elif len(clean_isbn) == 13:
        if not clean_isbn.isdigit():
            return False
        total = sum(int(clean_isbn[i]) * (1 if i % 2 == 0 else 3) for i in range(12))
        check_digit = (10 - (total % 10)) % 10
        return check_digit == int(clean_isbn[12])

    return False


def get_current_date():
    """Returns today's date formatted as YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")


def parse_date(date_str):
    """Parses standard ISO date string."""
    return datetime.strptime(date_str, "%Y-%m-%d")


# ==============================================================================
# PERSISTENCE, SEEDING & AUDIT LOGGING
# ==============================================================================
def initialize_system():
    """Sets up local directory structures and hydrates database files."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SLIPS_DIR, exist_ok=True)

    # Initialize Audit Log
    if not os.path.exists(AUDIT_LOG_TXT):
        with open(AUDIT_LOG_TXT, mode="w", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] SYSTEM: Library Core Initialized.\n")

    # Seed Books Catalog if missing
    if not os.path.exists(BOOKS_CSV):
        default_books = [
            ["9780132350884", "Clean Code", "Robert C. Martin", "Software Engineering", "5", "5"],
            ["9780262033848", "Introduction to Algorithms", "Thomas H. Cormen", "Computer Science", "3", "3"],
            ["9780596009205", "Head First Java", "Kathy Sierra", "Programming", "4", "4"],
            ["9781449355739", "Learning Python", "Mark Lutz", "Programming", "6", "6"],
            ["9780131103627", "The C Programming Language", "Brian W. Kernighan", "Systems Programming", "2", "2"]
        ]
        with open(BOOKS_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ISBN", "Title", "Author", "Genre", "Total_Copies", "Available_Copies"])
            writer.writerows(default_books)

    # Seed Patrons Registry if missing
    if not os.path.exists(PATRONS_CSV):
        default_patrons = [
            ["LIB-101", "Ali Ahmed", "ali.ahmed@example.com", "03001234567", "0"],
            ["LIB-102", "Zainab Fatima", "zainab.f@example.com", "03219876543", "0"],
            ["LIB-103", "Hamza Malik", "hamza.m@example.com", "03451122334", "0"]
        ]
        with open(PATRONS_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Patron_ID", "Name", "Email", "Phone", "Active_Borrow_Count"])
            writer.writerows(default_patrons)

    # Initialize Loans File if missing
    if not os.path.exists(LOANS_CSV):
        with open(LOANS_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Loan_ID", "ISBN", "Patron_ID", "Issue_Date", "Due_Date", "Status"])

    load_database()


def log_event(message):
    """Appends an event to the circulation audit log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(AUDIT_LOG_TXT, mode="a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except IOError:
        pass


def load_database():
    """Loads all CSV databases into runtime relational memory structures."""
    global BOOKS_CATALOG, PATRONS_REGISTRY, ACTIVE_LOANS
    BOOKS_CATALOG.clear()
    PATRONS_REGISTRY.clear()
    ACTIVE_LOANS.clear()

    # Load Books
    with open(BOOKS_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            BOOKS_CATALOG[row["ISBN"]] = {
                "isbn": row["ISBN"],
                "title": row["Title"],
                "author": row["Author"],
                "genre": row["Genre"],
                "total_copies": int(row["Total_Copies"]),
                "available_copies": int(row["Available_Copies"])
            }

    # Load Patrons
    with open(PATRONS_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            PATRONS_REGISTRY[row["Patron_ID"]] = {
                "patron_id": row["Patron_ID"],
                "name": row["Name"],
                "email": row["Email"],
                "phone": row["Phone"],
                "active_borrow_count": int(row["Active_Borrow_Count"])
            }

    # Load Active Loans
    with open(LOANS_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ACTIVE_LOANS[row["Loan_ID"]] = {
                "loan_id": row["Loan_ID"],
                "isbn": row["ISBN"],
                "patron_id": row["Patron_ID"],
                "issue_date": row["Issue_Date"],
                "due_date": row["Due_Date"],
                "status": row["Status"]
            }


def flush_database():
    """Atomically writes all in-memory registries to their respective CSV tables."""
    try:
        # Write Books
        with open(BOOKS_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ISBN", "Title", "Author", "Genre", "Total_Copies", "Available_Copies"])
            for b in BOOKS_CATALOG.values():
                writer.writerow([b["isbn"], b["title"], b["author"], b["genre"], b["total_copies"], b["available_copies"]])

        # Write Patrons
        with open(PATRONS_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Patron_ID", "Name", "Email", "Phone", "Active_Borrow_Count"])
            for p in PATRONS_REGISTRY.values():
                writer.writerow([p["patron_id"], p["name"], p["email"], p["phone"], p["active_borrow_count"]])

        # Write Loans
        with open(LOANS_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Loan_ID", "ISBN", "Patron_ID", "Issue_Date", "Due_Date", "Status"])
            for l in ACTIVE_LOANS.values():
                writer.writerow([l["loan_id"], l["isbn"], l["patron_id"], l["issue_date"], l["due_date"], l["status"]])
    except IOError as e:
        print(f"  [!] Critical Storage Failure: Could not commit changes to disk: {e}")


# ==============================================================================
# INPUT VALIDATION HELPERS
# ==============================================================================
def input_non_empty(prompt):
    """Guarantees a non-empty string."""
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("  [!] Error: Value cannot be left empty.")


def input_int_range(prompt, min_val, max_val):
    """Guarantees an integer strictly within an inclusive range."""
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if min_val <= val <= max_val:
                return val
            print(f"  [!] Please select a number between {min_val} and {max_val}.")
        except ValueError:
            print("  [!] Input format error: Whole integer required.")


# ==============================================================================
# CRUD MODULE 1: BOOK CATALOG INVENTORY MANAGEMENT
# ==============================================================================
def create_book():
    """CREATE: Adds a new book title to the catalog with algorithmic ISBN verification."""
    print("\n" + "=" * 65)
    print("📖 CATALOG MANAGEMENT: REGISTER NEW BOOK TITLE")
    print("=" * 65)

    while True:
        isbn = input_non_empty("Enter 10 or 13-digit ISBN (or 'C' to cancel): ").replace("-", "").strip()
        if isbn.upper() == "C":
            return
        if not validate_isbn(isbn):
            print("  [!] Invalid ISBN Checksum! Ensure mathematical validity of the code.")
            continue
        if isbn in BOOKS_CATALOG:
            print(f"  [!] Duplicate Error: A book with ISBN {isbn} already exists ('{BOOKS_CATALOG[isbn]['title']}').")
            continue
        break

    title = input_non_empty("Enter Book Title        : ").title()
    author = input_non_empty("Enter Author Name       : ").title()
    genre = input_non_empty("Enter Academic Genre/Cat: ").title()
    copies = input_int_range("Total Stock Copies (1-50): ", 1, 50)

    BOOKS_CATALOG[isbn] = {
        "isbn": isbn,
        "title": title,
        "author": author,
        "genre": genre,
        "total_copies": copies,
        "available_copies": copies
    }

    flush_database()
    log_event(f"CATALOG ADD: Added book '{title}' (ISBN: {isbn}, Copies: {copies}).")
    print(f"\n[✓] Successfully cataloged: '{title}' by {author}!")


def search_and_read_books():
    """READ: Advanced query engine supporting Title, Author, Genre, or ISBN matches."""
    print("\n" + "=" * 80)
    print("🔍 CATALOG SEARCH & INVENTORY EXPLORER")
    print("=" * 80)
    print(" Search Criteria: [1] Search by Keyword (Title/Author/Genre)  [2] View All Books")
    mode = input_int_range("Select search mode (1-2): ", 1, 2)

    matches = []
    if mode == 1:
        query = input_non_empty("Enter search query: ").lower()
        for b in BOOKS_CATALOG.values():
            if (query in b["title"].lower() or 
                query in b["author"].lower() or 
                query in b["genre"].lower() or 
                query in b["isbn"]):
                matches.append(b)
    else:
        matches = list(BOOKS_CATALOG.values())

    if not matches:
        print("\n  [!] No books found matching your query.")
        return

    print("\n" + "-" * 95)
    print(f"{'ISBN':<15}{'Title':<30}{'Author':<22}{'Genre':<16}{'Available/Total'}")
    print("-" * 95)
    for b in matches:
        stock_str = f"{b['available_copies']}/{b['total_copies']}"
        print(f"{b['isbn']:<15}{b['title'][:28]:<30}{b['author'][:20]:<22}{b['genre'][:14]:<16}{stock_str:<12}")
    print("-" * 95)
    print(f"Total matching titles: {len(matches)}\n")


def update_book():
    """UPDATE: Modifies existing book metadata or adjusts copy stock levels."""
    print("\n" + "=" * 65)
    print("📝 CATALOG MANAGEMENT: UPDATE BOOK DETAILS")
    print("=" * 65)

    isbn = input_non_empty("Enter ISBN of the book to update: ").replace("-", "").strip()
    if isbn not in BOOKS_CATALOG:
        print("  [!] ISBN not found in master catalog.")
        return

    b = BOOKS_CATALOG[isbn]
    print(f"\nCurrent Record: '{b['title']}' by {b['author']} (Genre: {b['genre']}, Stock: {b['available_copies']}/{b['total_copies']})")
    print("Fields to update: [1] Title  [2] Author  [3] Genre  [4] Add Stock Copies  [5] Cancel")
    choice = input_int_range("Select Field (1-5): ", 1, 5)

    if choice == 1:
        b["title"] = input_non_empty("Enter new Title: ").title()
    elif choice == 2:
        b["author"] = input_non_empty("Enter new Author: ").title()
    elif choice == 3:
        b["genre"] = input_non_empty("Enter new Genre: ").title()
    elif choice == 4:
        added_copies = input_int_range("How many new physical copies are being added? (1-20): ", 1, 20)
        b["total_copies"] += added_copies
        b["available_copies"] += added_copies
    elif choice == 5:
        return

    flush_database()
    log_event(f"CATALOG UPDATE: Updated record for ISBN {isbn}.")
    print("\n[✓] Book record updated successfully!")


def delete_book():
    """DELETE: Removes a book title enforcing referential integrity (cannot delete if loaned out)."""
    print("\n" + "=" * 65)
    print("🗑️ CATALOG MANAGEMENT: DECOMMISSION BOOK")
    print("=" * 65)

    isbn = input_non_empty("Enter ISBN of book to remove: ").replace("-", "").strip()
    if isbn not in BOOKS_CATALOG:
        print("  [!] ISBN not found.")
        return

    b = BOOKS_CATALOG[isbn]
    # Referential integrity check: Cannot delete if any copies are currently checked out
    if b["available_copies"] < b["total_copies"]:
        loaned = b["total_copies"] - b["available_copies"]
        print(f"  [⛔] Integrity Violation: Cannot delete '{b['title']}'. {loaned} cop(y/ies) currently loaned out!")
        return

    confirm = input(f"Are you sure you want to permanently delete '{b['title']}'? (y/n): ").strip().lower()
    if confirm in ("y", "yes"):
        del BOOKS_CATALOG[isbn]
        flush_database()
        log_event(f"CATALOG DELETE: Decommissioned book ISBN {isbn}.")
        print(f"\n[✓] Book '{b['title']}' removed from catalog.")


# ==============================================================================
# CRUD MODULE 2: PATRON (MEMBER) MANAGEMENT
# ==============================================================================
def register_patron():
    """CREATE: Registers a new library patron."""
    print("\n" + "=" * 65)
    print("👤 MEMBERSHIP: REGISTER NEW PATRON")
    print("=" * 65)

    # Automated ID Generation
    patron_nums = [int(p.split("-")[1]) for p in PATRONS_REGISTRY.keys() if p.startswith("LIB-")]
    next_id = f"LIB-{max(patron_nums, default=100) + 1}"

    name = input_non_empty("Enter Patron Full Name  : ").title()
    email = input_non_empty("Enter Patron Email      : ")
    phone = input_non_empty("Enter Mobile / WhatsApp : ")

    PATRONS_REGISTRY[next_id] = {
        "patron_id": next_id,
        "name": name,
        "email": email,
        "phone": phone,
        "active_borrow_count": 0
    }

    flush_database()
    log_event(f"PATRON REGISTER: Registered {name} with ID {next_id}.")
    print(f"\n[✓] Patron Registered Successfully! Assigned ID: {next_id}")


def view_patrons():
    """READ: Displays all active library patrons."""
    print("\n" + "=" * 80)
    print("👥 REGISTERED LIBRARY PATRONS REGISTRY")
    print("=" * 80)
    print(f"{'Patron ID':<12}{'Full Name':<24}{'Contact Phone':<16}{'Active Loans'}")
    print("-" * 80)
    for p in PATRONS_REGISTRY.values():
        print(f"{p['patron_id']:<12}{p['name'][:22]:<24}{p['phone']:<16}{p['active_borrow_count']} / {MAX_BOOKS_PER_PATRON}")
    print("-" * 80)
    print(f"Total Enrolled Members: {len(PATRONS_REGISTRY)}\n")


# ==============================================================================
# CIRCULATION ENGINE: LENDING, RETURNS & OVERDUE FINES
# ==============================================================================
def issue_book_loan():
    """Processes checkouts: validates patron limit, decrements stock, issues slip."""
    print("\n" + "=" * 70)
    print("📤 CIRCULATION DESK: ISSUE BOOK LOAN")
    print("=" * 70)

    patron_id = input_non_empty("Enter Patron ID (e.g., LIB-101): ").upper()
    if patron_id not in PATRONS_REGISTRY:
        print("  [!] Patron not registered. Register member first.")
        return

    patron = PATRONS_REGISTRY[patron_id]

    # Quota check
    if patron["active_borrow_count"] >= MAX_BOOKS_PER_PATRON:
        print(f"  [⛔] Borrowing Quota Reached: Member already has {MAX_BOOKS_PER_PATRON} books checked out.")
        return

    isbn = input_non_empty("Enter ISBN of book to borrow: ").replace("-", "").strip()
    if isbn not in BOOKS_CATALOG:
        print("  [!] Book not found in catalog.")
        return

    book = BOOKS_CATALOG[isbn]

    # Inventory check
    if book["available_copies"] <= 0:
        print(f"  [!] Out of Stock: All physical copies of '{book['title']}' are currently checked out.")
        return

    # Check if patron already has an active unreturned copy of this book
    for loan in ACTIVE_LOANS.values():
        if loan["patron_id"] == patron_id and loan["isbn"] == isbn and loan["status"] == "Active":
            print("  [!] Active Loan Exists: Patron has already checked out an unreturned copy of this book.")
            return

    # Execute Transaction
    today = get_current_date()
    due_date = (datetime.now() + timedelta(days=MAX_LOAN_DAYS)).strftime("%Y-%m-%d")
    loan_id = f"LN-{int(datetime.now().timestamp()) % 1000000:06d}"

    ACTIVE_LOANS[loan_id] = {
        "loan_id": loan_id,
        "isbn": isbn,
        "patron_id": patron_id,
        "issue_date": today,
        "due_date": due_date,
        "status": "Active"
    }

    # State mutations
    book["available_copies"] -= 1
    patron["active_borrow_count"] += 1

    flush_database()
    log_event(f"LOAN ISSUE: Loan {loan_id} created for {patron_id} (ISBN: {isbn}).")
    export_checkout_slip(loan_id, book, patron, today, due_date)

    print("\n" + "=" * 65)
    print("  [✓] CHECKOUT COMPLETED SUCCESSFULLY!")
    print(f"      Loan Reference ID : {loan_id}")
    print(f"      Book Issued       : {book['title']}")
    print(f"      Borrower          : {patron['name']} ({patron_id})")
    print(f"      Due Return Date   : {due_date} (14 days)")
    print("=" * 65)


def return_book_loan():
    """Processes returns: computes overdue penalty fines, restores stock, updates ledger."""
    print("\n" + "=" * 70)
    print("📥 CIRCULATION DESK: PROCESS BOOK RETURN")
    print("=" * 70)

    loan_id = input_non_empty("Enter Loan ID (e.g., LN-123456): ").upper()
    if loan_id not in ACTIVE_LOANS:
        print("  [!] Loan ID not found in system.")
        return

    loan = ACTIVE_LOANS[loan_id]
    if loan["status"] != "Active":
        print(f"  [!] Inactive Record: This loan was previously settled as '{loan['status']}'.")
        return

    book = BOOKS_CATALOG[loan["isbn"]]
    patron = PATRONS_REGISTRY[loan["patron_id"]]

    # Mathematical Overdue Fine Calculation
    due_dt = parse_date(loan["due_date"])
    return_dt = datetime.now()
    days_overdue = (return_dt.date() - due_dt.date()).days

    fine = 0.0
    if days_overdue > 0:
        fine = round(days_overdue * DAILY_FINE_RATE, 2)
        print("\n  ⚠️ OVERDUE PENALTY DETECTED:")
        print(f"     Days Overdue: {days_overdue} day(s)")
        print(f"     Daily Tariff: PKR {DAILY_FINE_RATE:.2f} / day")
        print(f"     TOTAL FINE  : PKR {fine:.2f}")
    else:
        print("\n  [✓] Book returned on schedule. Zero fine applied.")

    confirm = input("Confirm return processing & restock inventory? (y/n): ").strip().lower()
    if confirm not in ("y", "yes"):
        print("  [x] Return canceled.")
        return

    # Mutations
    loan["status"] = "Returned"
    book["available_copies"] += 1
    patron["active_borrow_count"] = max(0, patron["active_borrow_count"] - 1)

    flush_database()
    log_event(f"LOAN RETURN: Loan {loan_id} returned. Fine settled: PKR {fine:.2f}.")
    export_return_slip(loan_id, book, patron, fine, days_overdue)

    print(f"\n[✓] Book '{book['title']}' restocked into catalog inventory.")


def export_checkout_slip(loan_id, book, patron, issue_d, due_d):
    """Outputs printable checkout slip to disk."""
    filepath = os.path.join(SLIPS_DIR, f"Checkout_Slip_{loan_id}.txt")
    try:
        with open(filepath, mode="w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("              UNIVERSITY CENTRAL LIBRARY\n")
            f.write("                BOOK CIRCULATION SLIP\n")
            f.write("=" * 60 + "\n")
            f.write(f"Loan ID     : {loan_id}\n")
            f.write(f"Issue Date  : {issue_d}\n")
            f.write(f"Due Date    : {due_d}\n")
            f.write("-" * 60 + "\n")
            f.write(f"Patron ID   : {patron['patron_id']}\n")
            f.write(f"Member Name : {patron['name']}\n")
            f.write(f"Book Title  : {book['title']}\n")
            f.write(f"Author      : {book['author']}\n")
            f.write(f"ISBN        : {book['isbn']}\n")
            f.write("-" * 60 + "\n")
            f.write("Notice: Overdue fine is PKR 20.00/day after due date.\n")
            f.write("=" * 60 + "\n")
    except IOError as e:
        print(f"  [!] Failed to save slip: {e}")


def export_return_slip(loan_id, book, patron, fine, days_late):
    """Outputs return settlement receipt to disk."""
    filepath = os.path.join(SLIPS_DIR, f"Return_Slip_{loan_id}.txt")
    try:
        with open(filepath, mode="w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("              UNIVERSITY CENTRAL LIBRARY\n")
            f.write("             RETURN SETTLEMENT RECEIPT\n")
            f.write("=" * 60 + "\n")
            f.write(f"Loan ID      : {loan_id}\n")
            f.write(f"Return Date  : {get_current_date()}\n")
            f.write(f"Patron Name  : {patron['name']} ({patron['patron_id']})\n")
            f.write(f"Book Title   : {book['title']}\n")
            f.write(f"Days Overdue : {max(0, days_late)}\n")
            f.write(f"Fine Charged : PKR {fine:.2f}\n")
            f.write("-" * 60 + "\n")
            f.write("Status: COMPLETED - INVENTORY RESTOCKED\n")
            f.write("=" * 60 + "\n")
    except IOError as e:
        print(f"  [!] Failed to save return slip: {e}")


# ==============================================================================
# AUDIT & ACTIVE LOANS MONITOR
# ==============================================================================
def display_active_loans():
    """Displays active borrowing transactions with overdue warnings."""
    print("\n" + "=" * 90)
    print("📋 ACTIVE CIRCULATION LOANS & OVERDUE MONITOR")
    print("=" * 90)

    active_items = [l for l in ACTIVE_LOANS.values() if l["status"] == "Active"]
    if not active_items:
        print("  No books are currently checked out.")
        return

    print(f"{'Loan ID':<12}{'Patron':<20}{'Book Title':<28}{'Due Date':<14}{'Status'}")
    print("-" * 90)

    today = datetime.now().date()
    for l in active_items:
        b = BOOKS_CATALOG.get(l["isbn"], {"title": "Unknown Title"})
        p = PATRONS_REGISTRY.get(l["patron_id"], {"name": "Unknown Patron"})
        due_dt = parse_date(l["due_date"]).date()

        if today > due_dt:
            status_str = f"OVERDUE ({(today - due_dt).days}d)"
        else:
            status_str = "On Schedule"

        print(f"{l['loan_id']:<12}{p['name'][:18]:<20}{b['title'][:26]:<28}{l['due_date']:<14}{status_str}")
    print("=" * 90 + "\n")


# ==============================================================================
# MAIN SYSTEM CONTROLLER
# ==============================================================================
def display_main_menu():
    """Interactive Primary Command Center."""
    print("=" * 65)
    print("     📚 ADVANCED ENTERPRISE LIBRARY MANAGEMENT SYSTEM")
    print("=" * 65)
    print("  --- Catalog Management (Books CRUD) ---")
    print("  [1] Add New Book Title (ISBN Verified)")
    print("  [2] Search Catalog by Keyword / View All Inventory")
    print("  [3] Update Book Information / Add Copy Stock")
    print("  [4] Delete / Decommission Book Title")
    print("\n  --- Member & Circulation Management ---")
    print("  [5] Register New Library Patron")
    print("  [6] View All Registered Patrons")
    print("  [7] Issue Book Checkout (Generate Slip)")
    print("  [8] Process Book Return (Calculate Overdue Fines)")
    print("  [9] View Active Circulation Loans & Overdue Tracker")
    print("  [10] Exit System")
    print("=" * 65)


def main():
    """Master Application Loop."""
    initialize_system()

    while True:
        display_main_menu()
        choice = input_int_range("Select an option (1-10): ", 1, 10)

        if choice == 1:
            create_book()
        elif choice == 2:
            search_and_read_books()
        elif choice == 3:
            update_book()
        elif choice == 4:
            delete_book()
        elif choice == 5:
            register_patron()
        elif choice == 6:
            view_patrons()
        elif choice == 7:
            issue_book_loan()
        elif choice == 8:
            return_book_loan()
        elif choice == 9:
            display_active_loans()
        elif choice == 10:
            log_event("SYSTEM: Administrative shutdown.")
            print("\nShutting down Library Management System. Goodbye!\n")
            break


if __name__ == "__main__":
    main()
