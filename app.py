from flask import Flask, redirect, url_for, render_template, request, session
from db import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
import random

app = Flask("__main__")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app) # to add the app inside SQLAlchemy()

class players(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    team = db.Column(db.String(100))
    year = db.Column(db.Integer)
    url = db.Column(db.String(200))
    numG = db.Column(db.Integer)
    numC = db.Column(db.Integer)
    
    
    def __init__(self, name, team, year, url, numG, numC):
        self.name = name
        self.team = team
        self.year = year
        self.url = url
        self.numG = numG
        self.numC = numC

@app.route("/")
def home():
    return render_template("index.html")
 
@app.route("/new", methods=["POST", "GET"])
def new():
    name = None
    if request.method == "POST":
        name = request.form["nm"]
        team = request.form["tm"]
        url = request.form["lk"]
        usr = players(name, team, url)
        db.session.add(usr)
        db.session.commit()
        return redirect(url_for("view"))
    else:
        return render_template("new.html")

@app.route("/view")
def view():
    return render_template("view.html", values=players.query.all())

@app.route("/gen")
def gen():
    length = players.query.order_by(players._id.desc()).first()
    if length is not None:
        num = str(random.randint(1, length._id))
        return render_template("gen.html", value=players.query.filter_by(_id=num).first())
    else:
        return render_template("gen.html", value="blank")

@app.route("/clear", methods=["POST", "GET"])
def clear():
    if request.method == "POST":
        db.session.query(players).delete()
        db.session.commit()
        return redirect(url_for("view"))
    else:
        return render_template("clear.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)