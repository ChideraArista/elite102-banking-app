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
                    id INTEGER PRIMARY KEY AUTOINCREMENT, --Unique identifier for each transactions; automatically increments with each new entry
                    sending_account_id INTEGER NOT NULL, --Foreign key referencing accounts table; indicates account transaction is sent from; cannot be null
                    receiving_account_id INTEGER NOT NULL, --Foreign key referencing accounts table; indicates account transaction is sent to; cannot be null
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

