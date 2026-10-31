"""
Project 04: Digital ATM Simulation & Automated Teller Management System
Course Level: 1st Semester CS / Programming Fundamentals
Concepts Used:
  - While loops & Sentinel Control Flags
  - Modular Functions with State Passing
  - Dictionaries & In-Memory Ledgers
  - Hashlib / String transformations for secure PIN management
  - Mathematical Transaction Validation (Denominations, Limits, Overdrafts)
  - Persistent File I/O: CSV Accounts Database and TXT Transaction Slips
  - Defensive Exception Handling (try/except)
"""

import os
import csv
import hashlib
from datetime import datetime

# ==============================================================================
# GLOBAL CONFIGURATION & DATA STORAGE CONSTANTS
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "atm_data")
RECEIPTS_DIR = os.path.join(BASE_DIR, "receipts")
ACCOUNTS_CSV = os.path.join(DATA_DIR, "accounts_db.csv")
AUDIT_LOG_TXT = os.path.join(DATA_DIR, "atm_audit_log.txt")

# ATM Machine Physical Reserve Limits
ATM_VAULT = {
    "cash_reserve": 500000.0,
    "max_withdrawal_per_txn": 50000.0,
    "min_withdrawal_per_txn": 500.0,
    "valid_denominations": [5000, 1000, 500]
}

# In-Memory Customer Account Registry
# Form: { card_number: { name, pin_hash, balance, account_type, status, failed_attempts, tx_history } }
ACCOUNTS_REGISTRY = {}


# ==============================================================================
# SECURITY & CRYPTOGRAPHIC HASHING UTILITY
# ==============================================================================
def hash_pin(pin_str):
    """Generates a secure SHA-256 hash representation of a 4-digit PIN."""
    return hashlib.sha256(pin_str.encode("utf-8")).hexdigest()


# ==============================================================================
# SYSTEM INITIALIZATION & PERSISTENCE
# ==============================================================================
def initialize_system():
    """Sets up local directory structures and loads/creates persistent account store."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RECEIPTS_DIR, exist_ok=True)

    # Initialize Hardware Audit Log
    if not os.path.exists(AUDIT_LOG_TXT):
        with open(AUDIT_LOG_TXT, mode="w", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ATM SYSTEM: Automated Teller Online.\n")

    # Seed Default Bank Customers if CSV does not exist
    if not os.path.exists(ACCOUNTS_CSV):
        default_seed_accounts = [
            ["1001", "Ali Ahmed", hash_pin("1234"), "85000.0", "Current", "Active", "0"],
            ["1002", "Fatima Zahra", hash_pin("4321"), "142000.0", "Savings", "Active", "0"],
            ["1003", "Usman Tariq", hash_pin("7890"), "25000.0", "Current", "Active", "0"],
            ["1004", "Ayesha Khan", hash_pin("0000"), "500.0", "Savings", "Active", "0"]
        ]
        with open(ACCOUNTS_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Card_Number", "Account_Holder", "PIN_Hash", "Balance", 
                "Account_Type", "Account_Status", "Failed_Attempts"
            ])
            writer.writerows(default_seed_accounts)

    load_accounts_from_csv()


def log_vault_action(message):
    """Appends an event to the local hardware audit trail."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(AUDIT_LOG_TXT, mode="a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except IOError:
        pass


def load_accounts_from_csv():
    """Hydrates runtime dictionary from CSV flat database."""
    global ACCOUNTS_REGISTRY
    ACCOUNTS_REGISTRY.clear()

    try:
        with open(ACCOUNTS_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                c_num = row["Card_Number"]
                ACCOUNTS_REGISTRY[c_num] = {
                    "card_number": c_num,
                    "name": row["Account_Holder"],
                    "pin_hash": row["PIN_Hash"],
                    "balance": float(row["Balance"]),
                    "type": row["Account_Type"],
                    "status": row["Account_Status"],
                    "failed_attempts": int(row["Failed_Attempts"]),
                    "transactions": []
                }
    except Exception as e:
        print(f"  [!] Database Sync Warning: {e}")


def save_accounts_to_csv():
    """Flushes active balances and lockout states to disk."""
    try:
        with open(ACCOUNTS_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Card_Number", "Account_Holder", "PIN_Hash", "Balance", 
                "Account_Type", "Account_Status", "Failed_Attempts"
            ])
            for acc in ACCOUNTS_REGISTRY.values():
                writer.writerow([
                    acc["card_number"], acc["name"], acc["pin_hash"], 
                    acc["balance"], acc["type"], acc["status"], acc["failed_attempts"]
                ])
    except IOError as e:
        print(f"  [!] Disk Write Error: {e}")


