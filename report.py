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

#Clears all reports
def report(database):
    for player in database.query.all():
        player.numR = 0
    db.session.commit()

#Changes a players url
def fix(database):
    url = request.form["url"]
    id = int(request.form["id"])
    player = database.query.filter_by(_id=id).first()
    player.url = url
    player.numR = 0
    db.session.commit()
     
#Calls Google Images API and returns a player object and 4 queried images
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