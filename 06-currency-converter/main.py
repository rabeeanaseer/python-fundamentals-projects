"""
Project 06: Enterprise Foreign Exchange (Forex) & Multi-Currency Conversion Engine
Course Level: 1st Semester CS / Programming Fundamentals
Concepts Used:
  - Dictionaries & Nested Dictionaries (Currency metadata & rate mappings)
  - Mathematical Triangulation (Base-USD pivot conversion)
  - While and For loops with Sentinel Control
  - Lists, Tuples, and String Formatter Specifiers
  - File I/O: CSV transaction logging, JSON-like persistent rate overrides, TXT receipt generation
  - Defensive Input Validation & Exception Handling (try/except)
"""

import os
import csv
import json
from datetime import datetime

# ==============================================================================
# GLOBAL DIRECTORIES & PERSISTENCE PATHS
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "fx_data")
RECEIPTS_DIR = os.path.join(BASE_DIR, "receipts")
HISTORY_CSV = os.path.join(DATA_DIR, "conversion_history.csv")
RATES_OVERRIDE_JSON = os.path.join(DATA_DIR, "custom_rates.json")
AUDIT_LOG_TXT = os.path.join(DATA_DIR, "fx_audit_log.txt")

# ==============================================================================
# DEFAULT BASE RATES (Relative to 1.00 USD) & CURRENCY METADATA
# Form: "CODE": {"name": ..., "symbol": ..., "rate_per_usd": float, "country": ...}
# ==============================================================================
DEFAULT_EXCHANGE_MATRIX = {
    "USD": {"name": "United States Dollar", "symbol": "\$", "rate": 1.00, "region": "North America"},
    "PKR": {"name": "Pakistani Rupee", "symbol": "₨", "rate": 278.50, "region": "South Asia"},
    "EUR": {"name": "Euro", "symbol": "€", "rate": 0.92, "region": "European Union"},
    "GBP": {"name": "British Pound Sterling", "symbol": "£", "rate": 0.79, "region": "United Kingdom"},
    "AED": {"name": "United Arab Emirates Dirham", "symbol": "د.إ", "rate": 3.67, "region": "Middle East"},
    "SAR": {"name": "Saudi Riyal", "symbol": "﷼", "rate": 3.75, "region": "Middle East"},
    "JPY": {"name": "Japanese Yen", "symbol": "¥", "rate": 154.20, "region": "East Asia"},
    "CNY": {"name": "Chinese Yuan Renminbi", "symbol": "¥", "rate": 7.24, "region": "East Asia"},
    "CAD": {"name": "Canadian Dollar", "symbol": "C\$", "rate": 1.38, "region": "North America"},
    "AUD": {"name": "Australian Dollar", "symbol": "A\$", "rate": 1.52, "region": "Oceania"},
    "INR": {"name": "Indian Rupee", "symbol": "₹", "rate": 83.90, "region": "South Asia"},
    "TRY": {"name": "Turkish Lira", "symbol": "₺", "rate": 34.25, "region": "Eurasia"}
}

# Runtime working rates
ACTIVE_EXCHANGE_MATRIX = {}


# ==============================================================================
# SYSTEM INITIALIZATION & PERSISTENCE
# ==============================================================================
def initialize_system():
    """Sets up local directories and loads or seeds persistent exchange rates."""
    global ACTIVE_EXCHANGE_MATRIX
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RECEIPTS_DIR, exist_ok=True)

    # Initialize Audit Log
    if not os.path.exists(AUDIT_LOG_TXT):
        with open(AUDIT_LOG_TXT, mode="w", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] SYSTEM: Foreign Exchange Engine Initialized.\n")

    # Initialize CSV Transaction History
    if not os.path.exists(HISTORY_CSV):
        with open(HISTORY_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Timestamp", "Transaction_ID", "Source_Currency", "Source_Amount",
                "Target_Currency", "Target_Amount", "Exchange_Rate", "Fee_Applied", "Net_Received"
            ])

    # Load custom rates if saved, otherwise default
    if os.path.exists(RATES_OVERRIDE_JSON):
        try:
            with open(RATES_OVERRIDE_JSON, mode="r", encoding="utf-8") as f:
                ACTIVE_EXCHANGE_MATRIX = json.load(f)
        except Exception:
            ACTIVE_EXCHANGE_MATRIX = DEFAULT_EXCHANGE_MATRIX.copy()
    else:
        ACTIVE_EXCHANGE_MATRIX = DEFAULT_EXCHANGE_MATRIX.copy()


