import sqlite3
import os

def init_db():
    if os.path.exists('neonverify.db'):
        os.remove('neonverify.db')

    conn = sqlite3.connect('neonverify.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Insert dummy admin user
    # Password is 'complex_password_123' but it doesn't matter due to SQLi
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'neon_cyber_admin_2077')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('guest', 'guest')")

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
