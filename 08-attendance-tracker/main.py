"""
Project 08: Enterprise Automated Attendance Tracker & Academic Eligibility Engine
Course Level: 1st/2nd Semester CS - Advanced Programming Fundamentals
Concepts Used:
  - Advanced Date & Time Manipulation (datetime, time, timedelta)
  - Persistent Multi-Column CSV Matrix Handling (Reading & Dynamic Row/Column Slicing)
  - Dictionaries, Tuples, and Sets for Fast O(1) Lookups & Duplicate Guards
  - Dynamic Punctuality Classifications (Present, Late Arrival, Absent, Excused)
  - Statistical Metric Aggregations & Percentage Deficit Alarms (< 75% Rule)
  - Defensive Exception Handling & Formatted String Reports
"""

import os
import csv
from datetime import datetime, time, timedelta

# ==============================================================================
# GLOBAL CONFIGURATION & DATA STORAGE CONSTANTS
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "attendance_data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

ROSTER_CSV = os.path.join(DATA_DIR, "students_roster.csv")
ATTENDANCE_CSV = os.path.join(DATA_DIR, "attendance_matrix.csv")
AUDIT_LOG_TXT = os.path.join(DATA_DIR, "tracker_audit_log.txt")

# Institutional Attendance Policy Rules
SESSION_START_TIME = time(9, 0, 0)      # 09:00:00 AM Standard Class Start
GRACE_PERIOD_MINUTES = 15               # Until 09:15:00 AM -> Marked "Present"
LATE_THRESHOLD_MINUTES = 45             # 09:16 AM to 09:45 AM -> Marked "Late"
                                        # After 09:45 AM -> Marked "Absent"
MINIMUM_ATTENDANCE_PCT = 75.0           # University Examination Eligibility Threshold

# In-Memory Registers
# Roster: { roll_no: { "roll_no", "name", "department", "semester", "rfid_uid" } }
STUDENTS_ROSTER = {}
# Attendance Matrix: { roll_no: { date_str: status_str } }
ATTENDANCE_MATRIX = {}
# Recorded unique dates list
RECORDED_DATES = []


# ==============================================================================
# SYSTEM INITIALIZATION & PERSISTENCE
# ==============================================================================
def initialize_system():
    """Initializes local directories and loads database files."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    if not os.path.exists(AUDIT_LOG_TXT):
        with open(AUDIT_LOG_TXT, mode="w", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] SYSTEM: Attendance Tracker Online.\n")

    # Seed master students roster if missing
    if not os.path.exists(ROSTER_CSV):
        default_students = [
            ["SE-2026-01", "Hamza Ali", "Software Engineering", "1st", "RFID-0911"],
            ["SE-2026-02", "Ayesha Khan", "Software Engineering", "1st", "RFID-0912"],
            ["SE-2026-03", "Bilal Ahmed", "Computer Science", "1st", "RFID-0913"],
            ["SE-2026-04", "Fatima Noor", "Computer Science", "1st", "RFID-0914"],
            ["SE-2026-05", "Zainab Tariq", "Data Science", "1st", "RFID-0915"],
            ["SE-2026-06", "Usman Shah", "Software Engineering", "1st", "RFID-0916"],
            ["SE-2026-07", "Mahnoor Fatima", "Computer Science", "1st", "RFID-0917"]
        ]
        with open(ROSTER_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Roll_No", "Full_Name", "Department", "Semester", "RFID_UID"])
            writer.writerows(default_students)

    load_roster_and_matrix()


def log_audit(message):
    """Appends an event to the local audit trail."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(AUDIT_LOG_TXT, mode="a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except IOError:
        pass


