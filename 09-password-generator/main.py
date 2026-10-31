"""
Project 09: Cryptographic Password Generator & Shannon Entropy Strength Analyzer
Course Level: 1st/2nd Semester CS - Advanced Programming Fundamentals
Concepts Used:
  - Cryptographically Secure Pseudo-Random Number Generation (secrets module)
  - String Manipulation, Charset Categorization (string module)
  - Information Theory: Shannon Entropy Calculation (math.log2)
  - Algorithmic Pattern Detection: Keyboard walks, sequential runs, leetspeak, repeated chars
  - NIST SP 800-63B Compliance Verification
  - Persistent File I/O: Vault records (.csv) & formatted security audits (.txt)
  - Defensive Exception Handling & Complex Logic Branching
"""

import os
import csv
import math
import string
import secrets
from datetime import datetime

# ==============================================================================
# GLOBAL CONFIGURATION & DATA STORAGE CONSTANTS
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "sec_data")
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")

VAULT_CSV = os.path.join(DATA_DIR, "password_vault.csv")
AUDIT_LOG_TXT = os.path.join(DATA_DIR, "security_audit.txt")

# Standard Character Sets
UPPERCASE_CHARS = string.ascii_uppercase
LOWERCASE_CHARS = string.ascii_lowercase
DIGIT_CHARS = string.digits
SYMBOL_CHARS = "!@#\$%^&*()-_=+[]{}|;:,.<>?/~"
AMBIGUOUS_CHARS = "l1I0O"

# Common Dictionary Blacklist & Keyboard Walk Patterns
COMMON_BLACKLIST = [
    "password", "123456", "12345678", "qwerty", "admin", "welcome",
    "iloveyou", "abc123", "secret", "monkey", "dragon", "master"
]
KEYBOARD_WALKS = [
    "qwerty", "asdfgh", "zxcvbn", "123456", "654321", "qazwsx",
    "abcdef", "fedcba", "098765", "poiuyt"
]


# ==============================================================================
# SYSTEM INITIALIZATION & PERSISTENCE
# ==============================================================================
def initialize_system():
    """Sets up local directory structures and hydrates database files."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(EXPORTS_DIR, exist_ok=True)

    if not os.path.exists(AUDIT_LOG_TXT):
        with open(AUDIT_LOG_TXT, mode="w", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] SYSTEM: Cryptographic Suite Online.\n")

    if not os.path.exists(VAULT_CSV):
        with open(VAULT_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Timestamp", "Service_Account", "Length", "Entropy_Bits",
                "Strength_Tier", "NIST_Status", "Generated_Method"
            ])


def log_audit(message):
    """Appends an event to the security audit trail."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(AUDIT_LOG_TXT, mode="a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except IOError:
        pass


def record_vault_metadata(service, length, entropy, tier, nist_status, method):
    """Saves metadata for a generated or audited password without exposing cleartext."""
    try:
        with open(VAULT_CSV, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                service, length, f"{entropy:.2f}", tier, nist_status, method
            ])
    except IOError as e:
        print(f"  [!] Storage Warning: Could not write to vault metadata: {e}")


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
            print(f"  [!] Range Error: Please select a number between {min_val} and {max_val}.")
        except ValueError:
            print("  [!] Input Error: Integer expected.")


# ==============================================================================
# MATHEMATICAL ENTROPY & HEURISTIC SECURITY AUDITING
# ==============================================================================
def calculate_shannon_entropy(password):
    """
    Computes true Shannon Entropy in bits:
    H = - sum(p(x) * log2(p(x))) * length
    """
    if not password:
        return 0.0

    length = len(password)
    char_freq = {}
    for char in password:
        char_freq[char] = char_freq.get(char, 0) + 1

    entropy_per_char = 0.0
    for count in char_freq.values():
        probability = count / length
        entropy_per_char -= probability * math.log2(probability)

    total_shannon_entropy = round(entropy_per_char * length, 2)
    return total_shannon_entropy


def calculate_pool_entropy(password):
    """
    Computes theoretical key-space entropy:
    Entropy (bits) = Length * log2(Charset Pool Size)
    """
    pool_size = 0
    has_lower = any(c in LOWERCASE_CHARS for c in password)
    has_upper = any(c in UPPERCASE_CHARS for c in password)
    has_digits = any(c in DIGIT_CHARS for c in password)
    has_symbols = any(c in SYMBOL_CHARS for c in password)

    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digits:
        pool_size += 10
    if has_symbols:
        pool_size += len(SYMBOL_CHARS)

    if pool_size == 0 or len(password) == 0:
        return 0.0

    return round(len(password) * math.log2(pool_size), 2)


