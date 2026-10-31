"""
Project 05: University Trivia & Computer Science Quiz Engine with Leaderboard
Course Level: 1st Semester CS / Programming Fundamentals
Concepts Used:
  - Lists and Tuples (Immutability for Question-Answer banks)
  - Dictionaries for player profiles, lifelines, and stats
  - Random module (shuffling questions, dynamic distractors, 50:50 lifelines)
  - Time module (response duration tracking & speed-bonus calculation)
  - Persistent File I/O: CSV leaderboard storage and ASCII TXT certificates
  - Modular functions with clean parameter passing
  - Defensive exception handling and strict input sanitization
"""

import os
import csv
import time
import random
from datetime import datetime

# ==============================================================================
# GLOBAL DIRECTORIES & PERSISTENCE PATHS
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "quiz_data")
CERTS_DIR = os.path.join(BASE_DIR, "certificates")
LEADERBOARD_CSV = os.path.join(DATA_DIR, "leaderboard.csv")
AUDIT_LOG_TXT = os.path.join(DATA_DIR, "quiz_audit_log.txt")

# ==============================================================================
# QUESTION BANK (Lists of Tuples & Dictionaries)
# Structure: (Category, Difficulty, Question, [Option A, B, C, D], Correct_Index_0_to_3, Explanation)
# ==============================================================================
MASTER_QUESTION_BANK = [
    # --- Category: Computer Science & Programming Fundamentals ---
    (
        "CS Fundamentals", "Easy",
        "Which symbol is used for single-line comments in Python?",
        ["//", "/*", "#", "--"],
        2,
        "Python uses the hash character (#) to indicate single-line comments."
    ),
    (
        "CS Fundamentals", "Easy",
        "Which of the following data structures is immutable in Python?",
        ["List", "Dictionary", "Set", "Tuple"],
        3,
        "Tuples cannot be altered once instantiated, making them immutable."
    ),
    (
        "CS Fundamentals", "Medium",
        "What is the average time complexity of searching an element in a Python dictionary?",
        ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
        0,
        "Python dictionaries use hash tables, providing O(1) average lookup time."
    ),
    (
        "CS Fundamentals", "Medium",
        "What does the acronym 'RAM' stand for in computer hardware?",
        ["Read Access Memory", "Random Access Memory", "Rapid Action Module", "Run Active Memory"],
        1,
        "RAM stands for Random Access Memory, the main volatile working memory."
    ),
    (
        "CS Fundamentals", "Hard",
        "In Python, what is the underlying algorithmic paradigm of the Timsort sorting function?",
        ["Pure Quicksort", "Merge Sort and Insertion Sort hybrid", "Heap Sort and Radix Sort", "Bubble Sort"],
        1,
        "Timsort is an adaptive hybrid derived from merge sort and insertion sort."
    ),
    (
        "CS Fundamentals", "Hard",
        "Which CPU scheduling algorithm is non-preemptive by design?",
        ["Round Robin", "Shortest Remaining Time First", "First-Come, First-Served (FCFS)", "Priority Preemptive"],
        2,
        "Standard FCFS processes execute completely until exit without preemption."
    ),

    # --- Category: Mathematics & Logic ---
    (
        "Mathematics", "Easy",
        "What is the binary equivalent of the decimal integer 13?",
        ["1011", "1101", "1110", "1001"],
        1,
        "13 in binary is 8 + 4 + 0 + 1, which translates to 1101 in base-2."
    ),
    (
        "Mathematics", "Medium",
        "If a coin is tossed 3 times, what is the probability of getting exactly 2 heads?",
        ["1/8", "1/4", "3/8", "1/2"],
        2,
        "Possible outcomes are 8. The combinations with 2 heads (HHT, HTH, THH) are 3/8."
    ),
    (
        "Mathematics", "Hard",
        "What is the value of 7! (7 factorial)?",
        ["720", "2520", "5040", "40320"],
        2,
        "7! = 7 * 6 * 5 * 4 * 3 * 2 * 1 = 5,040."
    ),

    # --- Category: General Science & Technology ---
    (
        "Science & Tech", "Easy",
        "Who is universally credited as the world's first computer programmer?",
        ["Alan Turing", "Ada Lovelace", "Charles Babbage", "Grace Hopper"],
        1,
        "Ada Lovelace published the first algorithm for Charles Babbage's Analytical Engine."
    ),
    (
        "Science & Tech", "Medium",
        "Which port is standard for secure web traffic using HTTPS?",
        ["80", "21", "443", "8080"],
        2,
        "Port 443 is the standard default port designated for encrypted HTTPS traffic."
    ),
    (
        "Science & Tech", "Hard",
        "Which of the following sorting algorithms is NOT a comparison sort?",
        ["Merge Sort", "Counting Sort", "Quicksort", "Heap Sort"],
        1,
        "Counting Sort sorts in linear time O(n+k) by tabulating item frequencies."
    )
]


