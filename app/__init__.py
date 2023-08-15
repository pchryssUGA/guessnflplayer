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

load_dotenv()
app = Flask('__main__', static_folder='app/static', template_folder='app/templates')
app.register_blueprint(gen_blueprint, url_prefix='/gen')
app.permanent_session_lifetime = timedelta(hours=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db.init_app(app) 
migrate = Migrate(app, db)
login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return AdminUser.query.get(user_id)

#Creates admin views
admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(AdminUser, db.session))
admin.add_view(MyModelView(player_database, db.session))
admin.add_view(ScrapeView(name='Scrape', endpoint='scrape'))
admin.add_view(AiView(name='AI', endpoint='ai'))
admin.add_view(ReportView(name='Report', endpoint='report'))

from app import views