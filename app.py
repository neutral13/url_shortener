from flask import Flask, redirect, render_template, request, url_for  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
import string
import random


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Urls(db.Model):  # type: ignore
    id = db.Column("id", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(6))

    def __init__(self, long, short):
        self.long = long
        self.short = short


with app.app_context():
    db.create_all()


def shorten_url():
    letters = string.ascii_lowercase = string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=6)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters


@app.route("/", methods=["POST", "GET"])
def homepage():
    if request.method == "POST":
        url_received = request.form["nm"]
        found_url = Urls.query.filter_by(long=url_received).first()
        if found_url:
            return redirect(url_for("display_short_url", url=found_url.short))
        else:
            short_url = shorten_url()
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))
    else:
        return render_template("homepage.html")


@app.route("/display/<url>")
def display_short_url(url):
    return render_template("shorturl.html", short_url_display=url)


@app.route("/<short_url>")
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return "<h1>Url dosen't exist</h1>"


if __name__ == "__main__":
    app.run(port=8000, debug=True)
