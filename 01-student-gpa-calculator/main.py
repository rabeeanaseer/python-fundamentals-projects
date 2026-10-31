"""
Project 01: Comprehensive Student Grading, GPA Calculator & Academic Records System
Course Level: 1st Semester CS / Programming Fundamentals
Concepts Used: 
  - Functions & Modularity
  - Loops (for, while, nested loops)
  - Data Structures (Lists, Tuples, Dictionaries, Nested Dictionaries)
  - String Formatting & Dynamic Table Rendering
  - File I/O (Persistent CSV Database and Text Report Exporter)
  - Input Validation & Exception Handling (try/except)
  - Statistical Aggregations (Min, Max, Mean, Weighted Averages)
"""

import os
import csv
from datetime import datetime

# ==============================================================================
# GLOBAL CONFIGURATION & DATA STORAGE CONSTANTS
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_PATH = os.path.join(BASE_DIR, "records.csv")
TXT_REPORTS_DIR = os.path.join(BASE_DIR, "transcripts")

# Standard 4.0 GPA Conversion Scale (Percentage, Letter Grade, Points, Remark)
GRADE_SCALE = [
    (85.0, 100.0, "A",  4.00, "Exceptional"),
    (80.0, 84.99, "A-", 3.70, "Excellent"),
    (75.0, 79.99, "B+", 3.30, "Very Good"),
    (70.0, 74.99, "B",  3.00, "Good"),
    (65.0, 69.99, "B-", 2.70, "Above Average"),
    (61.0, 64.99, "C+", 2.30, "Average"),
    (58.0, 60.99, "C",  2.00, "Satisfactory"),
    (55.0, 57.99, "C-", 1.70, "Marginal Pass"),
    (50.0, 54.99, "D",  1.00, "Low Pass"),
    (0.0,  49.99, "F",  0.00, "Fail")
]

# In-Memory Storage for Active Session
STUDENT_REGISTRY = []


# ==============================================================================
# UTILITY & VALIDATION FUNCTIONS
# ==============================================================================
def initialize_system():
    """Initializes local folders and ensures CSV file has proper headers."""
    if not os.path.exists(TXT_REPORTS_DIR):
        os.makedirs(TXT_REPORTS_DIR)

    if not os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Timestamp", "Student_ID", "Student_Name", "Semester", 
                "Total_Courses", "Total_Credits", "Avg_Percentage", 
                "GPA", "Standing", "Passed_Courses", "Failed_Courses"
            ])


def get_valid_string(prompt, allow_empty=False):
    """Safely prompts user for non-empty text input."""
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("  [!] Error: This field cannot be left blank.")


def get_valid_int(prompt, min_val, max_val):
    """Prompts for an integer within an inclusive range with robust validation."""
    while True:
        raw_val = input(prompt).strip()
        try:
            val = int(raw_val)
            if min_val <= val <= max_val:
                return val
            print(f"  [!] Range Error: Please input an integer between {min_val} and {max_val}.")
        except ValueError:
            print("  [!] Format Error: Please enter a valid whole number (no symbols or letters).")


def get_valid_float(prompt, min_val, max_val):
    """Prompts for a float within an inclusive range with robust validation."""
    while True:
        raw_val = input(prompt).strip()
        try:
            val = float(raw_val)
            if min_val <= val <= max_val:
                return round(val, 2)
            print(f"  [!] Range Error: Value must be between {min_val} and {max_val}.")
        except ValueError:
            print("  [!] Format Error: Please enter a valid numerical decimal value.")


# ==============================================================================
# CORE ACADEMIC COMPUTATION ENGINES
# ==============================================================================
def calculate_grade_and_points(score):
    """
    Maps percentage mark to official letter grade, grade points, and remark.
    """
    for min_score, max_score, grade, points, remark in GRADE_SCALE:
        if min_score <= score <= max_score:
            return grade, points, remark
    return "F", 0.00, "Fail"


