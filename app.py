from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# File to store survey responses
EXCEL_FILE = "survey_responses.xlsx"

@app.route("/", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        # Get responses from form
        data = {
            "Invested in Stocks": request.form.get("q1"),
            "Bought Stocks in 6 Months": request.form.get("q2"),
            "Risk Tolerance (0-10)": request.form.get("q3"),
            "Trust in People": request.form.get("q4"),
            "Time Preference": request.form.get("q5"),
        }

        # Convert to DataFrame
        df = pd.DataFrame([data])

        # Append to Excel file (create if not exists)
        if not os.path.exists(EXCEL_FILE):
            df.to_excel(EXCEL_FILE, index=False)
        else:
            with pd.ExcelWriter(EXCEL_FILE, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
                df.to_excel(writer, index=False, header=False, startrow=writer.sheets["Sheet1"].max_row)

        return "Thank you! Your response has been recorded."

    return render_template("survey.html")

if __name__ == "__main__":
    app.run(debug=True)
