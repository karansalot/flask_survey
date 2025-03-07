import os
import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://your_local_db_url_here")

# Function to get database connection
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Create Table (Run Only Once)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id SERIAL PRIMARY KEY,
            invested_stocks TEXT,
            bought_stocks TEXT,
            risk_tolerance INTEGER,
            trust TEXT,
            time_preference TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()  # Ensure database is set up on startup

@app.route("/", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        q1 = request.form.get("q1")
        q2 = request.form.get("q2")
        q3 = request.form.get("q3")
        q4 = request.form.get("q4")
        q5 = request.form.get("q5")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO responses (invested_stocks, bought_stocks, risk_tolerance, trust, time_preference)
            VALUES (%s, %s, %s, %s, %s)
        ''', (q1, q2, q3, q4, q5))
        conn.commit()
        conn.close()

        return "Thank you! Your response has been recorded."

    return render_template("survey.html")

@app.route("/responses")
def view_responses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM responses")
    data = cursor.fetchall()
    conn.close()
    
    return "<br>".join([str(row) for row in data])

if __name__ == "__main__":
    app.run(debug=True)
