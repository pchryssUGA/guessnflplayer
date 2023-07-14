from flask import Flask, Blueprint, render_template, request, redirect, url_for
from db import db
from flask_sqlalchemy import SQLAlchemy
from models import playersDB
import random

gen_blueprint = Blueprint("gen", __name__, static_folder="static", template_folder="templates_gen")

@gen_blueprint.route("/", methods=["POST", "GET"])
def gen():
    #gen is only generated from a POST request, code should never get passed the if
    if request.method == "POST":
        if (request.form["submit"] == "First Generate"):
            fromVal = request.form["from_range"]
            toVal = request.form["to_range"]
            pickTeam = request.form["pick_team"]
            #length gives the LAST id of a chosen teams set of players. If length is none, players exist for this team
            length = playersDB.query.filter_by(team=pickTeam).filter(playersDB.year >= fromVal).filter(playersDB.year <= toVal).order_by(playersDB._id.desc()).first()
            if length is not None:
                #first gives the FIRST id of a chosen teams set of players. This gives the code a safe range of ids to randomly select from.
                first = playersDB.query.filter_by(team=pickTeam).first()
                num = str(random.randint(first._id, length._id))
                currPlayer = playersDB.query.filter_by(team=pickTeam).filter(playersDB.year >= fromVal).filter(playersDB.year <= toVal).filter_by(_id=num).first()
                currPlayer.numG = currPlayer.numG + 1
                db.session.commit()
                return render_template("gen.html", values=[currPlayer, fromVal, toVal])
            else:
                return render_template("gen.html", value="blank")     


        elif (request.form["submit"] == "Generate a New Player"):
            fromVal = request.form["from_range"]
            toVal = request.form["to_range"]
            pickTeam = request.form["pick_team"]
            #length gives the LAST id of a chosen teams set of players. If length is none, players exist for this team
            length = playersDB.query.filter_by(team=pickTeam).order_by(playersDB._id.desc()).first()
            if length is not None:
                #first gives the FIRST id of a chosen teams set of players. This gives the code a safe range of ids to randomly select from.
                first = playersDB.query.filter_by(team=pickTeam).first()
                num = str(random.randint(first._id, length._id))
                currPlayer = playersDB.query.filter_by(team=pickTeam).filter(playersDB.year >= fromVal).filter(playersDB.year <= toVal).filter_by(_id=num).first()
                currPlayer.numG = currPlayer.numG + 1
                db.session.commit()
                return render_template("gen.html", values=[currPlayer, fromVal, toVal])
            else:
                return render_template("gen.html", value="blank")     
        elif (request.form["submit"] == "Report This Player"):
            playerID = int(request.form["pick_team"])
            reportPlayer = playersDB.query.filter_by(_id=playerID).first()
            reportPlayer.numR = reportPlayer.numR + 1
            db.session.commit()
            length = playersDB.query.filter_by(team=reportPlayer.team).order_by(playersDB._id.desc()).first()
            if length is not None:
                #first gives the FIRST id of a chosen teams set of players. This gives the code a safe range of ids to randomly select from.
                first = playersDB.query.filter_by(team=reportPlayer.team).first()
                num = str(random.randint(first._id, length._id))
                currPlayer = playersDB.query.filter_by(team=reportPlayer.team).filter_by(_id=num).first()
                currPlayer.numG = currPlayer.numG + 1
                db.session.commit()
            return render_template("gen.html", value=currPlayer)     
    else:
        return render_template("gen.html", value="blank")
    

@gen_blueprint.route("/result<name>", methods=["POST", "GET"])
def result(name):
    dbPlayer = playersDB.query.filter_by(name=name).first()
    guess = request.form["guess"]
    if guess == name:
        dbPlayer.numC = dbPlayer.numC + 1
        db.session.commit()
        return render_template("result.html", values=["Correct :)", dbPlayer])
    else:
        return render_template("result.html", values=["Incorrect :(", dbPlayer])