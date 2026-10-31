"""
Project 03: Precision Number Guessing Game with Adaptive AI Hint Engine
Course Level: 1st Semester CS / Programming Fundamentals
Concepts Used:
  - random module (choice, randint)
  - Nested while and for loops with break/continue sentinels
  - Mathematical logic: Parity, primality testing, factors/divisibility, ranges
  - Lists, Dictionaries, and Tuples for round state tracking
  - File I/O: Persistent high-score leaderboard (.csv) and match history log (.txt)
  - Defensive error handling (try/except, boundary checks)
  - Score decay mechanics and adaptive dynamic hint system
"""

import os
import csv
import math
import random
from datetime import datetime

# ==============================================================================
# GLOBAL PATHS & DIRECTORIES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "game_data")
LEADERBOARD_CSV = os.path.join(DATA_DIR, "leaderboard.csv")
MATCH_LOG_TXT = os.path.join(DATA_DIR, "match_history.txt")

# ==============================================================================
# GAME CONFIGURATION PRESETS
# ==============================================================================
DIFFICULTY_TIERS = {
    1: {"name": "Novice", "min": 1, "max": 50, "max_attempts": 10, "base_score": 500, "hint_penalty": 30},
    2: {"name": "Adept", "min": 1, "max": 100, "max_attempts": 7, "base_score": 1000, "hint_penalty": 75},
    3: {"name": "Master", "min": 1, "max": 500, "max_attempts": 9, "base_score": 2500, "hint_penalty": 150},
    4: {"name": "Grandmaster", "min": 1, "max": 1000, "max_attempts": 10, "base_score": 5000, "hint_penalty": 300},
    5: {"name": "Custom", "min": 1, "max": 100, "max_attempts": 10, "base_score": 1000, "hint_penalty": 50}
}


# ==============================================================================
# SYSTEM INITIALIZATION & PERSISTENCE
# ==============================================================================
def initialize_system():
    """Initializes local data directories and CSV leaderboard file."""
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(LEADERBOARD_CSV):
        with open(LEADERBOARD_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Timestamp", "Player_Name", "Difficulty", "Secret_Number",
                "Attempts_Used", "Max_Attempts", "Hints_Unlocked", "Final_Score", "Outcome"
            ])

    if not os.path.exists(MATCH_LOG_TXT):
        with open(MATCH_LOG_TXT, mode="w", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] GAME ENGINE: Initialization complete.\n")


def log_match_history(record):
    """Appends match round summary to local log file."""
    line = (
        f"[{record['timestamp']}] Player: {record['player']} | Mode: {record['difficulty']} | "
        f"Secret: {record['secret']} | Attempts: {record['attempts']}/{record['max_attempts']} | "
        f"Score: {record['score']} | Status: {record['outcome']}\n"
    )
    try:
        with open(MATCH_LOG_TXT, mode="a", encoding="utf-8") as f:
            f.write(line)
    except IOError:
        pass


def save_score_to_leaderboard(record):
    """Saves player record to persistent CSV database."""
    try:
        with open(LEADERBOARD_CSV, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                record["timestamp"],
                record["player"],
                record["difficulty"],
                record["secret"],
                record["attempts"],
                record["max_attempts"],
                record["hints_used"],
                record["score"],
                record["outcome"]
            ])
    except IOError as e:
        print(f"  [!] Storage Warning: Could not write to leaderboard: {e}")


# ==============================================================================
# INPUT VALIDATION HELPERS
# ==============================================================================
def input_non_empty(prompt):
    """Prompts user for non-empty text."""
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("  [!] Error: Value cannot be left empty.")


def input_int_range(prompt, min_val, max_val):
    """Ensures user inputs an integer strictly within an inclusive range."""
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if min_val <= val <= max_val:
                return val
            print(f"  [!] Range Error: Please enter a whole number between {min_val} and {max_val}.")
        except ValueError:
            print("  [!] Input Error: Invalid characters detected. Integer expected.")