# ==============================================================================
# INPUT VALIDATION UTILITIES
# ==============================================================================
def get_clean_string(prompt):
    """Returns validated, non-empty terminal input."""
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("  [!] Input cannot be empty. Please retry.")


def get_valid_int(prompt, min_val, max_val):
    """Validates integer within specified boundaries."""
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if min_val <= val <= max_val:
                return val
            print(f"  [!] Value must be between {min_val} and {max_val}.")
        except ValueError:
            print("  [!] Invalid number. Whole numbers expected.")


def get_valid_float(prompt, min_val, max_val):
    """Validates decimal currency within specified bounds."""
    while True:
        raw = input(prompt).strip()
        try:
            val = float(raw)
            if min_val <= val <= max_val:
                return round(val, 2)
            print(f"  [!] Amount must be between PKR {min_val:,.2f} and PKR {max_val:,.2f}.")
        except ValueError:
            print("  [!] Invalid monetary input. Decimal value expected.")


# ==============================================================================
# AUTHENTICATION & SECURITY SUBSYSTEM
# ==============================================================================
def authenticate_user():
    """
    Handles user login flow with card check and 3-attempt PIN security lockout.
    Returns: account dictionary if authenticated, None otherwise.
    """
    print("\n" + "=" * 65)
    print("💳 SECURE CARD INSERTION & USER AUTHENTICATION")
    print("=" * 65)

    card_num = get_clean_string("Insert Card (Enter 4-Digit Card Number): ")

    if card_num not in ACCOUNTS_REGISTRY:
        print("  [x] Card unrecognized. Transaction terminated.")
        log_vault_action(f"AUTH REJECT: Unrecognized card number '{card_num}' entered.")
        return None

    account = ACCOUNTS_REGISTRY[card_num]

    # Verify card status
    if account["status"] == "LOCKED":
        print("\n  [⛔] SECURITY ALERT: This card has been BLOCKED due to excessive failed PIN attempts.")
        print("       Please contact your bank branch to unblock your credentials.")
        log_vault_action(f"AUTH BLOCKED: Access attempted on locked account {card_num}.")
        return None

    # PIN Verification Loop (Max 3 Attempts)
    while account["failed_attempts"] < 3:
        remaining_chances = 3 - account["failed_attempts"]
        pin_input = input(f"Enter 4-Digit Secret PIN ({remaining_chances} attempt(s) remaining): ").strip()

        if hash_pin(pin_input) == account["pin_hash"]:
            account["failed_attempts"] = 0
            save_accounts_to_csv()
            log_vault_action(f"AUTH SUCCESS: Account {card_num} ({account['name']}) logged in.")
            print(f"\n[✓] Welcome, {account['name']}!")
            return account
        else:
            account["failed_attempts"] += 1
            save_accounts_to_csv()
            print("  [!] Incorrect PIN.")

    # Trigger Lockout if 3 attempts are spent
    account["status"] = "LOCKED"
    save_accounts_to_csv()
    log_vault_action(f"SECURITY LOCKOUT: Account {card_num} locked after 3 bad PIN inputs.")
    print("\n  [⛔] PIN EXHAUSTED: Card has been disabled for safety.")
    return None


# ==============================================================================
# TRANSACTION OPERATIONAL ENGINES
# ==============================================================================
def execute_balance_inquiry(account):
    """Displays real-time in-memory balance breakdown."""
    print("\n" + "-" * 55)
    print("💼 ACCOUNT INQUIRY SUMMARY")
    print("-" * 55)
    print(f" Account Holder : {account['name']}")
    print(f" Card Number    : ****-****-****-{account['card_number'][-4:]}")
    print(f" Account Tier   : {account['type']} Account")
    print(f" Available Cash : PKR {account['balance']:,.2f}")
    print("-" * 55)
    log_vault_action(f"INQUIRY: Balance check for {account['card_number']}.")


