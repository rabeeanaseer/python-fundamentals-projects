
# 🎓 Student Grading & GPA Management System

A comprehensive, menu-driven Python CLI application designed to automate student grading, weighted semester GPA calculations, academic transcript generation, and cohort-level performance analytics.

Part of the **10 Beginner Python Projects – First Semester Collection**, this project demonstrates structured programming, functions, conditional logic, loops, dictionaries, CSV file handling, and input validation through a practical academic management system.

---

## 📌 Project Overview

Calculating university GPA involves more than simply averaging examination marks. It requires converting percentages into letter grades, assigning grade points, accounting for course credit hours, calculating quality points, and determining academic standing.

This application provides an all-in-one console-based academic records management solution.

Users can enter student information, calculate weighted GPAs on a 4.00 scale, maintain persistent student records, search academic data, analyze class performance, and generate individual academic transcripts.

It is designed for educational purposes and demonstrates how fundamental Python concepts can be combined to solve a practical problem.

---

## ✨ Features

### 🎯 Academic Grading & GPA Calculation

- **Weighted GPA Calculation:** Calculates quality points using:

  \[
  \text{Quality Points} = \text{Grade Points} \times \text{Credit Hours}
  \]

  \[
  \text{GPA} = \frac{\text{Total Quality Points}}{\text{Total Credit Hours}}
  \]

- **Flexible Scoring Methods:**
  - Direct Score: Enter a composite score between 0 and 100.
  - Weighted Assessment Breakdown: Calculate final marks from assignments, quizzes, midterm examinations, and final examinations.

- **Academic Standing Classification:** Assigns academic performance categories based on GPA thresholds, including honors, good standing, warning, and probation categories.

### 📊 Student Records Management

- **Persistent CSV Storage:** Saves student records in `records.csv`.
- **Batch Entry Mode:** Process multiple student records in one session.
- **Student Search:** Find previously saved records using Student ID or Name.
- **Data Management:** Maintains student academic information for future retrieval.

### 📄 Automated Transcript Generation

- Generates formatted individual student transcripts.
- Displays course titles, credit hours, marks, letter grades, grade points, and quality points.
- Calculates total credit hours and cumulative quality points.
- Displays semester GPA and academic standing.
- Saves printable transcript reports as `.txt` files.

### 📈 Cohort Performance Analytics

- Calculates class average GPA.
- Calculates average class percentage.
- Identifies top-performing students.
- Displays honor roll and probation distributions.
- Generates an in-terminal grade distribution visualization.

### 🛡️ Input Validation & Error Handling

- Validates numerical input and student information.
- Handles empty inputs and invalid data types.
- Prevents out-of-range scores and credit-hour values.
- Uses defensive error handling to reduce unexpected application crashes.

---

## 🛠️ Grading & Academic Criteria

### Percentage-to-GPA Conversion Scale

The application uses the following illustrative grading scale:

| Percentage Range | Letter Grade | Grade Points | Performance Remark |
|:---:|:---:|:---:|---|
| 85.0% – 100.0% | **A** | 4.00 | Exceptional |
| 80.0% – 84.99% | **A-** | 3.70 | Excellent |
| 75.0% – 79.99% | **B+** | 3.30 | Very Good |
| 70.0% – 74.99% | **B** | 3.00 | Good |
| 65.0% – 69.99% | **B-** | 2.70 | Above Average |
| 61.0% – 64.99% | **C+** | 2.30 | Average |
| 58.0% – 60.99% | **C** | 2.00 | Satisfactory |
| 55.0% – 57.99% | **C-** | 1.70 | Marginal Pass |
| 50.0% – 54.99% | **D** | 1.00 | Low Pass |
| 0.0% – 49.99% | **F** | 0.00 | Fail |

> **Note:** This is an illustrative grading scale for the project. Actual grading policies and academic standing classifications vary between universities and institutions.

### Weighted Assessment Breakdown

The application supports the following assessment distribution:

| Assessment Component | Weight |
|---|:---:|
| Assignments | 15% |
| Quizzes | 15% |
| Midterm Examination | 30% |
| Final Terminal Examination | 40% |
| **Total** | **100%** |

---

## 📚 Python Concepts Demonstrated

This project demonstrates practical applications of fundamental Python programming concepts.

| Python Concept | Application |
|---|---|
| Variables & Data Types | Storing student and academic information |
| User Input & Output | Interactive console interface |
| Conditional Statements | Grade assignment and academic classification |
| Loops | Repeated student and course entry |
| Functions | Modular application structure |
| Lists & Dictionaries | Managing student and course data |
| File Handling | Persistent academic records |
| CSV Module | Reading and writing student databases |
| Exception Handling | Managing invalid input and errors |
| DateTime Module | Generating transcript timestamps |
| String Formatting | Aligning transcript and analytics tables |

---

## 📂 Project Structure

