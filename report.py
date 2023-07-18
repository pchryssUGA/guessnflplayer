from flask import Flask, Blueprint, render_template, request, redirect, url_for
from db import db
from flask_sqlalchemy import SQLAlchemy
from models import player_database
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API = "https://customsearch.googleapis.com/customsearch/v1?"
KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_API_CX")

report_blueprint = Blueprint("report", __name__, static_folder="static", template_folder="templates_report")

@report_blueprint.route("/", methods=["POST", "GET"])
def report():
    if request.method == "POST":
        if request.form["submit"] == "Clear Reports":
            for player in player_database.query.all():
                player.numR = 0
            db.session.commit()
            return render_template("report.html", values=player_database.query.order_by(player_database.numR.desc(), player_database._id).all())
    return render_template("report.html", values=player_database.query.order_by(player_database.numR.desc(), player_database._id).all())

@report_blueprint.route("/fix", methods=["POST", "GET"])
def fix():
    if request.method == "POST":
        if request.form["submit"] == "Pick this image":
            url = request.form["url"]
            id = int(request.form["id"])
            player = player_database.query.filter_by(_id=id).first()
            player.url = url
            player.numR = 0
            db.session.commit()
            return render_template("report.html", values=player_database.query.order_by(player_database.numR.desc(), player_database._id).all())
    id = int(request.form["id"])
    images = []
    player = player_database.query.filter_by(_id=id).first()
    query = "nfl " + player.name + " playing for " + player.team + " clear image by himself"
    response = requests.get(API+"cx="+CX+"&num=4&q="+query+"&searchType=image&access_token="+KEY+"&key="+KEY)
    json = response.json()
    for i in range(4):
        imageItems = json['items'][i]
        imageLink = imageItems['link']
        images.append(imageLink)
    return render_template("fix.html", values=[player, images])