from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            stored_password = result[0]
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if stored_password == hashed_password:
                # Authentication successful, you can set up session or redirect to a protected page
                return render_template("home.html")
            else:
                return '''
                <script>
                    alert("Incorrect username or password.");
                    window.location.href = '/login';
                </script>'''
        else:
            return '''
                <script>
                    alert("User Not found, Please register.");
                    window.location.href = '/registeration';
                </script>'''
        conn.close()
    return render_template("login.html")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]

        if (
            len(password) < 10
            or not any(c.islower() for c in password)
            or not any(c.isupper() for c in password)
            or not any(c.isdigit() for c in password)
            or not any(c.isalnum() for c in password)
        ):
            return '''
                <script>
                    alert("Password does not meet the requirements.");
                    window.location.href = '/registration';
                </script>'''

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            return '''
                <script>
                    alert("Username already exists. Please choose a different username or Login.");
                    window.location.href = '/registration';
                </script>'''
        
        cursor.execute(
            """
            INSERT INTO users (username, email, password, phone)
            VALUES (?, ?, ?, ?)
        """,
            (username, email, hashed_password, phone),
        )

        conn.commit()
        conn.close()

        # Redirect to the login page
        return redirect(url_for("login"))

    return render_template("registration.html")


@app.route("/home")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)