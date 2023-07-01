from flask import Flask, redirect, url_for, render_template, request, session
from scrape import scrape_blueprint
from db import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
from models import players
import random

app = Flask("__main__")
app.register_blueprint(scrape_blueprint, url_prefix="/scrape")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app) # to add the app inside SQLAlchemy()


@app.route("/home")
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
        usr = players(name, team, 2021, url, 0, 0)
        db.session.add(usr)
        db.session.commit()
        return redirect(url_for("view"))
    else:
        return render_template("new.html")

@app.route("/view")
def view():
    return render_template("view.html", values=players.query.all())

@app.route("/gen", methods=["POST", "GET"] )
def gen():
    length = players.query.order_by(players._id.desc()).first()
    if length is not None:
        num = str(random.randint(1, length._id))
        currPlayer = players.query.filter_by(_id=num).first()
        return render_template("gen.html", value=currPlayer)
    else:
        return render_template("gen.html", value="blank")

@app.route("/result<name>", methods=["POST", "GET"])
def result(name):
    dbPlayer = players.query.filter_by(name=name).first()
    guess = request.form["guess"]
    if guess == name:
        dbPlayer.numC = dbPlayer.numC + 1
        dbPlayer.numG = dbPlayer.numG + 1
        db.session.commit()
        return render_template("result.html", value="correct")
    else:
        dbPlayer.numG = dbPlayer.numG + 1
        db.session.commit()
        return render_template("result.html", value="Incorrect")

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