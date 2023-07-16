from flask import Flask, Blueprint, render_template, request, redirect, url_for
from db import db
from flask_sqlalchemy import SQLAlchemy
from models import player_database

report_blueprint = Blueprint("report", __name__, static_folder="static", template_folder="templates_report")

@report_blueprint.route("/", methods=["POST", "GET"])
def report():
    if request.method == "POST":
        for player in player_database.query.all():
            player.numR = 0
        return render_template("report.html", values=player_database.query.order_by(player_database.numR.desc(), player_database._id).all())
    return render_template("report.html", values=player_database.query.order_by(player_database.numR.desc(), player_database._id).all())

@report_blueprint.route("/fix", methods=["POST", "GET"])
def fix():
    return render_template("fix.html")