import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def is_competition_available(competition):
    now = datetime.now()
    comp_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    if comp_date < now:
        competition["available"] = False
    else:
        competition["available"] = True
    return competition


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        # Checking if competition is past or not
        _listOfCompetitions = [is_competition_available(c) for c in listOfCompetitions]
        return _listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST", "GET"])
def showSummary():
    if request.method == "POST":
        try:
            club = [c for c in clubs if c["email"] == request.form["email"]][0]
            return render_template("welcome.html", club=club, competitions=competitions)

        except IndexError:
            flash("Please enter a valid email")
            return redirect(url_for("index"))

    if request.method == "GET":
        # Retrieve the club data
        club_name = request.args.get("club")
        club = [c for c in clubs if c["name"] == club_name][0]
        if club is not None:
            return render_template("welcome.html", club=club, competitions=competitions)
        else:
            return redirect(url_for("index"))


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundCompetition["available"] is False:
        flash("This competition is not available")
        return render_template("welcome.html", club=club, competitions=competitions)
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    MAXPLACES = 12
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    club_points = int(club["points"])
    placesRequired = int(request.form["places"])
    placesAvailble = int(competition["numberOfPlaces"])
    if competition["available"] is False:
        flash("This competition is not available")
        return render_template("welcome.html", club=club, competitions=competitions)
    if placesRequired > MAXPLACES:
        flash("You cannot book more than 12 places for a competition")
        return render_template("welcome.html", club=club, competitions=competitions)
    elif placesRequired > club_points:
        flash(
            f"You don't have enough points ({club_points}) to reedem {placesRequired} places"
        )
        return render_template("welcome.html", club=club, competitions=competitions)
    elif placesRequired > placesAvailble:
        flash(
            f"You are trying to reedem  places ({placesRequired}) than available ({placesAvailble}"
        )
        return render_template("welcome.html", club=club, competitions=competitions)
    else:
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )
        # Competition no more available if place available = 0
        if int(competition["numberOfPlaces"]) < 1:
            competition["available"] = False
        club["points"] = int(club["points"]) - (placesRequired)
        flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/board")
def board():
    current_club_name = request.args.get("club")
    return render_template("board.html", club_name=current_club_name, clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
