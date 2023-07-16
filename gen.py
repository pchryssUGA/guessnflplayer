from flask import Flask, Blueprint, render_template, request, redirect, url_for
from db import db
from flask_sqlalchemy import SQLAlchemy
from models import player_database
import random

gen_blueprint = Blueprint("gen", __name__, static_folder="static", template_folder="templates_gen")

@gen_blueprint.route("/", methods=["POST", "GET"])
def gen():
    #gen is only generated from a POST request, code should never get passed the if
    if request.method == "POST":
        fromVal = request.form["from_range"]
        toVal = request.form["to_range"]
        pickTeam = request.form["pick_team"]
        if (request.form["submit"] == "First Generate"):
            #length gives the LAST id of a chosen teams set of players. If length is none, players exist for this team
            length = player_database.query.filter_by(team=pickTeam).filter(player_database.year >= fromVal).filter(player_database.year <= toVal).order_by(player_database._id.desc()).first()
            if length is not None:
                #first gives the FIRST id of a chosen teams set of players. This gives the code a safe range of ids to randomly select from.
                first = player_database.query.filter_by(team=pickTeam).filter(player_database.year >= fromVal).filter(player_database.year <= toVal).first()
                num = str(random.randint(first._id, length._id))
                currPlayer = player_database.query.filter_by(team=pickTeam).filter(player_database.year >= fromVal).filter(player_database.year <= toVal).filter_by(_id=num).first()
                currPlayer.numG = currPlayer.numG + 1
                db.session.commit()
                return render_template("gen.html", values=[currPlayer, fromVal, toVal])
            else:
                return render_template("gen.html", value="blank")     
        elif (request.form["submit"] == "Generate a New Player"):
            #length gives the LAST id of a chosen teams set of players. If length is none, players exist for this team
            length = player_database.query.filter_by(team=pickTeam).filter(player_database.year >= fromVal).filter(player_database.year <= toVal).order_by(player_database._id.desc()).first()
            if length is not None:
                #first gives the FIRST id of a chosen teams set of players. This gives the code a safe range of ids to randomly select from.
                first = player_database.query.filter_by(team=pickTeam).filter(player_database.year >= fromVal).filter(player_database.year <= toVal).first()
                num = str(random.randint(first._id, length._id))
                currPlayer = player_database.query.filter_by(team=pickTeam).filter(player_database.year >= fromVal).filter(player_database.year <= toVal).filter_by(_id=num).first()
                currPlayer.numG = currPlayer.numG + 1
                db.session.commit()
                return render_template("gen.html", values=[currPlayer, fromVal, toVal])
            else:
                return render_template("gen.html", value="blank")     
        elif (request.form["submit"] == "Report This Player"):
            playerID = int(request.form["pick_id"])
            reportPlayer = player_database.query.filter_by(_id=playerID).first()
            reportPlayer.numR = reportPlayer.numR + 1
            db.session.commit()
            length = player_database.query.filter_by(team=pickTeam).filter(player_database.year >= fromVal).filter(player_database.year <= toVal).order_by(player_database._id.desc()).first()
            if length is not None:
                #first gives the FIRST id of a chosen teams set of players. This gives the code a safe range of ids to randomly select from.
                first = player_database.query.filter_by(team=pickTeam).filter(player_database.year >= fromVal).filter(player_database.year <= toVal).first()
                num = str(random.randint(first._id, length._id))
                currPlayer = player_database.query.filter_by(team=pickTeam).filter(player_database.year >= fromVal).filter(player_database.year <= toVal).filter_by(_id=num).first()
                currPlayer.numG = currPlayer.numG + 1
                db.session.commit()
                return render_template("gen.html", values=[currPlayer, fromVal, toVal]) 
            else:
                return render_template("gen.html", value="blank")     
    else:
        return render_template("gen.html", value="blank")
    

@gen_blueprint.route("/result<name>", methods=["POST", "GET"])
def result(name):
    dbPlayer = player_database.query.filter_by(name=name).first()
    fromYear = request.form["from_range"]
    toYear = request.form["to_range"]
    guess = request.form["guess"]
    if guess == name:
        dbPlayer.numC = dbPlayer.numC + 1
        db.session.commit()
        return render_template("result.html", values=["Correct :)", dbPlayer, fromYear, toYear])
    else:
        return render_template("result.html", values=["Incorrect :(", dbPlayer, fromYear, toYear])