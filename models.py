from db import db

class players(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    team = db.Column(db.String(100))
    year = db.Column(db.Integer)
    url = db.Column(db.String(200))
    numG = db.Column(db.Integer)
    numC = db.Column(db.Integer)
    
    
    def __init__(self, name, team, year, url, numG, numC):
        self.name = name
        self.team = team
        self.year = year
        self.url = url
        self.numG = numG
        self.numC = numC