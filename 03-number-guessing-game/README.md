
# 🎯 Precision Number Guessing Game with AI Hint System

An interactive, terminal-based Python number guessing game featuring an algorithmic hint engine, thermal proximity feedback, multiple difficulty levels, dynamic scoring, and a persistent leaderboard.

Part of the **10 Beginner Python Projects – First Semester Collection**, this project demonstrates practical applications of random number generation, loops, conditional statements, mathematical operations, functions, input validation, and file handling through an engaging game environment.

---

## 📌 Project Overview

Traditional number guessing games provide basic directional feedback, telling players whether their guess is higher or lower than the hidden number.

This project takes the classic guessing game further by introducing an algorithmic hint system that provides mathematical clues about the secret number.

Players can request hints involving parity, prime numbers, mathematical factors, numerical ranges, digit sums, and modular arithmetic. Each hint comes with a scoring penalty, encouraging players to balance strategy and accuracy.

The application also features multiple difficulty levels, hot-and-cold proximity feedback, a dynamic scoring system, and persistent player rankings.

It is designed for educational purposes and demonstrates how fundamental Python concepts can be combined to create an interactive, logic-driven game.

---

## ✨ Features

### 🧠 Algorithmic Hint Engine

Players can enter `0` during gameplay to request a mathematical hint about the hidden number.

The hint system includes:

1. **Parity Analysis:** Determines whether the secret number is even or odd.
2. **Prime Number Detection:** Identifies whether the target number is prime.
3. **Factor Identification:** Reveals a mathematical divisor when the secret number is composite.
4. **Range Constriction:** Provides a narrower numerical range around the hidden target.
5. **Digit Analytics:** Calculates the sum of the secret number's individual digits.
6. **Modulo Analysis:** Reveals the final digit using modular arithmetic (`Target % 10`).

Each hint reduces the player's current score, making strategic hint usage an important part of the game.

### 🔥 Thermal Proximity Feedback

The game provides feedback based on how close the player's guess is to the hidden number.

In addition to directional hints, players receive proximity classifications such as:

- **Boiling Hot:** Extremely close to the target.
- **Warm:** Relatively close.
- **Chilly:** Still some distance away.
- **Freezing Cold:** Far from the target.

This feature encourages players to use numerical reasoning rather than relying entirely on random guesses.

### 🎮 Multiple Difficulty Levels

The game provides four predefined difficulty tiers and a customizable mode.

| Difficulty | Number Range | Maximum Attempts | Base Score | Hint Penalty |
|---|:---:|:---:|---:|---:|
| **Novice** | 1–50 | 10 | 500 pts | -30 pts |
| **Adept** | 1–100 | 7 | 1,000 pts | -75 pts |
| **Master** | 1–500 | 9 | 2,500 pts | -150 pts |
| **Grandmaster** | 1–1,000 | 10 | 5,000 pts | -300 pts |
| **Custom** | User-defined | User-defined | 1,000 pts | -50 pts |

**Custom Mode:** Players can define their own lower bounds, upper bounds, and maximum attempts.

### 🏆 Dynamic Scoring System

- Starts each game with a difficulty-based base score.
- Deducts points for incorrect guesses.
- Applies penalties for requesting mathematical hints.
- Rewards unused attempts after successfully finding the target.
- Calculates a final score based on performance and accuracy.

**Accuracy Bonus:** Every unused attempt upon winning awards an additional 100 points.

### 📊 Persistent Leaderboard

- Stores successful game results in `game_data/leaderboard.csv`.
- Maintains player names and scores.
- Automatically ranks the Top 10 players.
- Provides a persistent Hall of Fame across game sessions.

### 📝 Match History & Audit Logging

- Records completed game sessions.
- Tracks victories and defeats.
- Stores timestamps and match outcomes.
- Saves chronological records in `game_data/match_history.txt`.

### 🛡️ Input Validation & Error Handling

- Rejects guesses outside the permitted numerical range.
- Handles invalid input types and unexpected characters.
- Detects duplicate guesses without consuming attempts.
- Validates custom difficulty settings.
- Prevents invalid hint requests from disrupting gameplay.

---

## 📚 Python Concepts Demonstrated

This project demonstrates how fundamental Python programming concepts can be applied to game development.

| Python Concept | Application |
|---|---|
| Variables & Data Types | Tracking scores, attempts, and hidden numbers |
| User Input & Output | Interactive gameplay |
| Conditional Statements | Evaluating guesses and difficulty settings |
| While Loops | Maintaining continuous gameplay |
| Functions | Organizing game logic into reusable components |
| Random Module | Generating secret numbers |
| Lists | Maintaining previous guesses and rankings |
| Mathematical Operations | Parity, factors, digit sums, and modulo |
| Math Module | Efficient integer square root calculations |
| CSV Module | Persistent leaderboard storage |
| File Handling | Recording match history |
| DateTime Module | Generating match timestamps |
| Exception Handling | Handling invalid user input |

---

## 🎮 Game Rules & Scoring

### Scoring System

| Action | Scoring Effect |
|---|---:|
| Starting a game | Receives difficulty-based base score |
| Incorrect guess | Deducts points |
| Requesting a hint | Applies difficulty-based hint penalty |
| Winning with unused attempts | +100 points per unused attempt |
| Duplicate guess | No attempt consumed |