# ==============================================================================
# SYSTEM INITIALIZATION & PERSISTENCE
# ==============================================================================
def initialize_system():
    """Sets up local directory structures and ensures files exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(CERTS_DIR, exist_ok=True)

    if not os.path.exists(LEADERBOARD_CSV):
        with open(LEADERBOARD_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Timestamp", "Quiz_ID", "Player_Name", "Category", 
                "Difficulty", "Score", "Accuracy_Pct", "Total_Time_Sec", "Rank_Grade"
            ])

    if not os.path.exists(AUDIT_LOG_TXT):
        with open(AUDIT_LOG_TXT, mode="w", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] QUIZ ENGINE: System ready.\n")


def log_event(message):
    """Appends an event to the internal audit trail."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(AUDIT_LOG_TXT, mode="a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except IOError:
        pass


def save_leaderboard_entry(record):
    """Appends a completed quiz record to the persistent CSV leaderboard."""
    try:
        with open(LEADERBOARD_CSV, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                record["timestamp"],
                record["quiz_id"],
                record["player_name"],
                record["category"],
                record["difficulty"],
                record["score"],
                record["accuracy"],
                record["duration"],
                record["grade"]
            ])
    except IOError as e:
        print(f"  [!] Storage Warning: Could not write to leaderboard: {e}")


# ==============================================================================
# INPUT VALIDATION HELPERS
# ==============================================================================
def input_non_empty(prompt):
    """Ensures input string contains non-whitespace characters."""
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("  [!] Field error: Value cannot be left empty.")


def input_int_range(prompt, min_val, max_val):
    """Ensures user inputs an integer strictly within an inclusive range."""
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if min_val <= val <= max_val:
                return val
            print(f"  [!] Range Error: Please select an option between {min_val} and {max_val}.")
        except ValueError:
            print("  [!] Input Error: Integer expected.")


# ==============================================================================
# LIFELINE IMPLEMENTATIONS (50:50 and Ask the Audience)
# ==============================================================================
def apply_fifty_fifty(options, correct_idx):
    """Eliminates two incorrect options, leaving the correct one and one random distractor."""
    incorrect_indices = [i for i in range(len(options)) if i != correct_idx]
    surviving_distractor = random.choice(incorrect_indices)
    
    modified_options = []
    for idx, opt in enumerate(options):
        if idx == correct_idx or idx == surviving_distractor:
            modified_options.append(opt)
        else:
            modified_options.append("--- [ELIMINATED] ---")
    return modified_options


