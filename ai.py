import openai
import os
from db import db
from flask import request

teams = {'nyj': 'New York Jets',
         'buf': 'Buffalo Bills',
         'nwe': 'New England Patriots',
         'mia': 'Miami Dolphins',
         'rav': 'Baltimore Raves',
         'cin': 'Cincinatti Bengals',
         'cle': 'Cleveland Browns',
         'pit': 'Pittsburgh Steelers',
         'htx': 'Houston Texans',
         'clt': 'Indianapolis Colts',
         'jax': 'Jacksonville Jaguars',
         'oti': 'Tennessee Titans',
         'den': 'Denver Broncos',
         'kan': 'Kansis City Chiefs',
         'rai': 'Las Vegas Raiders',
         'sdg': 'Los Angeles Chargers',
         'dal': 'Dallas Cowboys',
         'nyg': 'New York Giants',
         'phi': 'Philadelphia Eagles',
         'was': 'Washington Commanders',
         'chi': 'Chicago Bears',
         'det': 'Detroit Lions',
         'gnb': 'Green Bay Packers',
         'min': 'Minnesota Vikings',
         'atl': 'Atlanta Falcons',
         'car': 'Carolina Panthers',
         'nor': 'New Orleans Saints',
         'tam': 'Tampa Bay Buccaneers',
         'crd': 'Arizona Cardinals',
         'ram': 'Los Angeles Rams',
         'sfo': 'San Francisco 49ers',
         'sea': 'Seattle Seahawks'}

openai.api_key = os.getenv('OPENAI_API_KEY')

#Adds AI generated descriptions to each player that does not already have a description
def ai(database):
#    if request.method == 'POST':
#        for gen_team in teams.items():
#            players = database.query.filter_by(team=gen_team).filter(database.year > 2010)
#            for player in players:
#                name = player.name
#                year = player.year
#                team = teams.get(player.team)
#                output = openai.ChatCompletion.create(
#                    model='gpt-3.5-turbo',
#                    messages=[{'role': 'user',
#                               'content':
#                               'Write a 4 sentence summary about '+name+'s career with the '+team+'. Be certain to include when he joined the team(year), how he j#oined the team(drafted, traded for, or signed as free agent), his stats/accolades from '+year+', and when/how he left the team or if he is still on the team.'}]
#                )
#                content = output.choices[0].message.content
#                player.desc = content
#        db.session.commit()
    print("hello")