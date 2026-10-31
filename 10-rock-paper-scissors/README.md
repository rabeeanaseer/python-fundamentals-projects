
# ⚔️ Rock, Paper, Scissors Game | Adaptive AI & RPSLS Tournament Arena

An interactive Python command-line game featuring Classic Rock, Paper, Scissors and the extended Rock, Paper, Scissors, Lizard, Spock (RPSLS) variant.

The project includes an adaptive computer opponent powered by a first-order Markov Chain prediction model, multiple difficulty levels, tournament modes, persistent match history, and automatically generated scorecards.

Built as the culminating project in a first-semester Python programming fundamentals collection, it demonstrates practical applications of probability, data structures, graph-based game logic, conditional algorithms, file handling, and modular programming.

---

## 📌 Project Overview

Traditional Rock, Paper, Scissors games usually rely on random computer choices and simple conditional statements.

This project introduces an adaptive opponent that analyzes the player's previous moves and uses observed patterns to estimate their next selection.

It supports two game variants:

1. **Classic Mode:** Rock, Paper, and Scissors.
2. **Extended RPSLS Mode:** Rock, Paper, Scissors, Lizard, and Spock.

The system also supports multi-round tournaments, score tracking, match history, and printable tournament reports.

---

## ✨ Features

### 🎮 1. Dual Game Variants

**Classic Rock, Paper, Scissors**

- Rock defeats Scissors.
- Scissors defeats Paper.
- Paper defeats Rock.

**Extended Rock, Paper, Scissors, Lizard, Spock (RPSLS)**

Includes five possible moves and ten directed winning relationships.

- Rock crushes Scissors.
- Rock crushes Lizard.
- Paper covers Rock.
- Paper disproves Spock.
- Scissors cuts Paper.
- Scissors decapitates Lizard.
- Lizard eats Paper.
- Lizard poisons Spock.
- Spock smashes Scissors.
- Spock vaporizes Rock.

### 🧠 2. Adaptive Markov Chain AI

The computer opponent tracks the player's move history and analyzes transitions between consecutive selections.

For example, if a player frequently chooses Paper after Rock, the system can use that observed pattern when predicting the next move.

The transition probability is calculated as:

\[
P(M_t=j\mid M_{t-1}=i)
=
\frac{\text{Count}(i\rightarrow j)}
{\sum_k\text{Count}(i\rightarrow k)}
\]

Where:

- \(M_t\) = current move.
- \(M_{t-1}\) = previous move.
- \(i\) and \(j\) = possible game moves.
- `Count` = observed transition frequency.

**Laplace smoothing** can be applied to avoid zero-probability transitions when the system has limited historical data.

The predicted player move is then countered using the game's winning relationships.

### 🎯 3. Three AI Difficulty Profiles

The application provides three opponent profiles:

| Difficulty | Strategy |
|---|---|
| Standard RNG | Selects moves using a random distribution |
| Tactical Bot | Uses Markov predictions with a random fallback |
| Master Engine | Uses a higher prediction probability with occasional random variation |

**Tactical Bot:**
- 50% probability of using the predicted player move.
- 50% random fallback.

**Master Engine:**
- 85% probability of using the predicted player move.
- 15% random variation.

*These percentages describe the intended strategy. Actual behavior depends on the implementation and available player history.*

### 🏆 4. Tournament Management

Supports multiple tournament formats:

- Best of 3.
- Best of 5.
- Best of 9.
- Custom target-win limits.

Tournament features include:

- Real-time score tracking.
- Round-by-round results.
- Tie and stalemate tracking.
- Player and computer win counts.
- Automatic tournament completion.
- Final match summaries.

### 📊 5. Persistent Tournament History

Stores completed tournament records in:

`game_data/tournament_history.csv`

Recorded information includes:

- Unique tournament IDs.
- Date and time.
- Player aliases.
- Game variants.
- AI difficulty levels.
- Final scores.
- Tournament outcomes.
- Win ratios.

### 🧾 6. Printable Tournament Scorecards

Automatically generates text-based tournament reports in the `scorecards/` directory.