def determine_academic_standing(gpa, failed_count):
    """Evaluates student's formal institutional standing based on GPA and backlogs."""
    if failed_count > 2:
        return "Critical Academic Probation"
    elif failed_count > 0:
        return "Conditional Academic Warning"
    elif gpa >= 3.80:
        return "Summa Cum Laude (Dean's Highest Honor Roll)"
    elif gpa >= 3.65:
        return "Magna Cum Laude (Dean's Honor Roll)"
    elif gpa >= 3.50:
        return "Cum Laude (Distinction)"
    elif gpa >= 3.00:
        return "Good Standing"
    elif gpa >= 2.00:
        return "Satisfactory Standing"
    else:
        return "Academic Probation"


def collect_course_score():
    """
    Offers option to enter direct final score or calculate via weighted components:
    Assignments (15%), Quizzes (15%), Midterm (30%), Final Exam (40%).
    """
    print("    Scoring Method:")
    print("      [1] Direct Raw Total Score (0-100)")
    print("      [2] Weighted Components Breakdown (Quiz, Assignment, Midterm, Final)")
    mode = get_valid_int("    Choose scoring option (1 or 2): ", 1, 2)

    if mode == 1:
        return get_valid_float("    Enter Total Final Score (0 - 100): ", 0.0, 100.0)
    else:
        print("      -> Component Evaluation:")
        quizzes = get_valid_float("         Quizzes Total (0-15%): ", 0.0, 15.0)
        assignments = get_valid_float("         Assignments Total (0-15%): ", 0.0, 15.0)
        midterm = get_valid_float("         Midterm Exam (0-30%): ", 0.0, 30.0)
        final_exam = get_valid_float("         Final Terminal Exam (0-40%): ", 0.0, 40.0)
        total_calculated = quizzes + assignments + midterm + final_exam
        print(f"      => Aggregate Computed Score: {total_calculated:.2f}%")
        return total_calculated


# ==============================================================================
# STUDENT RECORD CREATION & BATCH PROCESSING
# ==============================================================================
def input_single_student_data():
    """Gathers all demographic and course data for a single student."""
    print("\n" + "=" * 80)
    print("📝 STUDENT ENROLLMENT & MARKS ENTRY MODULE")
    print("=" * 80)

    student_name = get_valid_string("Enter Student Full Name          : ").title()
    student_id = get_valid_string("Enter Student Registration / ID  : ").upper()
    semester = get_valid_string("Enter Semester / Term (e.g., F26): ").upper()
    
    num_courses = get_valid_int("Enter Total Enrolled Courses (1-12): ", 1, 12)

    courses_records = []

    print("\n--- COURSE DETAILS INPUT ---")
    for i in range(1, num_courses + 1):
        print(f"\n[Course #{i} of {num_courses}]")
        course_name = get_valid_string("  Course Name / Code : ").upper()
        credit_hours = get_valid_int("  Credit Hours (1-6) : ", 1, 6)
        obtained_score = collect_course_score()

        grade, grade_point, remark = calculate_grade_and_points(obtained_score)
        quality_points = round(grade_point * credit_hours, 2)

        course_entry = {
            "name": course_name,
            "credits": credit_hours,
            "score": obtained_score,
            "grade": grade,
            "grade_point": grade_point,
            "quality_points": quality_points,
            "remark": remark
        }
        courses_records.append(course_entry)

    # Compute Aggregate Metrics
    total_credits = sum(c["credits"] for c in courses_records)
    total_quality_points = sum(c["quality_points"] for c in courses_records)
    total_score_sum = sum(c["score"] for c in courses_records)
    avg_percentage = round(total_score_sum / num_courses, 2)
    final_gpa = round(total_quality_points / total_credits, 2) if total_credits > 0 else 0.00
    
    passed_count = sum(1 for c in courses_records if c["grade"] != "F")
    failed_count = num_courses - passed_count
    standing = determine_academic_standing(final_gpa, failed_count)

    # Compile Final Structured Student Profile
    student_profile = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id": student_id,
        "name": student_name,
        "semester": semester,
        "courses": courses_records,
        "num_courses": num_courses,
        "total_credits": total_credits,
        "total_quality_points": total_quality_points,
        "avg_percentage": avg_percentage,
        "gpa": final_gpa,
        "standing": standing,
        "passed_count": passed_count,
        "failed_count": failed_count
    }

    # Store in Active Session & Persist to Files
    STUDENT_REGISTRY.append(student_profile)
    save_record_to_csv(student_profile)
    export_individual_transcript(student_profile)

    # Render Visual Result Card Immediately
    display_transcript(student_profile)


