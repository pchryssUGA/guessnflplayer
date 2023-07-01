from flask import Flask, Blueprint, render_template, request, redirect, url_for

scrape_blueprint = Blueprint("scrape", __name__, static_folder="static", template_folder="templates")

@scrape_blueprint.route("/", methods=["POST", "GET"])
def scrape():
    if request.method == "POST":
        team = request.form["tm"]
        startDate = request.form["sd"]
        endDate = request.form["ed"]
        run(team, startDate, endDate)
    return render_template("scrape.html")

def run(tm, sd, ed):
    print("Team: "+tm)
    print("Start Date: "+sd)
    print("End Date: "+ed)
    

