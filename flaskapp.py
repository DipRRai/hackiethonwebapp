from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///input.db'
db = SQLAlchemy(app)

hours = "1~"
days = "3:04:2021~"
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
    global isChanged
    """
    global g_hours
    global isChanged
    if request.method == "POST":
        g_hours = request.form["hours"]
        isChanged = True
        return redirect("/stats/")
    else:
        return render_template("statsOverview.html", hours=g_hours)
    """
    global hours
    global days

    if request.method == "POST":
        hours = request.form["hours"]
        days = request.form["days"]
        isChanged = True
        return "success"
    else:
        temp = ""
        sum = 0
        ylabl = []
        for i in hours:
            if i != ('~'):
                temp = temp + i
            elif i == ('~'):
                ylabl.append(float(temp))
                temp = ""
        temp = ""
        xlabl = []
        color = []
        for i in days:
            if i != ('~'):
                if i == ':':
                    temp = temp + "/"
                else:
                    temp = temp + i
            elif i == ('~'):
                xlabl.append(str(temp))
                temp = ""
        # small fix for bar graph that creates color values equal to the number of labels (since each label requires a reparate rgba value)
        for i in ylabl:
            color.append("rgba(255, 99, 132, 0.2)")
            sum += i
        average = round(sum / len(ylabl), 2)
        return render_template("statsOverview.html", xlabl=xlabl, ylabl=ylabl, color=color, sum=sum, average=average)


@app.route('/stats/<hours>', methods=['POST','GET'])
def stats(hours):
    return render_template("statsOverview.html", hours = hours)


if __name__ == "__main__":
    app.run(debug=True)