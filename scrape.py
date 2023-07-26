from flask import Flask, Blueprint, render_template, request, redirect, url_for
from db import db
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
#from models import player_database
from dotenv import load_dotenv
import os
load_dotenv()

API = "https://customsearch.googleapis.com/customsearch/v1?"
KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_API_CX")

playerArray = []
nameSet = set()

class Person:
    def __init__(self, name, year, url):
        self.name = name
        self.year = year
        self.url = url

#scrape_blueprint = Blueprint("scrape", __name__, static_folder="static", template_folder="templates")
#@scrape_blueprint.route("/", methods=["POST", "GET"])
def scrape(database):
    if request.method == "POST":
        if request.form["scrape_type"] == "real":
            team = request.form["tm"]
            startDate = request.form["sd"]
            endDate = request.form["ed"]
            run(database, team, startDate, endDate)
            return render_template("scrape.html")
        elif request.form["scrape_type"] == "dummy":
            zach = database("Zach Wilson", "nyj", 2021, "https://i2-prod.mirror.co.uk/incoming/article29751424.ece/ALTERNATES/n615/0_GettyImages-1345565987.jpg", "hi", 0, 0, 0)
            michael = database("Michael Carter", "nyj", 2021, "https://jetsxfactor.com/wp-content/uploads/2022/05/Michael-Carter-II-NY-Jets-PFF-Stats-Duke-2021-Draft-Pick.jpg", "hi", 0, 0, 0)
            keelan = database("Keelan Cole", "nyj", 2021, "https://jetsxfactor.com/wp-content/uploads/2021/03/Keelan-Cole-Jets.jpg", "hi", 0, 0, 0)
            corey = database("Corey Davis", "nyj", 2021, "https://jetsxfactor.com/wp-content/uploads/2021/11/Ryan-Griffin-Elijah-Moore-NY-Jets-GM-Joe-Douglas.jpg", "hi", 0, 0, 0)
            ryan = database("Ryan Griffin", "nyj", 2021, "https://jetsxfactor.com/wp-content/uploads/2021/09/Mike-LaFleur-Scheme-Film-NY-Jets-Trevon-Wesco-2021.jpg", "hi", 0, 0, 0)
            trevon = database("Trevon Wesco", "nyj", 2021, "https://jetsxfactor.com/wp-content/uploads/2021/12/George-Fant-Helmet-NY-Jets-Stats-PFF-Grade-Contract.jpg", "hi", 0, 0, 0)
            db.session.add(zach)
            db.session.add(michael)
            db.session.add(keelan)
            db.session.add(corey)
            db.session.add(ryan)
            db.session.add(trevon)
            db.session.commit()

def run(database, tm, sd, ed):
    nameSet = set()
    playerArray = []
    playerArray = []
    for i in range(int(ed), int(sd), -1):
        year = str(i)
        currentLink = 'https://www.pro-football-reference.com/teams/'+tm+'/'+year+'_roster.htm'
        currentData = requests.get(currentLink)
        currentDoc = BeautifulSoup(currentData.text, "html.parser")
        df = pd.read_html(currentData.content)
        table = df[0]
        player_names = table['Player']
        for player in player_names:
            query = "nfl " + player + " playing for " + tm + " clear image by himself"
            response = requests.get(API+"cx="+CX+"&num=1&q="+query+"&searchType=image&access_token="+KEY+"&key="+KEY)
            image = response.json()
            imageItems = image['items'][0]
            imageLink = imageItems['link']
            if (player[-1] == '*'):
                if (player[:-1] not in nameSet):
                    nameSet.add(player[:-1])
                    playerArray.append(Person(player[:-1], year, imageLink))                
            elif (player[-1] == '+'):
                if (player[:-2] not in nameSet):
                    nameSet.add(player[:-2])
                    playerArray.append(Person(player[:-2], year, imageLink))
            else:
                if ((player not in nameSet) and (player != "Offensive Starters") and (player != "Defensive Starters")):
                    nameSet.add(player)
                    playerArray.append(Person(player, year, imageLink))
    playerArray = sorted(playerArray, key=lambda x: x.year)
    for player in playerArray:
        newPlayer = database(player.name, tm, year, player.url, "",  0, 0, 0)
        db.session.add(newPlayer)
    db.session.commit()
    
    
    
    

