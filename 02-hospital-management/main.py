"""
Project 02: Enterprise Hospital & Patient Ward Management System
Course Level: 1st Semester CS / Programming Fundamentals
Concepts Used:
  - Dictionaries & Nested Dictionaries (In-memory record store)
  - Modular Functions (30+ specialized subroutines)
  - While loops & For loops with break/continue sentinels
  - List comprehensions & tuple unpacking
  - String manipulation & tabular ASCII rendering
  - File I/O: Plaintext receipt generation (.txt) & structured CSV persistence (.csv)
  - Exception handling (ValueError, FileNotFoundError, IOError)
  - Date & time manipulation via datetime standard library
"""

import os
import csv
from datetime import datetime

# ==============================================================================
# GLOBAL DIRECTORIES & PERSISTENCE PATHS
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "hospital_data")
INVOICES_DIR = os.path.join(BASE_DIR, "invoices")
PATIENTS_CSV = os.path.join(DATA_DIR, "patients_database.csv")
ROOMS_CSV = os.path.join(DATA_DIR, "rooms_inventory.csv")
AUDIT_LOG_TXT = os.path.join(DATA_DIR, "audit_log.txt")

# ==============================================================================
# IN-MEMORY CLINICAL DATA STORE
# ==============================================================================
# Room Configurations: Type, Base Rate/Day, Department, Total Available
DEFAULT_ROOM_INVENTORY = {
    "101": {"type": "General Ward", "daily_rate": 1200.0, "status": "Available", "patient_id": None},
    "102": {"type": "General Ward", "daily_rate": 1200.0, "status": "Available", "patient_id": None},
    "103": {"type": "General Ward", "daily_rate": 1200.0, "status": "Available", "patient_id": None},
    "201": {"type": "Semi-Private Room", "daily_rate": 3500.0, "status": "Available", "patient_id": None},
    "202": {"type": "Semi-Private Room", "daily_rate": 3500.0, "status": "Available", "patient_id": None},
    "301": {"type": "Private Deluxe Suite", "daily_rate": 7500.0, "status": "Available", "patient_id": None},
    "302": {"type": "Private Deluxe Suite", "daily_rate": 7500.0, "status": "Available", "patient_id": None},
    "401": {"type": "Intensive Care Unit (ICU)", "daily_rate": 15000.0, "status": "Available", "patient_id": None},
    "402": {"type": "Intensive Care Unit (ICU)", "daily_rate": 15000.0, "status": "Available", "patient_id": None},
}

# Standard Doctors & Departments
DOCTORS_DIRECTORY = {
    "DOC-01": {"name": "Dr. Sarah Khan", "dept": "Cardiology", "fee": 2500.0},
    "DOC-02": {"name": "Dr. Ahmed Raza", "dept": "Neurology", "fee": 3000.0},
    "DOC-03": {"name": "Dr. Fatima Noor", "dept": "General Medicine", "fee": 1500.0},
    "DOC-04": {"name": "Dr. Bilal Siddiqui", "dept": "Orthopedics", "fee": 2200.0},
    "DOC-05": {"name": "Dr. Ayesha Tariq", "dept": "Pediatrics", "fee": 1800.0},
}

# Master Patient Registry: { patient_id: { details... } }
PATIENTS_REGISTRY = {}
ROOMS_REGISTRY = {}


# ==============================================================================
# INITIALIZATION & AUDIT LOGGING
# ==============================================================================
def initialize_storage():
    """Sets up folders and database files if they do not exist."""
    global ROOMS_REGISTRY
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(INVOICES_DIR, exist_ok=True)

    # Initialize Rooms Registry
    ROOMS_REGISTRY = DEFAULT_ROOM_INVENTORY.copy()

    # Create CSV database if not present
    if not os.path.exists(PATIENTS_CSV):
        with open(PATIENTS_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Patient_ID", "Full_Name", "Age", "Gender", "Phone",
                "Blood_Group", "Assigned_Doctor", "Room_Number", "Diagnosis",
                "Admission_Date", "Discharge_Date", "Status", "Total_Billed"
            ])

    # Initialize Audit Log
    if not os.path.exists(AUDIT_LOG_TXT):
        with open(AUDIT_LOG_TXT, mode="w", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] SYSTEM: Hospital Database Initialized.\n")

    load_patients_from_csv()