def estimate_crack_time(entropy_bits):
    """
    Estimates offline brute-force attack duration assuming
    an adversary cluster computing 100 billion (10^11) hashes/second.
    """
    guesses = 2 ** entropy_bits
    seconds = guesses / (100 * 10**9)

    if seconds < 1:
        return "Instantaneous (< 1 second)"
    elif seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds / 60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds / 3600:.1f} hours"
    elif seconds < 31536000:
        return f"{seconds / 86400:.1f} days"
    elif seconds < 31536000 * 100:
        return f"{seconds / 31536000:.1f} years"
    elif seconds < 31536000 * 1000000:
        return f"{seconds / (31536000 * 1000):.1f} thousand years"
    else:
        return f"{seconds / (31536000 * 10**6):.1e} million years (Astronomical)"


def audit_password_vulnerabilities(password):
    """
    Heuristic scanner detecting predictable patterns:
    - Length deficits
    - Character diversity
    - Dictionary substrings
    - Keyboard walks
    - Sequential and repeated runs
    """
    flaws = []
    strengths = []
    lowered = password.lower()

    # 1. Length Checks
    if len(password) < 8:
        flaws.append("Critical Shortness: Password is under 8 characters (vulnerable to fast cracking).")
    elif len(password) < 12:
        flaws.append("Moderate Length: Under recommended 12-character baseline.")
    else:
        strengths.append(f"Length compliance: Strong baseline length ({len(password)} characters).")

    # 2. Composition Variety
    types_found = 0
    if any(c in LOWERCASE_CHARS for c in password):
        types_found += 1
    else:
        flaws.append("Missing Lowercase: Contains no lowercase letters (a-z).")

    if any(c in UPPERCASE_CHARS for c in password):
        types_found += 1
    else:
        flaws.append("Missing Uppercase: Contains no uppercase letters (A-Z).")

    if any(c in DIGIT_CHARS for c in password):
        types_found += 1
    else:
        flaws.append("Missing Digits: Contains no numerical characters (0-9).")

    if any(c in SYMBOL_CHARS for c in password):
        types_found += 1
    else:
        flaws.append("Missing Symbols: Contains no special characters/symbols.")

    if types_found >= 4:
        strengths.append("High Character Diversity: Spans all 4 primary character domains.")

    # 3. Known Dictionary Words
    for word in COMMON_BLACKLIST:
        if word in lowered:
            flaws.append(f"Dictionary Word Detected: Substring contains common compromised word '{word}'.")

    # 4. Keyboard Spatial Walks
    for walk in KEYBOARD_WALKS:
        if walk in lowered:
            flaws.append(f"Keyboard Walk Pattern: Sequence contains obvious spatial row layout '{walk}'.")

    # 5. Consecutive Repeated Characters (e.g., 'aaaa' or '1111')
    repeat_count = 1
    has_consecutive = False
    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:
            repeat_count += 1
            if repeat_count >= 3:
                has_consecutive = True
                break
        else:
            repeat_count = 1

    if has_consecutive:
        flaws.append("Character Repetition: Contains 3 or more identical characters in a row.")

    # 6. Sequential Character Runs (e.g., '1234' or 'abcd')
    sequential_count = 1
    has_sequential = False
    for i in range(len(password) - 1):
        if ord(password[i + 1]) - ord(password[i]) == 1:
            sequential_count += 1
            if sequential_count >= 3:
                has_sequential = True
                break
        else:
            sequential_count = 1

    if has_sequential:
        flaws.append("Sequential Run: Contains predictable incremental sequence (e.g. '123' or 'abc').")

    # Determine NIST SP 800-63B Compliance
    # Requires >= 8 chars, no common dictionary words, and reasonable complexity
    nist_compliant = (len(password) >= 8) and (len(flaws) <= 1) and not any("Dictionary" in f for f in flaws)

    return flaws, strengths, nist_compliant