```text
01-student-gpa-calculator/
│
├── main.py              # Main application source code
├── records.csv          # Auto-generated student database
├── README.md            # Project documentation
│
└── transcripts/         # Auto-generated transcript directory
    ├── Transcript_CS-101_F26.txt
    └── Transcript_CS-102_F26.txt
```

**Note:** `records.csv` and the `transcripts/` directory are generated automatically when the application saves records or exports transcripts. They may not exist before the first execution.

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

### 2. Clone the Repository

```bash
git clone https://github.com/rabeeanaseer/python-fundamentals-projects.git
```

### 3. Navigate to the Project Directory

```bash
cd python-fundamentals-projects/01-student-gpa-calculator
```

### 4. Run the Application

```bash
python main.py
```

No external packages or `pip install` commands are required.

---

## 🖥️ Application Menu

Upon launching the application, users can navigate through the following interactive menu:

```text
============================================================
       ACADEMIC GRADING & GPA MANAGEMENT SYSTEM
============================================================
  [1] Enter Single Student Grades & Generate Transcript
  [2] Batch Entry Mode (Multiple Students in Sequence)
  [3] Search Database by Student ID or Name
  [4] View Class Cohort Statistical Analytics
  [5] View Official Grading Scale & Criteria
  [6] Open / Verify Saved Transcripts Directory
  [7] Exit Application
============================================================
```

### Menu Options

| Option | Functionality |
|:---:|---|
| 1 | Enter individual student information, calculate grades, and generate a transcript. |
| 2 | Process multiple student records in sequence. |
| 3 | Search saved records using Student ID or Name. |
| 4 | View class-wide performance statistics and rankings. |
| 5 | Display the grading scale and academic criteria. |
| 6 | Open or verify the saved transcripts directory. |
| 7 | Exit the application. |

---

## 📄 Sample Academic Transcript

The following is an illustrative example of the generated transcript format:

```text
================================================================================
                     OFFICIAL ACADEMIC TRANSCRIPT
================================================================================
 Student Name   : Jane Doe                     Student ID : CS-2026-042
 Semester / Term: FALL 2026                    Generated  : 2026-10-31 10:25:00
--------------------------------------------------------------------------------
#  Course Title / Code       Credits  Marks    Grade   GP    Quality Pts
--------------------------------------------------------------------------------
1  PROGRAMMING FUNDAMENTALS  4        88.5     A       4.00  16.00
2  DISCRETE MATHEMATICS      3        82.0     A-      3.70  11.10
3  DIGITAL LOGIC DESIGN      3        74.0     B       3.00  9.00
4  FUNCTIONAL ENGLISH        2        91.0     A       4.00  8.00
--------------------------------------------------------------------------------
Total Credit Hours Attempted                  : 12
Total Quality Points Accumulated              : 44.10
Cumulative Weighted Percentage                : 83.88%
Semester Grade Point Average (GPA)            : 3.68 / 4.00
Official Academic Standing                    : Magna Cum Laude (Dean's Honor Roll)
--------------------------------------------------------------------------------

--- INDIVIDUAL COURSE ANALYTICS ---
 • Courses Cleared : 4 | Backlogs/Failed : 0
 • Highest Score   : 91.00% (FUNCTIONAL ENGLISH)
 • Lowest Score    : 74.00% (DIGITAL LOGIC DESIGN)

--- GRADE DISTRIBUTION VISUALIZER ---
   Grade A   | 02 course(s) ██████
   Grade A-  | 01 course(s) ███
   Grade B   | 01 course(s) ███
================================================================================
```

*Sample data is illustrative and intended to demonstrate the application's output format.*

---

## ⚙️ Technical Highlights

- **Standard Library Only:** Uses Python's built-in modules, including `os`, `csv`, and `datetime`. No third-party dependencies are required.
- **Structured Programming:** Organizes application logic into reusable functions.
- **Persistent Data Storage:** Uses CSV files to retain student records between application sessions.
- **Defensive Error Handling:** Handles invalid data types, empty inputs, and out-of-range values.
- **Formatted Console Output:** Uses Python string formatting to align academic tables and transcript information.
- **Automated File Generation:** Creates transcript directories and individual text reports when needed.

---

## 🎯 Learning Outcomes

After exploring this project, beginners should be able to:

1. Build menu-driven Python applications.
2. Apply conditional logic to real-world grading scenarios.
3. Use loops for repeated data entry and processing.
4. Organize programs using reusable functions.
5. Manage structured data using lists and dictionaries.
6. Read and write persistent records using CSV files.
7. Generate formatted reports using Python.
8. Implement basic input validation and exception handling.
9. Apply mathematical formulas to practical programming problems.

---

## 💡 Learning Recommendations

If you are a beginner, try the following:

- Understand the grading formula before exploring the implementation.
- Run the application with different student records.
- Experiment with different credit hours and marks.
- Observe how letter grades and GPA values change.
- Try adding additional academic features independently.
- Rebuild the application from scratch after understanding its logic.

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
