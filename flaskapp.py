from flask import Flask, render_template
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
    return render_template("statsOverview.html", hours=g_hours)

@app.route('/stats/<hours>', methods=['POST','GET'])
def stats(hours):
    global g_hours
    g_hours = hours
    return render_template("statsOverview.html", hours = g_hours)


if __name__ == "__main__":
    app.run(debug=True)
