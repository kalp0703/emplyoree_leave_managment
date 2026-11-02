from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection, create_table

app = Flask(__name__)

# Create database table
create_table()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Apply for leave
@app.route("/apply", methods=["GET", "POST"])
def apply_leave():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        reason = request.form["reason"]

        if end_date < start_date:
            return "End date cannot be before start date"

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO leave_requests
            (employee_name, employee_email, start_date, end_date, reason)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, start_date, end_date, reason))

        conn.commit()
        conn.close()

        return redirect(url_for("leave_status"))

    return render_template("apply_leave.html")


# View leave requests
@app.route("/status")
def leave_status():

    conn = get_db_connection()

    requests = conn.execute(
        "SELECT * FROM leave_requests ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("leave_status.html", requests=requests)


if __name__ == "__main__":
    app.run(debug=True)