import sqlite3

DB_NAME = "tabungan.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    # Buat tabel members
    c.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    # Buat tabel savings
    c.execute("""
        CREATE TABLE IF NOT EXISTS savings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            week INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            FOREIGN KEY(member_id) REFERENCES members(id)
        )
    """)

    conn.commit()
    conn.close()

def insert_members():
    members = [
        #Masukkan Daftar disini
        "Budi", "yani"
    ]

    conn = get_db()
    c = conn.cursor()

    # Cek apakah sudah ada data
    c.execute("SELECT COUNT(*) FROM members")
    count = c.fetchone()[0]

    if count == 0:
        for m in members:
            c.execute("INSERT INTO members (name) VALUES (?)", (m,))
        conn.commit()

    conn.close()