Each scorecard can include:

- Tournament identification.
- Player and opponent details.
- Selected ruleset.
- Final score.
- Number of rounds.
- Draw count.
- Overall result.
- Round-by-round move history.
- Winning explanations.

### 📝 7. System Audit Logging

Maintains an audit log containing relevant game activities, such as:

- Tournament initialization.
- Player selections.
- Computer selections.
- Round outcomes.
- Tournament completion.
- Scorecard generation.

---

## 📐 RPSLS Game Rules

The extended game uses five moves, with each move defeating exactly two other moves.

| Move | Defeats | Explanation |
|---|---|---|
| Rock | Scissors, Lizard | Crushes Scissors; crushes Lizard |
| Paper | Rock, Spock | Covers Rock; disproves Spock |
| Scissors | Paper, Lizard | Cuts Paper; decapitates Lizard |
| Lizard | Spock, Paper | Poisons Spock; eats Paper |
| Spock | Scissors, Rock | Smashes Scissors; vaporizes Rock |

### Game Logic

The application can represent the winning relationships using a dictionary or adjacency structure.

For example:

```python
winning_moves = {
    "Rock": ["Scissors", "Lizard"],
    "Paper": ["Rock", "Spock"],
    "Scissors": ["Paper", "Lizard"],
    "Lizard": ["Spock", "Paper"],
    "Spock": ["Scissors", "Rock"]
}
```

A round is resolved by checking whether the player's move defeats the computer's move, whether the computer's move defeats the player's move, or whether both selected the same move.

---

## 📐 Markov Chain Prediction Model

The adaptive opponent uses previous player selections to estimate future behavior.

A first-order Markov model assumes that the next move depends on the immediately preceding move:

\[
P(M_{t+1}\mid M_t)
\]

For example, suppose the player's observed transitions include:

| Previous Move | Next Move | Frequency |
|---|---|---:|
| Rock | Paper | 6 |
| Rock | Scissors | 3 |
| Rock | Lizard | 1 |

The estimated transition probabilities are:

- Paper: 60%
- Scissors: 30%
- Lizard: 10%

The AI can select the most likely next move and choose a counter-move.

**Important:** This is statistical pattern prediction, not machine learning in the modern model-training sense. Its effectiveness depends on the player's behavior, the amount of observed data, and how predictable their choices are.

---

## 🛠️ Technologies Used

- **Python 3.8+**
- `random` — Computer move selection and randomized strategy.
- `csv` — Persistent tournament history.
- `os` — Directory and file management.
- `datetime` — Tournament timestamps and record generation.

No third-party Python packages are required.

---

## 📂 Project Structure

```text
10-rock-paper-scissors/
│
├── main.py
├── README.md
│
├── game_data/
│   ├── tournament_history.csv
│   └── game_audit_log.txt
│
└── scorecards/
    ├── Scorecard_TRN-1001.txt
    └── Scorecard_TRN-1002.txt
```

**Note:** The `game_data/` and `scorecards/` directories and their files are generated automatically when the application runs.

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

### 3. Navigate to the Project Directory

```bash
cd python-fundamentals-projects/10-rock-paper-scissors
```

### 4. Run the Application

```bash
python main.py
```

---

## 🖥️ Interactive Console Interface

The application provides a menu-driven interface for starting tournaments, reviewing historical matches, exploring game rules, and viewing audit logs.

```text
=================================================================
      ⚔️ ADAPTIVE ROCK, PAPER, SCISSORS / RPSLS ARENA
=================================================================
  [1] Start New Tournament Series (Best-of-N)
  [2] View Historical Tournament Ledger (CSV)
  [3] View Game Variants & Move Rules
  [4] View Game Audit Logs
  [5] Exit System
=================================================================
```

---

## 🎮 Sample Round Simulation

Example of a tournament round using the extended RPSLS ruleset:

