from app import *
from statistics import mean,mode
from bs4 import BeautifulSoup
from datetime import datetime, date
from operator import itemgetter
from unidecode import unidecode
import time
import requests
import ipdb

with app.app_context():

    # at_bat_one = AtBat(
    #                 inning= 1,
    #                 pitches = 5,
    #                 balls = 2,
    #                 strikes = 2,
    #                 result = "nothing",
    #                 strength = "soft",
    #                 location = "right field",
    #                 rbi = 1,
    #                 score = 1,
    #                 sb = 1,
    #                 sb_att = 1,
    #                 team = "Dummy",
    #                 result_stdev = 1
    #                 )

    # db.session.add(at_bat_one)

    # at_bat_two = AtBat(
    #                 inning= 1,
    #                 pitches = 5,
    #                 balls = 2,
    #                 strikes = 2,
    #                 result = "nothing",
    #                 strength = "soft",
    #                 location = "right field",
    #                 rbi = 100,
    #                 score = 100,
    #                 sb = 100,
    #                 sb_att = 100,
    #                 team = "Dummy",
    #                 result_stdev = 100
    #                 )

    # db.session.add(at_bat_two)

    # at_bat_three = AtBat(
    #                 inning= 1,
    #                 pitches = 5,
    #                 balls = 2,
    #                 strikes = 2,
    #                 result = "nothing",
    #                 strength = "soft",
    #                 location = "right field",
    #                 rbi = 1000,
    #                 score = 1000,
    #                 sb = 1000,
    #                 sb_att = 1000,
    #                 team = "Dummy",
    #                 result_stdev = 1000
    #                 )

    # db.session.add(at_bat_three)


    game = Game.query.first()
    hitter = Hitter.query.first()
    pitcher = Pitcher.query.first()

    dummies = [ab for ab in AtBat.query.all() if ab.team=="Dummy"]

    for dummy in dummies:
        dummy.game = game
        dummy.hitter = hitter
        dummy.pitcher = pitcher



    db.session.commit()

    print("Done")
       