# ==============================================================================
# DISPLAY & REPORT GENERATION ENGINES
# ==============================================================================
def display_transcript(student):
    """Renders an ASCII academic transcript to the standard output terminal."""
    print("\n" + "=" * 80)
    print("                     OFFICIAL ACADEMIC TRANSCRIPT")
    print("=" * 80)
    print(f" Student Name   : {student['name']:<28} Student ID : {student['id']}")
    print(f" Semester / Term: {student['semester']:<28} Generated  : {student['timestamp']}")
    print("-" * 80)
    print(f"{'#':<3}{'Course Title / Code':<26}{'Credits':<9}{'Marks':<9}{'Grade':<8}{'GP':<6}{'Quality Pts'}")
    print("-" * 80)

    for idx, c in enumerate(student["courses"], start=1):
        print(
            f"{idx:<3}"
            f"{c['name'][:24]:<26}"
            f"{c['credits']:<9}"
            f"{c['score']:<9.1f}"
            f"{c['grade']:<8}"
            f"{c['grade_point']:<6.2f}"
            f"{c['quality_points']:<10.2f}"
        )

    print("-" * 80)
    print(f"{'Total Credit Hours Attempted':<45} : {student['total_credits']}")
    print(f"{'Total Quality Points Accumulated':<45} : {student['total_quality_points']:.2f}")
    print(f"{'Cumulative Weighted Percentage':<45} : {student['avg_percentage']:.2f}%")
    print(f"{'Semester Grade Point Average (GPA)':<45} : {student['gpa']:.2f} / 4.00")
    print(f"{'Official Academic Standing':<45} : {student['standing']}")
    print("-" * 80)

    # Performance Breakdown
    scores = [c["score"] for c in student["courses"]]
    max_score = max(scores)
    min_score = min(scores)
    best_courses = [c["name"] for c in student["courses"] if c["score"] == max_score]
    lowest_courses = [c["name"] for c in student["courses"] if c["score"] == min_score]

    print("\n--- INDIVIDUAL COURSE ANALYTICS ---")
    print(f" • Courses Cleared : {student['passed_count']} | Backlogs/Failed : {student['failed_count']}")
    print(f" • Highest Score   : {max_score:.2f}% ({', '.join(best_courses)})")
    print(f" • Lowest Score    : {min_score:.2f}% ({', '.join(lowest_courses)})")

    # Visual Bar Chart for Grade Distribution
    print("\n--- GRADE DISTRIBUTION VISUALIZER ---")
    grade_tokens = [c["grade"] for c in student["courses"]]
    unique_grades = sorted(list(set(grade_tokens)))
    for g in unique_grades:
        count = grade_tokens.count(g)
        bar = "█" * (count * 3)
        print(f"   Grade {g:<3} | {count:02d} course(s) {bar}")
    print("=" * 80 + "\n")


# ==============================================================================
# FILE PERSISTENCE & EXPORT ENGINES
# ==============================================================================
def save_record_to_csv(student):
    """Appends summary row to persistent records.csv."""
    try:
        with open(CSV_FILE_PATH, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                student["timestamp"],
                student["id"],
                student["name"],
                student["semester"],
                student["num_courses"],
                student["total_credits"],
                student["avg_percentage"],
                student["gpa"],
                student["standing"],
                student["passed_count"],
                student["failed_count"]
            ])
    except IOError as e:
        print(f"  [!] Disk Warning: Could not write to CSV database: {e}")


