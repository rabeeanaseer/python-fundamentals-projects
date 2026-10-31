"""
Project 10: Adaptive Game-Theoretic Rock, Paper, Scissors & RPSLS Arena
Course Level: 1st/2nd Semester CS - Advanced Programming Fundamentals
Concepts Used:
  - 2D Outcome Matrices & Adjacency Dictionaries (Modular Game Rules)
  - Markov Chain Transition Probability Modeling for Predictive AI
  - Extended Variant Mechanics: Rock, Paper, Scissors, Lizard, Spock (RPSLS)
  - Tournament Series Engine (Best-of-N match play with win-streak tracking)
  - Persistent File I/O: CSV Tournament History and Formatted ASCII Scorecards
  - Defensive Exception Handling, Type Checks, and Statistics Aggregation
"""

import os
import csv
import random
from datetime import datetime

# ==============================================================================
# GLOBAL CONFIGURATION & DATA STORAGE CONSTANTS
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "game_data")
SCORECARDS_DIR = os.path.join(BASE_DIR, "scorecards")

HISTORY_CSV = os.path.join(DATA_DIR, "tournament_history.csv")
AUDIT_LOG_TXT = os.path.join(DATA_DIR, "game_audit_log.txt")

# ==============================================================================
# GAME VARIANT ADJACENCY MATRICES
# Format: Attacking_Move: {Defeated_Move: Verb_Description}
# ==============================================================================
CLASSIC_RULES = {
    "Rock": {"Scissors": "crushes"},
    "Paper": {"Rock": "covers"},
    "Scissors": {"Paper": "cuts"}
}

RPSLS_RULES = {
    "Rock": {"Scissors": "crushes", "Lizard": "crushes"},
    "Paper": {"Rock": "covers", "Spock": "disproves"},
    "Scissors": {"Paper": "cuts", "Lizard": "decapitates"},
    "Lizard": {"Spock": "poisons", "Paper": "eats"},
    "Spock": {"Scissors": "smashes", "Rock": "vaporizes"}
}

MOVE_ABBREVIATIONS = {
    "R": "Rock", "P": "Paper", "S": "Scissors",
    "L": "Lizard", "K": "Spock",
    "ROCK": "Rock", "PAPER": "Paper", "SCISSORS": "Scissors",
    "LIZARD": "Lizard", "SPOCK": "Spock"
}

# Markov Transition Model: Tracks frequency of (Previous_Move -> Current_Move)
# Initialized dynamically depending on active game variant
MARKOV_CHAIN = {}


# ==============================================================================
# SYSTEM INITIALIZATION & PERSISTENCE
# ==============================================================================
def initialize_system():
    """Initializes local storage directories and files."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SCORECARDS_DIR, exist_ok=True)

    if not os.path.exists(AUDIT_LOG_TXT):
        with open(AUDIT_LOG_TXT, mode="w", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] SYSTEM: Game Engine Online.\n")

    if not os.path.exists(HISTORY_CSV):
        with open(HISTORY_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Timestamp", "Tournament_ID", "Player_Name", "Game_Mode",
                "Target_Wins", "Player_Score", "AI_Score", "Ties",
                "Total_Rounds", "Outcome", "AI_Difficulty"
            ])


def log_event(message):
    """Appends an operational message to the local audit trail."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(AUDIT_LOG_TXT, mode="a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except IOError:
        pass


def save_tournament_record(record):
    """Appends a finished tournament outcome to the persistent CSV database."""
    try:
        with open(HISTORY_CSV, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                record["timestamp"],
                record["tournament_id"],
                record["player_name"],
                record["game_mode"],
                record["target_wins"],
                record["player_score"],
                record["ai_score"],
                record["ties"],
                record["total_rounds"],
                record["outcome"],
                record["ai_difficulty"]
            ])
    except IOError as e:
        print(f"  [!] Storage Warning: Could not write tournament to CSV: {e}")


