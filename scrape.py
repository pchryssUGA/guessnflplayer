from flask import Flask, Blueprint, render_template, request, redirect, url_for
from db import db
from flask_sqlalchemy import SQLAlchemy
from openpyxl import load_workbook
import pandas as pd
import requests
import json
#from models import player_database
from dotenv import load_dotenv
import os

project_folder = os.path.expanduser('/home/pchryss/RandomPlayer')
load_dotenv(os.path.join(project_folder, '.env'))

API = 'https://customsearch.googleapis.com/customsearch/v1?'
KEY = os.getenv('GOOGLE_API_KEY')
CX = os.getenv('GOOGLE_API_CX')
WEBSITE = os.getenv('WEBSITE')

wb = load_workbook(filename='/home/pchryss/2022_nfl_starters.xlsx')
roster_sheet = wb['Regular Season 22']

nameSet = set()
scrape_teams = {'crd': 'Arizona Cardinals',
                'atl': 'Atlanta Falcons',
                'rav': 'Baltimore Ravens',
                'buf': 'Buffalo Bills',
                'car': 'Carolina Panthers',
                'chi': 'Chicago Bears',
                'cin': 'Cincinatti Bengals',
                'cle': 'Cleveland Browns',
                'dal': 'Dallas Cowboys',
                'den': 'Denver Broncos',
                'det': 'Detroit Lions',
                'gnb': 'Green Bay Packers',
                'htx': 'Houston Texans',
                'clt': 'Indianapolis Colts',
                'jax': 'Jacksonville Jaguars',
                'kan': 'Kansis City Chiefs',
                'rai': 'Las Vegas Raiders',
                'sdg': 'Los Angeles Chargers',
                'ram': 'Los Angeles Rams',
                'mia': 'Miami Dolphins',
                'min': 'Minnesota Vikings',
                'nwe': 'New England Patriots',    
                'nor': 'New Orleans Saints',
                'nyg': 'New York Giants',
                'nyj': 'New York Jets',
                'phi': 'Philadelphia Eagles',
                'pit': 'Pittsburgh Steelers',
                'sfo': 'San Francisco 49ers',
                'sea': 'Seattle Seahawks',
                'tam': 'Tampa Bay Buccaneers',
                'oti': 'Tennessee Titans',            
                'was': 'Washington Commanders'}

sheet_teams = {'crd': 'B',
               'atl': 'C',
               'rav': 'D',
               'buf': 'E',
               'car': 'F',
               'chi': 'G',
               'cin': 'H',
               'cle': 'I',
               'dal': 'J',
               'den': 'K',
               'det': 'L',
               'gnb': 'M',
               'htx': 'N',
               'clt': 'O',
               'jax': 'P',
               'kan': 'Q',
               'rai': 'R',
               'sdg': 'S',
               'ram': 'T',
               'mia': 'U',
               'min': 'V',
               'nwe': 'W',
               'nor': 'X',
               'nyg': 'Y',
               'nyj': 'Z',
               'phi': 'AA',
               'pit': 'AB',
               'sfo': 'AC',
               'sea': 'AD',
               'tam': 'AE',
               'oti': 'AF',
               'was': 'AG'}               

#Represents a player object
class Player:
    def __init__(self, name, year, url):
        self.name = name
        self.year = year
        self.url = url

def scrape(database):
    if request.method == 'POST':
        team = request.form['tm']
        startDate = request.form['sd']
        endDate = request.form['ed']
        run(database, team, startDate, endDate)
        
#Function that runs the scraper
def run(database, tm, startDate, endDate):
    team = scrape_teams.get(tm)
    playerArray = []
    
    #Iterates through the scrape for every year requested. Uses the pandas library to locate a table populated with player names
    for i in range(int(endDate), int(startDate), -1):
        year = str(i)
        if year == '2022':
            player_names = []
            col = sheet_teams.get(tm)
            for i in range(2, 23):
                player_names.append(roster_sheet[col+str(i)].value)
        else:
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
            if (player == 'Offensive Starters' or player == 'Defensive Starters'):
                continue
            elif (player[-1] == '*' or player[-1] == '+'):
                if (player[-2] == '*'):
                    player = player[:-2] 
                else:
                    player = player[:-1]
            if (player  in nameSet):
                continue
            query = 'NFL ' + player + ' playing for ' + team + ' in game ' + year
            response = requests.get(API+'cx='+CX+'&num=1&q='+query+'&searchType=image&access_token='+KEY+'&key='+KEY+'&fileType=JPEG')
            image = response.json()
            print(player)
            imageItems = image['items'][0]
            imageLink = imageItems['link']
            nameSet.add(player)
            playerArray.append(Player(player, year, imageLink))
    #Sorts the array by year and then iterates through each name, adding them to the database
    playerArray = sorted(playerArray, key=lambda x: x.year)
    for player in playerArray:
        name = player.name.replace(' ', '_')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
        f = open('/home/pchryss/RandomPlayer/static/images/'+tm+'/'+player.year+'/'+name+'.jpg', 'wb')
        f.write(requests.get(player.url, headers=headers,verify=False).content)
        f.close()
        newPlayer = database(player.name, tm, player.year, '/static/images/'+tm+'/'+player.year+'/'+name+'.jpg', '',  0, 0, 0)
        db.session.add(newPlayer)
    db.session.commit()
    
    
    
    

