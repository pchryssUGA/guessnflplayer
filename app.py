import os
import requests
from models import player_database, admin_user, MyModelView, MyAdminIndexView, ScrapeView, AiView, ReportView
from flask import Flask, redirect, url_for, render_template, request, session
from gen import gen_blueprint
from db import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_admin import Admin, AdminIndexView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from flask_admin.contrib.sqla import ModelView
from datetime import timedelta


project_folder = os.path.expanduser('/home/pchryss/RandomPlayer')
load_dotenv(os.path.join(project_folder, '.env'))
AWS_API_WEBSITE=os.getenv('AWS_API_WEBSITE')

#Initilize app settings
app = Flask('__main__', static_folder='/home/pchryss/RandomPlayer/static', template_folder='/home/pchryss/RandomPlayer/templates')
app.register_blueprint(gen_blueprint, url_prefix='/gen')
app.permanent_session_lifetime = timedelta(hours=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pchryss/RandomPlayer/instance/posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = os.getenv('SECRET_KEY')
app.secret_key = "a"
db.init_app(app) 
migrate = Migrate(app, db)
login = LoginManager(app)

#Function that logs a user in
@login.user_loader
def load_user(user_id):
    return admin_user.query.get(user_id)

#Creates views for admin panel
admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(admin_user, db.session))
admin.add_view(MyModelView(player_database, db.session))
admin.add_view(ScrapeView(name='Scrape', endpoint='scrape'))
admin.add_view(AiView(name='AI', endpoint='ai'))
admin.add_view(ReportView(name='Report', endpoint='report'))



#Home page
@app.route('/', methods=['POST', 'GET'] )
def home():
    return render_template('index.html')

#Login page
@app.route('/login', methods={'POST', 'GET'})
def login():
    if request.method == 'POST':
        admin = admin_user.query.get(1)
        username = request.form['username']
        password = request.form['password']
        question = request.form['question']
        if username == admin.username and password == admin.password and question == admin.question:
            session.permanent = True
            session['admin'] = 'true'
            return redirect(url_for('home'))
    return render_template('login.html')

#Logout page
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return 'Logged Out'

#Report Bug page
@app.route('/bug', methods={'POST', 'GET'})
def bug():
    if request.method == 'POST':
        subject = request.form['subject']
        message = request.form['message']
        response = requests.get(AWS_API_WEBSITE + 'subject=' + subject + '&message=' + message)
    return render_template('bug.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
