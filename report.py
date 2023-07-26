from flask import Flask, Blueprint, render_template, request, redirect, url_for
from db import db
from flask_sqlalchemy import SQLAlchemy
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API = "https://customsearch.googleapis.com/customsearch/v1?"
KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_API_CX")

report_blueprint = Blueprint("report", __name__, static_folder="static", template_folder="templates_report")

@report_blueprint.route("/", methods=["POST", "GET"])
def report(database):
    if request.method == "POST":
        if request.form["submit"] == "Clear Reports":
            for player in database.query.all():
                player.numR = 0
            db.session.commit()

@report_blueprint.route("/fix", methods=["POST", "GET"])
def fix(database, id):
    if request.method == "POST":
        if request.form["submit"] == "Pick this image":
            url = request.form["url"]
            id = int(request.form["id"])
            player = database.query.filter_by(_id=id).first()
            player.url = url
            player.numR = 0
            db.session.commit()
     
def get_player(database):       
    id = int(request.form["id"])
    images = []
    player = database.query.filter_by(_id=id).first()
    query = "nfl " + player.name + " playing for " + player.team + " clear image by himself"
    response = requests.get(API+"cx="+CX+"&num=4&q="+query+"&searchType=image&access_token="+KEY+"&key="+KEY)
    json = response.json()
    for i in range(4):
        imageItems = json['items'][i]
        imageLink = imageItems['link']
        images.append(imageLink)
    return [player, images]