def execute_cash_withdrawal(account):
    """Processes cash dispense with denomination checks and vault deductions."""
    print("\n" + "=" * 60)
    print("💵 DISPENSE CASH WITHDRAWAL")
    print("=" * 60)
    print(f" Daily Per-Txn Limit : PKR {ATM_VAULT['max_withdrawal_per_txn']:,.2f}")
    print(f" Minimum Withdrawal  : PKR {ATM_VAULT['min_withdrawal_per_txn']:,.2f}")
    print(f" Allowed Multiples   : Multiples of PKR 500 only")
    print("-" * 60)

    amount = get_valid_float("Enter amount to withdraw (PKR): ", ATM_VAULT["min_withdrawal_per_txn"], ATM_VAULT["max_withdrawal_per_txn"])

    # Denomination validation (e.g., cannot dispense PKR 730)
    if amount % 500 != 0:
        print("  [x] Denomination Error: ATM can only dispense in multiples of PKR 500.")
        return

    # User balance check
    if amount > account["balance"]:
        print(f"  [x] Insufficient Funds! Current balance: PKR {account['balance']:,.2f}")
        return

    # Vault hardware reserve check
    if amount > ATM_VAULT["cash_reserve"]:
        print("  [x] Terminal Notice: ATM physical vault lacks cash reserve to fulfill this request.")
        log_vault_action(f"VAULT WARNING: Cash reserve low. Rejected {amount} PKR.")
        return

    # Process Transaction
    account["balance"] -= amount
    ATM_VAULT["cash_reserve"] -= amount
    txn_id = f"TXN-{len(account['transactions']) + 1001}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    txn_record = {
        "id": txn_id,
        "type": "WITHDRAWAL",
        "amount": amount,
        "balance_after": account["balance"],
        "timestamp": timestamp
    }
    account["transactions"].append(txn_record)
    save_accounts_to_csv()
    log_vault_action(f"WITHDRAW: {account['card_number']} withdrew PKR {amount:,.2f}.")

    # Calculate Cash Dispense Bill Counts
    rem = int(amount)
    bills_5000 = rem // 5000
    rem %= 5000
    bills_1000 = rem // 1000
    rem %= 1000
    bills_500 = rem // 500

    print("\n" + "=" * 60)
    print("  [✓] PLEASE COLLECT YOUR CASH FROM DISPENSER:")
    if bills_5000:
        print(f"      • PKR 5,000 Notes : {bills_5000}")
    if bills_1000:
        print(f"      • PKR 1,000 Notes : {bills_1000}")
    if bills_500:
        print(f"      • PKR 500 Notes   : {bills_500}")
    print(f"  Remaining Account Balance: PKR {account['balance']:,.2f}")
    print("=" * 60)

    offer_printed_receipt(account, txn_record)


def execute_cash_deposit(account):
    """Credits cash back to account balance and replenishes terminal vault."""
    print("\n" + "=" * 60)
    print("📥 AUTOMATED CASH DEPOSIT ENVELOPE")
    print("=" * 60)

    amount = get_valid_float("Enter total cash amount to deposit (PKR): ", 100.0, 500000.0)

    account["balance"] += amount
    ATM_VAULT["cash_reserve"] += amount
    txn_id = f"TXN-{len(account['transactions']) + 1001}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    txn_record = {
        "id": txn_id,
        "type": "DEPOSIT",
        "amount": amount,
        "balance_after": account["balance"],
        "timestamp": timestamp
    }
    account["transactions"].append(txn_record)
    save_accounts_to_csv()
    log_vault_action(f"DEPOSIT: {account['card_number']} deposited PKR {amount:,.2f}.")

    print(f"\n[✓] Deposit Confirmed! New Balance: PKR {account['balance']:,.2f}")
    offer_printed_receipt(account, txn_record)


