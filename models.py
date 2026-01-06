from database import get_db

def get_all_members():
    db = get_db()
    rows = db.execute("SELECT * FROM members").fetchall()
    db.close()
    return rows

def get_member_by_id(member_id):
    db = get_db()
    row = db.execute("SELECT * FROM members WHERE id=?", (member_id,)).fetchone()
    db.close()
    return row

def add_saving(member_id, week, amount):
    db = get_db()
    db.execute("INSERT INTO savings (member_id, week, amount) VALUES (?, ?, ?)", (member_id, week, amount))
    db.commit()
    db.close()

def get_filled_weeks(member_id):
    db = get_db()
    rows = db.execute("SELECT week FROM savings WHERE member_id=? ORDER BY week ASC", (member_id,)).fetchall()
    db.close()
    return [{'week': row['week']} for row in rows]

def get_savings_by_member(member_id):
    db = get_db()
    rows = db.execute("SELECT * FROM savings WHERE member_id=? ORDER BY week", (member_id,)).fetchall()
    db.close()
    return rows

def get_total_savings(member_id):
    db = get_db()
    total = db.execute("SELECT SUM(amount) FROM savings WHERE member_id=?", (member_id,)).fetchone()[0]
    db.close()
    return total or 0

def get_last_week(member_id):
    db = get_db()
    row = db.execute("SELECT MAX(week) AS last_week FROM savings WHERE member_id=?", (member_id,)).fetchone()
    db.close()
    return row["last_week"]

def get_global_total():
    db = get_db()
    total = db.execute("SELECT SUM(amount) FROM savings").fetchone()[0]
    db.close()
    return total or 0

def delete_saving(member_id, week):
    db = get_db()
    db.execute("DELETE FROM savings WHERE member_id = ? AND week = ?", (member_id, week))
    db.commit()
    db.close()

def add_member(name):
    db = get_db()
    db.execute("INSERT INTO members (name) VALUES (?)", (name,))
    db.commit()
    db.close()

def update_member(member_id, name):
    db = get_db()
    db.execute("UPDATE members SET name=? WHERE id=?", (name, member_id))
    db.commit()
    db.close()

def delete_member(member_id):
    db = get_db()
    # Hapus tabungan dulu (foreign key safety)
    db.execute("DELETE FROM savings WHERE member_id=?", (member_id,))
    db.execute("DELETE FROM members WHERE id=?", (member_id,))
    db.commit()
    db.close()
