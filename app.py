import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "findit-development-key")
DATABASE = os.environ.get("DATABASE_PATH", os.path.join(app.instance_path, "findit.db"))

os.makedirs(app.instance_path, exist_ok=True)


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                category TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT,
                report_type TEXT NOT NULL CHECK(report_type IN ('Lost', 'Found')),
                status TEXT NOT NULL DEFAULT 'Open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()


@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    report_type = request.args.get("type", "").strip()
    query = "SELECT * FROM items WHERE 1=1"
    params = []

    if search:
        query += " AND (item_name LIKE ? OR category LIKE ? OR location LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])

    if report_type in ("Lost", "Found"):
        query += " AND report_type = ?"
        params.append(report_type)

    query += " ORDER BY created_at DESC, id DESC"

    with get_db() as db:
        items = db.execute(query, params).fetchall()
        counts = {
            "total": db.execute("SELECT COUNT(*) FROM items").fetchone()[0],
            "lost": db.execute("SELECT COUNT(*) FROM items WHERE report_type='Lost'").fetchone()[0],
            "found": db.execute("SELECT COUNT(*) FROM items WHERE report_type='Found'").fetchone()[0],
            "returned": db.execute("SELECT COUNT(*) FROM items WHERE status='Returned'").fetchone()[0],
        }

    return render_template(
        "index.html", items=items, counts=counts, search=search, selected_type=report_type
    )


@app.route("/report", methods=["POST"])
def report_item():
    item_name = request.form.get("item_name", "").strip()
    category = request.form.get("category", "").strip()
    location = request.form.get("location", "").strip()
    description = request.form.get("description", "").strip()
    report_type = request.form.get("report_type", "").strip()

    if not item_name or not category or not location or report_type not in ("Lost", "Found"):
        flash("Please complete the required fields.", "error")
        return redirect(url_for("index"))

    with get_db() as db:
        db.execute(
            """INSERT INTO items (item_name, category, location, description, report_type)
               VALUES (?, ?, ?, ?, ?)""",
            (item_name, category, location, description, report_type),
        )
        db.commit()

    flash(f"{report_type} item reported successfully.", "success")
    return redirect(url_for("index"))


@app.route("/items/<int:item_id>/returned", methods=["POST"])
def mark_returned(item_id):
    with get_db() as db:
        db.execute("UPDATE items SET status='Returned' WHERE id=?", (item_id,))
        db.commit()
    flash("Item marked as returned.", "success")
    return redirect(url_for("index"))


@app.get("/health")
def health():
    return {"status": "healthy"}, 200


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