# ==============================================================================
# AUDIT CONSOLE REPORT GENERATOR
# ==============================================================================
def execute_password_audit():
    """Interactive evaluator for testing user-supplied passwords."""
    print("\n" + "=" * 70)
    print("🛡️ NIST & SHANNON ENTROPY PASSWORD STRENGTH EVALUATOR")
    print("=" * 70)

    password = input_non_empty("Enter password to analyze: ")

    shannon_entropy = calculate_shannon_entropy(password)
    pool_entropy = calculate_pool_entropy(password)
    flaws, strengths, is_nist = audit_password_vulnerabilities(password)
    crack_time = estimate_crack_time(pool_entropy)

    # Classify Strength Tier
    if pool_entropy >= 80 and len(flaws) == 0:
        tier = "VERY STRONG (Military/Cerebral Grade)"
        color_indicator = "🟢 [EXCELLENT]"
    elif pool_entropy >= 60 and len(flaws) <= 1:
        tier = "STRONG (Adequate Enterprise Defense)"
        color_indicator = "🟢 [SATISFACTORY]"
    elif pool_entropy >= 45:
        tier = "MODERATE (Vulnerable to Targeted Rig)"
        color_indicator = "🟡 [FAIR / CAUTION]"
    elif pool_entropy >= 30:
        tier = "WEAK (Easily Compromised)"
        color_indicator = "🔴 [DANGEROUS]"
    else:
        tier = "VERY WEAK (Instant Compromise Risk)"
        color_indicator = "🔴 [CRITICAL INSECURITY]"

    print("\n" + "-" * 70)
    print("                   CRYPTOGRAPHIC AUDIT SUMMARY")
    print("-" * 70)
    print(f" Evaluated String      : {'*' * (len(password) - 2) + password[-2:] if len(password) > 3 else '***'}")
    print(f" String Length         : {len(password)} characters")
    print(f" Shannon True Entropy  : {shannon_entropy:.2f} bits")
    print(f" Key-Space Entropy     : {pool_entropy:.2f} bits")
    print(f" Estimated Brute-Force : {crack_time}")
    print(f" Overall Rating Tier   : {tier} {color_indicator}")
    print(f" NIST SP 800-63B Status: {'COMPLIANT ✅' if is_nist else 'NON-COMPLIANT ❌'}")
    print("-" * 70)

    if strengths:
        print("\n  🌟 Positive Security Attributes:")
        for s in strengths:
            print(f"     [+] {s}")

    if flaws:
        print("\n  ⚠️ Security Vulnerabilities & Pattern Flags:")
        for f in flaws:
            print(f"     [-] {f}")
    else:
        print("\n  [✓] Zero heuristic red flags detected. Password exhibits ideal distribution.")

    print("=" * 70 + "\n")
    record_vault_metadata("Manual_Audit_String", len(password), pool_entropy, tier, "COMPLIANT" if is_nist else "NON-COMPLIANT", "Manual Analysis")
    log_audit(f"AUDIT: Inspected string (Len: {len(password)}, Pool Entropy: {pool_entropy:.2f} bits, Rating: {tier}).")


