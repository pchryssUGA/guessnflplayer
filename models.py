from db import db
from flask_login import UserMixin, LoginManager, current_user
from flask_admin.contrib.sqla import ModelView
from flask import Flask, redirect, url_for, request, session
from flask_admin import Admin, AdminIndexView, BaseView, expose
from scrape import scrape
from ai import ai
from report import report, fix, get_player

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
    
class AdminUser(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    question = db.Column((db.String(20)))

class MyModelView(ModelView):
    def is_accessible(self):
        if "admin" in session:
            return True
        return False
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))
    
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if "admin" in session:
            return True
        return False
    
class ScrapeView(BaseView):
    @expose("/", methods=("GET", "POST"))
    def index(self):
        scrape(player_database)
        return self.render("admin/scrape.html")
    
    def is_accessible(self):
        if "admin" in session:
            return True
        return False
    
class AiView(BaseView):
    @expose("/", methods=("GET", "POST"))
    def index(self):
        ai(player_database)
        return self.render("admin/ai.html")
    
    def is_accessible(self):
        if "admin" in session:
            return True
        return False
    
class ReportView(BaseView):
    @expose("/", methods=("GET", "POST"))
    def index(self):            
        report(player_database)
        return self.render("admin/report.html", values=player_database.query.order_by(player_database.numR.desc(), player_database._id).all())
    
    def is_accessible(self):
        if "admin" in session:
            return True
        return False
    
