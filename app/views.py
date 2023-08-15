import os
import requests
from app.models import player_database, AdminUser, MyModelView, MyAdminIndexView, ScrapeView, AiView, ReportView
from flask import Flask, redirect, url_for, render_template, request, session
from app.gen import gen_blueprint
from app.db import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_admin import Admin, AdminIndexView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from flask_admin.contrib.sqla import ModelView
from datetime import timedelta
from app import app

#Home page
@app.route('/', methods=['POST', 'GET'] )
def home():
    return render_template('index.html')

#Login page
@app.route('/login', methods={'POST', 'GET'})
def login():
    if request.method == 'POST':
        print('hello')
        admin = AdminUser.query.get(1)
        username = request.form['username']
        password = request.form['password']
        question = request.form['question']
        if username == admin.username and password == admin.password and question == admin.question:
            session.permanent = True
            session['admin'] = 'true'
            return redirect(url_for('home'))
    return render_template('/login.html')

#Logout page
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return 'Logged Out'
    