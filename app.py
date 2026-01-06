from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import get_db, init_db, insert_members
from models import (
    get_all_members,
    get_member_by_id,
    get_savings_by_member,
    get_total_savings,
    get_last_week,
    get_global_total,
    add_saving,
    get_filled_weeks,
    delete_saving,
    add_member,
    update_member,
    delete_member
)
import locale, platform

app = Flask(__name__)

# =====================
# FILTER RUPIAH
# =====================
def format_rupiah(value):
    if value is None:
        return "0"
    try:
        if platform.system() == "Windows":
            locale.setlocale(locale.LC_NUMERIC, 'Indonesian_Indonesia.1252')
        else:
            locale.setlocale(locale.LC_NUMERIC, 'id_ID.UTF-8')
    except:
        locale.setlocale(locale.LC_NUMERIC, 'C')
    return locale.format_string("%d", int(value), grouping=True)

app.jinja_env.filters['format_rupiah'] = format_rupiah

init_db()
insert_members()

# ==========================================================
# SCAN / INDEX
# ==========================================================
@app.route("/me")
def me():
    return render_template("me.html")

# =====================
# DASHBOARD
# =====================
@app.route("/")
def index():
    members = get_all_members()
    data = []

    for m in members:
        total = get_total_savings(m["id"])
        last_week = get_last_week(m["id"]) or 0
        next_week = last_week + 1 if last_week < 52 else None

        notif = ""
        if total >= 100000:
            notif = "Hebat! Sudah Banyak"
        elif last_week >= 10:
            notif = "Mantap! 10 minggu 💪"

        data.append({
            "member": m,
            "total": total,
            "count": last_week,
            "notif": notif,
            "next_week": next_week
        })

    return render_template(
        "index.html",
        data=data,
        global_total=get_global_total()
    )

# =====================
# TABUNGAN
# =====================
@app.route("/add/<int:member_id>", methods=["POST"])
def add(member_id):
    week = int(request.form.get("week"))
    last_week = get_last_week(member_id) or 0
    next_week = last_week + 1 if last_week < 52 else None

    if week != next_week:
        return "Minggu tidak valid", 400

    add_saving(member_id, week, 10000)
    return redirect(url_for("index"))

@app.route("/edit/<int:member_id>", methods=["POST"])
def edit(member_id):
    week = int(request.form.get("week"))
    delete_saving(member_id, week)
    return redirect(url_for("index"))

@app.route("/api/filled_weeks/<int:member_id>")
def api_filled_weeks(member_id):
    return jsonify({"filled_weeks": get_filled_weeks(member_id)})

# =====================
# DATA ANGGOTA
# =====================
@app.route("/members")
def members_list():
    members = get_all_members()
    data = []

    for m in members:
        data.append({
            "id": m["id"],
            "name": m["name"],
            "total": get_total_savings(m["id"]),
            "last_week": get_last_week(m["id"]) or 0
        })

    return render_template("anggota.html", members=data)

@app.route("/members/add", methods=["POST"])
def member_add():
    add_member(request.form.get("name"))
    return redirect(url_for("members_list"))

@app.route("/members/edit/<int:id>", methods=["POST"])
def member_edit(id):
    update_member(id, request.form.get("name"))
    return redirect(url_for("members_list"))

@app.route("/members/delete/<int:id>", methods=["POST"])
def member_delete(id):
    delete_member(id)
    return redirect(url_for("members_list"))

# =====================
# DETAIL ANGGOTA
# =====================
@app.route("/members/<int:member_id>")
def member_detail(member_id):
    member = get_member_by_id(member_id)
    savings = get_savings_by_member(member_id)

    total = sum(s["amount"] for s in savings)
    labels = [f"Minggu {s['week']}" for s in savings]
    values = [s["amount"] for s in savings]

    return render_template(
        "member_detail.html",
        member=member,
        savings=savings,
        total=total,
        labels=labels,
        values=values
    )

if __name__ == "__main__":
    app.run(debug=True)