def execute_funds_transfer(account):
    """Direct Peer-to-Peer balance transfer between two valid bank cards."""
    print("\n" + "=" * 60)
    print("🔁 INTER-ACCOUNT FUNDS TRANSFER (1-LINK)")
    print("=" * 60)

    target_card = get_clean_string("Enter Beneficiary 4-Digit Card Number: ")

    if target_card == account["card_number"]:
        print("  [x] Transfer Error: Cannot transfer funds to the same source card.")
        return

    if target_card not in ACCOUNTS_REGISTRY:
        print("  [x] Beneficiary card number not found in 1-Link network.")
        return

    target_account = ACCOUNTS_REGISTRY[target_card]
    print(f"Beneficiary Account: {target_account['name']} ({target_account['type']} Account)")

    amount = get_valid_float("Enter transfer amount (PKR): ", 100.0, 100000.0)

    if amount > account["balance"]:
        print(f"  [x] Insufficient balance! Available: PKR {account['balance']:,.2f}")
        return

    # Execute transfer
    account["balance"] -= amount
    target_account["balance"] += amount

    txn_id = f"TXN-{len(account['transactions']) + 1001}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sender_record = {
        "id": txn_id,
        "type": f"TRANSFER TO {target_card}",
        "amount": amount,
        "balance_after": account["balance"],
        "timestamp": timestamp
    }
    account["transactions"].append(sender_record)
    target_account["transactions"].append({
        "id": f"TXN-RCV-{len(target_account['transactions']) + 1}",
        "type": f"RECEIVED FROM {account['card_number']}",
        "amount": amount,
        "balance_after": target_account["balance"],
        "timestamp": timestamp
    })

    save_accounts_to_csv()
    log_vault_action(f"TRANSFER: PKR {amount:,.2f} from {account['card_number']} to {target_card}.")

    print(f"\n[✓] Transfer successful! PKR {amount:,.2f} credited to {target_account['name']}.")
    print(f"    Your updated balance: PKR {account['balance']:,.2f}")
    offer_printed_receipt(account, sender_record)


def change_account_pin(account):
    """Allows user to securely update their 4-digit PIN."""
    print("\n" + "=" * 60)
    print("🔐 CHANGE PIN CODE")
    print("=" * 60)

    current_pin = input("Enter current PIN: ").strip()
    if hash_pin(current_pin) != account["pin_hash"]:
        print("  [x] Authentication Error: Current PIN incorrect.")
        return

    while True:
        new_pin = input("Enter new 4-digit numeric PIN: ").strip()
        if len(new_pin) == 4 and new_pin.isdigit():
            confirm_pin = input("Confirm new 4-digit PIN: ").strip()
            if new_pin == confirm_pin:
                account["pin_hash"] = hash_pin(new_pin)
                save_accounts_to_csv()
                log_vault_action(f"PIN CHANGED: User on account {account['card_number']}.")
                print("\n[✓] PIN updated successfully!")
                return
            else:
                print("  [x] PINs do not match. Please try again.")
        else:
            print("  [!] PIN must be exactly 4 digits.")


# ==============================================================================
# RECEIPT GENERATION & STATEMENT PRINTING
# ==============================================================================
def offer_printed_receipt(account, txn):
    """Prompts user if they want an ASCII receipt exported to disk."""
    choice = input("\nWould you like a printed receipt for this transaction? (y/n): ").strip().lower()
    if choice in ("y", "yes"):
        receipt_filename = f"Receipt_{txn['id']}.txt"
        receipt_path = os.path.join(RECEIPTS_DIR, receipt_filename)
        try:
            with open(receipt_path, mode="w", encoding="utf-8") as f:
                f.write("=" * 55 + "\n")
                f.write("             NATIONAL DIGITAL ATM TERMINAL\n")
                f.write("               TRANSACTION RECEIPT SLIP\n")
                f.write("=" * 55 + "\n")
                f.write(f"Terminal ID     : ATM-ISB-0941\n")
                f.write(f"Date & Time     : {txn['timestamp']}\n")
                f.write(f"Transaction ID  : {txn['id']}\n")
                f.write(f"Card Number     : ****-****-****-{account['card_number'][-4:]}\n")
                f.write(f"Account Holder  : {account['name']}\n")
                f.write(f"Transaction     : {txn['type']}\n")
                f.write(f"Amount Involved : PKR {txn['amount']:,.2f}\n")
                f.write(f"Closing Balance : PKR {txn['balance_after']:,.2f}\n")
                f.write("-" * 55 + "\n")
                f.write("       Thank you for banking with us online!\n")
                f.write("=" * 55 + "\n")
            print(f"  [✓] Receipt saved to: {receipt_path}")
        except IOError as e:
            print(f"  [!] Receipt printing failed: {e}")