def log_event(message):
    """Appends an event to the local audit log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(AUDIT_LOG_TXT, mode="a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except IOError:
        pass


def save_rates_to_file():
    """Flushes active rate matrix to JSON file."""
    try:
        with open(RATES_OVERRIDE_JSON, mode="w", encoding="utf-8") as f:
            json.dump(ACTIVE_EXCHANGE_MATRIX, f, indent=2)
    except IOError as e:
        print(f"  [!] Disk Warning: Could not save custom rates: {e}")


def append_history_record(record):
    """Saves transaction row to CSV database."""
    try:
        with open(HISTORY_CSV, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                record["timestamp"],
                record["txn_id"],
                record["source_curr"],
                f"{record['source_amt']:.2f}",
                record["target_curr"],
                f"{record['target_amt']:.2f}",
                f"{record['effective_rate']:.6f}",
                f"{record['fee']:.2f}",
                f"{record['net_amt']:.2f}"
            ])
    except IOError as e:
        print(f"  [!] Storage Warning: Could not log to CSV: {e}")


# ==============================================================================
# INPUT VALIDATION UTILITIES
# ==============================================================================
def input_non_empty(prompt):
    """Validates non-empty string."""
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("  [!] Error: Value cannot be blank.")


def input_int_range(prompt, min_val, max_val):
    """Validates integer within specified boundaries."""
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if min_val <= val <= max_val:
                return val
            print(f"  [!] Range error: Enter an integer between {min_val} and {max_val}.")
        except ValueError:
            print("  [!] Format error: Integer expected.")


def input_float_positive(prompt, min_val=0.01, max_val=1e9):
    """Validates positive float currency amount."""
    while True:
        raw = input(prompt).strip()
        try:
            val = float(raw)
            if min_val <= val <= max_val:
                return round(val, 2)
            print(f"  [!] Amount out of range ({min_val:,.2f} to {max_val:,.2f}).")
        except ValueError:
            print("  [!] Format error: Decimal number expected.")


def prompt_valid_currency(prompt_text):
    """Forces user to pick a recognized ISO currency code from matrix."""
    while True:
        code = input(prompt_text).strip().upper()
        if code in ACTIVE_EXCHANGE_MATRIX:
            return code
        print(f"  [!] Currency '{code}' not supported. Type 'LIST' to see supported currencies.")
        if code == "LIST":
            display_supported_currencies()


# ==============================================================================
# CORE MATHEMATICAL ARITHMETIC & TRIANGULATION
# ==============================================================================
def calculate_cross_rate(source_curr, target_curr):
    """
    Computes direct cross exchange rate between two arbitrary currencies
    using USD as the mathematical pivot:
    Cross Rate = Rate(Target / USD) / Rate(Source / USD)
    """
    source_to_usd = ACTIVE_EXCHANGE_MATRIX[source_curr]["rate"]
    target_to_usd = ACTIVE_EXCHANGE_MATRIX[target_curr]["rate"]
    
    cross_rate = target_to_usd / source_to_usd
    return cross_rate


def convert_currency_amount(amount, source_curr, target_curr, fee_rate=0.01):
    """
    Converts amount from source to target, applying a service spread fee (default 1%).
    Returns: (gross_target, effective_rate, fee_in_target, net_target)
    """
    cross_rate = calculate_cross_rate(source_curr, target_curr)
    gross_converted = amount * cross_rate
    fee_amount = gross_converted * fee_rate
    net_received = gross_converted - fee_amount
    
    return gross_converted, cross_rate, fee_amount, net_received


# ==============================================================================
# CONVERSION OPERATIONS & RECEIPT EXPORTS
# ==============================================================================
def execute_single_conversion():
    """Primary interactive conversion flow with optional text receipt export."""
    print("\n" + "=" * 70)
    print("💱 STANDARD CURRENCY CONVERSION & REMITTANCE COUNTER")
    print("=" * 70)

    source_curr = prompt_valid_currency("Enter Source Currency Code (e.g., USD, PKR, EUR): ")
    target_curr = prompt_valid_currency("Enter Target Currency Code (e.g., PKR, AED, GBP): ")

    if source_curr == target_curr:
        print("  [!] Source and target currencies are identical. Conversion rate is 1.0000.")
        return

    amount = input_float_positive(f"Enter amount in {source_curr}: ")

    # Choose Service Fee Tier
    print("\nSelect Processing Service Tier:")
    print("  [1] Standard Transfer  (1.0% FX Spread Fee)")
    print("  [2] Express Remittance (2.5% Priority Network Fee)")
    print("  [3] VIP / Institutional (0.0% Zero Fee)")
    tier_choice = input_int_range("Select Tier (1-3): ", 1, 3)
    fee_map = {1: 0.01, 2: 0.025, 3: 0.00}
    chosen_fee_rate = fee_map[tier_choice]

    gross_val, cross_rate, fee_val, net_val = convert_currency_amount(
        amount, source_curr, target_curr, chosen_fee_rate
    )

    src_meta = ACTIVE_EXCHANGE_MATRIX[source_curr]
    tgt_meta = ACTIVE_EXCHANGE_MATRIX[target_curr]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txn_id = f"FX-{int(datetime.now().timestamp()) % 1000000:06d}"

    # Visual Output
    print("\n" + "-" * 70)
    print("                    EXCHANGE SETTLEMENT SUMMARY")
    print("-" * 70)
    print(f" Transaction ID   : {txn_id}")
    print(f" Date & Timestamp : {timestamp}")
    print(f" Source Amount    : {src_meta['symbol']} {amount:,.2f} {source_curr} ({src_meta['name']})")
    print(f" Effective Rate   : 1 {source_curr} = {cross_rate:.6f} {target_curr}")
    print(f" Inverted Rate    : 1 {target_curr} = {1 / cross_rate:.6f} {source_curr}")
    print(f" Gross Equivalent : {tgt_meta['symbol']} {gross_val:,.2f} {target_curr}")
    print(f" Service Fee      : {tgt_meta['symbol']} {fee_val:,.2f} {target_curr} ({(chosen_fee_rate * 100):.1f}%)")
    print(f" Net Transferred  : {tgt_meta['symbol']} {net_val:,.2f} {target_curr}")
    print("-" * 70)

    # Persist to CSV
    record = {
        "timestamp": timestamp,
        "txn_id": txn_id,
        "source_curr": source_curr,
        "source_amt": amount,
        "target_curr": target_curr,
        "target_amt": gross_val,
        "effective_rate": cross_rate,
        "fee": fee_val,
        "net_amt": net_val
    }
    append_history_record(record)
    log_event(f"CONVERT: {amount} {source_curr} to {net_val:.2f} {target_curr} [TXN: {txn_id}].")

    # Offer receipt export
    receipt_prompt = input("Do you want to export an official .txt receipt slip? (y/n): ").strip().lower()
    if receipt_prompt in ("y", "yes"):
        export_receipt_slip(record, src_meta, tgt_meta)


def export_receipt_slip(record, src_meta, tgt_meta):
    """Exports structured receipt to receipts directory."""
    filename = f"FX_Receipt_{record['txn_id']}.txt"
    filepath = os.path.join(RECEIPTS_DIR, filename)

    try:
        with open(filepath, mode="w", encoding="utf-8") as f:
            f.write("=" * 65 + "\n")
            f.write("             GLOBAL FOREIGN EXCHANGE SERVICES\n")
            f.write("               OFFICIAL CONVERSION RECEIPT\n")
            f.write("=" * 65 + "\n")
            f.write(f"Transaction ID    : {record['txn_id']}\n")
            f.write(f"Date & Time       : {record['timestamp']}\n")
            f.write(f"Source Currency   : {record['source_curr']} - {src_meta['name']}\n")
            f.write(f"Remitted Amount   : {src_meta['symbol']} {record['source_amt']:,.2f}\n")
            f.write("-" * 65 + "\n")
            f.write(f"Direct Cross Rate : 1 {record['source_curr']} = {record['effective_rate']:.6f} {record['target_curr']}\n")
            f.write(f"Gross Target Amt  : {tgt_meta['symbol']} {record['target_amt']:,.2f}\n")
            f.write(f"Processing Surcharge: {tgt_meta['symbol']} {record['fee']:,.2f}\n")
            f.write(f"NET SETTLED VALUE : {tgt_meta['symbol']} {record['net_amt']:,.2f} {record['target_curr']}\n")
            f.write("-" * 65 + "\n")
            f.write("Status: TRANSACTION SETTLED & VERIFIED\n")
            f.write("Thank you for using Global FX Services.\n")
            f.write("=" * 65 + "\n")
        print(f"  [✓] Receipt saved: {filepath}")
    except IOError as e:
        print(f"  [!] Failed to save receipt: {e}")


def execute_batch_conversion():
    """Converts a single base amount into ALL supported currencies at once."""
    print("\n" + "=" * 75)
    print("🌐 MULTI-CURRENCY BATCH PORTFOLIO CONVERSION")
    print("=" * 75)

    base_curr = prompt_valid_currency("Enter Base Currency (e.g., USD, PKR): ")
    amount = input_float_positive(f"Enter amount in {base_curr}: ")

    print("\n" + "-" * 75)
    print(f" Portfolio Snapshot for: {ACTIVE_EXCHANGE_MATRIX[base_curr]['symbol']} {amount:,.2f} {base_curr}")
    print("-" * 75)
    print(f"{'Code':<6}{'Currency Name':<28}{'Rate (vs Base)':<18}{'Equivalent Value'}")
    print("-" * 75)

    for code, info in ACTIVE_EXCHANGE_MATRIX.items():
        if code == base_curr:
            continue
        cross_rate = calculate_cross_rate(base_curr, code)
        converted_val = amount * cross_rate
        print(f"{code:<6}{info['name'][:26]:<28}{cross_rate:<18.4f}{info['symbol']} {converted_val:>14,.2f}")

    print("=" * 75 + "\n")
    log_event(f"BATCH: Multi-currency evaluation of {amount} {base_curr}.")


# ==============================================================================
# EXCHANGE RATE MANAGEMENT (CRUD)
# ==============================================================================
def display_supported_currencies():
    """Renders formatted table of all registered currency rates vs USD."""
    print("\n" + "=" * 75)
    print("📊 ACTIVE FOREIGN EXCHANGE MATRIX (BASE: 1.00 USD)")
    print("=" * 75)
    print(f"{'Code':<6}{'Symbol':<8}{'Currency Name':<28}{'Region':<16}{'Rate per 1 USD'}")
    print("-" * 75)
    for code, meta in sorted(ACTIVE_EXCHANGE_MATRIX.items()):
        print(f"{code:<6}{meta['symbol']:<8}{meta['name'][:26]:<28}{meta['region']:<16}{meta['rate']:>12.4f}")
    print("=" * 75 + "\n")


def update_or_add_currency():
    """Allows administrators to update an existing rate or add a new currency."""
    print("\n" + "=" * 65)
    print("⚙️ CUSTOM RATE CONFIGURATION & ADDITION")
    print("=" * 65)

    code = input_non_empty("Enter 3-Letter ISO Currency Code (e.g. AED, SGD): ").upper()

    if code in ACTIVE_EXCHANGE_MATRIX:
        print(f"Current recorded rate for {code} is {ACTIVE_EXCHANGE_MATRIX[code]['rate']} per 1 USD.")
        new_rate = input_float_positive(f"Enter new exchange rate per 1 USD: ")
        ACTIVE_EXCHANGE_MATRIX[code]["rate"] = new_rate
        save_rates_to_file()
        log_event(f"RATE UPDATE: {code} set to {new_rate} per USD.")
        print(f"  [✓] Successfully updated rate for {code}!")
    else:
        print(f"Adding new currency '{code}' to registry.")
        name = input_non_empty("Enter Full Currency Name: ").title()
        symbol = input_non_empty("Enter Currency Symbol (e.g. \$, ₨, €): ")
        region = input_non_empty("Enter Geographical Region: ").title()
        rate = input_float_positive("Enter Exchange Rate relative to 1.00 USD: ")

        ACTIVE_EXCHANGE_MATRIX[code] = {
            "name": name,
            "symbol": symbol,
            "rate": rate,
            "region": region
        }
        save_rates_to_file()
        log_event(f"NEW CURRENCY: Added {code} ({name}) at rate {rate}.")
        print(f"  [✓] Currency {code} successfully added and saved to storage!")


def reset_default_rates():
    """Resets exchange matrix to initial hardcoded values."""
    global ACTIVE_EXCHANGE_MATRIX
    confirm = input("Reset all exchange rates back to default factory rates? (y/n): ").strip().lower()
    if confirm in ("y", "yes"):
        ACTIVE_EXCHANGE_MATRIX = DEFAULT_EXCHANGE_MATRIX.copy()
        if os.path.exists(RATES_OVERRIDE_JSON):
            os.remove(RATES_OVERRIDE_JSON)
        log_event("SYSTEM: Exchange rates restored to factory defaults.")
        print("  [✓] All rates have been reset to factory defaults.\n")


# ==============================================================================
# AUDIT & TRANSACTION HISTORY VIEWER
# ==============================================================================
def display_conversion_history():
    """Displays last 10 conversions stored in persistent CSV."""
    print("\n" + "=" * 85)
    print("📜 RECENT CONVERSION TRANSACTION LOGS")
    print("=" * 85)

    if not os.path.exists(HISTORY_CSV):
        print("  [!] No transaction history found.")
        return

    records = []
    try:
        with open(HISTORY_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
    except IOError as e:
        print(f"  [!] Failed to read CSV history: {e}")
        return

    if not records:
        print("  [!] History database is empty. Execute a conversion first.")
        return

    print(f"{'Txn ID':<11}{'Date / Time':<20}{'Pair':<12}{'Source Amount':<16}{'Net Received'}")
    print("-" * 85)
    for r in records[-10:]:
        pair_str = f"{r['Source_Currency']}->{r['Target_Currency']}"
        print(f"{r['Transaction_ID']:<11}{r['Timestamp']:<20}{pair_str:<12}{r['Source_Amount']:<16}{r['Net_Received']}")
    print("=" * 85 + "\n")


# ==============================================================================
# MAIN APPLICATION CONTROLLER
# ==============================================================================
def display_main_menu():
    """Primary navigation menu."""
    print("=" * 60)
    print("        💱 GLOBAL MULTI-CURRENCY FOREX ENGINE")
    print("=" * 60)
    print("  [1] Single Pair Currency Conversion & Remittance")
    print("  [2] Multi-Currency Batch Portfolio Snapshot")
    print("  [3] View Active Currency Exchange Rates Table")
    print("  [4] Update Existing Rate or Add New Currency")
    print("  [5] View Historical Conversion Ledger (CSV)")
    print("  [6] Reset Rates to Factory Defaults")
    print("  [7] Exit Application")
    print("=" * 60)


def main():
    """Main execution loop."""
    initialize_system()

    while True:
        display_main_menu()
        choice = input_int_range("Select an option (1-7): ", 1, 7)

        if choice == 1:
            execute_single_conversion()
        elif choice == 2:
            execute_batch_conversion()
        elif choice == 3:
            display_supported_currencies()
        elif choice == 4:
            update_or_add_currency()
        elif choice == 5:
            display_conversion_history()
        elif choice == 6:
            reset_default_rates()
        elif choice == 7:
            log_event("SYSTEM: Application shutdown.")
            print("\nExiting Currency Converter. Have a great day!\n")
            break


if __name__ == "__main__":
    main()
