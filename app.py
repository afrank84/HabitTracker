from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DATA_DIR = "data"

START_DATE = datetime(2025, 3, 11)
END_DATE = datetime(2025, 3, 31)


def get_user_data(username):
    filepath = os.path.join(DATA_DIR, f"{username}.json")
    if not os.path.exists(filepath):
        return {"username": username, "habits": []}
    with open(filepath, "r") as f:
        return json.load(f)


def get_date_range():
    days = []
    current = START_DATE
    while current <= END_DATE:
        days.append({
            "date": current.strftime("%Y-%m-%d"),
            "label": current.strftime("%b<br>%-d<br>%a"),
            "is_current": False,
            "is_weekend": current.weekday() >= 5
        })
        current += timedelta(days=1)
    days.append({
        "date": "2025-04-01",
        "label": "Apr<br>1<br>TUE",
        "is_current": True
    })
    return days


@app.route("/")
def index():
    username = "frank"
    user_data = get_user_data(username)
    days = get_date_range()
    return render_template("index.html", user=user_data, days=days)


@app.route("/update", methods=["POST"])
def update():
    data = request.json
    username = data["username"]
    filepath = os.path.join(DATA_DIR, f"{username}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(debug=True)
