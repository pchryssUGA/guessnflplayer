from flask import Flask, Blueprint, render_template, request, redirect, url_for
from db import db
from flask_sqlalchemy import SQLAlchemy
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API = 'https://customsearch.googleapis.com/customsearch/v1?'
KEY = os.getenv('GOOGLE_API_KEY')
CX = os.getenv('GOOGLE_API_CX')

#Resets the numR variable of all players to 0
def reset_reports(database):
    for player in database.query.all():
        player.numR = 0
    db.session.commit()

#Resets the numC variable of all players to 0
def reset_numC(database):
    for player in database.query.all():
        player.numC = 0
    db.session.commit()

#Resets the numG variable of all players to 0
def reset_numG(database):
    for player in database.query.all():
        player.numG = 0
    db.session.commit()
    
#Function that is called when an admin needs to generate potential images to replace a reported players "bad" image
def get_player(database, need_better):       
    id = int(request.form['id'])
    images = []
    player = database.query.filter_by(_id=id).first()
    year = str(player.year)
    print(player.name)
    print(player.team)
    print(year)
    query = 'NFL ' + player.name + ' playing for ' + player.team + ' in game ' + year
    #need_better is True when the first four images are not good. This makes the query broader and helps find images for players that are not as popular
    if need_better is True:
        query = 'NFL ' + player.name + ' in game'
    else:
        query = 'NFL ' + player.name + ' playing for ' + player.team + ' in game ' + year
    response = requests.get(API+'cx='+CX+'&num=5&q='+query+'&searchType=image&access_token='+KEY+'&key='+KEY)
    json = response.json()
    for i in range(len(json['items'])):
        imageItems = json['items'][i]
        imageLink = imageItems['link']
        images.append(imageLink)
    return [player, images]

#Function that is called when an admin picks an image to replace a reported players "bad" image
def fix(database):
    url = request.form['url']
    id = int(request.form['id'])
    player = database.query.filter_by(_id=id).first()
    year = str(player.year)
    name = player.name
    name = player.name.replace(' ', '_')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    f = open('/home/pchryss/RandomPlayer/static/images/'+player.team+'/'+year+'/'+name+'.jpg', 'wb')
    f.write(requests.get(url, headers=headers, verify=False).content)
    f.close()
    player.numR = 0
    db.session.commit()