def display_mini_statement(account):
    """Outputs recent transactions registered in the active session."""
    print("\n" + "=" * 70)
    print(f"📜 MINI-STATEMENT: LAST 5 TRANSACTIONS ({account['name']})")
    print("=" * 70)

    if not account["transactions"]:
        print("  No transactions executed during this active session.")
        print(f"  Current settled account balance: PKR {account['balance']:,.2f}")
        return

    print(f"{'Txn ID':<12}{'Timestamp':<20}{'Type':<22}{'Amount (PKR)':<14}{'Balance'}")
    print("-" * 70)
    for t in account["transactions"][-5:]:
        print(f"{t['id']:<12}{t['timestamp']:<20}{t['type']:<22}{t['amount']:<14,.2f}PKR {t['balance_after']:,.2f}")
    print("=" * 70 + "\n")


# ==============================================================================
# MAIN TERMINAL LOOP CONTROLLER
# ==============================================================================
def run_atm_session(account):
    """Session loop that runs once a customer card is authenticated."""
    while True:
        print("\n" + "=" * 55)
        print("          ATM CUSTOMER SERVICES MENU")
        print("=" * 55)
        print("  [1] Balance Inquiry")
        print("  [2] Fast Cash / Cash Withdrawal")
        print("  [3] Cash Deposit")
        print("  [4] Inter-Bank Funds Transfer")
        print("  [5] View Mini-Statement")
        print("  [6] Change PIN Code")
        print("  [7] Return Card & Eject Session")
        print("=" * 55)

        choice = get_valid_int("Select transaction service (1-7): ", 1, 7)

        if choice == 1:
            execute_balance_inquiry(account)
        elif choice == 2:
            execute_cash_withdrawal(account)
        elif choice == 3:
            execute_cash_deposit(account)
        elif choice == 4:
            execute_funds_transfer(account)
        elif choice == 5:
            display_mini_statement(account)
        elif choice == 6:
            change_account_pin(account)
        elif choice == 7:
            print(f"\n[✓] Card returned. Have a nice day, {account['name']}!\n")
            log_vault_action(f"EJECT: Card {account['card_number']} session finished.")
            break


def main():
    """Hardware initialization and standby loop."""
    initialize_system()

    while True:
        print("\n" + "#" * 60)
        print("       🏛️  NATIONAL VIRTUAL ATM MACHINE (STANDBY)")
        print("#" * 60)
        print("  [1] Insert Card / Start Banking Session")
        print("  [2] View ATM Physical Vault Status (Admin)")
        print("  [3] View Hardware Audit Trail Logs (Admin)")
        print("  [4] Power Down Simulator")
        print("#" * 60)

        option = get_valid_int("Select Terminal Action (1-4): ", 1, 4)

        if option == 1:
            authenticated_account = authenticate_user()
            if authenticated_account:
                run_atm_session(authenticated_account)
        elif option == 2:
            print("\n--- ATM PHYSICAL VAULT METRICS ---")
            print(f" Cash Reserve Remaining : PKR {ATM_VAULT['cash_reserve']:,.2f}")
            print(f" Max Per-Txn Limit      : PKR {ATM_VAULT['max_withdrawal_per_txn']:,.2f}")
            print(f" Supported Bill Types   : {ATM_VAULT['valid_denominations']}\n")
        elif option == 3:
            print("\n--- RECENT AUDIT LOGS ---")
            if os.path.exists(AUDIT_LOG_TXT):
                with open(AUDIT_LOG_TXT, mode="r", encoding="utf-8") as f:
                    for line in f.readlines()[-10:]:
                        print("  " + line.strip())
            print()
        elif option == 4:
            log_vault_action("SYSTEM SHUTDOWN: Maintenance shutdown.")
            print("\nPowering down ATM Terminal. Goodbye!\n")
            break


if __name__ == "__main__":
    main()
