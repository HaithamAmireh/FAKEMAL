import json
from datetime import date, datetime
from random import randint

import requests
from flask import Flask, render_template, request

Y = 2000  # dummy leap year to allow input X-02-29 (leap day)
seasons = [
    ("winter", (date(Y, 1, 1), date(Y, 3, 20))),
    ("spring", (date(Y, 3, 21), date(Y, 6, 20))),
    ("summer", (date(Y, 6, 21), date(Y, 9, 22))),
    ("autumn", (date(Y, 9, 23), date(Y, 12, 20))),
    ("winter", (date(Y, 12, 21), date(Y, 12, 31))),
]


def get_season(now):
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons if start <= now <= end)


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    anime = "*"
    if request.method == "POST":
        anime = request.form.get("anime")
    api = "https://api.jikan.moe/v4/anime?q=" + anime + "&sfw"
    res = requests.get(api)
    data = json.loads(res.text)
    return render_template("home.html", anime=data["data"], title="FAKEMAL:Home")


@app.route("/seasonal", methods=["GET", "POST"])
def seasonal():
    year = str(datetime.now().year)
    season = get_season(date.today())
    if request.method == "POST":
        year = request.form.get("year")
        season = request.form.get("season")
    api = "https://api.jikan.moe/v4/seasons/" + year + "/" + season
    # TODO: Add page handling
    res = requests.get(api)
    data = json.loads(res.text)
    pages = data["pagination"]["last_visible_page"]
    print(pages)
    return render_template(
        "seasonal.html", animes=data["data"], year=year, season=season, title="FAKEMAL:Seasonal"
    )


@app.route("/random")
def random_anime():
    api = "https://api.jikan.moe/v4/anime/" + str(randint(1, 10000))
    res = requests.get(api)
    while res.status_code != 200:
        api = "https://api.jikan.moe/v4/anime/" + str(randint(1, 10000))
        res = requests.get(api)
    data = json.loads(res.text)
    return render_template("random.html", anime=data["data"], title="Random anime")
