# Welcome to bank boy :D

# Database Setup
import sqlite3
DB_NAME = 'bank.db'

#  --- CONNECT TO DATABASE ---
def connect():
    return sqlite3.connect(DB_NAME) # Connects to the database, bank.db

# --- CREATE TABLES ---
def create_tables():
    conn = connect() # Establishes connection within a variable
    cursor = conn.cursor() # Creates a cursor object using established database connection, which allows us to execute SQL commands

# Creating accounts table if it doesn't already exist with the following columns: id (INTEGER; PRIMARY KEY), name (TEXT), balance (REAL)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
                   id INTEGER PRIMARY KEY AUTOINCREMENT, --Unique identifier for each account; automatically increments with each new entry
                   name TEXT NOT NULL,  --Name of account holder; cannot be null
                   balance REAL NOT NULL DEFAULT 0.0 --Current balance of account; cannot be null; defaults to 0.0
                   )
                   ''')

# Creating transactions table if it doesn't already exist with the following columns: id (INTEGER; PRIMARY KEY), sending_account_id (INTEGER), recieving_account_id (INTEGER), type (TEXT), amount (REAL), timestamp (DATETIME)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, --Unique identifier for each transaction; automatically increments with each new entry
                    sending_account_id INTEGER, --Foreign key referencing accounts table; indicates account transaction is sent from
                    receiving_account_id INTEGER, --Foreign key referencing accounts table; indicates account transaction is sent to
                    type TEXT NOT NULL, --type of transaction (e.g., 'deposit', 'withdrawal', 'transfer'); cannot be null
                    amount REAL NOT NULL, --amount of of money moved in the transaction; cannot be null
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, --timestamp of when transaction occured; defaults to current date and time
                    FOREIGN KEY (sending_account_id) REFERENCES accounts(id), --Establishes foreign key relationship with accounts table for sending account
                    FOREIGN KEY (receiving_account_id) REFERENCES accounts(id) --Establishes foreign key relationship with accounts table for receiving account
                   )
                   ''')
    conn.commit() # Commits changes to database, ensuring that the created tables are saved and available for use
    conn.close() # Closes the database connection, freeing up resources and ensuring that changes are properly saved (good practice)

# NOT NULL provides automatic error handling by preventing insertion of null values into these critical fields, ensuring the integrity and consistency of data within the database.

# THE CORE FUNCTIONS -- Creating an account, depositing money, withdrawing money, checking balance, and listing accounts

# --- CREATE ACCOUNT ---
def create_account(name, deposit):
    conn = connect() # Establishes connection within a variable
    cursor = conn.cursor() # Creates a cursor object using established database connection, which allows us to execute SQL commands

    cursor.execute(
        'INSERT INTO accounts (name, balance) VALUES (?, ?)',
        (name, deposit) # Inserts a new account into the accounts table with provided name and initial deposit amount -- NOTE: (?, ?) is a placeholder for the values that will be safely inserted into the SQL command (name, balance) to prevent SQL injection attacks and ensure proper handling of user input)
    )
    conn.commit() # Commits changes to database, ensuring that the newly created account is saved and available for use
    conn.close() # Closes the database connection, freeing up resources and ensuring that changes are properly saved (good practice)
    print(f"Account created for {name} with initial deposit of ${deposit:.2f}") # Prints a confirmation message indicating that the account has been successfully created, including the account holder's name and the initial deposit amount formatted to two decimal places (floating-point representation of currency).

# --- TRANSACTION TYPE: DEPOSIT ---
def deposit():
    conn = connect() # Establishes connection within a variable
    cursor = conn.cursor() # Creates a cursor object using established database connection, which allows us to execute SQL commands

    try: 
        account_id = int(input("Enter account IDD: ")) # Prompts user to enter the account ID for the deposit transaction and converts the input to an integer (error handling in case of non-integer input)
        amount = float(input("Enter deposit amount: ")) # Prompts user to enter the deposit amount and converts the input to a floating-point number (error handling in case of non-numeric input)

        #Status Validation
        if amount <= 0:
            print("Deposit amount must be positive")
            return
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
        result = cursor.fetchone() # Fetches the current balance of the specified account from the database

        if result is None:
            print("Account not found")
            return
        
        #Update Balance
        cursor.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (amount, account_id)
        )

        #Record Transaction
        cursor.execute(
            '''
              INSERT INTO transactions(sending_account_id, receiving_account_id, type, amount)
              VALUES (?, ?, 'deposit', ?)
            ''',
            (None, account_id, amount) # Inserts a new transaction record into the transactions table with the following values: sending_account_id is set to None (since it's a deposit), receiving_account_id is set to the account_id where the deposit is being made, type is set to 'deposit', and amount is set to the deposit amount entered by the user. This allows us to keep a record of all deposit transactions in the database for future reference and auditing purposes.
        )

        conn.commit() # Commits changes to database, ensuring that the updated account balance and new transaction record are saved and available for use
        print(f"Deposited ${amount:.2f} successfully")

    except ValueError:
        print("Invalid input. Please enter numbers only.")

    finally:
        conn.close() # Closes the database connection, freeing up resources and ensuring that changes are properly saved (good practice)

