# Database Setup
import sqlite3
DB_NAME = 'bank.db'

def connect():
    return sqlite3.connect(DB_NAME) # Connects to the database, bank.db

def create_tables():
    conn = connect() # Establishes connection within a variable
    cursor = conn.cursor() # Creates a cursor object using established database connection, which allows us to execute SQL commands

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
                   )
                   ''')










print("Hello Elite102!")

conn = sqlite3.connect('fake_database.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS favorite_foods")
cursor.execute("CREATE TABLE favorite_foods (id INTEGER PRIMARY KEY, food_name TEXT, rating REAL)")
cursor.execute("INSERT INTO favorite_foods (id, food_name, rating) VALUES (1, 'Salad', 5);")
cursor.execute("INSERT INTO favorite_foods (id, food_name, rating) VALUES(2, 'Ice Cream Sandwich', 4.75);")
rows = cursor.execute("SELECT * FROM favorite_foods").fetchall()
for row in rows:
    print(row)

conn.commit()
conn.close()