from flask import Flask, render_template, request, redirect, jsonify, session
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
app.secret_key = "atomicpotatos"

hours = "1~"
days = "3:04:2021~"
isChanged = False

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    app_time = db.Column(db.String(10000), nullable=False)
    screen_time = db.Column(db.String(10000), nullable=False)

#Returns default home page
@app.route("/", methods=['POST', 'GET'])
def home():
    #db.create_all()
    #user_obj = Users.query.filter_by(username=session['user']).first()
    #user_obj.app_time = "Word.exe~0|"
    #db.session.commit()
    return render_template("home.html", session=session)

#Get current user's screen time statistics
@app.route("/get_timestats", methods=['POST', 'GET'])
def get_timestats():
    if request.method == "POST":
        if "user" not in session:
            return "notLoggedIn"
        else:
            user_obj = Users.query.filter_by(username=session['user']).first()
            return user_obj.screen_time
    else:
        return "You are not meant to be here"

@app.route("/get_appstats", methods=["POST","GET"])
def get_appstats():
    if request.method == "POST":
        if "user" not in session:
            return "notLoggedIn"
        else:
            user_obj = Users.query.filter_by(username=session['user']).first()
            return user_obj.app_time
    else:
        return "You are not meant to be here"

#Config page for apps that needs to be monitored
@app.route("/config", methods=["POST", "GET"])
def config():
    if "user" not in session:
        return redirect("/login")
    else:
        user_obj = Users.query.filter_by(username=session['user']).first()
        key_val_pair = list(filter(lambda x: len(x) != 0, user_obj.app_time.split("|")))
        apps = [name.split("~")[0] for name in key_val_pair]
        app_dict = {}
        for entry in key_val_pair:
            key = entry.split("~")[0]
            val = entry.split("~")[1]
            app_dict[key] = val
        if request.method == "POST":
            if "submit" in request.form and request.form["submit"] == "addapp":
                app_name = request.form["appname"]
                if app_name not in apps:
                    apps.append(app_name)
                    app_dict[app_name] = "0"
                    db_str = ""
                    for app in apps:
                        db_str += f"{app}~{app_dict[app]}|"
                    user_obj.app_time = db_str
                    db.session.commit()
                return redirect("/config")
            elif "deleteapp" in request.form and request.form["deleteapp"] != "":
                apps.remove(request.form["deleteapp"])
                db_str = ""
                for app in apps:
                    db_str += f"{app}~{app_dict[app]}|"
                user_obj.app_time = db_str
                db.session.commit()
                return redirect("/config")
        else:
            user_obj = Users.query.filter_by(username=session['user']).first()
            print(user_obj.app_time)
            return render_template("config.html", apps=apps)

#Login check with client
@app.route("/login_client", methods=["GET", "POST"])
def login_check():
    isLoggedIn = False
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cred = Users.query.order_by(Users.id).all()
        for user in cred:
            if user.username == username and user.password == password:
                session["user"] = username
                isLoggedIn = True
                break
        if isLoggedIn:
            return "success"
        else:
            return "fail"
    else:
        return "You are not supposed to be on here"

#Login page
@app.route("/login", methods=["POST", "GET"])
def login():
    isLoggedIn = False
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if request.form["button"] == "Login":
            cred = Users.query.order_by(Users.id).all()
            for user in cred:
                if user.username == username and user.password == password:
                    session["user"] = username
                    isLoggedIn = True
                    break
            if isLoggedIn:
                return redirect("/")
            else:
                return redirect("/login")
        elif request.form["button"] == "Register":
            db.session.add(Users(username = username, password = password, app_time = "example.exe~0|",screen_time="1:1:2000~1|"))
            db.session.commit()
            session["user"] = username
            return redirect("/")
        else:
            session.pop("user", None)
            return redirect("/")
    else:
        return render_template("login.html")

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

#New method with POST requests
@app.route('/stats/', methods=["POST", "GET"])
def display():
    global isChanged
    #global hours
    #global days

    if request.method == "POST":
        if "user" not in session:
            return "Not Logged In"
        else:
            #print(request.form)
            if "stats" in request.form:
                user_obj = Users.query.filter_by(username=session['user']).first()
                user_obj.screen_time = request.form["stats"]
                db.session.commit()
                isChanged = True
                return "success"
            elif "appstats" in request.form:
                #print(request.form["appstats"])
                user_obj = Users.query.filter_by(username=session['user']).first()
                user_obj.app_time = request.form["appstats"]
                db.session.commit()
                isChanged = True
                return "success"
            else:
                return redirect("/stats")
    else:
        if "user" not in session:
            return redirect("/login")
        user_obj = Users.query.filter_by(username=session['user']).first()
        #print(user_obj.app_time)
        key_val_pair = list(filter(lambda x: len(x) !=0, user_obj.screen_time.split("|")))
        xlabl = []
        ylabl = []
        for pair in key_val_pair:
            hour = pair.split("~")[1]
            day = pair.split("~")[0]
            ylabl.append(float(hour))
            xlabl.append(str(day))
        sum = 0
        color = []
        # small fix for bar graph that creates color values equal to the number of labels (since each label requires a reparate rgba value)
        for i in ylabl:
            color.append("rgba(255, 99, 132, 0.2)")
            sum += i
        if len(ylabl) > 0:
            average = round(sum / len(ylabl), 2)
            hasdataBar = True
        else:
            average = 0
            hasdataBar = False
        #######################
        #Examples of what data input could be like
        #######################

        donutXlabel = []
        donutYlabel = []

        key_val_pair = list(filter(lambda x: len(x) != 0, user_obj.app_time.split("|")))

        #print(key_val_pair)

        for pair in key_val_pair:
            time = pair.split("~")[1]
            appName = pair.split("~")[0]
            if appName == "datetime":
                continue
            else:
                donutXlabel.append(appName)
                donutYlabel.append(float(time))
        if len(donutYlabel) > 0:
            hasdataDonut = True
        else:
            hasdataDonut = False

        #print(donutXlabel)
        #print(donutYlabel)

        return render_template("statsOverview.html", xlabl=xlabl, ylabl=ylabl, color=color, sum=sum, average=average, session = session, donutXlabel = donutXlabel, donutYlabel = donutYlabel, hasdataBar = hasdataBar, hasdataDonut = hasdataDonut)















 ######################################################################################################
      #Old method for URL query
#####################################################################################################     
#Current stats page with autogenerating graph
#url.com/<hours>/<days>
#hours in order matching days separated by ~ for each new entry (hours can support float values)
#days in order matching hours separated by ~ for each new entry, additionally use : instead of / w
#the graph scales with number of entries so as long as you can make a link it can generate a graph
#the graph type can be customised by just changing one word (bar, line ...)
#Example link
#http://127.0.0.1:5000/stats/6.9~5.2~3.7~5.8~8~/3:04:2021~4:04:2021~5:04:2021~6:04:2021~7:04:2021~~
@app.route('/stats/<hours>/<days>', methods=['POST','GET'])
def stats(hours, days):
#Converts input link into sets of arrays that is fed into graph.js
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
    #small fix for bar graph that creates color values equal to the number of labels (since each label requires a reparate rgba value)
    for i in ylabl:
        color.append("rgba(255, 99, 132, 0.2)")
        sum += i
    average = round(sum / len(ylabl), 2)
    return render_template("statsOverview.html", xlabl = xlabl, ylabl = ylabl, color = color, sum = sum, average = average)


if __name__ == "__main__":
    app.run(debug=True)