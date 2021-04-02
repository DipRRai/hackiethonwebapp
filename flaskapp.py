from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///input.db'
db = SQLAlchemy(app)



@app.route("/", methods=['POST'])
def home():
    return render_template("home.html")

@app.route('/stats/<hours>', methods=['POST','GET'])
def stats(hours):
    return render_template("statsOverview.html", hours = hours)


if __name__ == "__main__":
    app.run(debug=True)



#asd;lfkjasdl;kfjasd;lkfj

#Test branching merge/pull rqeuest
=======