def apply_ask_ai_or_audience(options, correct_idx):
    """Simulates crowd/AI confidence poll heavily weighting the correct answer."""
    percentages = [0, 0, 0, 0]
    # Assign majority confidence to correct answer (between 55% and 85%)
    correct_confidence = random.randint(55, 85)
    percentages[correct_idx] = correct_confidence
    
    remainder = 100 - correct_confidence
    other_indices = [i for i in range(4) if i != correct_idx]
    
    for i in range(len(other_indices) - 1):
        idx = other_indices[i]
        allocated = random.randint(0, remainder)
        percentages[idx] = allocated
        remainder -= allocated
    percentages[other_indices[-1]] = remainder

    print("\n  📊 AUDIENCE / AI POLL INTELLIGENCE:")
    labels = ["A", "B", "C", "D"]
    for i in range(4):
        bar = "█" * (percentages[i] // 3)
        print(f"     [{labels[i]}] {percentages[i]:2d}% {bar}")
    print()


# ==============================================================================
# CORE QUIZ ENGINE & SESSION CONTROLLER
# ==============================================================================
def filter_questions(category, difficulty):
    """Selects and shuffles question pool based on player preferences."""
    pool = []
    for q in MASTER_QUESTION_BANK:
        match_cat = (category == "All" or q[0] == category)
        match_diff = (difficulty == "All" or q[1] == difficulty)
        if match_cat and match_diff:
            pool.append(q)

    # If filter is too narrow, fallback to all
    if not pool:
        pool = list(MASTER_QUESTION_BANK)

    random.shuffle(pool)
    return pool


def run_quiz_session():
    """Main gameplay loop handling questioning, timers, lifelines, and scoring."""
    print("\n" + "=" * 70)
    print("🧠 NEW QUIZ CHALLENGE SETUP")
    print("=" * 70)

    player_name = input_non_empty("Enter Contestant Full Name: ").title()

    # Category Selection
    print("\nSelect Knowledge Category:")
    print(" [1] All Categories Combined (Mixed)")
    print(" [2] Computer Science Fundamentals")
    print(" [3] Mathematics & Logic")
    print(" [4] General Science & Tech")
    cat_sel = input_int_range("Select (1-4): ", 1, 4)
    cat_map = {1: "All", 2: "CS Fundamentals", 3: "Mathematics", 4: "Science & Tech"}
    chosen_cat = cat_map[cat_sel]

    # Difficulty Selection
    print("\nSelect Difficulty Level:")
    print(" [1] Mixed (Standard Progressive)")
    print(" [2] Easy")
    print(" [3] Medium")
    print(" [4] Hard")
    diff_sel = input_int_range("Select (1-4): ", 1, 4)
    diff_map = {1: "All", 2: "Easy", 3: "Medium", 4: "Hard"}
    chosen_diff = diff_map[diff_sel]

    # Question Limit
    limit = input_int_range("\nEnter number of questions for this round (3 to 10): ", 3, 10)
    question_pool = filter_questions(chosen_cat, chosen_diff)[:limit]

    # Lifelines Available
    lifelines = {"5050": True, "audience": True}

    score = 0
    correct_count = 0
    start_session_time = time.time()
    session_logs = []

    print("\n" + "#" * 70)
    print(f" Contestant : {player_name} | Questions: {len(question_pool)}")
    print(" Scoring    : Correct Answer = +100 Base Points")
    print(" Speed Bonus: Up to +50 additional points for answering within 10s")
    print(" Lifelines  : Type 'L1' for 50:50 | Type 'L2' for Audience Poll")
    print("#" * 70)
    input("\nPress ENTER when you are ready to begin...")

    # Iterate through questions
    for idx, (cat, diff, question_text, original_options, correct_idx, explanation) in enumerate(question_pool, start=1):
        print("\n" + "=" * 70)
        print(f"QUESTION {idx} OF {len(question_pool)} [{cat} | {diff}]")
        print(f"'{question_text}'")
        print("-" * 70)

        # Working copy of options
        active_options = list(original_options)
        eliminated_mode = False

        while True:
            # Display options
            letters = ["A", "B", "C", "D"]
            for opt_i in range(4):
                print(f"   [{letters[opt_i]}] {active_options[opt_i]}")

            # Lifelines indicator
            l1_status = "Available" if lifelines["5050"] else "Used"
            l2_status = "Available" if lifelines["audience"] else "Used"
            print(f"\n   [Lifelines: L1 (50:50) - {l1_status} | L2 (Audience) - {l2_status}]")

            # Timing the answer
            start_q_time = time.time()
            user_input = input("Your Choice (A, B, C, D) or Lifeline (L1/L2): ").strip().upper()
            duration = time.time() - start_q_time

            # Lifeline 1: 50:50
            if user_input == "L1":
                if not lifelines["5050"]:
                    print("  [!] You have already used your 50:50 lifeline!")
                    continue
                lifelines["5050"] = False
                active_options = apply_fifty_fifty(active_options, correct_idx)
                eliminated_mode = True
                print("\n  💡 50:50 Activated: Two wrong options eliminated!")
                continue

            # Lifeline 2: Ask the Audience
            if user_input == "L2":
                if not lifelines["audience"]:
                    print("  [!] You have already used your Audience lifeline!")
                    continue
                lifelines["audience"] = False
                apply_ask_ai_or_audience(active_options, correct_idx)
                continue

            # Validate answer choice
            if user_input not in letters:
                print("  [!] Invalid choice. Please enter A, B, C, D or a valid lifeline.")
                continue

            selected_idx = letters.index(user_input)

            # Prevent selecting an eliminated option
            if eliminated_mode and active_options[selected_idx].startswith("---"):
                print("  [!] That option has been eliminated! Pick one of the remaining choices.")
                continue

            # Check correctness
            if selected_idx == correct_idx:
                base_points = 100
                # Speed bonus: 50 max points decaying after 10 seconds
                speed_bonus = max(0, int(50 - (duration * 2)))
                q_total = base_points + speed_bonus
                score += q_total
                correct_count += 1

                print(f"\n  ✅ CORRECT! (+{base_points} pts + {speed_bonus} speed bonus = +{q_total} pts)")
                print(f"     Explanation: {explanation}")
                session_logs.append((question_text, "CORRECT", q_total))
            else:
                correct_letter = letters[correct_idx]
                print(f"\n  ❌ INCORRECT! The correct answer was [{correct_letter}] {original_options[correct_idx]}")
                print(f"     Explanation: {explanation}")
                session_logs.append((question_text, "INCORRECT", 0))

            break

    # Final tally calculations
    total_duration = round(time.time() - start_session_time, 1)
    total_questions = len(question_pool)
    accuracy_pct = round((correct_count / total_questions) * 100, 1)

    # Grade determination
    if accuracy_pct >= 90:
        grade = "A+ (Grandmaster)"
    elif accuracy_pct >= 75:
        grade = "A (Distinction)"
    elif accuracy_pct >= 60:
        grade = "B (Proficient)"
    elif accuracy_pct >= 40:
        grade = "C (Average)"
    else:
        grade = "F (Needs Revision)"

    quiz_id = f"QZ-{random.randint(1000, 9999)}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    quiz_record = {
        "timestamp": timestamp,
        "quiz_id": quiz_id,
        "player_name": player_name,
        "category": chosen_cat,
        "difficulty": chosen_diff,
        "score": score,
        "accuracy": accuracy_pct,
        "duration": total_duration,
        "grade": grade,
        "correct": correct_count,
        "total": total_questions
    }

    # Persist results
    save_leaderboard_entry(quiz_record)
    export_certificate(quiz_record)
    log_event(f"MATCH: {player_name} completed {quiz_id} | Score: {score} | Grade: {grade}.")

    # Render Terminal Report Card
    print("\n" + "=" * 70)
    print("                  🎉 QUIZ CHALLENGE COMPLETED")
    print("=" * 70)
    print(f" Contestant Name     : {player_name}")
    print(f" Quiz Certificate ID : {quiz_id}")
    print(f" Questions Attempted : {total_questions}")
    print(f" Correct Answers     : {correct_count} / {total_questions}")
    print(f" Accuracy Score      : {accuracy_pct}%")
    print(f" Total Score Points  : {score} pts")
    print(f" Time Elapsed        : {total_duration} seconds")
    print(f" Awarded Rating      : {grade}")
    print("=" * 70)
    print(f"[✓] Official certificate exported to: certificates/Certificate_{quiz_id}.txt\n")


