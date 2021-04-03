from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///input.db'
db = SQLAlchemy(app)

g_hours = "default"

#Returns default home page
@app.route("/", methods=['POST', 'GET'])
def home():
    return render_template("home.html")

#Bo's app compatable version of older stats page
@app.route('/stats/', methods=["POST", "GET"])
def display():
    global g_hours
    if request.method == "POST":
        g_hours = request.form["hours"]
        return redirect("/stats/")
    return render_template("statsOverview.html", hours=g_hours)

#Current stats page with autogenerating graph
#url.com/<hours>/<days>
#hours in order matching days separated by ~ for each new entry (hours can support float values)
#days in order matching hours separated by ~ for each new entry, additionally use : instead of / w
#the graph scales with number of entries so as long as you can make a link it can generate a graph
#the graph type can be customised by just changing one word (bar, line ...)
#Example link
#http://127.0.0.1:5000/stats/6.9~5.2~3.7~/3:04:2021~4:04:2021~5:04:2021~
@app.route('/stats/<hours>/<days>', methods=['POST','GET'])
def stats(hours, days):
#Converts input link into sets of arrays that is fed into graph.js
    temp = ""
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
    #small fix for bar graph that creates color values equal to the number of labels (since each label requires a reparate rgba value)
    for i in xlabl:
        color.append("rgba(255, 99, 132, 0.2)")
    return render_template("statsOverview.html", xlabl = xlabl, ylabl = ylabl, color = color)


if __name__ == "__main__":
    app.run(debug=True)