# ==============================================================================
# INPUT VALIDATION HELPERS
# ==============================================================================
def input_non_empty(prompt):
    """Guarantees non-empty text input."""
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("  [!] Field error: Value cannot be left empty.")


def input_int_range(prompt, min_val, max_val):
    """Ensures input is a whole number within an inclusive boundary."""
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if min_val <= val <= max_val:
                return val
            print(f"  [!] Range Error: Select an option between {min_val} and {max_val}.")
        except ValueError:
            print("  [!] Input Error: Integer expected.")


# ==============================================================================
# MARKOV CHAIN PREDICTIVE AI ENGINE
# ==============================================================================
def reset_markov_chain(moves_list):
    """Rebuilds transition frequency table for selected move pool."""
    global MARKOV_CHAIN
    MARKOV_CHAIN.clear()
    for m1 in moves_list:
        MARKOV_CHAIN[m1] = {m2: 1 for m2 in moves_list}  # Laplace smoothing with initial 1


def record_player_transition(previous_move, current_move):
    """Increments observed transition probability between consecutive moves."""
    if previous_move and previous_move in MARKOV_CHAIN:
        if current_move in MARKOV_CHAIN[previous_move]:
            MARKOV_CHAIN[previous_move][current_move] += 1


def predict_player_next_move(previous_move, moves_list):
    """
    Predicts player's next move based on highest historical transition frequency.
    Falls back to uniform random choice if insufficient history exists.
    """
    if not previous_move or previous_move not in MARKOV_CHAIN:
        return random.choice(moves_list)

    transitions = MARKOV_CHAIN[previous_move]
    highest_count = max(transitions.values())
    candidates = [m for m, count in transitions.items() if count == highest_count]
    return random.choice(candidates)


def get_counter_move(predicted_move, rules_matrix):
    """
    Determines an optimal move that defeats the predicted player selection.
    """
    winning_moves = [attacker for attacker, victims in rules_matrix.items() if predicted_move in victims]
    return random.choice(winning_moves)


def select_ai_move(difficulty, previous_player_move, moves_list, rules_matrix):
    """
    Decision engine:
      - Random: Completely uniform random choice.
      - Tactical: 50% Markov prediction, 50% random.
      - Master (Markov Chain): 85% Markov prediction, 15% random noise.
    """
    if difficulty == "Random" or not previous_player_move:
        return random.choice(moves_list)

    chance = random.random()
    if difficulty == "Tactical":
        use_prediction = chance < 0.50
    else:  # Master
        use_prediction = chance < 0.85

    if use_prediction:
        predicted_move = predict_player_next_move(previous_player_move, moves_list)
        return get_counter_move(predicted_move, rules_matrix)
    else:
        return random.choice(moves_list)


# ==============================================================================
# OUTCOME EVALUATION MATRIX
# ==============================================================================
def evaluate_round(player_move, ai_move, rules_matrix):
    """
    Determines round winner using adjacency rules.
    Returns: (Outcome: 'Player'|'AI'|'Tie', Verb_Phrase: str)
    """
    if player_move == ai_move:
        return "Tie", f"Both opponents selected {player_move}"

    if ai_move in rules_matrix[player_move]:
        verb = rules_matrix[player_move][ai_move]
        return "Player", f"{player_move} {verb} {ai_move}"

    if player_move in rules_matrix[ai_move]:
        verb = rules_matrix[ai_move][player_move]
        return "AI", f"{ai_move} {verb} {player_move}"

    return "Tie", "Inconclusive clash"


