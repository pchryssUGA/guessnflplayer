from flask import Flask, Blueprint, render_template, request, redirect, url_for
from db import db
from flask_sqlalchemy import SQLAlchemy
from models import player_database
import random
import requests
import os
from dotenv import load_dotenv
load_dotenv()

gen_blueprint = Blueprint("gen", __name__, static_folder="static", template_folder="templates_gen")
API = "https://customsearch.googleapis.com/customsearch/v1?"
KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_API_CX")

#This function is used to notify me when a player has been reported 3 times. 
# It first access the Google Images API and querys 4 potential replacement images, storing them in variables.
# Then, it uses those images as parameters to call an AWS API gateway that I have created
# This API gateway in turn triggers the lambda which utilizes AWS SES services to send me an email with the
#  reported player name, id, and images formatted with proper HTML
def call_lambda(reportedID):
    api = "https://qv0ge6dcdl.execute-api.us-east-2.amazonaws.com/test/send?"
    id = str(reportedID)
    fixPlayer = player_database.query.filter_by(_id=int(id)).first()
    name = fixPlayer.name
    query = "nfl " + fixPlayer.name + " playing for " + fixPlayer.team + " clear image by himself"
    response = requests.get(API+"cx="+CX+"&num=4&q="+query+"&searchType=image&access_token="+KEY+"&key="+KEY)
    json = response.json()
    imageOne = json["items"][0]["link"]
    imageTwo = json["items"][1]["link"]
    imageThree = json["items"][2]["link"]
    imageFour = json["items"][3]["link"]
    
    response = requests.get(api + "playerID=" + id + "&playerName=" + name + "&imageOne=" + imageOne + "&imageTwo=" + imageTwo + "&imageThree=" + imageThree + "&imageFour=" + imageFour)
    returned = response.json()
    print(returned)

#Generate a new player
@gen_blueprint.route("/", methods=["POST", "GET"])
def gen():
    #Gen is only generated from a POST request, code should never get passed the if/else statement
    if request.method == "POST":
        fromVal = request.form["from_range"]
        toVal = request.form["to_range"]
        pickTeam = request.form["pick_team"]
        #If the user is wishing to report a player, it will add a report to the players numR variable, and check if the player has 3 reports
        # If the player has 3 report, it will call the call_lambda function
        if (request.form["submit"] == "Report This Player"):
            playerID = int(request.form["pick_id"])
            reportPlayer = player_database.query.filter_by(_id=playerID).first()
            reportPlayer.numR = reportPlayer.numR + 1
            db.session.commit()
            if reportPlayer.numR == 3:
                call_lambda(reportPlayer._id)
        #If length is none, there are no players for the selected year range. This helps exclude edge cases such as fromYear being greater than toYear
        length = player_database.query.filter_by(team=pickTeam).filter(player_database.year >= fromVal).filter(player_database.year <= toVal).order_by(player_database._id.desc()).first()
        if length is not None:
            #First gives the FIRST id of a chosen teams set of players. This is important as it gives the program a safe range of ids to choose from, 
#           # as players from a specific team from a specific year are given ids at the same time (e.g., 1-21 are NYJ, 2021)
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
    
#Displays the result of the user's guess
@gen_blueprint.route("/result/<name>", methods=["POST", "GET"])
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