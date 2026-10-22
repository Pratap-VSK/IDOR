import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'hospital.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS medical_records (id INTEGER PRIMARY KEY, user_id INTEGER, disease TEXT, bill_amount TEXT)''')
    
    # Insert mock data
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123')")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (2, 'john', 'password')")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (3, 'alice', 'alice123')")
    
    cursor.execute("INSERT OR IGNORE INTO medical_records (id, user_id, disease, bill_amount) VALUES (1, 1, 'None', '$0')")
    cursor.execute("INSERT OR IGNORE INTO medical_records (id, user_id, disease, bill_amount) VALUES (2, 2, 'Diabetes', '$500')")
    cursor.execute("INSERT OR IGNORE INTO medical_records (id, user_id, disease, bill_amount) VALUES (3, 3, 'Cancer', '$5000')")
    
    conn.commit()
    conn.close()
    print("[*] Database setup complete.")

if __name__ == "__main__":
    init_db()