# ==============================================================================
# SCORECARD CERTIFICATE EXPORT ENGINE
# ==============================================================================
def export_certificate(record):
    """Outputs a formatted ASCII completion certificate into the certificates folder."""
    filename = f"Certificate_{record['quiz_id']}.txt"
    filepath = os.path.join(CERTS_DIR, filename)

    try:
        with open(filepath, mode="w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write("             ACADEMIC KNOWLEDGE EVALUATION ASSESSMENT\n")
            f.write("               OFFICIAL CERTIFICATE OF COMPLETION\n")
            f.write("=" * 70 + "\n")
            f.write(f"Certificate Ref : {record['quiz_id']}\n")
            f.write(f"Issue Date      : {record['timestamp']}\n")
            f.write(f"Candidate Name  : {record['player_name']}\n")
            f.write(f"Category Domain : {record['category']}\n")
            f.write(f"Difficulty Tier : {record['difficulty']}\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total Questions : {record['total']}\n")
            f.write(f"Correct Answers : {record['correct']}\n")
            f.write(f"Final Accuracy  : {record['accuracy']}%\n")
            f.write(f"Accumulated Pts : {record['score']} Points\n")
            f.write(f"Session Duration: {record['duration']} Seconds\n")
            f.write(f"Performance Tier: {record['grade']}\n")
            f.write("-" * 70 + "\n")
            f.write("Certified by: Python Fundamentals Quiz Evaluation Subsystem\n")
            f.write("=" * 70 + "\n")
    except IOError as e:
        print(f"  [!] Failed to export certificate file: {e}")


# ==============================================================================
# LEADERBOARD & ANALYTICS VIEWER
# ==============================================================================
def display_leaderboard():
    """Displays top scores ordered by highest score points."""
    print("\n" + "=" * 80)
    print("🏆 GLOBAL TRIVIA HALL OF FAME & LEADERBOARD")
    print("=" * 80)

    if not os.path.exists(LEADERBOARD_CSV):
        print("  [!] No recorded scores. Take a quiz first!")
        return

    entries = []
    try:
        with open(LEADERBOARD_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                entries.append(row)
    except IOError as e:
        print(f"  [!] Failed to read leaderboard database: {e}")
        return

    if not entries:
        print("  [!] Leaderboard is currently empty.")
        return

    # Sort descending by Score (convert to integer)
    entries.sort(key=lambda x: int(x["Score"]), reverse=True)

    print(f"{'Rank':<6}{'Contestant':<20}{'Category':<18}{'Score':<10}{'Accuracy':<10}{'Grade'}")
    print("-" * 80)
    for rank, row in enumerate(entries[:10], start=1):
        print(f"#{rank:<5}{row['Player_Name'][:18]:<20}{row['Category'][:16]:<18}{row['Score']:<10}{row['Accuracy_Pct']:<10}{row['Rank_Grade']}")
    print("=" * 80 + "\n")


def display_session_logs():
    """Displays recent activity log."""
    print("\n" + "=" * 70)
    print("📋 QUIZ AUDIT TRAIL LOGS")
    print("=" * 70)
    if not os.path.exists(AUDIT_LOG_TXT):
        print("  [!] Log file empty.")
        return

    try:
        with open(AUDIT_LOG_TXT, mode="r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-10:]:
                print(" " + line.strip())
    except IOError as e:
        print(f"  [!] Could not read logs: {e}")
    print("=" * 70 + "\n")


# ==============================================================================
# MAIN APPLICATION CONTROLLER
# ==============================================================================
def display_main_menu():
    """Interactive primary menu."""
    print("=" * 60)
    print("       🧠 UNIVERSITY QUIZ & TRIVIA EVALUATOR")
    print("=" * 60)
    print("  [1] Start New Quiz Round")
    print("  [2] View Global Top 10 Leaderboard")
    print("  [3] View System Audit & Session History")
    print("  [4] How to Play & Lifeline Rules")
    print("  [5] Exit Application")
    print("=" * 60)


def show_game_rules():
    """Explains scoring formula, time bonuses, and lifeline rules."""
    print("\n" + "=" * 70)
    print("📖 HOW TO PLAY & SCORING MECHANICS")
    print("=" * 70)
    print(" 1. Questions & Categories:")
    print("    Select specific categories (CS, Math, Tech) or mix them.")
    print(" 2. Scoring & Speed Bonus:")
    print("    - Each correct answer gives 100 Base Points.")
    print("    - Speed Bonus: Answering within 10 seconds adds up to +50 bonus points.")
    print(" 3. Available Lifelines:")
    print("    - L1 (50:50)  : Eliminates two incorrect choices, leaving 2 options.")
    print("    - L2 (Audience): Simulates an AI/audience poll with confidence bars.")
    print("    - Note: Each lifeline can only be activated ONCE per quiz.")
    print(" 4. Official Certification:")
    print("    Completing a quiz generates an official printable .txt report card.")
    print("=" * 70 + "\n")


def main():
    """System entry loop."""
    initialize_system()

    while True:
        display_main_menu()
        choice = input_int_range("Select an option (1-5): ", 1, 5)

        if choice == 1:
            run_quiz_session()
        elif choice == 2:
            display_leaderboard()
        elif choice == 3:
            display_session_logs()
        elif choice == 4:
            show_game_rules()
        elif choice == 5:
            log_event("SYSTEM: Application shutdown.")
            print("\nThank you for participating! Happy learning.\n")
            break


if __name__ == "__main__":
    main()