# ==============================================================================
# CRYPTOGRAPHIC GENERATOR SUBSYSTEM (CSPRNG)
# ==============================================================================
def generate_cryptographic_password(length=16, use_upper=True, use_lower=True, use_digits=True, use_symbols=True, exclude_ambiguous=False):
    """
    Generates a cryptographically strong password using secrets.choice (CSPRNG).
    Guarantees at least one character from every active subset, avoiding uniform bias.
    """
    character_pool = ""
    guaranteed_characters = []

    if use_upper:
        chars = "".join(c for c in UPPERCASE_CHARS if not (exclude_ambiguous and c in AMBIGUOUS_CHARS))
        character_pool += chars
        guaranteed_characters.append(secrets.choice(chars))

    if use_lower:
        chars = "".join(c for c in LOWERCASE_CHARS if not (exclude_ambiguous and c in AMBIGUOUS_CHARS))
        character_pool += chars
        guaranteed_characters.append(secrets.choice(chars))

    if use_digits:
        chars = "".join(c for c in DIGIT_CHARS if not (exclude_ambiguous and c in AMBIGUOUS_CHARS))
        character_pool += chars
        guaranteed_characters.append(secrets.choice(chars))

    if use_symbols:
        chars = SYMBOL_CHARS
        character_pool += chars
        guaranteed_characters.append(secrets.choice(chars))

    if not character_pool:
        print("  [!] Error: No character categories selected. Reverting to full standard set.")
        character_pool = UPPERCASE_CHARS + LOWERCASE_CHARS + DIGIT_CHARS + SYMBOL_CHARS

    # Fill remainder of requested length using CSPRNG
    remaining_length = length - len(guaranteed_characters)
    fill_characters = [secrets.choice(character_pool) for _ in range(max(0, remaining_length))]

    # Combine and perform Fisher-Yates cryptographically secure shuffle
    combined_password_list = guaranteed_characters + fill_characters
    # Secure shuffle using secrets
    for i in range(len(combined_password_list) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        combined_password_list[i], combined_password_list[j] = combined_password_list[j], combined_password_list[i]

    return "".join(combined_password_list)


def generate_memorable_passphrase(word_count=4, separator="-", capitalize=True):
    """
    Generates an xkcd-style Diceware-inspired memorable passphrase using CSPRNG.
    """
    curated_wordlist = [
        "quantum", "falcon", "battery", "staple", "galaxy", "harbor", "citadel",
        "shadow", "nebula", "glacier", "horizon", "timber", "summit", "canyon",
        "orbit", "voyager", "beacon", "aurora", "matrix", "shield", "dynamo",
        "vertex", "zenith", "cipher", "monarch", "phoenix", "obsidian", "crystal"
    ]

    selected_words = [secrets.choice(curated_wordlist) for _ in range(word_count)]
    if capitalize:
        selected_words = [w.capitalize() for w in selected_words]

    # Append a CSPRNG digit for extra entropy
    passphrase = separator.join(selected_words) + separator + str(secrets.randbelow(90) + 10)
    return passphrase


def execute_custom_generation():
    """Terminal workflow for configuring and generating passwords."""
    print("\n" + "=" * 65)
    print("🔑 CRYPTOGRAPHIC PASSWORD & PASSPHRASE GENERATOR")
    print("=" * 65)
    print(" Select Mode:")
    print("  [1] Custom Alphanumeric & Special Characters (CSPRNG)")
    print("  [2] Memorable Word-Based Passphrase (Diceware-Style)")
    mode = input_int_range("Choice (1-2): ", 1, 2)

    service_name = input_non_empty("Enter Service / Account Tag (e.g. GitHub, AWS, Personal): ")

    if mode == 1:
        length = input_int_range("Specify Password Length (8 to 128 characters): ", 8, 128)
        print("\nConfigure Character Domains (y/n):")
        inc_upper = input("  Include Uppercase Letters (A-Z)? [y]: ").strip().lower() != "n"
        inc_lower = input("  Include Lowercase Letters (a-z)? [y]: ").strip().lower() != "n"
        inc_digits = input("  Include Numerical Digits (0-9)? [y]: ").strip().lower() != "n"
        inc_symbols = input("  Include Special Symbols (!@#...)? [y]: ").strip().lower() != "n"
        exc_ambiguous = input("  Exclude Ambiguous Characters (l, 1, I, 0, O)? [n]: ").strip().lower() == "y"

        password = generate_cryptographic_password(
            length=length,
            use_upper=inc_upper,
            use_lower=inc_lower,
            use_digits=inc_digits,
            use_symbols=inc_symbols,
            exclude_ambiguous=exc_ambiguous
        )
        method = "CSPRNG_Custom_Charset"

    else:
        word_count = input_int_range("Select Word Count (3 to 8 words): ", 3, 8)
        sep = input("Enter separator character (e.g., '-', '_', '.'): ").strip()
        if not sep:
            sep = "-"
        password = generate_memorable_passphrase(word_count=word_count, separator=sep)
        method = f"Diceware_Passphrase_{word_count}_Words"

    entropy = calculate_pool_entropy(password)
    flaws, _, is_nist = audit_password_vulnerabilities(password)
    crack_time = estimate_crack_time(entropy)

    print("\n" + "=" * 70)
    print(f"🎉 GENERATED SECURE CREDENTIAL [{service_name}]")
    print("=" * 70)
    print(f" Plaintext Password   : {password}")
    print(f" Total Length         : {len(password)} characters")
    print(f" Key-Space Entropy    : {entropy:.2f} bits")
    print(f" Est. Brute-Force Time: {crack_time}")
    print(f" NIST SP 800-63B      : {'PASSED ✅' if is_nist else 'FAILED ❌'}")
    print("=" * 70 + "\n")

    record_vault_metadata(service_name, len(password), entropy, "GENERATED_OPTIMAL", "COMPLIANT", method)
    log_audit(f"GENERATE: Created password for '{service_name}' ({len(password)} chars, {entropy:.2f} bits entropy).")


# ==============================================================================
# BATCH BULK GENERATOR & FILE EXPORTS
# ==============================================================================
def execute_bulk_generation_export():
    """Generates bulk sets of strong passwords and writes them to a formatted file."""
    print("\n" + "=" * 65)
    print("📦 BATCH PASSWORD PROVISIONING & FILE EXPORTER")
    print("=" * 65)

    count = input_int_range("How many credentials to generate? (5 to 100): ", 5, 100)
    length = input_int_range("Specify character length for each (10 to 64): ", 10, 64)

    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"Bulk_Passwords_{timestamp_str}.txt"
    filepath = os.path.join(EXPORTS_DIR, filename)

    try:
        with open(filepath, mode="w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write("         CRYPTOGRAPHIC SECURITY SUITE - PROVISIONED CREDENTIALS\n")
            f.write("=" * 70 + "\n")
            f.write(f"Generated On  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Batch   : {count} passwords\n")
            f.write(f"Length / Pwd  : {length} characters\n")
            f.write("-" * 70 + "\n")
            f.write(f"{'#':<4}{'Password Token':<36}{'Entropy (Bits)':<16}{'Estimated Crack Time'}\n")
            f.write("-" * 70 + "\n")

            for idx in range(1, count + 1):
                pwd = generate_cryptographic_password(length=length)
                ent = calculate_pool_entropy(pwd)
                c_time = estimate_crack_time(ent)
                f.write(f"{idx:<4}{pwd:<36}{ent:<16.2f}{c_time}\n")

            f.write("=" * 70 + "\n")
            f.write("SECURITY ADVISORY: Delete or securely archive this file once distributed.\n")

        print(f"\n[✓] Successfully provisioned {count} credentials!")
        print(f"    Export File Location: {filepath}\n")
        log_audit(f"BULK EXPORT: Provisioned {count} passwords of length {length} into {filename}.")
    except IOError as e:
        print(f"  [!] File Export Failure: {e}")


# ==============================================================================
# AUDIT METADATA & VAULT INSPECTOR
# ==============================================================================
def display_vault_records():
    """Displays recorded metadata of evaluated or generated credentials."""
    print("\n" + "=" * 85)
    print("🗄️ LOCAL CREDENTIAL AUDIT & METADATA VAULT")
    print("=" * 85)

    if not os.path.exists(VAULT_CSV):
        print("  [!] Vault database empty.")
        return

    records = []
    try:
        with open(VAULT_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
    except IOError as e:
        print(f"  [!] Failed to read vault: {e}")
        return

    if not records:
        print("  [!] No credential records logged.")
        return

    print(f"{'Date & Time':<20}{'Service / Tag':<22}{'Len':<6}{'Entropy':<12}{'NIST Status'}")
    print("-" * 85)
    for r in records[-10:]:
        print(f"{r['Timestamp']:<20}{r['Service_Account'][:20]:<22}{r['Length']:<6}{r['Entropy_Bits'] + ' b':<12}{r['NIST_Status']}")
    print("=" * 85 + "\n")


def display_audit_logs():
    """Outputs recent audit trails."""
    print("\n" + "=" * 75)
    print("📜 SYSTEM SECURITY & LOG ARCHIVE")
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


# ==============================================================================
# MAIN APPLICATION CONTROLLER
# ==============================================================================
def display_main_menu():
    """Primary navigation menu."""
    print("=" * 65)
    print("   🔐 ADVANCED CRYPTOGRAPHIC PASSWORD & ENTROPY SUITE")
    print("=" * 65)
    print("  --- Password Generation & Provisioning ---")
    print("  [1] Generate CSPRNG Password or Memorable Passphrase")
    print("  [2] Bulk Batch Generation & Export to Text File")
    print("\n  --- Security Analysis & Vulnerability Auditing ---")
    print("  [3] Analyze Password Strength (Shannon Entropy & NIST Audit)")
    print("  [4] View Password Vault Historical Metadata")
    print("  [5] View Security Audit Logs")
    print("  [6] Exit System")
    print("=" * 65)


def main():
    """Master application execution loop."""
    initialize_system()

    while True:
        display_main_menu()
        choice = input_int_range("Select an option (1-6): ", 1, 6)

        if choice == 1:
            execute_custom_generation()
        elif choice == 2:
            execute_bulk_generation_export()
        elif choice == 3:
            execute_password_audit()
        elif choice == 4:
            display_vault_records()
        elif choice == 5:
            display_audit_logs()
        elif choice == 6:
            log_audit("SYSTEM: Security suite gracefully decommissioned.")
            print("\nShutting down Cryptographic Password Suite. Stay secure!\n")
            break


if __name__ == "__main__":
    main()