def log_action(message):
    """Appends an event with a timestamp to the audit trail."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    try:
        with open(AUDIT_LOG_TXT, mode="a", encoding="utf-8") as f:
            f.write(entry)
    except IOError:
        pass


def load_patients_from_csv():
    """Restores saved patient records from disk into the runtime dictionary."""
    global PATIENTS_REGISTRY, ROOMS_REGISTRY
    if not os.path.exists(PATIENTS_CSV):
        return

    try:
        with open(PATIENTS_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                p_id = row["Patient_ID"]
                PATIENTS_REGISTRY[p_id] = {
                    "id": p_id,
                    "name": row["Full_Name"],
                    "age": int(row["Age"]) if row["Age"].isdigit() else 0,
                    "gender": row["Gender"],
                    "phone": row["Phone"],
                    "blood_group": row["Blood_Group"],
                    "doctor": row["Assigned_Doctor"],
                    "room": row["Room_Number"],
                    "diagnosis": row["Diagnosis"],
                    "admission_date": row["Admission_Date"],
                    "discharge_date": row["Discharge_Date"],
                    "status": row["Status"],
                    "total_billed": float(row["Total_Billed"]) if row["Total_Billed"] else 0.0,
                    "medications": [],
                    "lab_tests": []
                }
                # If patient is actively admitted, update room status
                if row["Status"] == "Admitted" and row["Room_Number"] in ROOMS_REGISTRY:
                    ROOMS_REGISTRY[row["Room_Number"]]["status"] = "Occupied"
                    ROOMS_REGISTRY[row["Room_Number"]]["patient_id"] = p_id
    except Exception as e:
        print(f"  [!] Notice: Database sync notice - {e}")


def save_all_patients_to_csv():
    """Flushes active in-memory dictionary back to the persistent CSV file."""
    try:
        with open(PATIENTS_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Patient_ID", "Full_Name", "Age", "Gender", "Phone",
                "Blood_Group", "Assigned_Doctor", "Room_Number", "Diagnosis",
                "Admission_Date", "Discharge_Date", "Status", "Total_Billed"
            ])
            for p in PATIENTS_REGISTRY.values():
                writer.writerow([
                    p["id"], p["name"], p["age"], p["gender"], p["phone"],
                    p["blood_group"], p["doctor"], p["room"], p["diagnosis"],
                    p["admission_date"], p["discharge_date"], p["status"],
                    p.get("total_billed", 0.0)
                ])
    except IOError as e:
        print(f"  [!] Critical File Error: Unable to save patient data: {e}")


# ==============================================================================
# INPUT VALIDATION ROUTINES
# ==============================================================================
def input_non_empty(prompt):
    """Ensures input string contains non-whitespace characters."""
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("  [!] Field error: Value cannot be empty.")


def input_int_range(prompt, min_val, max_val):
    """Validates integer within inclusive boundary."""
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if min_val <= val <= max_val:
                return val
            print(f"  [!] Range error: Enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("  [!] Input error: Integer expected.")


def input_float_range(prompt, min_val, max_val):
    """Validates floating-point numbers within bounds."""
    while True:
        raw = input(prompt).strip()
        try:
            val = float(raw)
            if min_val <= val <= max_val:
                return round(val, 2)
            print(f"  [!] Range error: Value must be between {min_val} and {max_val}.")
        except ValueError:
            print("  [!] Input error: Decimal/float expected.")


def input_blood_group():
    """Forces selection from recognized medical blood groups."""
    valid_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    while True:
        bg = input(f"Enter Blood Group ({', '.join(valid_groups)}): ").strip().upper()
        if bg in valid_groups:
            return bg
        print("  [!] Invalid group. Please input standard classification (e.g. O+, B-).")


def input_gender():
    """Validates gender input."""
    valid_genders = ["Male", "Female", "Other"]
    while True:
        print("Select Gender: [1] Male  [2] Female  [3] Other")
        choice = input_int_range("Choice: ", 1, 3)
        return valid_genders[choice - 1]


# ==============================================================================
# PATIENT ADMISSION & REGISTRATION
# ==============================================================================
def generate_patient_id():
    """Generates unique sequential clinical identification code."""
    now = datetime.now()
    year_prefix = now.strftime("%y")
    existing_nums = [
        int(pid.split("-")[1])
        for pid in PATIENTS_REGISTRY.keys()
        if pid.startswith(f"P{year_prefix}-") and pid.split("-")[1].isdigit()
    ]
    next_num = max(existing_nums, default=0) + 1
    return f"P{year_prefix}-{next_num:04d}"


def display_available_rooms():
    """Prints formatted table of rooms ready for intake."""
    print("\n" + "-" * 70)
    print(f"{'Room #':<10}{'Ward/Type':<30}{'Daily Tariff (PKR)':<20}{'Status'}")
    print("-" * 70)
    available_found = False
    for r_num, info in ROOMS_REGISTRY.items():
        if info["status"] == "Available":
            available_found = True
            print(f"{r_num:<10}{info['type']:<30}{info['daily_rate']:<20.2f}{info['status']}")
    print("-" * 70)
    return available_found


def select_attending_doctor():
    """Presents registered doctor list and returns selected doctor profile."""
    print("\n--- Available Medical Specialists ---")
    doc_keys = list(DOCTORS_DIRECTORY.keys())
    for idx, key in enumerate(doc_keys, start=1):
        doc = DOCTORS_DIRECTORY[key]
        print(f" [{idx}] {doc['name']} - {doc['dept']} (Consultation: PKR {doc['fee']:.2f})")

    sel = input_int_range("Assign Consulting Doctor (1-5): ", 1, len(doc_keys))
    chosen_key = doc_keys[sel - 1]
    return DOCTORS_DIRECTORY[chosen_key]["name"], DOCTORS_DIRECTORY[chosen_key]["fee"]


def admit_new_patient():
    """Full onboarding procedure for admitting a patient to a ward."""
    print("\n" + "=" * 70)
    print("🏥 INTAKE DESK: INPATIENT ADMISSION & BED ASSIGNMENT")
    print("=" * 70)

    # Check bed availability first
    if not display_available_rooms():
        print("  [!] Notice: All wards and ICU rooms are currently occupied.")
        return

    # Select room
    while True:
        room_choice = input_non_empty("Enter Room Number to assign: ")
        if room_choice in ROOMS_REGISTRY:
            if ROOMS_REGISTRY[room_choice]["status"] == "Available":
                break
            else:
                print(f"  [!] Room {room_choice} is already occupied. Choose another.")
        else:
            print("  [!] Room not found in hospital inventory.")

    # Gather patient details
    patient_id = generate_patient_id()
    print(f"Generated Unique Patient ID: {patient_id}")
    name = input_non_empty("Patient Full Name            : ").title()
    age = input_int_range("Patient Age                  : ", 0, 125)
    gender = input_gender()
    phone = input_non_empty("Contact Telephone/Emergency  : ")
    blood_group = input_blood_group()
    doctor_name, doctor_fee = select_attending_doctor()
    diagnosis = input_non_empty("Provisional Diagnosis/Reason : ")
    admission_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Reserve room
    ROOMS_REGISTRY[room_choice]["status"] = "Occupied"
    ROOMS_REGISTRY[room_choice]["patient_id"] = patient_id

    # Construct patient record
    patient_record = {
        "id": patient_id,
        "name": name,
        "age": age,
        "gender": gender,
        "phone": phone,
        "blood_group": blood_group,
        "doctor": doctor_name,
        "doctor_fee": doctor_fee,
        "room": room_choice,
        "diagnosis": diagnosis,
        "admission_date": admission_timestamp,
        "discharge_date": "N/A",
        "status": "Admitted",
        "total_billed": 0.0,
        "medications": [],
        "lab_tests": []
    }

    PATIENTS_REGISTRY[patient_id] = patient_record
    save_all_patients_to_csv()
    log_action(f"ADMIT: Patient {patient_id} ({name}) assigned to Room {room_choice} under {doctor_name}.")

    print("\n" + "=" * 70)
    print(f"✅ Patient {name} admitted successfully!")
    print(f"   Record ID : {patient_id}")
    print(f"   Ward Room : {room_choice} ({ROOMS_REGISTRY[room_choice]['type']})")
    print("=" * 70)


# ==============================================================================
# CLINICAL SERVICES (MEDICATIONS & INVESTIGATIONS)
# ==============================================================================
def add_clinical_services():
    """Appends medications or diagnostic laboratory investigations to an admitted patient."""
    print("\n" + "=" * 70)
    print("🧪 CLINICAL SERVICES, PHARMACY & DIAGNOSTIC BILLING")
    print("=" * 70)

    p_id = input_non_empty("Enter Admitted Patient ID (e.g. P26-0001): ").upper()
    if p_id not in PATIENTS_REGISTRY:
        print("  [!] Error: Patient ID not found.")
        return

    patient = PATIENTS_REGISTRY[p_id]
    if patient["status"] != "Admitted":
        print(f"  [!] Inactive Record: Patient is currently '{patient['status']}'.")
        return

    print(f"\nActive Patient: {patient['name']} | Room: {patient['room']} | Doctor: {patient['doctor']}")
    print("Select Service to Add:")
    print(" [1] Dispense Pharmacy Prescription / Medication")
    print(" [2] Order Diagnostic Lab Investigation / Imaging")
    print(" [3] Return to Main Menu")

    choice = input_int_range("Select (1-3): ", 1, 3)

    if choice == 1:
        med_name = input_non_empty("Enter Medication Name & Dosage : ")
        cost = input_float_range("Medication Cost (PKR)           : ", 10.0, 100000.0)
        patient["medications"].append({"item": med_name, "cost": cost, "time": datetime.now().strftime("%Y-%m-%d %H:%M")})
        log_action(f"PHARMACY: Dispensed '{med_name}' to {p_id} (PKR {cost:.2f}).")
        print(f"  [✓] Logged {med_name} (PKR {cost:.2f}) to patient's active ledger.")

    elif choice == 2:
        test_catalog = [
            ("Complete Blood Count (CBC)", 850.0),
            ("Comprehensive Metabolic Panel", 2200.0),
            ("Chest X-Ray Digital", 1500.0),
            ("12-Lead Electrocardiogram (ECG)", 1200.0),
            ("Abdominal Ultrasound", 3500.0),
            ("Brain MRI Scan", 18000.0),
        ]
        print("\nStandard Diagnostic Packages:")
        for i, (test, fee) in enumerate(test_catalog, 1):
            print(f"   [{i}] {test:<35} : PKR {fee:.2f}")
        print("   [7] Custom Investigation")

        t_sel = input_int_range("Select Test: ", 1, 7)
        if t_sel == 7:
            t_name = input_non_empty("Enter Diagnostic Test Name: ")
            t_fee = input_float_range("Test Price (PKR): ", 100.0, 200000.0)
        else:
            t_name, t_fee = test_catalog[t_sel - 1]

        patient["lab_tests"].append({"test": t_name, "fee": t_fee, "time": datetime.now().strftime("%Y-%m-%d %H:%M")})
        log_action(f"LAB: Prescribed test '{t_name}' to {p_id} (PKR {t_fee:.2f}).")
        print(f"  [✓] Logged test '{t_name}' (PKR {t_fee:.2f}) to ledger.")


# ==============================================================================
# PATIENT DISCHARGE & ITEMIZED INVOICE ENGINE
# ==============================================================================
def discharge_patient():
    """Calculates days stayed, tallies room, doctor, pharmacy, and lab charges, then vacates bed."""
    print("\n" + "=" * 70)
    print("💳 DISCHARGE BILLING & SETTLEMENT COUNTER")
    print("=" * 70)

    p_id = input_non_empty("Enter Patient ID for Discharge: ").upper()
    if p_id not in PATIENTS_REGISTRY:
        print("  [!] Error: Patient ID not found.")
        return

    patient = PATIENTS_REGISTRY[p_id]
    if patient["status"] != "Admitted":
        print(f"  [!] Patient is not actively admitted (Current Status: {patient['status']}).")
        return

    # Compute stay duration
    admission_time = datetime.strptime(patient["admission_date"], "%Y-%m-%d %H:%M:%S")
    discharge_time = datetime.now()
    delta_days = (discharge_time - admission_time).days
    stay_days = max(1, delta_days)  # Minimum 1 billing cycle day

    # Fetch room tariff
    room_number = patient["room"]
    daily_rate = ROOMS_REGISTRY.get(room_number, {}).get("daily_rate", 1500.0)
    total_room_charges = stay_days * daily_rate

    # Doctor fee
    doctor_fee = patient.get("doctor_fee", 2000.0)

    # Pharmacy & Lab charges
    meds_total = sum(m["cost"] for m in patient.get("medications", []))
    labs_total = sum(t["fee"] for t in patient.get("lab_tests", []))

    # Taxes & Discounts
    subtotal = total_room_charges + doctor_fee + meds_total + labs_total
    tax_rate = 0.05  # 5% healthcare surcharge
    tax_amount = round(subtotal * tax_rate, 2)
    grand_total = subtotal + tax_amount

    # Present Final Breakdown
    print("\n" + "=" * 76)
    print("                   SHIFA GENERAL HOSPITAL & SURGICAL CENTER")
    print("                         FINAL DISCHARGE INVOICE")
    print("=" * 76)
    print(f" Patient ID      : {patient['id']:<25} Bed/Room No : {room_number}")
    print(f" Patient Name    : {patient['name']:<25} Attending   : {patient['doctor']}")
    print(f" Admission Date  : {patient['admission_date']}")
    print(f" Discharge Date  : {discharge_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" Duration of Stay: {stay_days} Day(s)")
    print("-" * 76)
    print(f" {'Item Description':<45} {'Units':<10} {'Amount (PKR)':>16}")
    print("-" * 76)
    print(f" Room Rent ({ROOMS_REGISTRY[room_number]['type']}){'':<12} {stay_days:<10} {total_room_charges:>16.2f}")
    print(f" Consultant Physician Rounds & Checkup{'':<9} 1          {doctor_fee:>16.2f}")

    if patient.get("medications"):
        print(f" Pharmacy Prescriptions ({len(patient['medications'])} items){'':<17} --         {meds_total:>16.2f}")
    if patient.get("lab_tests"):
        print(f" Pathology & Radiology Labs ({len(patient['lab_tests'])} tests){'':<14} --         {labs_total:>16.2f}")

    print("-" * 76)
    print(f" {'Subtotal':<57} PKR {subtotal:>12.2f}")
    print(f" {'Hospital Service Levy / Tax (5%)':<57} PKR {tax_amount:>12.2f}")
    print(f" {'GRAND TOTAL DUE':<57} PKR {grand_total:>12.2f}")
    print("=" * 76)

    confirm = input("Confirm payment settlement and finalize discharge? (y/n): ").strip().lower()
    if confirm not in ("y", "yes"):
        print("  [x] Discharge aborted. Patient remains marked as Admitted.")
        return

    # Update patient record
    patient["status"] = "Discharged"
    patient["discharge_date"] = discharge_time.strftime("%Y-%m-%d %H:%M:%S")
    patient["total_billed"] = grand_total

    # Free the room
    if room_number in ROOMS_REGISTRY:
        ROOMS_REGISTRY[room_number]["status"] = "Available"
        ROOMS_REGISTRY[room_number]["patient_id"] = None

    # Persist
    save_all_patients_to_csv()
    export_invoice_to_file(patient, stay_days, total_room_charges, doctor_fee, meds_total, labs_total, subtotal, tax_amount, grand_total)
    log_action(f"DISCHARGE: Patient {p_id} cleared and room {room_number} freed. Total settled: PKR {grand_total:.2f}.")

    print(f"\n[✓] Patient {patient['name']} officially discharged. Invoice stored to /invoices/.")


def export_invoice_to_file(patient, days, room_fee, doc_fee, meds, labs, sub, tax, total):
    """Exports structured plain-text bill to invoices directory."""
    filename = f"Invoice_{patient['id']}.txt"
    filepath = os.path.join(INVOICES_DIR, filename)

    try:
        with open(filepath, mode="w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write("           HOSPITAL CARE MANAGEMENT SYSTEM - OFFICIAL RECEIPT\n")
            f.write("=" * 70 + "\n")
            f.write(f"Invoice Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Patient ID   : {patient['id']}\n")
            f.write(f"Full Name    : {patient['name']}\n")
            f.write(f"Age / Gender : {patient['age']} yrs / {patient['gender']}\n")
            f.write(f"Contact      : {patient['phone']}\n")
            f.write(f"Consultant   : {patient['doctor']}\n")
            f.write(f"Ward Room    : {patient['room']}\n")
            f.write(f"Admitted     : {patient['admission_date']}\n")
            f.write(f"Discharged   : {patient['discharge_date']}\n")
            f.write(f"Total Days   : {days}\n")
            f.write("-" * 70 + "\n")
            f.write(f"Room Charges ({days} days)           : PKR {room_fee:.2f}\n")
            f.write(f"Doctor Professional Services         : PKR {doc_fee:.2f}\n")
            f.write(f"Pharmacy Medications Dispensed       : PKR {meds:.2f}\n")
            f.write(f"Pathology & Laboratory Investigations: PKR {labs:.2f}\n")
            f.write("-" * 70 + "\n")
            f.write(f"Net Subtotal                         : PKR {sub:.2f}\n")
            f.write(f"Healthcare Service Surcharge (5%)    : PKR {tax:.2f}\n")
            f.write(f"TOTAL SETTLED PAYMENT                : PKR {total:.2f}\n")
            f.write("=" * 70 + "\n")
            f.write("Status: PAID IN FULL - THANK YOU\n")
    except IOError as e:
        print(f"  [!] Failed to save receipt file: {e}")


# ==============================================================================
# REPORTING, RECORD SEARCH & INVENTORY STATUS
# ==============================================================================
def search_patient_records():
    """Queries master patient store by ID, Full Name, or Telephone Number."""
    print("\n" + "=" * 70)
    print("🔍 PATIENT RECORD SEARCH")
    print("=" * 70)
    query = input_non_empty("Enter Patient ID, Name, or Phone to query: ").lower()

    matches = [
        p for p in PATIENTS_REGISTRY.values()
        if query in p["id"].lower() or query in p["name"].lower() or query in p["phone"].lower()
    ]

    if not matches:
        print(f"  [!] No matching patient profiles found for '{query}'.")
        return

    print("\n" + "=" * 90)
    print(f"{'ID':<11}{'Full Name':<22}{'Age/Sex':<10}{'Doctor':<20}{'Room':<8}{'Status':<12}{'Diagnosis'}")
    print("=" * 90)
    for p in matches:
        age_sex = f"{p['age']}/{p['gender'][0]}"
        print(f"{p['id']:<11}{p['name'][:20]:<22}{age_sex:<10}{p['doctor'][:18]:<20}{p['room']:<8}{p['status']:<12}{p['diagnosis']}")
    print("=" * 90 + "\n")


def display_ward_occupancy():
    """Displays real-time breakdown of all hospital beds and current occupants."""
    print("\n" + "=" * 75)
    print("🏥 REAL-TIME WARD OCCUPANCY & BED TRACKER")
    print("=" * 75)
    print(f"{'Room #':<8}{'Ward Tier':<26}{'Daily Tariff':<16}{'Status':<12}{'Occupant'}")
    print("-" * 75)
    total_rooms = len(ROOMS_REGISTRY)
    occupied_count = 0

    for r_no, r_info in ROOMS_REGISTRY.items():
        occupant_display = "None"
        if r_info["status"] == "Occupied":
            occupied_count += 1
            pid = r_info["patient_id"]
            pname = PATIENTS_REGISTRY.get(pid, {}).get("name", "Unknown")
            occupant_display = f"{pid} ({pname[:10]})"

        print(f"{r_no:<8}{r_info['type']:<26}PKR {r_info['daily_rate']:<12.2f}{r_info['status']:<12}{occupant_display}")

    available_count = total_rooms - occupied_count
    occupancy_pct = (occupied_count / total_rooms) * 100 if total_rooms > 0 else 0.0

    print("-" * 75)
    print(f"Summary: Total Beds: {total_rooms} | Occupied: {occupied_count} | Available: {available_count} | Occupancy Rate: {occupancy_pct:.1f}%")
    print("=" * 75 + "\n")


def display_hospital_metrics():
    """Generates managerial executive summary of clinical operations."""
    print("\n" + "=" * 70)
    print("📊 HOSPITAL EXECUTIVE ANALYTICS DASHBOARD")
    print("=" * 70)

    total_registered = len(PATIENTS_REGISTRY)
    currently_admitted = sum(1 for p in PATIENTS_REGISTRY.values() if p["status"] == "Admitted")
    discharged_count = sum(1 for p in PATIENTS_REGISTRY.values() if p["status"] == "Discharged")
    total_revenue = sum(p.get("total_billed", 0.0) for p in PATIENTS_REGISTRY.values())

    print(f" Lifetime Registered Patients   : {total_registered}")
    print(f" Currently In-Hospital Patients : {currently_admitted}")
    print(f" Successfully Discharged Cases  : {discharged_count}")
    print(f" Total Revenue Generated        : PKR {total_revenue:,.2f}")

    # Doctor patient loads
    print("\nDoctor Caseload Breakdown:")
    doc_counts = {}
    for p in PATIENTS_REGISTRY.values():
        doc = p.get("doctor", "Unassigned")
        doc_counts[doc] = doc_counts.get(doc, 0) + 1

    for doc, count in doc_counts.items():
        bar = "█" * count
        print(f"  {doc:<25} : {count:02d} patient(s) {bar}")
    print("=" * 70 + "\n")


def display_audit_logs():
    """Outputs recent entries from audit trail."""
    print("\n" + "=" * 75)
    print("📋 SYSTEM AUDIT & TRANSACTION LOGS")
    print("=" * 75)
    if not os.path.exists(AUDIT_LOG_TXT):
        print("  [!] No logs recorded.")
        return

    try:
        with open(AUDIT_LOG_TXT, mode="r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-15:]:  # Display last 15 actions
                print(line.strip())
    except IOError as e:
        print(f"  [!] Unable to read audit log: {e}")
    print("=" * 75 + "\n")


# ==============================================================================
# MAIN SYSTEM CONTROLLER
# ==============================================================================
def display_main_menu():
    """Outputs primary interactive terminal choices."""
    print("=" * 65)
    print("     🏥 SHIFA CLINICAL WARD & HOSPITAL MANAGEMENT SYSTEM")
    print("=" * 65)
    print("  [1] Admit New Patient & Allocate Bed")
    print("  [2] Prescribe Medications or Lab Investigations")
    print("  [3] Process Patient Discharge & Generate Final Bill")
    print("  [4] View Real-Time Bed & Ward Occupancy Status")
    print("  [5] Search Patient Records by ID, Name, or Phone")
    print("  [6] View Hospital Executive Analytics & Doctor Caseloads")
    print("  [7] View System Audit Log")
    print("  [8] Open Saved Data & Invoice Folder Locations")
    print("  [9] Exit System")
    print("=" * 65)


def main():
    """Main program entry loop."""
    initialize_storage()

    while True:
        display_main_menu()
        choice = input_int_range("Select an option (1-9): ", 1, 9)

        if choice == 1:
            admit_new_patient()
        elif choice == 2:
            add_clinical_services()
        elif choice == 3:
            discharge_patient()
        elif choice == 4:
            display_ward_occupancy()
        elif choice == 5:
            search_patient_records()
        elif choice == 6:
            display_hospital_metrics()
        elif choice == 7:
            display_audit_logs()
        elif choice == 8:
            print(f"\n  [i] CSV Records Database : {PATIENTS_CSV}")
            print(f"  [i] Invoices Directory   : {INVOICES_DIR}")
            print(f"  [i] Audit Trail Log      : {AUDIT_LOG_TXT}\n")
        elif choice == 9:
            log_action("SYSTEM: Operator logged out. Graceful shutdown.")
            print("\nShutting down Hospital Management Console. Goodbye!\n")
            break


if __name__ == "__main__":
    main()