# --- TRANSACTION TYPE: WITHDRAW ---
def withdraw():
    conn = connect()
    cursor = conn.cursor()

    try:
        account_id = int(input("Enter account ID: "))
        amount = float(input("Enter withdrawal amount: "))

        # --- Status Validation ---
        if amount <= 0:
            print("Withdrawal amount must be positive")
            return
        
        # --- Check Account ---
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
        result = cursor.fetchone()

        if result is None:
            print("Account not found")
            return
        
        balance = result[0]

        if balance < amount:
            print("Insufficient funds")
            return
        
        # --- Update Balance ---
        cursor.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?",
            (amount, account_id)
        )

        # --- Record Transaction ---
        cursor.execute(
            '''
            INSERT INTO transactions (sending_account_id, receiving_account_id, type, amount)
            VALUES (?, ?, 'withdraw', ?)
            ''',
            (account_id, None, amount)
        )

        conn.commit()
        print(f"Withdrew ${amount:.2f} successfully")

    except ValueError:
        print("Invalid input.")

    finally:
        conn.close()
    
# CHECK BALANCE
def check_balance():
    conn = connect()
    cursor = conn.cursor()

    try:
        account_id = int(input("Enter account ID: "))

        cursor.execute("SELECT name, balance FROM accounts WHERE id = ?", (account_id,))
        result = cursor.fetchone()

        if result:
            print(f"\nAccount: {result[0]}")
            print(f"Balance: ${result[1]:.2f}")
        else:
            print("Account not found.")

    except ValueError:
        print("Invalid input.")

    finally:
        conn.close()

# LIST ACCOUNTS 
def list_accounts():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, balance FROM accounts")
    accounts = cursor.fetchall()

    conn.close()

    if not accounts:
        print("No accounts found.")
        return

    print("\n--- Accounts ---")
    for acc in accounts:
        print(f"ID: {acc[0]} | Name: {acc[1]} | Balance: ${acc[2]:.2f}")

# --- MENU SYSTEM ---
def menu():
    while True:
        print("\n=== BANK BOY ===")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. List Accounts")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter name: ")
            try:
                deposit_amt = float(input("Initial deposit: "))
                if deposit_amt < 0:
                    print("Deposit cannot be negative.")
                    continue
                create_account(name, deposit_amt)
            except ValueError:
                print("Invalid amount.")

        elif choice == "2":
            deposit()

        elif choice == "3":
            withdraw()

        elif choice == "4":
            check_balance()

        elif choice == "5":
            list_accounts()

        elif choice == "6":
            print("Goodbye! Thanks for using Bank Boy. :D")
            break

        else:
            print("Invalid choice. Please try again.")
    
if __name__ == "__main__":
    create_tables()
    menu()

# DEMO -- Function Tests (manual run)
# 1. CREATE ACCOUNT
# Input:
#   Option: 1
#   Name: John
#   Deposit: 100
# Expected:
#   Account created successfully with $100.00

# 2. DEPOSIT (VALID)
# Input:
#   Option: 2
#   Account ID: 1
#   Amount: 50
# Expected:
#   Deposit successful
#   New balance should be $150.00

# 3. WITHDRAW (VALID)
# Input:
#   Option: 3
#   Account ID: 1
#   Amount: 30
# Expected:
#   Withdrawal successful
#   New balance should be $120.00

# 4. CHECK BALANCE
# Input:
#   Option: 4
#   Account ID: 1
# Expected:
#   Displays:
#     Name: John
#     Balance: $120.00

# 5. LIST ACCOUNTS
# Input:
#   Option: 5
# Expected:
#   Shows all accounts including:
#     ID: 1 | Name: John | Balance: $120.00

# 
# ALSO!: EDGE CASE TESTS
#

# Deposit negative amount:
#   Input: -50
#   Expected: "Deposit amount must be positive"

# Withdraw more than balance:
#   Input: withdraw 500
#   Expected: "Insufficient funds"

# Invalid account ID:
#   Input: ID that doesn't exist (e.g., 999)
#   Expected: "Account not found"

# Invalid input (letters instead of numbers):
#   Expected: "Invalid input"

    
