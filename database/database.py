import sqlite3
from pathlib import Path

DB_PATH = Path("database/database.db")

def get_conn():
    return sqlite3.connect(DB_PATH, isolation_level=None)

def init_db():
    with get_conn() as c:
        c.execute("""PRAGMA journal_mode=WAL;""")  # better concurrency
        c.execute("""PRAGMA foreign_keys=ON;""")
        c.execute("""CREATE TABLE IF NOT EXISTS connection_logs (
                  id INTEGER PRIMARY KEY,
                  ip TEXT UNIQUE NOT NULL,
                  created_at DATETIME DEFAULT CURRENT_TIMESTAMP)""")
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")
        c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            sender TEXT NOT NULL,
            recipient TEXT NOT NULL,
            ciphertext BLOB NOT NULL,
            nonce BLOB NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(sender) REFERENCES users(username),
            FOREIGN KEY(recipient) REFERENCES users(username)
        )""")
        c.execute("""CREATE INDEX IF NOT EXISTS idx_messages_recipient ON messages(recipient, created_at);""")
        
def add_log(ip: str, message: str):
    with get_conn() as c:
        c.execute("INSERT OR IGNORE INTO connection_logs(ip, message) VALUES (?, ?)", (ip, message))

def add_user(username: str):
    print("added user")
    with get_conn() as c:
        c.execute("INSERT OR IGNORE INTO users(username) VALUES (?)", (username,))
    
def save_message(sender: str, recipient: str, nonce: bytes, ciphertext: bytes):
    with get_conn() as c:
        c.execute("""INSERT INTO messages(sender, recipient, nonce, ciphertext)
                     VALUES (?,?,?,?)""", (sender, recipient, nonce, ciphertext))
        
def list_messages_for(user: str, limit: int = 50):
    with get_conn() as c:
        cur = c.execute("""SELECT sender, nonce, ciphertext, created_at
                           FROM messages
                           WHERE recipient=?
                           ORDER BY created_at DESC
                           LIMIT ?""", (user, limit))
        return cur.fetchall()
    
