import json
from datetime import date, datetime
from multiprocessing import Value

import numpy as np
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


counter = Value("i", 1)

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
    api = "https://api.jikan.moe/v4/seasons/now"
    year = str(datetime.now().year)
    season = get_season(date.today())
    if request.method == "POST":
        year = request.form.get("year")
        season = request.form.get("season")
        api = "https://api.jikan.moe/v4/seasons/" + year + "/" + season
    res = requests.get(api)
    data = json.loads(res.text)
    pages = data["pagination"]["last_visible_page"]
    full_data = data["data"]
    while pages > 1:
        api = "https://api.jikan.moe/v4/seasons/" + year + "/" + season + "?page=" + str(pages)
        res = requests.get(api)
        data = json.loads(res.text)
        full_data = np.append(full_data, data["data"])
        pages -= 1
    print(len(full_data))
    return render_template(
        "seasonal.html", animes=full_data, year=year, season=season, title="FAKEMAL:Seasonal"
    )


@app.route("/random", methods=["GET", "POST"])
def random_anime():
    api = "https://api.jikan.moe/v4/random/anime"
    res = requests.get(api)
    while res.status_code != 200:
        api = "https://api.jikan.moe/v4/random/anime"
        res = requests.get(api)
    data = json.loads(res.text)
    return render_template("random.html", anime=data["data"], title="FAKEMAL:Random")


@app.route("/top_manga", methods=["GET", "POST"])
def top_manga():
    api = "https://api.jikan.moe/v4/top/manga"
    res = requests.get(api)
    data = json.loads(res.text)
    if request.method == "POST":
        with counter.get_lock():
            counter.value += 1
            next_page = counter.value
        api = "https://api.jikan.moe/v4/top/manga" + "?page=" + str(next_page)
        res = requests.get(api)
        data = json.loads(res.text)
        return render_template(
            "top_manga.html",
            manga=data["data"],
            title="FAKEMAL:Top Manga",
            current_page_number=counter.value,
            next_page_number=next_page,
        )
    return render_template(
        "top_manga.html", manga=data["data"], title="FAKEMAL:Top Manga", current_page_number=1
    )


@app.route("/top_anime", methods=["GET", "POST"])
def top_anime():
    api = "https://api.jikan.moe/v4/top/anime"
    res = requests.get(api)
    data = json.loads(res.text)
    if request.method == "POST":
        with counter.get_lock():
            counter.value += 1
            next_page = counter.value
        api = "https://api.jikan.moe/v4/top/anime" + "?page=" + str(next_page)
        res = requests.get(api)
        data = json.loads(res.text)
    return render_template("top_anime.html", anime=data["data"], title="FAKEMAL:Top Anime")
