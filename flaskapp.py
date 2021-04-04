from flask import Flask, render_template, request, redirect, jsonify, session, send_file
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
app.secret_key = "atomicpotatos"

hours = "1~"
days = "3:04:2021~"
isChanged = False

#Database model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    app_time = db.Column(db.String(10000), nullable=False)
    screen_time = db.Column(db.String(10000), nullable=False)
    screen_time_goal = db.Column(db.Integer, nullable=False)
    app_time_goals = db.Column(db.String(10000), nullable=False)

#Returns default home page
@app.route("/", methods=['POST', 'GET'])
def home():
    #db.create_all()
    #return "bruh"
    if "user" in session:
        user_obj = Users.query.filter_by(username=session['user']).first()
        key_val_pair = list(filter(lambda x: len(x) != 0, user_obj.app_time.split("|")))
        apps = [name.split("~")[0] for name in key_val_pair]
        app_dict = {}
        for entry in key_val_pair:
            key = entry.split("~")[0]
            val = entry.split("~")[1]
            app_dict[key] = val

        app_goal_dict = {}
        app_time_pair = list(filter(lambda x: len(x) != 0, user_obj.app_time_goals.split("|")))
        for entry in app_time_pair:
            app_name = entry.split("~")[0]
            goal_time = entry.split("~")[1]
            app_goal_dict[app_name] = goal_time
    else:
        apps = []


    #print(user_obj.app_time_goals)

    if request.method == "POST":
        print(request.form)
        if "screentimesubmit" in request.form:
            screen_time_goal = request.form["screentimegoal"]
            if len(screen_time_goal) == 0:
                screen_time_goal = 0
            user_obj = Users.query.filter_by(username=session['user']).first()
            user_obj.screen_time_goal = int(screen_time_goal)
            db.session.commit()
            return redirect("/")

        elif "submit" in request.form and request.form["submit"] == "addapp":
            app_name = request.form["appname"]
            if app_name not in apps:
                apps.append(app_name)
                app_dict[app_name] = "0"
                app_goal_dict[app_name] = "0"
                db_str = ""
                apptime_str = ""
                for app in apps:
                    db_str += f"{app}~{app_dict[app]}|"
                    if app != "datetime":
                        apptime_str += f"{app}~{app_goal_dict[app]}|"
                user_obj.app_time = db_str
                user_obj.app_time_goals = apptime_str
                db.session.commit()
            return redirect("/")

        elif "apptimesubmit" in request.form and request.form["apptimesubmit"] != "":
            app_goal = request.form[request.form["apptimesubmit"]]
            app_goal_dict[request.form["apptimesubmit"]] = app_goal
            #print(app_goal_dict)
            db_str = ""
            for app_name in apps:
                if app_name != "datetime":
                    db_str += f"{app_name}~{app_goal_dict[app_name]}|"
            user_obj.app_time_goals = db_str
            db.session.commit()
            return redirect("/")

        elif "deleteapp" in request.form and request.form["deleteapp"] != "":
            apps.remove(request.form["deleteapp"])
            db_str = ""
            for app in apps:
                db_str += f"{app}~{app_dict[app]}|"

            user_obj.app_time = db_str
            db.session.commit()
            return redirect("/")

        elif "button" in request.form and request.form["button"] == "Stats":
            return redirect("/stats")

        elif "button" in request.form and request.form["button"] == "Login":
            return redirect("/login")

        return redirect("/")
    else:
        #user_obj = Users.query.filter_by(username=session['user']).first()
        return render_template("home.html", session=session, apps =apps)

#URL that is reserved for the smart companion app. Returns screen time usage data
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

#URL that is reserved for the smart companion app. Returns app usage data
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
    return "Deprecated. Check main page"

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
            cred = Users.query.order_by(Users.id).all()
            for user in cred:
                if username == user.username:
                    return redirect("/login")
            db.session.add(Users(username = username, password = password, app_time = "",screen_time="", screen_time_goal = 0, app_time_goals = ""))
            db.session.commit()
            session["user"] = username
            return redirect("/")
        else:
            session.pop("user", None)
            return redirect("/")
    else:
        return render_template("login.html")

#URL that updates the statistics page. If data has been updated by companion app, URL will instruct stats page to refresh
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

#Returns statistics page, and also receives data sent by companion app.
@app.route('/stats/', methods=["POST", "GET"])
def display():
    global isChanged
    #global hours
    #global days

    if request.method == "POST":
        if "user" not in session:
            return redirect("/login")
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
            elif "returnHome" in request.form:
                return redirect("/")
            elif "download" in request.form:
                print("Download")
                return send_file(filename_or_fp="HackiethonProject.exe", as_attachment=True)
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
            ylabl.append(round((float(hour) / 60),2))
            xlabl.append(str(day))

        sum = 0
        color = []
        # small fix for bar graph that creates color values equal to the number of labels (since each label requires a reparate rgba value)
        for i in ylabl:
            color.append("rgba(255, 99, 132, 0.2)")
            sum += i

        if len(ylabl) > 0:
            average = round(sum / len(ylabl), 2)
            hasdataBar = "True"
        else:
            average = 0
            hasdataBar = "False"

        donutXlabel = []
        donutYlabel = []

        key_val_pair = list(filter(lambda x: len(x) != 0, user_obj.app_time.split("|")))

        #print(key_val_pair)
        app_time_dict = {}
        for pair in key_val_pair:
            time = pair.split("~")[1]
            appName = pair.split("~")[0]
            if appName == "datetime":
                continue
            else:
                app_time_dict[appName] = float(time) / 60
                donutXlabel.append(appName)
                donutYlabel.append(round((float(time) / 60),2))

        if len(donutYlabel) > 0:
            hasdataDonut = "True"
        else:
            hasdataDonut = "False"

        if len(ylabl) == 0:
            screen_time_today = 0
        else:
            screen_time_today = float(ylabl[-1])

        app_goal_dict = {}
        key_val_pair = list(filter(lambda x: len(x) != 0, user_obj.app_time_goals.split("|")))
        for pair in key_val_pair:
            time = pair.split("~")[1]
            appName = pair.split("~")[0]
            if appName == "datetime":
                continue
            else:
                app_goal_dict[appName] = float(time)

        #print(app_time_dict)
        #print(app_goal_dict)

        return render_template("statsOverview.html", xlabl=xlabl, ylabl=ylabl, color=color, sum=sum, average=average, session = session, donutXlabel = donutXlabel, donutYlabel = donutYlabel, hasdataBar = hasdataBar, hasdataDonut = hasdataDonut, user=user_obj, sc_time = screen_time_today, apptime=app_time_dict, appgoal=app_goal_dict)

if __name__ == "__main__":
    app.run(debug=True)