# ==============================================================================
# TOURNAMENT ARENA CONTROLLER
# ==============================================================================
def run_tournament():
    """Runs a complete multi-round tournament series."""
    print("\n" + "=" * 70)
    print("⚔️ ENTER THE STRATEGY COMBAT ARENA")
    print("=" * 70)

    player_name = input_non_empty("Enter Competitor Call-Sign / Name: ").title()

    # Mode Selection
    print("\nSelect Game Variant Rules:")
    print("  [1] Classic Edition (Rock, Paper, Scissors)")
    print("  [2] Extended Edition (Rock, Paper, Scissors, Lizard, Spock)")
    mode_sel = input_int_range("Choice (1-2): ", 1, 2)

    if mode_sel == 1:
        game_mode = "Classic"
        rules_matrix = CLASSIC_RULES
        valid_moves = ["Rock", "Paper", "Scissors"]
        valid_keys = ["R", "P", "S"]
        menu_hint = "[R] Rock | [P] Paper | [S] Scissors"
    else:
        game_mode = "RPSLS"
        rules_matrix = RPSLS_RULES
        valid_moves = ["Rock", "Paper", "Scissors", "Lizard", "Spock"]
        valid_keys = ["R", "P", "S", "L", "K"]
        menu_hint = "[R] Rock | [P] Paper | [S] Scissors | [L] Lizard | [K] Spock"

    reset_markov_chain(valid_moves)

    # Difficulty Selection
    print("\nSelect Opponent AI Intelligence:")
    print("  [1] Standard RNG  (Uniform Random Distribution)")
    print("  [2] Tactical Bot  (50% Pattern Adaptation)")
    print("  [3] Master Engine (85% Predictive Markov Modeling)")
    diff_sel = input_int_range("Choice (1-3): ", 1, 3)
    diff_map = {1: "Random", 2: "Tactical", 3: "Master"}
    ai_difficulty = diff_map[diff_sel]

    # Series Target
    print("\nSelect Tournament Target:")
    print("  [1] Best of 3  (First to 2 wins)")
    print("  [2] Best of 5  (First to 3 wins)")
    print("  [3] Best of 9  (First to 5 wins)")
    print("  [4] Custom Goal")
    tgt_sel = input_int_range("Choice (1-4): ", 1, 4)
    target_map = {1: 2, 2: 3, 3: 5}
    if tgt_sel in target_map:
        target_wins = target_map[tgt_sel]
    else:
        target_wins = input_int_range("Specify points needed to win tournament (1 to 20): ", 1, 20)

    # Tournament State Variables
    player_score = 0
    ai_score = 0
    ties = 0
    round_number = 0
    previous_player_move = None
    round_logs = []

    print("\n" + "#" * 70)
    print(f" Contestant  : {player_name} vs. AI ({ai_difficulty})")
    print(f" Game Variant: {game_mode} | Victory Threshold: First to {target_wins} Wins")
    print(f" Move Syntax : {menu_hint}")
    print("#" * 70)
    input("\nPress ENTER to begin the tournament...")

    # Main Match Loop
    while player_score < target_wins and ai_score < target_wins:
        round_number += 1
        print(f"\n--- [ROUND {round_number}] --- Score: {player_name} [{player_score}] | AI [{ai_score}] (Ties: {ties})")

        # Gather player move
        while True:
            raw_input = input(f"Choose your move ({'/'.join(valid_keys)}): ").strip().upper()
            if raw_input in MOVE_ABBREVIATIONS:
                player_move = MOVE_ABBREVIATIONS[raw_input]
                if player_move in valid_moves:
                    break
            print(f"  [!] Invalid choice. Please enter one of: {', '.join(valid_keys)}")

        # AI Move Calculation
        ai_move = select_ai_move(ai_difficulty, previous_player_move, valid_moves, rules_matrix)

        # Update Markov Chain based on previous player move
        record_player_transition(previous_player_move, player_move)
        previous_player_move = player_move

        # Evaluate Round
        winner, narrative = evaluate_round(player_move, ai_move, rules_matrix)

        if winner == "Player":
            player_score += 1
            badge = "🟢 POINT AWARDED TO YOU!"
        elif winner == "AI":
            ai_score += 1
            badge = "🔴 POINT AWARDED TO AI!"
        else:
            ties += 1
            badge = "🟡 STALEMATE / DRAW!"

        print(f"\n  Player Move : {player_move}")
        print(f"  AI Move     : {ai_move}")
        print(f"  Resolution  : {narrative} -> {badge}")

        round_logs.append({
            "round": round_number,
            "player": player_move,
            "ai": ai_move,
            "winner": winner,
            "narrative": narrative
        })

    # Tournament Conclusion
    tournament_outcome = "VICTORY" if player_score > ai_score else "DEFEAT"
    tournament_id = f"TRN-{int(datetime.now().timestamp()) % 1000000:06d}"
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    record = {
        "timestamp": timestamp_str,
        "tournament_id": tournament_id,
        "player_name": player_name,
        "game_mode": game_mode,
        "target_wins": target_wins,
        "player_score": player_score,
        "ai_score": ai_score,
        "ties": ties,
        "total_rounds": round_number,
        "outcome": tournament_outcome,
        "ai_difficulty": ai_difficulty
    }

    save_tournament_record(record)
    log_event(f"MATCH: {player_name} {tournament_outcome} vs {ai_difficulty} AI ({player_score}-{ai_score}, Rounds: {round_number}).")
    export_scorecard(record, round_logs)

    # Display Grand Summary
    print("\n" + "=" * 70)
    if tournament_outcome == "VICTORY":
        print(f"🏆 TOURNAMENT CHAMPION: CONGRATULATIONS, {player_name.upper()}!")
    else:
        print(f"💀 TOURNAMENT DEFEAT: THE {ai_difficulty.upper()} AI PREVAILED!")
    print("=" * 70)
    print(f" Tournament ID   : {tournament_id}")
    print(f" Final Standing  : {player_name} [{player_score}] - [{ai_score}] AI")
    print(f" Ties / Draws    : {ties}")
    print(f" Total Rounds    : {round_number}")
    print(f" Win Ratio       : {(player_score / round_number) * 100:.1f}%")
    print("=" * 70)
    print(f"[✓] Official tournament scorecard exported to: scorecards/Scorecard_{tournament_id}.txt\n")