def export_individual_transcript(student):
    """Generates a formatted printable TXT transcript file inside /transcripts/."""
    file_name = f"Transcript_{student['id']}_{student['semester']}.txt"
    file_path = os.path.join(TXT_REPORTS_DIR, file_name)

    try:
        with open(file_path, mode="w", encoding="utf-8") as f:
            f.write("=" * 76 + "\n")
            f.write("                   OFFICIAL ACADEMIC TRANSCRIPT REPORT\n")
            f.write("=" * 76 + "\n")
            f.write(f"Student Name    : {student['name']}\n")
            f.write(f"Registration ID : {student['id']}\n")
            f.write(f"Semester        : {student['semester']}\n")
            f.write(f"Date Issued     : {student['timestamp']}\n")
            f.write("-" * 76 + "\n")
            f.write(f"{'#':<3}{'Course Name':<28}{'Credits':<10}{'Marks':<10}{'Grade':<8}{'Quality Pts'}\n")
            f.write("-" * 76 + "\n")

            for i, c in enumerate(student["courses"], 1):
                f.write(
                    f"{i:<3}{c['name'][:26]:<28}{c['credits']:<10}{c['score']:<10.2f}"
                    f"{c['grade']:<8}{c['quality_points']:<10.2f}\n"
                )

            f.write("-" * 76 + "\n")
            f.write(f"Total Credits Enrolled : {student['total_credits']}\n")
            f.write(f"Quality Points Total   : {student['total_quality_points']:.2f}\n")
            f.write(f"Average Percentage     : {student['avg_percentage']:.2f}%\n")
            f.write(f"Semester GPA           : {student['gpa']:.2f} / 4.00\n")
            f.write(f"Academic Standing      : {student['standing']}\n")
            f.write("=" * 76 + "\n")
            f.write("Status: Digitally certified record.\n")
    except IOError as e:
        print(f"  [!] Disk Warning: Failed to export TXT transcript: {e}")


# ==============================================================================
# SEARCH, LOOKUP & COHORT ANALYTICS
# ==============================================================================
def search_student_record():
    """Allows instant searching by ID or Name from memory or CSV."""
    if not os.path.exists(CSV_FILE_PATH):
        print("  [!] No database found. Please add students first.")
        return

    query = get_valid_string("Enter Student ID or Full Name to search: ").lower()
    matches = []

    try:
        with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if query in row["Student_ID"].lower() or query in row["Student_Name"].lower():
                    matches.append(row)
    except IOError as e:
        print(f"  [!] Failed to read database: {e}")
        return

    if not matches:
        print(f"  [!] No records found matching query: '{query}'")
        return

    print("\n" + "=" * 90)
    print(f"🔍 SEARCH RESULTS ({len(matches)} MATCHES FOUND)")
    print("=" * 90)
    print(f"{'Student ID':<15}{'Full Name':<25}{'Semester':<12}{'Credits':<9}{'GPA':<8}{'Standing'}")
    print("-" * 90)
    for m in matches:
        print(f"{m['Student_ID']:<15}{m['Student_Name'][:23]:<25}{m['Semester']:<12}{m['Total_Credits']:<9}{m['GPA']:<8}{m['Standing']}")
    print("=" * 90 + "\n")


