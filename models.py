from db import db
from flask_login import UserMixin, LoginManager, current_user
from flask_admin.contrib.sqla import ModelView
from flask import Flask, redirect, url_for, request, session
from flask_admin import Admin, AdminIndexView, BaseView, expose
from scrape import scrape
from ai import ai
from report import reset_reports, reset_numC, reset_numG, fix, get_player

#Database representing an NFL player.
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

#Database that represents an admin user
class admin_user(db.Model, UserMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    question = db.Column((db.String(20)))

    def __init__(self, username, password, question):
        self.username = username
        self.password = password
        self.question = question

#This view displays all players
class MyModelView(ModelView):
    def is_accessible(self):
        if 'admin' in session:
            return True
        return False
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    
#This view displays admin info
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if 'admin' in session:
            return True
        return False

#This view is used for scraping new players to the database
class ScrapeView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        scrape(player_database)
        return self.render('admin/scrape.html')
    
    def is_accessible(self):
        if 'admin' in session:
            return True
        return False

#This view is used for generating descriptions for players
class AiView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        ai(player_database)
        return self.render('admin/ai.html')
    
    def is_accessible(self):
        if 'admin' in session:
            return True
        return False
    
#This view is used for fixing a reported players image
class ReportView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):            
        if request.method == 'POST':
            if request.form['submit'] == 'Fix Image':
                data = get_player(player_database, False)
                return self.render('admin/fix.html', values=[data[0], data[1]])
            elif request.form['submit'] == 'Better images':
                data = get_player(player_database, True)
                return self.render('admin/fix.html', values=[data[0], data[1]])
            elif request.form['submit'] == 'Pick this image':
                fix(player_database)
            elif request.form['submit'] == 'Clear Reports':
                reset_reports(player_database)
            elif request.form['submit'] == 'Clear numC':
                reset_numC(player_database)
            elif request.form['submit'] == 'Clear numG':
                reset_numG(player_database)
        return self.render('admin/report.html', values=player_database.query.order_by(player_database.numR.desc(), player_database._id).all())
    
    def is_accessible(self):
        if 'admin' in session:
            return True
        return False

    
    