```text
--- [ROUND 3] --- Score: Player [1] | AI [1] (Ties: 0)

Choose your move (R/P/S/L/K): K

  Player Move : Spock
  AI Move     : Lizard
  Resolution  : Lizard poisons Spock
  Result      : POINT AWARDED TO AI!

--- [ROUND 4] --- Score: Player [1] | AI [2] (Ties: 0)

Choose your move (R/P/S/L/K): R

  Player Move : Rock
  AI Move     : Scissors
  Resolution  : Rock crushes Scissors
  Result      : POINT AWARDED TO YOU!
```

---

## 📜 Sample Tournament Scorecard

The application can export a detailed text-based tournament scorecard.

```text
======================================================================
             TOURNAMENT MATCH SCORECARD
======================================================================
Tournament ID   : TRN-081492
Date & Time     : 2026-10-31 10:48:32
Contestant      : Player
Ruleset Variant : RPSLS
Opponent Engine : Master AI
----------------------------------------------------------------------
Final Standing  : Player [3] - [2] AI
Draws / Ties    : 1
Rounds Played   : 6
Overall Result  : VICTORY
----------------------------------------------------------------------
ROUND-BY-ROUND BREAKDOWN:
Round   Player Move    AI Move        Victor      Resolution
----------------------------------------------------------------------
#1      Rock           Scissors       Player      Rock crushes Scissors
#2      Rock           Paper          AI          Paper covers Rock
#3      Spock          Lizard          AI          Lizard poisons Spock
#4      Rock           Scissors       Player      Rock crushes Scissors
#5      Paper          Paper           Tie         Both selected Paper
#6      Spock          Rock            Player      Spock vaporizes Rock
======================================================================
```

*Sample data is illustrative.*

---

## 🧠 Python Concepts Demonstrated

This project provides practical experience with:

- Variables, data types, and operators.
- Conditional statements and loops.
- Functions and modular programming.
- Lists, dictionaries, and nested data structures.
- Random number generation.
- Probability and frequency calculations.
- Markov Chain transition models.
- Graph-based game relationships.
- Adjacency structures.
- Algorithmic decision-making.
- CSV file reading and writing.
- File and directory management.
- Date and time handling.
- Input validation and exception handling.
- Tournament scoring and statistics.

---

## 🎯 Learning Outcomes

After exploring this project, beginners should understand how to:

1. Build an interactive command-line game.
2. Implement multiple game rule systems.
3. Represent relationships between game moves using dictionaries.
4. Use random selection to simulate computer opponents.
5. Track player behavior through historical data.
6. Calculate transition probabilities.
7. Implement a basic first-order Markov prediction model.
8. Design difficulty levels using probabilistic strategies.
9. Manage multi-round tournaments.
10. Store match history and generate scorecards using file handling.

---

## 🔍 Suggested Improvements

Extend the project with additional features:

- A graphical interface using Tkinter or Pygame.
- A web-based multiplayer mode.
- Online tournament leaderboards.
- Persistent player profiles and statistics.
- Advanced opponent strategies using longer move histories.
- Reinforcement learning experiments.
- Tournament analytics and win-rate visualizations.
- Unit tests for all game rules and prediction algorithms.
- Difficulty adjustment based on player performance.

---

## 📺 Video Tutorial

Follow the project walkthrough to understand the game rules, explore the adaptive opponent, and learn how the Markov Chain prediction model works.

**YouTube:** [Watch the Project Tutorial](ADD_YOUTUBE_VIDEO_LINK)

---

## 🌐 Learning Resources

Explore more beginner-friendly programming projects and learning resources.

**Website:** [Visit My Learning Hub](ADD_WEBSITE_LINK)

**GitHub Repository:** [Python Fundamentals Projects](https://github.com/rabeeanaseer/python-fundamentals-projects)

---

## 🤝 Contributing

Suggestions, improvements, and contributions are welcome.

1. Fork the repository.
2. Create a new branch.
3. Implement your changes.
4. Submit a pull request.

---

## 📄 License

This project is intended for educational and learning purposes. Add a license file to the repository if you want to define explicit permissions for reuse and distribution.

---

## ⭐ Support

If this project helps you understand Python programming, probability, and basic game AI concepts, consider giving the repository a star on GitHub.

Explore the other projects in the collection and keep building!
