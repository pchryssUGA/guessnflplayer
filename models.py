from db import db

class player_database(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    team = db.Column(db.String(100))
    year = db.Column(db.Integer)
    url = db.Column(db.String(200))
    desc = db.Column(db.Text)
    numG = db.Column(db.Integer)
    numC = db.Column(db.Integer)
    numR = db.Column(db.Integer)
    
    
    def __init__(self, name, team, year, url, desc, numG, numC, numR):
        self.name = name
        self.team = team
        self.year = year
        self.url = url
        self.desc = desc
        self.numG = numG
        self.numC = numC
        self.numR = numR
    