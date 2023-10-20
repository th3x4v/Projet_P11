import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]

        # # Checking if competition is past or not, then render template
        # _competitions = update_competition_dict_with_past_bool(competitions)
        return render_template("welcome.html", club=club, competitions=competitions)

    except IndexError:
        flash("Please enter a valid email")
        return redirect(url_for("index"))


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
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
    if placesRequired > MAXPLACES:
        flash("You cannot book more than 12 places for a competition")
        return render_template("welcome.html", club=club, competitions=competitions)
    elif placesRequired > club_points:
        flash(
            f"You don't have enough points ({club_points}) to reedem {placesRequired} places"
        )
        return render_template("welcome.html", club=club, competitions=competitions)
    else:
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )
        club["points"] = int(club["points"]) - (placesRequired)
        flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
