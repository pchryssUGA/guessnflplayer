import openai
import os
from db import db
from flask import request

teams = {"nyj": "New York Jets"}
openai.api_key = os.getenv("OPENAI_API_KEY")

#Adds AI generated descriptions to each player that does not already have a description
def ai(database):
    if request.method == "POST":
        players = database.query.filter_by(team="nyj").filter(database.year > 2010).filter(desc="")
        for player in players:
            name = player.name
            team = teams.get(player.team)
            output = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user",
                "content":
                        "Write a 5 sentence summary about "+name+"s career with the "+team+". Be certain to include when he joined the team(year), how he joined the team(drafted, traded for, or signed as free agent), how he left the team (year), and how he left the team (traded, cut, or retired) or if he still on the team. "}]
            )
            content = output.choices[0].message.content
            player.desc = content
        db.session.commit()