# ==============================================================================
# SCORECARD EXPORTER ENGINE
# ==============================================================================
def export_scorecard(record, round_logs):
    """Outputs printable ASCII scorecard of the entire match series."""
    filepath = os.path.join(SCORECARDS_DIR, f"Scorecard_{record['tournament_id']}.txt")
    try:
        with open(filepath, mode="w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write("             OFFICIAL TOURNAMENT MATCH SCORECARD\n")
            f.write("=" * 70 + "\n")
            f.write(f"Tournament ID   : {record['tournament_id']}\n")
            f.write(f"Date & Time     : {record['timestamp']}\n")
            f.write(f"Contestant      : {record['player_name']}\n")
            f.write(f"Ruleset Variant : {record['game_mode']}\n")
            f.write(f"Opponent Engine : {record['ai_difficulty']} AI\n")
            f.write("-" * 70 + "\n")
            f.write(f"Final Standing  : {record['player_name']} [{record['player_score']}] - [{record['ai_score']}] AI\n")
            f.write(f"Draws / Ties    : {record['ties']}\n")
            f.write(f"Rounds Played   : {record['total_rounds']}\n")
            f.write(f"Overall Result  : {record['outcome']}\n")
            f.write("-" * 70 + "\n")
            f.write("ROUND-BY-ROUND AUDIT BREAKDOWN:\n")
            f.write(f"{'Round':<8}{'Player Move':<15}{'AI Move':<15}{'Victor':<12}{'Resolution'}\n")
            f.write("-" * 70 + "\n")

            for r in round_logs:
                f.write(f"#{r['round']:<7}{r['player']:<15}{r['ai']:<15}{r['winner']:<12}{r['narrative']}\n")

            f.write("=" * 70 + "\n")
            f.write("Verified by: Adaptive Game-Theoretic Arbiter Subsystem\n")
    except IOError as e:
        print(f"  [!] Failed to save scorecard: {e}")


# ==============================================================================
# LEADERBOARD & TOURNAMENT HISTORY VIEWER
# ==============================================================================
def display_tournament_history():
    """Displays last 10 tournament outcomes from persistent CSV database."""
    print("\n" + "=" * 90)
    print("📜 RECENT ARENA TOURNAMENT RECORDS")
    print("=" * 90)

    if not os.path.exists(HISTORY_CSV):
        print("  [!] History database empty. Play a tournament first!")
        return

    records = []
    try:
        with open(HISTORY_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
    except IOError as e:
        print(f"  [!] Failed to read tournament history: {e}")
        return

    if not records:
        print("  [!] No matches registered on disk.")
        return

    print(f"{'Tourn ID':<12}{'Timestamp':<20}{'Player':<18}{'Mode':<10}{'Score':<14}{'Result':<10}{'AI Tier'}")
    print("-" * 90)
    for r in records[-10:]:
        score_str = f"{r['Player_Score']} - {r['AI_Score']} (T:{r['Ties']})"
        print(f"{r['Tournament_ID']:<12}{r['Timestamp']:<20}{r['Player_Name'][:16]:<18}{r['Game_Mode']:<10}{score_str:<14}{r['Outcome']:<10}{r['AI_Difficulty']}")
    print("=" * 90 + "\n")


def display_ruleset_encyclopedia():
    """Outputs narrative rules and mechanics for both supported game variants."""
    print("\n" + "=" * 70)
    print("📖 GAME THEORY & ADJACENCY MATRIX ENCYCLOPEDIA")
    print("=" * 70)
    print(" 1. Classic Rules (3 Moves):")
    print("    - Rock crushes Scissors")
    print("    - Scissors cuts Paper")
    print("    - Paper covers Rock")
    print("\n 2. Extended RPSLS Rules (5 Moves - Sam Kass & Karen Bryla):")
    print("    - Scissors cuts Paper & decapitates Lizard")
    print("    - Paper covers Rock & disproves Spock")
    print("    - Rock crushes Lizard & crushes Scissors")
    print("    - Lizard poisons Spock & eats Paper")
    print("    - Spock smashes Scissors & vaporizes Rock")
    print("\n 3. Adaptive Markov Intelligence:")
    print("    The Master AI builds an empirical transition probability matrix")
    print("    P(Next_Move | Current_Move) based on your sequence of play.")
    print("    Avoid predictable habits to overcome the AI.")
    print("=" * 70 + "\n")


def display_audit_logs():
    """Outputs recent system audit records."""
    print("\n" + "=" * 75)
    print("📋 GAME ARBITER AUDIT TRAIL")
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
        print(f"  [!] Failed to read log: {e}")
    print("=" * 75 + "\n")


# ==============================================================================
# MAIN APPLICATION CONTROLLER
# ==============================================================================
def display_main_menu():
    """Interactive Primary Command Center."""
    print("=" * 65)
    print("      ⚔️ ADAPTIVE GAME-THEORETIC RPS / RPSLS ARENA")
    print("=" * 65)
    print("  [1] Start New Tournament Series (Best-of-N)")
    print("  [2] View Arena Historical Tournament Ledger (CSV)")
    print("  [3] View Variant Rules & Move Adjacency Matrices")
    print("  [4] View Arbiter Audit Logs")
    print("  [5] Exit System")
    print("=" * 65)


def main():
    """Master application loop."""
    initialize_system()

    while True:
        display_main_menu()
        choice = input_int_range("Select an option (1-5): ", 1, 5)

        if choice == 1:
            run_tournament()
        elif choice == 2:
            display_tournament_history()
        elif choice == 3:
            display_ruleset_encyclopedia()
        elif choice == 4:
            display_audit_logs()
        elif choice == 5:
            log_event("SYSTEM: Arbiter shutdown. Graceful exit.")
            print("\nLeaving the Combat Arena. Well played!\n")
            break


if __name__ == "__main__":
    main()
