from flask import Flask, redirect, url_for, render_template, request, session
from scrape import scrape_blueprint
from gen import gen_blueprint
from report import report_blueprint
from db import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
from models import player_database
from flask_migrate import Migrate
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask("__main__")
app.register_blueprint(scrape_blueprint, url_prefix="/scrape")
app.register_blueprint(gen_blueprint, url_prefix="/gen")
app.register_blueprint(report_blueprint, url_prefix="/report")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app) # to add the app inside SQLAlchemy()
migrate = Migrate(app, db)

teams = {"nyj": "New York Jets"}


@app.route("/", methods=["POST", "GET"] )
def home():
    return render_template("index.html")
    
@app.route("/ai", methods=["POST", "GET"])
def ai():
    if request.method == "POST":
        players = player_database.query.filter_by(team="nyj").filter(player_database.year > 2010)
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
        return render_template("ai.html")
    return render_template("ai.html")

@app.route("/view", methods=["POST", "GET"])
def view():
    if request.method == "POST":
        db.session.query(player_database).delete()
        db.session.commit()
        return render_template("view.html", values=player_database.query.all())
    return render_template("view.html", values=player_database.query.all())

    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)