def load_roster_and_matrix():
    """Hydrates student profiles and attendance records into memory."""
    global STUDENTS_ROSTER, ATTENDANCE_MATRIX, RECORDED_DATES
    STUDENTS_ROSTER.clear()
    ATTENDANCE_MATRIX.clear()
    RECORDED_DATES = []

    # 1. Load Roster
    with open(ROSTER_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            r_no = row["Roll_No"]
            STUDENTS_ROSTER[r_no] = {
                "roll_no": r_no,
                "name": row["Full_Name"],
                "dept": row["Department"],
                "semester": row["Semester"],
                "rfid": row["RFID_UID"]
            }
            ATTENDANCE_MATRIX[r_no] = {}

    # 2. Load Attendance Matrix
    if os.path.exists(ATTENDANCE_CSV):
        with open(ATTENDANCE_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            if headers and len(headers) > 2:
                RECORDED_DATES = headers[2:]  # Columns 0: Roll_No, 1: Name, 2+: Dates
                for row in reader:
                    if not row:
                        continue
                    r_no = row[0]
                    if r_no in ATTENDANCE_MATRIX:
                        for idx, d in enumerate(RECORDED_DATES):
                            status_val = row[2 + idx] if len(row) > (2 + idx) else "Absent"
                            ATTENDANCE_MATRIX[r_no][d] = status_val


def commit_attendance_matrix():
    """Flushes active attendance records into the persistent dynamic CSV matrix."""
    try:
        headers = ["Roll_No", "Full_Name"] + RECORDED_DATES
        with open(ATTENDANCE_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for r_no, profile in STUDENTS_ROSTER.items():
                row = [r_no, profile["name"]]
                for d in RECORDED_DATES:
                    row.append(ATTENDANCE_MATRIX.get(r_no, {}).get(d, "Absent"))
                writer.writerow(row)
    except IOError as e:
        print(f"  [!] Critical Storage Failure: Could not commit matrix: {e}")


# ==============================================================================
# INPUT VALIDATION UTILITIES
# ==============================================================================
def input_non_empty(prompt):
    """Guarantees non-empty text input."""
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("  [!] Field error: Value cannot be left blank.")


def input_int_range(prompt, min_val, max_val):
    """Guarantees valid integer within inclusive range."""
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if min_val <= val <= max_val:
                return val
            print(f"  [!] Range error: Enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("  [!] Input format error: Integer expected.")


# ==============================================================================
# ATTENDANCE RECORDING ENGINES
# ==============================================================================
def get_or_create_session_date():
    """Returns target date string formatted as YYYY-MM-DD."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    print(f"\nDefault session date is today: [{today_str}]")
    custom = input("Use today's date? (y/n, enter 'n' for custom historical date): ").strip().lower()

    if custom in ("n", "no"):
        while True:
            date_input = input_non_empty("Enter Date (YYYY-MM-DD): ")
            try:
                valid_date = datetime.strptime(date_input, "%Y-%m-%d")
                target_str = valid_date.strftime("%Y-%m-%d")
                break
            except ValueError:
                print("  [!] Invalid date format. Use YYYY-MM-DD (e.g., 2026-10-31).")
    else:
        target_str = today_str

    if target_str not in RECORDED_DATES:
        RECORDED_DATES.append(target_str)
        RECORDED_DATES.sort()

    return target_str


def conduct_manual_roll_call():
    """BATCH MODE: Iterates through entire enrolled roster for verbal roll call."""
    print("\n" + "=" * 70)
    print("📋 BATCH CLASSROOM ROLL CALL SESSION")
    print("=" * 70)

    target_date = get_or_create_session_date()
    print(f"Conducting Roll Call for Date: {target_date}")
    print("Enter status for each student: [P] Present | [A] Absent | [L] Late | [E] Excused")
    print("-" * 70)

    status_map = {"P": "Present", "A": "Absent", "L": "Late", "E": "Excused"}

    for idx, (r_no, student) in enumerate(STUDENTS_ROSTER.items(), start=1):
        prev = ATTENDANCE_MATRIX.get(r_no, {}).get(target_date, None)
        prev_disp = f" (Previously: {prev})" if prev else ""

        while True:
            inp = input(f"[{idx}/{len(STUDENTS_ROSTER)}] {r_no} - {student['name']:<22}{prev_disp}: ").strip().upper()
            if inp in status_map:
                ATTENDANCE_MATRIX[r_no][target_date] = status_map[inp]
                break
            print("    [!] Invalid status. Enter P, A, L, or E.")

    commit_attendance_matrix()
    log_audit(f"ROLL CALL: Conducted batch attendance for {target_date} ({len(STUDENTS_ROSTER)} students).")
    print(f"\n[✓] Roll call for {target_date} saved successfully to matrix database!\n")


def simulate_smart_rfid_checkin():
    """LIVE CHECK-IN: Evaluates arrival timestamp against institutional thresholds."""
    print("\n" + "=" * 75)
    print("🪪 SMART CARD / RFID & BIOMETRIC GATEWAY SIMULATION")
    print("=" * 75)

    target_date = datetime.now().strftime("%Y-%m-%d")
    if target_date not in RECORDED_DATES:
        RECORDED_DATES.append(target_date)
        RECORDED_DATES.sort()

    print(f" Active Date : {target_date}")
    print(f" Class Start : {SESSION_START_TIME.strftime('%I:%M %p')}")
    print(f" Grace Cutoff: +{GRACE_PERIOD_MINUTES} mins (Present) | Late Cutoff: +{LATE_THRESHOLD_MINUTES} mins (Late)")
    print("-" * 75)

    identifier = input_non_empty("Scan RFID Tag or Enter Roll No: ").strip().upper()

    # Match by Roll Number or RFID UID
    matched_student = None
    for s in STUDENTS_ROSTER.values():
        if s["roll_no"].upper() == identifier or s["rfid"].upper() == identifier:
            matched_student = s
            break

    if not matched_student:
        print(f"  [⛔] ACCESS REJECTED: Tag / Roll No '{identifier}' not found on registered roster.")
        log_audit(f"GATEWAY REJECT: Unrecognized identifier '{identifier}'.")
        return

    r_no = matched_student["roll_no"]

    # Check for duplicate check-in on the same date
    if target_date in ATTENDANCE_MATRIX.get(r_no, {}):
        existing_status = ATTENDANCE_MATRIX[r_no][target_date]
        print(f"\n  [!] Duplicate Check-In Guard:")
        print(f"      Student: {matched_student['name']} ({r_no})")
        print(f"      Already checked in for {target_date} as: '{existing_status}'.")
        return

    # Check-in timestamp selection
    print("\nCheck-in Timestamp Method:")
    print("  [1] Live Clock Time (Current Exact Minute)")
    print("  [2] Simulate Custom Check-In Time (HH:MM 24-hr format)")
    t_opt = input_int_range("Select (1-2): ", 1, 2)

    if t_opt == 1:
        check_time = datetime.now().time()
    else:
        while True:
            t_str = input_non_empty("Enter Arrival Time (HH:MM, e.g., 09:12 or 09:40): ")
            try:
                parsed_t = datetime.strptime(t_str, "%H:%M").time()
                check_time = parsed_t
                break
            except ValueError:
                print("  [!] Format error. Use HH:MM in 24-hour time.")

    # Mathematical Punctuality Classification
    arrival_dt = datetime.combine(datetime.today(), check_time)
    start_dt = datetime.combine(datetime.today(), SESSION_START_TIME)
    diff_minutes = (arrival_dt - start_dt).total_seconds() / 60.0

    if diff_minutes <= GRACE_PERIOD_MINUTES:
        status = "Present"
        tag_icon = "🟢"
    elif diff_minutes <= LATE_THRESHOLD_MINUTES:
        status = "Late"
        tag_icon = "🟡"
    else:
        status = "Absent"
        tag_icon = "🔴"

    ATTENDANCE_MATRIX[r_no][target_date] = status
    commit_attendance_matrix()
    log_audit(f"GATEWAY PASS: {r_no} ({matched_student['name']}) checked in at {check_time.strftime('%H:%M:%S')} -> {status}.")

    print("\n" + "=" * 65)
    print(f"  {tag_icon} ATTENDANCE REGISTERED")
    print(f"      Student     : {matched_student['name']} ({r_no})")
    print(f"      Department  : {matched_student['dept']}")
    print(f"      Time Logged : {check_time.strftime('%I:%M:%S %p')} (Offset: {diff_minutes:+.1f} mins)")
    print(f"      Status      : {status.upper()}")
    print("=" * 65)


# ==============================================================================
# ANALYTICS, MATRIX VIEWER & DEFICIT REPORTS
# ==============================================================================
def display_attendance_matrix():
    """Renders formatted multi-column attendance grid."""
    print("\n" + "=" * 95)
    print("📊 MASTER ATTENDANCE MATRIX & LOG RECORD")
    print("=" * 95)

    if not RECORDED_DATES:
        print("  [!] No attendance sessions recorded on disk.")
        return

    # Header Row
    header_str = f"{'Roll No':<13}{'Student Name':<20}"
    for d in RECORDED_DATES[-6:]:  # Show last 6 recorded days
        header_str += f"{d[5:]:<10}"  # Display MM-DD
    header_str += f"{'Total Pct':<10}"
    print(header_str)
    print("-" * 95)

    for r_no, profile in STUDENTS_ROSTER.items():
        row_str = f"{r_no:<13}{profile['name'][:18]:<20}"
        total_p = 0
        total_days = len(RECORDED_DATES)

        for d in RECORDED_DATES[-6:]:
            st = ATTENDANCE_MATRIX.get(r_no, {}).get(d, "Absent")
            code = "Pres" if st == "Present" else ("Late" if st == "Late" else ("Excs" if st == "Excused" else "Absn"))
            row_str += f"{code:<10}"

        # Calculate lifetime percentage
        for d in RECORDED_DATES:
            st = ATTENDANCE_MATRIX.get(r_no, {}).get(d, "Absent")
            if st in ("Present", "Excused"):
                total_p += 1.0
            elif st == "Late":
                total_p += 0.5  # 2 lates = 1 absence penalty

        pct = (total_p / total_days) * 100 if total_days > 0 else 0.0
        row_str += f"{pct:>6.1f}%"
        print(row_str)

    print("=" * 95)
    print("Legend: Pres = Present | Late = Late (0.5 credit) | Absn = Absent | Excs = Excused\n")


def generate_short_attendance_report():
    """Calculates students failing the institutional 75% attendance quota and exports report."""
    print("\n" + "=" * 80)
    print("⚠️ ACADEMIC DEFICIT WARNING: ATTENDANCE SHORTAGE (< 75%)")
    print("=" * 80)

    if not RECORDED_DATES:
        print("  [!] Insufficient data. Conduct attendance sessions first.")
        return

    total_sessions = len(RECORDED_DATES)
    defaulters = []

    for r_no, profile in STUDENTS_ROSTER.items():
        effective_score = 0.0
        p_count = 0
        l_count = 0
        a_count = 0

        for d in RECORDED_DATES:
            st = ATTENDANCE_MATRIX.get(r_no, {}).get(d, "Absent")
            if st in ("Present", "Excused"):
                effective_score += 1.0
                p_count += 1
            elif st == "Late":
                effective_score += 0.5
                l_count += 1
            else:
                a_count += 1

        pct = round((effective_score / total_sessions) * 100, 1)

        if pct < MINIMUM_ATTENDANCE_PCT:
            defaulters.append({
                "roll_no": r_no,
                "name": profile["name"],
                "dept": profile["dept"],
                "present": p_count,
                "late": l_count,
                "absent": a_count,
                "percentage": pct
            })

    if not defaulters:
        print(f"  [✓] Outstanding Compliance: 100% of students meet or exceed the {MINIMUM_ATTENDANCE_PCT}% threshold!")
        return

    print(f"{'Roll No':<14}{'Student Name':<22}{'Present':<9}{'Late':<8}{'Absent':<8}{'Score Pct':<10}{'Status'}")
    print("-" * 80)
    for d in defaulters:
        print(f"{d['roll_no']:<14}{d['name'][:20]:<22}{d['present']:<9}{d['late']:<8}{d['absent']:<8}{d['percentage']:<10.1f}DEBARRED")
    print("-" * 80)
    print(f"Critical Warning: {len(defaulters)} student(s) currently ineligible for terminal university exams.")

    # Export Formal Warning Sheet
    filepath = os.path.join(REPORTS_DIR, "Short_Attendance_Warning_Report.txt")
    try:
        with open(filepath, mode="w", encoding="utf-8") as f:
            f.write("=" * 75 + "\n")
            f.write("          UNIVERSITY ACADEMIC REGULATORY COMMITTEE\n")
            f.write("             DEBARRED ATTENDANCE DEFICIT NOTICE\n")
            f.write("=" * 75 + "\n")
            f.write(f"Generated On          : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Working Sessions: {total_sessions}\n")
            f.write(f"Mandated Threshold    : {MINIMUM_ATTENDANCE_PCT}%\n")
            f.write("-" * 75 + "\n")
            f.write(f"{'Roll No':<15}{'Student Name':<25}{'Attendance Pct':<18}{'Action Required'}\n")
            f.write("-" * 75 + "\n")
            for d in defaulters:
                f.write(f"{d['roll_no']:<15}{d['name']:<25}{d['percentage']:<18.1f}Exams Withheld\n")
            f.write("=" * 75 + "\n")
            f.write("Notice: Immediate submission of medical or institutional leaves required.\n")
        print(f"\n[✓] Defaulter notice exported to: reports/Short_Attendance_Warning_Report.txt\n")
    except IOError as e:
        print(f"  [!] Failed to export warning sheet: {e}")


def export_monthly_audit_slip():
    """Generates comprehensive ASCII audit sheet of the entire matrix."""
    timestamp_str = datetime.now().strftime("%Y-%m-%d")
    filepath = os.path.join(REPORTS_DIR, f"Attendance_Audit_{timestamp_str}.txt")

    try:
        with open(filepath, mode="w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("           FACULTY ATTENDANCE AUDIT & COMPLIANCE SUMMARY\n")
            f.write("=" * 80 + "\n")
            f.write(f"Audit Date           : {timestamp_str}\n")
            f.write(f"Total Academic Days  : {len(RECORDED_DATES)}\n")
            f.write(f"Enrolled Cohort Size : {len(STUDENTS_ROSTER)}\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Roll No':<15}{'Student Name':<25}{'Present':<10}{'Late':<8}{'Absent':<8}{'Overall %'}\n")
            f.write("-" * 80 + "\n")

            total_sessions = max(1, len(RECORDED_DATES))
            for r_no, profile in STUDENTS_ROSTER.items():
                p_c = sum(1 for d in RECORDED_DATES if ATTENDANCE_MATRIX.get(r_no, {}).get(d) in ("Present", "Excused"))
                l_c = sum(1 for d in RECORDED_DATES if ATTENDANCE_MATRIX.get(r_no, {}).get(d) == "Late")
                a_c = sum(1 for d in RECORDED_DATES if ATTENDANCE_MATRIX.get(r_no, {}).get(d) == "Absent")
                pct = ((p_c + (0.5 * l_c)) / total_sessions) * 100

                f.write(f"{r_no:<15}{profile['name']:<25}{p_c:<10}{l_c:<8}{a_c:<8}{pct:.1f}%\n")

            f.write("=" * 80 + "\n")
            f.write("Certified Official Academic Record.\n")
        print(f"\n[✓] Monthly audit sheet exported to: {filepath}\n")
    except IOError as e:
        print(f"  [!] Failed to export audit slip: {e}")


# ==============================================================================
# ROSTER REGISTRATION (ADD STUDENT)
# ==============================================================================
def add_new_student():
    """Registers a new student profile and assigns an RFID identifier."""
    print("\n" + "=" * 65)
    print("👤 ENROLLMENT: REGISTER NEW STUDENT")
    print("=" * 65)

    roll_no = input_non_empty("Enter Unique Roll Number (e.g., SE-2026-08): ").upper()
    if roll_no in STUDENTS_ROSTER:
        print(f"  [!] Duplicate Error: Roll No '{roll_no}' already exists.")
        return

    name = input_non_empty("Enter Student Full Name : ").title()
    dept = input_non_empty("Enter Academic Dept     : ").title()
    semester = input_non_empty("Enter Current Semester  : ")
    rfid = f"RFID-{random_rfid := 1000 + len(STUDENTS_ROSTER) + 1}"

    STUDENTS_ROSTER[roll_no] = {
        "roll_no": roll_no,
        "name": name,
        "dept": dept,
        "semester": semester,
        "rfid": rfid
    }
    ATTENDANCE_MATRIX[roll_no] = {}

    # Append to CSV
    try:
        with open(ROSTER_CSV, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([roll_no, name, dept, semester, rfid])
        commit_attendance_matrix()
        log_audit(f"ENROLL: Student {roll_no} ({name}) registered with Tag {rfid}.")
        print(f"\n[✓] Student {name} enrolled successfully with RFID Tag: {rfid}!")
    except IOError as e:
        print(f"  [!] Failed to save student to database: {e}")


# ==============================================================================
# MAIN APPLICATION CONTROLLER
# ==============================================================================
def display_main_menu():
    """Primary navigation menu."""
    print("=" * 65)
    print("     ⏰ AUTOMATED ATTENDANCE TRACKER & ELIGIBILITY ENGINE")
    print("=" * 65)
    print("  --- Attendance Recording Operations ---")
    print("  [1] Conduct Manual Classroom Roll Call (Batch Mode)")
    print("  [2] Simulate Smart Biometric / RFID Gateway Check-In")
    print("\n  --- Attendance Analytics & University Audits ---")
    print("  [3] View Complete Multi-Date Attendance Matrix")
    print("  [4] Run Short-Attendance Defaulters Audit (< 75% Rule)")
    print("  [5] Export Official Monthly Attendance Summary Report")
    print("\n  --- Roster & Administrative Settings ---")
    print("  [6] Enroll New Student to Roster")
    print("  [7] View System Audit Log")
    print("  [8] Exit System")
    print("=" * 65)


def display_audit_logs():
    """Outputs recent audit trails."""
    print("\n" + "=" * 75)
    print("📜 HARDWARE & SESSION AUDIT TRAIL")
    print("=" * 75)
    if not os.path.exists(AUDIT_LOG_TXT):
        print("  [!] Audit log empty.")
        return

    try:
        with open(AUDIT_LOG_TXT, mode="r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-10:]:
                print(" " + line.strip())
    except IOError as e:
        print(f"  [!] Could not read logs: {e}")
    print("=" * 75 + "\n")


def main():
    """Primary application execution loop."""
    initialize_system()

    while True:
        display_main_menu()
        choice = input_int_range("Select an option (1-8): ", 1, 8)

        if choice == 1:
            conduct_manual_roll_call()
        elif choice == 2:
            simulate_smart_rfid_checkin()
        elif choice == 3:
            display_attendance_matrix()
        elif choice == 4:
            generate_short_attendance_report()
        elif choice == 5:
            export_monthly_audit_slip()
        elif choice == 6:
            add_new_student()
        elif choice == 7:
            display_audit_logs()
        elif choice == 8:
            log_audit("SYSTEM: Operator logged out. Graceful shutdown.")
            print("\nShutting down Attendance Engine. Goodbye!\n")
            break


if __name__ == "__main__":
    main()
