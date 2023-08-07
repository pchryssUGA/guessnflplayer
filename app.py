from flask import Flask, redirect, url_for, render_template, request, session
from gen import gen_blueprint
from report import report_blueprint
from db import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
from models import player_database, AdminUser, MyModelView, MyAdminIndexView, ScrapeView, AiView, ReportView
from flask_migrate import Migrate
import os
import requests
from dotenv import load_dotenv
from flask_admin import Admin, AdminIndexView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from flask_admin.contrib.sqla import ModelView
from datetime import timedelta


load_dotenv()
app = Flask("__main__")
app.register_blueprint(gen_blueprint, url_prefix="/gen")
app.permanent_session_lifetime = timedelta(minutes=1)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
db.init_app(app) # to add the app inside SQLAlchemy()
migrate = Migrate(app, db)

teams = {"nyj": "New York Jets"}


@app.route("/", methods=["POST", "GET"] )
def home():
    return render_template("index.html")
    

login = LoginManager(app)
@login.user_loader

def load_user(user_id):
    return AdminUser.query.get(user_id)

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(AdminUser, db.session))
admin.add_view(MyModelView(player_database, db.session))
admin.add_view(ScrapeView(name="Scrape", endpoint="scrape"))
admin.add_view(AiView(name="AI", endpoint="ai"))
admin.add_view(ReportView(name="Report", endpoint="report"))

@app.route("/login", methods={"POST", "GET"})
def login():
    if request.method == "POST":
        print("hello")
        admin = AdminUser.query.get(1)
        username = request.form["username"]
        password = request.form["password"]
        question = request.form["question"]
        if username == admin.username and password == admin.password and question == admin.question:
            session.permanent = True
            session["admin"] = "true"
            return "Logged in :)"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return "Logged Out"

    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)