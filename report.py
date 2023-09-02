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

#Clears all reports
def reset_reports(database):
    for player in database.query.all():
        player.numR = 0
    db.session.commit()

def reset_numC(database):
    for player in database.query.all():
        player.numC = 0
    db.session.commit()

def reset_numG(database):
    for player in database.query.all():
        player.numG = 0
    db.session.commit()


#Changes a players url
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

def get_player(database, need_better):       
    id = int(request.form['id'])
    images = []
    player = database.query.filter_by(_id=id).first()
    year = str(player.year)
    query = 'NFL ' + player.name + ' playing for ' + player.team + ' in game ' + year
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
