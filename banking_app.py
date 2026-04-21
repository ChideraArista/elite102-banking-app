# Database Setup
import sqlite3
DB_NAME = 'bank.db'

def connect():
    return sqlite3.connect(DB_NAME) # Connects to the database, bank.db

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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
               id INTEGER PRIMARY KEY AUTOINCREMENT, --Unique identifier for each transactions; automatically increments with each new entry
               sending_account_id INTEGER NOT NULL, --Foreign key referencing accounts table; indicates account transaction is sent from; cannot be null
               receiving_account_id INTEGER NOT NULL, --Foreign key referencing accounts table; indicates account transaction is sent to; cannot be null
               ''')




