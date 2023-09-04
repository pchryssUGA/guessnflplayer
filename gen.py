from flask import Flask, Blueprint, render_template, request, redirect, url_for
from db import db
from flask_sqlalchemy import SQLAlchemy
from models import player_database
import random
import requests
import os
from dotenv import load_dotenv
load_dotenv()

#Set up blueprint and os variables
gen_blueprint = Blueprint('gen', __name__, static_folder='/home/pchryss/RandomPlayer/static', template_folder='/home/pchryss/RandomPlayer/templates_gen')
API = 'https://customsearch.googleapis.com/customsearch/v1?'
KEY = os.getenv('GOOGLE_API_KEY')
CX = os.getenv('GOOGLE_API_CX')

#Used to change website colors depending on a users chosen team
team_colors = {'crd': '#97233F',
               'atl': '#a71930',
               'rav': '#241773',
               'buf': '#00338D',
               'car': '#0085CA',
               'chi': '#C83803',
               'cin': '#FB4F14',
               'cle': '#FF3C00',
               'dal': '#041E42',
               'den': '#FB4F14',
               'det': '#0076B6',
               'gnb': '#203731',
               'htx': '#03202F',
               'clt': '#002C5F',
               'jax': '#006778',
               'kan': '#E31837',
               'rai': '#000000',
               'sdg': '#0080C6',
               'ram': '#003594',
               'mia': '#008E97',
               'min': '#4F2683',
               'nwe': '#002244',
               'nor': '#D3BC8D',
               'nyj': '#125740',
               'nyg': '#0B2265',
               'phi': '#004C54',
               'pit': '#101820',
               'sfo': '#AA0000',
               'sea': '#002244',
               'tam': '#D50A0A',
               'oti': '#4B92DB',
               'was': '#5A1414'}

#Generate a new player
@gen_blueprint.route('/', methods=['POST', 'GET'])
def gen():
   #Gen should generally only be generated using a post request, meaning a user has chosen a team
   if request.method == 'POST':
      fromVal = request.form['from_range']
      toVal = request.form['to_range']
      pickTeam = request.form['pick_team']
      #Reporting a player will increment their numR variable (numReport)
      if (request.form['submit'] == 'Report a Bad Image'):
         playerID = int(request.form['pick_id'])
         reportPlayer = player_database.query.filter_by(_id=playerID).first()
         reportPlayer.numR = reportPlayer.numR + 1
         db.session.commit()
      length = player_database.query.filter_by(team=pickTeam).filter(player_database.year >= fromVal).filter(player_database.year <= toVal).order_by(player_database._id.desc()).first()
      #If length is none, there are no players for the selected year range/team combination. This also helps exclude edge cases such as fromYear being greater than toYear
      if length is not None:
         #First gives the FIRST id of a chosen teams set of players. This is important as it gives the program a safe range of ids to choose from, 
         #           # as players from a specific team from a specific year are given ids at the same time (e.g., if 1-20 are NYJ, 2022, you only want to generate players 1-20)
         first = player_database.query.filter_by(team=pickTeam).filter(player_database.year >= fromVal).filter(player_database.year <= toVal).first()
         num = str(random.randint(first._id, length._id))
         currPlayer = player_database.query.filter_by(team=pickTeam).filter(player_database.year >= fromVal).filter(player_database.year <= toVal).filter_by(_id=num).first()            
         currPlayer.numG = currPlayer.numG + 1
         db.session.commit()
         team = currPlayer.team
         color = team_colors.get(team)
         return render_template('gen.html', values=[currPlayer, fromVal, toVal, color]) 
      else:
         return render_template('gen.html', value='blank')     
   else:
      return render_template('gen.html', value='blank')
   
#Displays the result of the user's guess
@gen_blueprint.route('/result/<id>', methods=['POST', 'GET'])
def result(id):
    dbPlayer = player_database.query.filter_by(_id=id).first()
    fromYear = request.form['from_range']
    toYear = request.form['to_range']
    guess = request.form['guess']
    color = team_colors.get(dbPlayer.team)
    #If the users guess was correct, it will increment the players numC variable (numCorrect)
    if guess.lower() == dbPlayer.name.lower():
        dbPlayer.numC = dbPlayer.numC + 1
        db.session.commit()
        return render_template('result.html', values=['Correct :)', dbPlayer, fromYear, toYear, color])
    else:
        return render_template('result.html', values=['Incorrect :(', dbPlayer, fromYear, toYear, color])
