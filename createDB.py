import sqlite3

# Connect to the database. If it does not exist, it will be created.
conn = sqlite3.connect('test.db')

# Create a cursor object.
c = conn.cursor()

# Check if users table exists and create if it doesn't
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT NOT NULL UNIQUE,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )
''')

# Check if images table exists and create if it doesn't
c.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        data BLOB NOT NULL,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')

# Commit your changes
conn.commit()

# Close the connection
conn.close()