The exact score deductions for incorrect guesses depend on the application's scoring implementation.

### Difficulty Progression

- **Novice:** Ideal for first-time players.
- **Adept:** Introduces a smaller attempt allowance.
- **Master:** Challenges players with a wider number range.
- **Grandmaster:** Tests numerical reasoning with a larger search space.
- **Custom:** Allows players to create their own challenge.

---

## 📂 Project Structure

```text
03-number-guessing-game/
│
├── main.py                     # Main game application
├── README.md                   # Project documentation
│
└── game_data/                  # Automatically created storage directory
    ├── leaderboard.csv         # Persistent high-score records
    └── match_history.txt       # Chronological match logs
```

**Note:** The `game_data/` directory and its files are generated automatically when the application performs relevant operations. They may not exist before the first execution.

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
cd python-fundamentals-projects/03-number-guessing-game
```

### 3. Run the Application

Execute the Python script:

```bash
python main.py
```

No external packages or `pip install` commands are required.

---

## 🖥️ Interactive Console Interface

Upon launching the application, players can navigate through the following menu:

```text
============================================================
     🎯 AI NUMBER GUESSING & INFERENCE SYSTEM
============================================================
  [1] Start New Guessing Game
  [2] View Top 10 Hall of Fame Leaderboard
  [3] View Recent Match History Audit
  [4] Display How the AI Hint Subsystem Works
  [5] Exit Application
============================================================
```

### Menu Options

| Option | Functionality |
|:---:|---|
| 1 | Start a new guessing game and select a difficulty level. |
| 2 | View the Top 10 player leaderboard. |
| 3 | Review recent match history and game outcomes. |
| 4 | Learn how the mathematical hint subsystem works. |
| 5 | Exit the application. |

---

## 🕹️ Sample Gameplay

The following is an illustrative gameplay session demonstrating hint usage, proximity feedback, and score calculation.

```text
[Attempt 3 of 7] - Attempts Left: 5 | Current Score: 715
Recent Guesses: [50 (High), 25 (Low)]

Enter guess [1 - 100] (or 0 for AI Hint): 0

*****************************************************************
💡 AI INTEL MODULE [Hint #1]:
   Parity Analysis: The secret number is an ODD number.
   (Penalty: -75 pts | Score now: 640)
*****************************************************************

[Attempt 3 of 7] - Attempts Left: 5 | Current Score: 640
Recent Guesses: [50 (High), 25 (Low)]

Enter guess [1 - 100] (or 0 for AI Hint): 37

  >> Direction  : Go HIGHER ⬆️!
  >> Thermal    : 🔥 BOILING HOT!

[Attempt 4 of 7] - Attempts Left: 4 | Current Score: 498
Recent Guesses: [50 (High), 25 (Low), 37 (Low)]

Enter guess [1 - 100] (or 0 for AI Hint): 39

======================================================================
🎉 INCREDIBLE! YOU FOUND THE TARGET: 39
   Rounds Taken   : 4
   Accuracy Bonus : +300 pts
   Final Score    : 798 pts
======================================================================
```

*Sample gameplay is illustrative and demonstrates the application's interface and gameplay flow.*

---

## ⚙️ Technical Highlights

- **Standard Library Only:** Uses Python's built-in `random`, `math`, `csv`, `os`, and `datetime` modules. No third-party dependencies are required.
- **Random Number Generation:** Uses Python's `random` module to generate hidden target numbers.
- **Mathematical Number Analysis:** Implements parity checking, prime detection, factor identification, digit summation, and modulo operations.
- **Integer Square Root Optimization:** Uses `math.isqrt(n)` for integer-based square root calculations in prime and factor checking, allowing trial division up to the square root of the target.
- **Dynamic State Management:** Uses loops and variables to maintain attempts, guesses, hints, and scoring.
- **Defensive Input Validation:** Handles invalid entries, duplicate guesses, and out-of-range values.
- **Persistent Data Storage:** Maintains leaderboard and match history across sessions.
- **Modular Game Logic:** Separates gameplay, scoring, hint generation, and record management into reusable functions.

---

## 🎯 Learning Outcomes

After exploring this project, beginners should be able to:

1. Generate random numbers using Python.
2. Build interactive games using loops and conditional statements.
3. Organize game logic using reusable functions.
4. Work with lists and numerical data.
5. Apply mathematical operations to solve programming problems.
6. Implement basic algorithms for prime and factor detection.
7. Create scoring systems using variables and arithmetic.
8. Read and write persistent data using CSV and text files.
9. Implement input validation and exception handling.
10. Build an interactive application with multiple difficulty levels.

---

## 💡 Learning Recommendations

If you are learning Python, try the following:

- Start with the basic higher-or-lower guessing logic.
- Understand how the `random` module generates a target number.
- Experiment with different number ranges and attempt limits.
- Study how parity and prime-number detection work.
- Modify the scoring and hint penalty system.
- Try adding new mathematical hints.
- Experiment with leaderboard sorting and ranking.
- Build your own guessing game after understanding the implementation.

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