def display_cohort_analytics():
    """Calculates class statistics: Average GPA, Top Ranker, Pass/Fail ratios."""
    if not os.path.exists(CSV_FILE_PATH):
        print("  [!] No records to analyze. Database is empty.")
        return

    records = []
    try:
        with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
    except IOError as e:
        print(f"  [!] Error opening file: {e}")
        return

    if not records:
        print("  [!] Database has no student entries.")
        return

    gpas = [float(r["GPA"]) for r in records]
    percentages = [float(r["Avg_Percentage"]) for r in records]
    
    total_students = len(records)
    cohort_avg_gpa = sum(gpas) / total_students
    cohort_avg_pct = sum(percentages) / total_students
    
    top_gpa = max(gpas)
    valedictorians = [r["Student_Name"] for r in records if float(r["GPA"]) == top_gpa]

    probation_count = sum(1 for r in records if "Probation" in r["Standing"])
    deans_list_count = sum(1 for g in gpas if g >= 3.50)

    print("\n" + "=" * 70)
    print("📊 CLASS COHORT & SEMESTER BATCH ANALYTICS")
    print("=" * 70)
    print(f" Total Registered Students Processed : {total_students}")
    print(f" Cohort Average Semester GPA         : {cohort_avg_gpa:.2f} / 4.00")
    print(f" Cohort Average Mark Percentage      : {cohort_avg_pct:.2f}%")
    print(f" Dean's Honor Roll Qualifiers (≥3.5) : {deans_list_count} students")
    print(f" Students on Academic Probation      : {probation_count} students")
    print("-" * 70)
    print(f" 🏆 Highest Class GPA Achieved       : {top_gpa:.2f}")
    print(f" 🌟 Valedictorian / Top Achiever(s)  : {', '.join(valedictorians)}")
    print("=" * 70 + "\n")


# ==============================================================================
# MAIN SYSTEM CONTROLLER & INTERACTIVE CONSOLE MENU
# ==============================================================================
def display_main_menu():
    """Displays user menu options."""
    print("=" * 60)
    print("      ACADEMIC GRADING & GPA MANAGEMENT SYSTEM")
    print("=" * 60)
    print("  [1] Enter Single Student Grades & Generate Transcript")
    print("  [2] Batch Entry Mode (Multiple Students in Sequence)")
    print("  [3] Search Database by Student ID or Name")
    print("  [4] View Class Cohort Statistical Analytics")
    print("  [5] View Official Grading Scale & Criteria")
    print("  [6] Open / Verify Saved Transcripts Directory")
    print("  [7] Exit Application")
    print("=" * 60)


def show_grading_scale():
    """Displays institutional grading scale matrix."""
    print("\n" + "=" * 60)
    print("             INSTITUTIONAL GRADING CRITERIA")
    print("=" * 60)
    print(f"{'Percentage Range':<20}{'Letter Grade':<15}{'Points':<10}{'Remarks'}")
    print("-" * 60)
    for min_s, max_s, grade, points, remark in GRADE_SCALE:
        range_str = f"{min_s:.1f}% - {max_s:.1f}%"
        print(f"{range_str:<20}{grade:<15}{points:<10.2f}{remark}")
    print("=" * 60 + "\n")


def main():
    """Main execution loop controlling program flow."""
    initialize_system()

    while True:
        display_main_menu()
        choice = get_valid_int("Select an option (1-7): ", 1, 7)

        if choice == 1:
            input_single_student_data()
        elif choice == 2:
            count = get_valid_int("How many students do you want to input? (1-50): ", 1, 50)
            for idx in range(1, count + 1):
                print(f"\n>>> PROCESSING STUDENT [{idx} OF {count}] <<<")
                input_single_student_data()
        elif choice == 3:
            search_student_record()
        elif choice == 4:
            display_cohort_analytics()
        elif choice == 5:
            show_grading_scale()
        elif choice == 6:
            print(f"\n  [i] All transcript text reports are stored at:")
            print(f"      {TXT_REPORTS_DIR}")
            print(f"  [i] Database CSV records are stored at:")
            print(f"      {CSV_FILE_PATH}\n")
        elif choice == 7:
            print("\nShutting down Academic Management System. Goodbye!\n")
            break


if __name__ == "__main__":
    main()
