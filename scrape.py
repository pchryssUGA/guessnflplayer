from flask import Flask, Blueprint, render_template, request, redirect, url_for
from db import db
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import requests
import json
#from models import player_database
from dotenv import load_dotenv
import os
load_dotenv()

API = 'https://customsearch.googleapis.com/customsearch/v1?'
KEY = os.getenv('GOOGLE_API_KEY')
CX = os.getenv('GOOGLE_API_CX')
WEBSITE = os.getenv('WEBSITE')

nameSet = set()
teams = {'nyj': 'New York Jets',
         'nwe': 'New England Patriots',
         'mia': 'Miami Dolphins',
         'buf': 'Buffalo Bills',
         'sea': 'Seattle Seahawks',
         'atl': 'Atlanta Falcons'}


#Represents a player object
class Player:
    def __init__(self, name, year, url):
        self.name = name
        self.year = year
        self.url = url

#Used to scrape players from the internet and 
def scrape(database):
    if request.method == 'POST':
        #Used for a real scrape
        if request.form['scrape_type'] == 'real':
            team = request.form['tm']
            startDate = request.form['sd']
            endDate = request.form['ed']
            run(database, team, startDate, endDate)
        #Used for a dummy scrape (testing purposes)
        elif request.form['scrape_type'] == 'dummy':
            zach = database('Zach Wilson', 'nyj', 2021, 'https://i2-prod.mirror.co.uk/incoming/article29751424.ece/ALTERNATES/n615/0_GettyImages-1345565987.jpg', 'hi', 0, 0, 0)
            michael = database('Michael Carter', 'nyj', 2021, 'https://jetsxfactor.com/wp-content/uploads/2022/05/Michael-Carter-II-NY-Jets-PFF-Stats-Duke-2021-Draft-Pick.jpg', 'hi', 0, 0, 0)
            keelan = database('Keelan Cole', 'nyj', 2021, 'https://jetsxfactor.com/wp-content/uploads/2021/03/Keelan-Cole-Jets.jpg', 'hi', 0, 0, 0)
            corey = database('Corey Davis', 'nyj', 2021, 'https://jetsxfactor.com/wp-content/uploads/2021/11/Ryan-Griffin-Elijah-Moore-NY-Jets-GM-Joe-Douglas.jpg', 'hi', 0, 0, 0)
            ryan = database('Ryan Griffin', 'nyj', 2021, 'https://jetsxfactor.com/wp-content/uploads/2021/09/Mike-LaFleur-Scheme-Film-NY-Jets-Trevon-Wesco-2021.jpg', 'hi', 0, 0, 0)
            trevon = database('Trevon Wesco', 'nyj', 2021, 'https://jetsxfactor.com/wp-content/uploads/2021/12/George-Fant-Helmet-NY-Jets-Stats-PFF-Grade-Contract.jpg', 'hi', 0, 0, 0)
            db.session.add(zach)
            db.session.add(michael)
            db.session.add(keelan)
            db.session.add(corey)
            db.session.add(ryan)
            db.session.add(trevon)
            db.session.commit()

#Function that runs the scraper
def run(database, tm, startDate, endDate):
    team = teams.get(tm)
    playerArray = []
    
    #Iterates through the scrape for every year requested. Uses the pandas library to locate a table populated with player names
    for i in range(int(endDate), int(startDate), -1):
        year = str(i)
        currentLink = WEBSITE+tm+'/'+year+'_roster.htm'
        currentData = requests.get(currentLink)
        df = pd.read_html(currentData.content)
        table = df[0]
        player_names = table['Player']
        #Iterates through every player name found in the table
        #First calls the Google Images API to generate an image url for the player
        #Then checks for duplicates (the website used uses * and + to denote pro bowl / all pro honors. In order to avoid 'Tom Brady' and 'Tom Brady+' from both being added,
        #the names are trimmed and then checked)
        for player in player_names:
            query = 'NFL ' + player + ' playing for ' + team + ' in game ' + year
            response = requests.get(API+'cx='+CX+'&num=1&q='+query+'&searchType=image&access_token='+KEY+'&key='+KEY+'&fileType=JPEG')
            image = response.json()
            imageItems = image['items'][0]
            imageLink = imageItems['link']
            if (player[-1] == '*'):
                if (player[:-1] not in nameSet):
                    nameSet.add(player[:-1])
                    playerArray.append(Player(player[:-1], year, imageLink))                
            elif (player[-1] == '+'):
                if (player[:-2] not in nameSet):
                    nameSet.add(player[:-2])
                    playerArray.append(Player(player[:-2], year, imageLink))
            else:
                if ((player not in nameSet) and (player != 'Offensive Starters') and (player != 'Defensive Starters')):
                    nameSet.add(player)
                    playerArray.append(Player(player, year, imageLink))
    #Sorts the array by year and then iterates through each name, adding them to the database
    playerArray = sorted(playerArray, key=lambda x: x.year)
    for player in playerArray:
        name = player.name.replace(' ', '_')
        f = open('static/images/'+tm+'/'+player.year+'/'+name+'.jpg', 'wb')
        f.write(requests.get(player.url).content)
        f.close()
        newPlayer = database(player.name, tm, player.year, 'static/images/'+tm+'/'+player.year+'/'+name+'.jpg', '',  0, 0, 0)
        db.session.add(newPlayer)
    db.session.commit()
    
    
    
    

