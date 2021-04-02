from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///input.db'
db = SQLAlchemy(app)

g_hours = "default"

@app.route("/", methods=['POST'])
def home():
    return render_template("home.html")

@app.route('/stats/', methods=["POST", "GET"])
def display():
    global g_hours
    if request.method == "POST":
        g_hours = request.form["hours"]
        return redirect("/stats/")
    return render_template("statsOverview.html", hours=g_hours)

@app.route('/stats/<hours>', methods=['POST','GET'])
def stats(hours):
    return render_template("statsOverview.html", hours = hours)


if __name__ == "__main__":
    app.run(debug=True)
