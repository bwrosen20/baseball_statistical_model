#!/usr/bin/env python3
from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Game, Pitcher, Hitter, AtBat

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Baseball Algorithm API"


@app.route('/games')
def games():

    games = []
    for game in Game.query.all():
        game_dict = {
            "home": game.home,
            "visitor": game.visitor,
            "date": game.date,
            "home_score":game.home_score,
            "visitor_score":game.away_score,
            "location":game.location,
            "temperature":game.temperature,
            "wind_direction":game.wind_direction,
            "wind_speed":game.wind_speed,
            "precipitation":game.precipitation,
            "cloud_or_sun":game.cloud_or_sun
        }
        games.append(game_dict)

    response = make_response(
        jsonify(games),
        200

    #      id = db.Column(db.Integer, primary_key=True)
    # visitor = db.Column(db.String)
    # home = db.Column(db.String)
    # location = db.Column(db.String)
    # temperature = db.Column(db.Integer)
    # wind_direction = db.Column(db.Integer)
    # wind_speed = db.Column(db.Integer)
    # precipitation = db.Column(db.String)
    # cloud_or_sun = db.Column(db.String)
    # home_score = db.Column(db.Integer)
    # away_score = db.Column(db.Integer)
    # date = db.Column(db.DateTime)
    # home_pitcher_result = db.Column(db.Integer)
    # away_pitcher_result = db.Column(db.Integer)
    # created_at = db.Column(db.DateTime, server_default=db.func.now())
    # updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    )

    return response

@app.route('/pitchers')
def pitchers():

    pitchers = []
    for pitcher in Pitcher.query.all():
        pitcher_dict = {
            "name": pitcher.name,
            "arm": pitcher.arm
        }
        pitchers.append(pitcher_dict)

    response = make_response(
        jsonify(pitchers),
        200
    )

    return response



if __name__ == '__main__':
    app.run(port=5555, debug=True)

#pip install -r requirements.txt