# ==============================================================================
# MATHEMATICAL AI HINT SUBSYSTEM
# ==============================================================================
def is_prime(n):
    """Evaluates whether an integer is prime."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def get_factors(n):
    """Returns list of positive divisors excluding 1 and itself."""
    factors = []
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            factors.append(i)
            if i*i != n:
                factors.append(n // i)
    factors.sort()
    return factors


def generate_ai_hints(secret, lower_bound, upper_bound):
    """
    Constructs a queue of progressive mathematical hints designed to be unlocked
    sequentially if the player requests assistance.
    """
    hints = []

    # Hint 1: Parity (Even / Odd)
    parity = "EVEN" if secret % 2 == 0 else "ODD"
    hints.append(f"Parity Analysis: The secret number is an {parity} number.")

    # Hint 2: Primality Check
    if is_prime(secret):
        hints.append("Number Theory: The secret number is a PRIME number (only divisible by 1 and itself).")
    else:
        factors = get_factors(secret)
        if factors:
            hints.append(f"Composite Analysis: It is NOT prime. A notable factor/divisor is {random.choice(factors)}.")
        else:
            hints.append("Number Theory: The secret number is composite (has multiple factors).")

    # Hint 3: Range Squeeze (Window narrows to 30% of original bounds)
    spread = upper_bound - lower_bound
    window_padding = max(5, int(spread * 0.15))
    window_min = max(lower_bound, secret - random.randint(1, window_padding))
    window_max = min(upper_bound, secret + random.randint(1, window_padding))
    hints.append(f"Range Constriction: The target is strictly contained within the sub-window [{window_min} to {window_max}].")

    # Hint 4: Sum of Digits or Multiples
    digits = [int(d) for d in str(secret)]
    digit_sum = sum(digits)
    hints.append(f"Digit Analytics: The sum of its digits equals {digit_sum}.")

    # Hint 5: Proximity modulo
    if secret > 10:
        remainder = secret % 10
        hints.append(f"Terminal Digit: The number ends with the digit {remainder} (Target % 10 = {remainder}).")
    else:
        hints.append(f"Arithmetic Offset: Target squared equals {secret ** 2}.")

    return hints


def evaluate_proximity_feedback(guess, secret, max_range):
    """
    Produces dynamic hot/cold thermal feedback based on distance to target.
    """
    diff = abs(guess - secret)
    ratio = diff / max_range

    if diff == 0:
        return "🎯 BULLSEYE! PERFECT HIT!"
    elif ratio <= 0.02:
        return "🔥 BOILING HOT! You are right at the doorstep (Distance ≤ 2% of range)!"
    elif ratio <= 0.05:
        return "♨️ VERY WARM! Extremely close."
    elif ratio <= 0.15:
        return "🌡️ WARM! Heading in the right direction."
    elif ratio <= 0.30:
        return "❄️ CHILLY! Decently far off."
    else:
        return "🧊 FREEZING COLD! Way off the mark."


# ==============================================================================
# CORE GAMEPLAY ROUND CONTROLLER
# ==============================================================================
def configure_difficulty():
    """Menu to select or customize gameplay parameters."""
    print("\n" + "=" * 65)
    print("🎯 SELECT DIFFICULTY PRESET")
    print("=" * 65)
    for k, v in DIFFICULTY_TIERS.items():
        if k != 5:
            print(f" [{k}] {v['name']:<12} : Range [{v['min']} - {v['max']:<4}] | {v['max_attempts']} Attempts | Base: {v['base_score']} pts")
        else:
            print(f" [{k}] Custom Mode  : User-defined boundaries and custom attempt limits")
    print("-" * 65)

    choice = input_int_range("Select Tier (1-5): ", 1, 5)

    if choice == 5:
        print("\n--- Setup Custom Game ---")
        c_min = input_int_range("Enter Lower Bound (min 1): ", 1, 10000)
        c_max = input_int_range(f"Enter Upper Bound (min {c_min + 5}): ", c_min + 5, 50000)
        c_att = input_int_range("Max Allowed Attempts (3 - 30): ", 3, 30)
        return {
            "name": "Custom",
            "min": c_min,
            "max": c_max,
            "max_attempts": c_att,
            "base_score": 1500,
            "hint_penalty": 100
        }

    return DIFFICULTY_TIERS[choice]


def play_game_round():
    """Executes an entire round of the number guessing game."""
    print("\n" + "=" * 70)
    print("🎮 NEW GAME ROUND: SYSTEM LOCKED ON TARGET")
    print("=" * 70)

    player_name = input_non_empty("Enter Player Call-Sign / Name: ").strip().title()
    cfg = configure_difficulty()

    secret_number = random.randint(cfg["min"], cfg["max"])
    max_range = cfg["max"] - cfg["min"]
    ai_hint_pool = generate_ai_hints(secret_number, cfg["min"], cfg["max"])

    # Round tracking variables
    attempts_left = cfg["max_attempts"]
    attempts_used = 0
    hints_unlocked = 0
    score = cfg["base_score"]
    guess_history = []
    won = False

    print("\n" + "#" * 70)
    print(f" Objective: Guess the secret number between {cfg['min']} and {cfg['max']}.")
    print(f" Difficulty: {cfg['name']} | Max Attempts: {cfg['max_attempts']} | Starting Points: {score}")
    print(f" Commands during turn: Type your number, or enter '0' to request an AI Hint.")
    print("#" * 70)

    while attempts_left > 0:
        print(f"\n[Attempt {attempts_used + 1} of {cfg['max_attempts']}] - Attempts Left: {attempts_left} | Current Score: {score}")
        
        # Display guess track record if available
        if guess_history:
            history_str = ", ".join(f"{g} ({d})" for g, d in guess_history[-5:])
            print(f" Recent Guesses: [{history_str}]")

        action = input(f" Enter guess [{cfg['min']} - {cfg['max']}] (or 0 for AI Hint): ").strip()

        # Check for Hint Request
        if action == "0":
            if hints_unlocked < len(ai_hint_pool):
                hint_text = ai_hint_pool[hints_unlocked]
                hints_unlocked += 1
                score = max(50, score - cfg["hint_penalty"])
                print("\n" + "*" * 65)
                print(f"💡 AI INTEL MODULE [Hint #{hints_unlocked}]:")
                print(f"   {hint_text}")
                print(f"   (Penalty: -{cfg['hint_penalty']} pts | Score now: {score})")
                print("*" * 65)
            else:
                print("  [!] AI Warning: All available intelligence hints have been exhausted for this target.")
            continue

        # Validate numeric guess
        try:
            guess = int(action)
        except ValueError:
            print("  [!] Invalid entry. Enter a valid integer or '0' for a hint.")
            continue

        if not (cfg["min"] <= guess <= cfg["max"]):
            print(f"  [!] Boundary Error: Target is between {cfg['min']} and {cfg['max']}.")
            continue

        if guess in [g[0] for g in guess_history]:
            print(f"  [!] Duplicate Notice: You have already tried {guess}. No penalty deducted.")
            continue

        # Valid Guess Processed
        attempts_used += 1
        attempts_left -= 1

        # Check Win
        if guess == secret_number:
            won = True
            # Bonus score for unused attempts
            accuracy_bonus = attempts_left * 100
            score += accuracy_bonus
            print("\n" + "=" * 70)
            print(f"🎉 INCREDIBLE! YOU FOUND THE TARGET: {secret_number}")
            print(f"   Rounds Taken   : {attempts_used}")
            print(f"   Accuracy Bonus : +{accuracy_bonus} pts")
            print(f"   Final Score    : {score} pts")
            print("=" * 70)
            break

        # Calculate Direction and Thermal Distance
        direction = "HIGHER ⬆️" if secret_number > guess else "LOWER ⬇️"
        proximity = evaluate_proximity_feedback(guess, secret_number, max_range)
        guess_history.append((guess, "Low" if secret_number > guess else "High"))

        # Linear score deduction per wrong attempt
        score = max(50, score - int(cfg["base_score"] / cfg["max_attempts"]))

        print(f"  >> Direction  : Go {direction}!")
        print(f"  >> Thermal    : {proximity}")

    # Outcome evaluation
    if not won:
        score = 0
        print("\n" + "=" * 70)
        print("💀 MISSION FAILED: OUT OF ATTEMPTS!")
        print(f"   The secret target was: {secret_number}")
        print("   Better luck on the next run!")
        print("=" * 70)

    # Compile match summary
    match_record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "player": player_name,
        "difficulty": cfg["name"],
        "secret": secret_number,
        "attempts": attempts_used,
        "max_attempts": cfg["max_attempts"],
        "hints_used": hints_unlocked,
        "score": score,
        "outcome": "VICTORY" if won else "DEFEAT"
    }

    save_score_to_leaderboard(match_record)
    log_match_history(match_record)


# ==============================================================================
# LEADERBOARD & METRICS DISPLAY
# ==============================================================================
def display_leaderboard():
    """Reads persistent CSV and renders top player hall of fame."""
    print("\n" + "=" * 80)
    print("🏆 GLOBAL PRECISION LEADERBOARD (HALL OF FAME)")
    print("=" * 80)

    if not os.path.exists(LEADERBOARD_CSV):
        print("  [!] No game records on disk. Play a round first!")
        return

    records = []
    try:
        with open(LEADERBOARD_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Outcome"] == "VICTORY":
                    records.append(row)
    except IOError as e:
        print(f"  [!] Leaderboard access error: {e}")
        return

    if not records:
        print("  [!] No victories recorded yet. Be the first to win!")
        return

    # Sort descending by Final Score
    records.sort(key=lambda r: int(r["Final_Score"]), reverse=True)

    print(f"{'Rank':<6}{'Player':<20}{'Difficulty':<15}{'Score':<10}{'Attempts':<12}{'Hints Used'}")
    print("-" * 80)
    for idx, r in enumerate(records[:10], start=1):
        attempts_display = f"{r['Attempts_Used']}/{r['Max_Attempts']}"
        print(f"#{idx:<5}{r['Player_Name'][:18]:<20}{r['Difficulty']:<15}{r['Final_Score']:<10}{attempts_display:<12}{r['Hints_Unlocked']}")
    print("=" * 80 + "\n")


def display_match_history():
    """Renders recent match logs."""
    print("\n" + "=" * 80)
    print("📜 RECENT MATCH AUDIT LOGS")
    print("=" * 80)
    if not os.path.exists(MATCH_LOG_TXT):
        print("  [!] Log file empty.")
        return

    try:
        with open(MATCH_LOG_TXT, mode="r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-10:]:
                print(" " + line.strip())
    except IOError as e:
        print(f"  [!] Failed to read log: {e}")
    print("=" * 80 + "\n")


# ==============================================================================
# MAIN APPLICATION CONTROLLER
# ==============================================================================
def display_main_menu():
    """Terminal navigation choices."""
    print("=" * 60)
    print("     🎯 AI NUMBER GUESSING & INFERENCE SYSTEM")
    print("=" * 60)
    print("  [1] Start New Guessing Game")
    print("  [2] View Top 10 Hall of Fame Leaderboard")
    print("  [3] View Recent Match History Audit")
    print("  [4] Display How the AI Hint Subsystem Works")
    print("  [5] Exit Application")
    print("=" * 60)


def show_hint_system_specs():
    """Explains how the mathematical hint system functions."""
    print("\n" + "=" * 70)
    print("🧠 MATHEMATICAL AI HINT SYSTEM ARCHITECTURE")
    print("=" * 70)
    print(" When you press '0' during your turn, the engine generates dynamic intel:")
    print("  1. Parity Check      : Analyzes whether target is strictly Even or Odd.")
    print("  2. Number Theory     : Determines primality or exposes factors if composite.")
    print("  3. Range Squeeze     : Dynamically narrows target window to a tight 30% bounds.")
    print("  4. Digit Analytics   : Computes exact sum of the target's composite digits.")
    print("  5. Proximity Modulo  : Reveals terminal digit via modular arithmetic.")
    print("  Note: Each hint costs score points depending on chosen difficulty.")
    print("=" * 70 + "\n")


def main():
    """Primary execution loop."""
    initialize_system()

    while True:
        display_main_menu()
        choice = input_int_range("Select an option (1-5): ", 1, 5)

        if choice == 1:
            play_game_round()
        elif choice == 2:
            display_leaderboard()
        elif choice == 3:
            display_match_history()
        elif choice == 4:
            show_hint_system_specs()
        elif choice == 5:
            print("\nShutting down AI Guessing Engine. Thanks for playing!\n")
            break


if __name__ == "__main__":
    main()
