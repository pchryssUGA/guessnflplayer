from flask import Flask, Blueprint, render_template, request, redirect, url_for
from db import db
from flask_sqlalchemy import SQLAlchemy
from models import players
import random

gen_blueprint = Blueprint("gen", __name__, static_folder="static", template_folder="templates_gen")
@gen_blueprint.route("/", methods=["POST", "GET"])
def gen():
    length = players.query.order_by(players._id.desc()).first()
    if length is not None:
        num = str(random.randint(1, length._id))
        currPlayer = players.query.filter_by(_id=num).first()
        return render_template("gen.html", value=currPlayer)
    else:
        return render_template("gen.html", value="blank")
    
@gen_blueprint.route("/result<name>", methods=["POST", "GET"])
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