from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///input.db'
db = SQLAlchemy(app)

g_hours = "default"
isChanged = False

@app.route("/", methods=['POST'])
def home():
    return render_template("home.html")

@app.route('/test', methods=['GET', 'POST'])
def testfn():
    global isChanged
    # GET request
    if request.method == 'GET':
        if isChanged:
            message = {'changed':'yes'}
            isChanged = False
        else:
            message = {'changed':'no'}
        return jsonify(message)  # serialize and use JSON headers

@app.route('/stats/', methods=["POST", "GET"])
def display():
    global g_hours
    global isChanged
    if request.method == "POST":
        g_hours = request.form["hours"]
        isChanged = True
        return redirect("/stats/")
    else:
        return render_template("statsOverview.html", hours=g_hours)

@app.route('/stats/<hours>', methods=['POST','GET'])
def stats(hours):
    return render_template("statsOverview.html", hours = hours)


if __name__ == "__main__":
    app.run(debug=True)