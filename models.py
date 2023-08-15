from db import db
from flask_login import UserMixin, LoginManager, current_user
from flask_admin.contrib.sqla import ModelView
from flask import Flask, redirect, url_for, request, session
from flask_admin import Admin, AdminIndexView, BaseView, expose
from scrape import scrape
from ai import ai
from report import report, fix, get_player

#Database that stores the players
class player_database(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
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

#Database that stores the admin information
class AdminUser(db.Model, UserMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    question = db.Column((db.String(20)))

#View that displays all players
class MyModelView(ModelView):
    def is_accessible(self):
        if 'admin' in session:
            return True
        return False
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
#View that displays admin information  
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if 'admin' in session:
            return True
        return False

#View used for scraping new players
class ScrapeView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        scrape(player_database)
        return self.render('admin/scrape.html')
    
    def is_accessible(self):
        if 'admin' in session:
            return True
        return False

#View used for generating new descriptions
class AiView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        ai(player_database)
        return self.render('admin/ai.html')
    
    def is_accessible(self):
        if 'admin' in session:
            return True
        return False
    
#View used for fixing reported players
class ReportView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):            
        if request.method == 'POST':
            if request.form['submit'] == 'Fix Image':
                data = get_player(player_database)
                return self.render('admin/fix.html', values=[data[0], data[1]])
            elif request.form['submit'] == 'Pick this image':
                fix(player_database)
            elif request.form['submit'] == 'Clear Reports':
                report(player_database)
        return self.render('admin/report.html', values=player_database.query.order_by(player_database.numR.desc(), player_database._id).all())
    
    def is_accessible(self):
        if 'admin' in session:
            return True
        return False

    
    
