from app import *
from statistics import mean,mode
from bs4 import BeautifulSoup
from datetime import datetime, date
from operator import itemgetter
from unidecode import unidecode
from sqlalchemy import and_
import time
import requests
import ipdb

with app.app_context():


    abs = AtBat.query.all()
    total_left = len(abs)

    for ab in abs:

        ab_total = 0
        if ab.result=="Home Run":
            ab_total+=10
        elif ab.result=="Triple":
            ab_total+=8
        elif ab.result=="Double":
            ab_total+=5
        elif ab.result=="Single":
            ab_total+=3
        elif "Hit" in ab.result or "Walk" in ab.result:
            ab_total+=2

        if ab.sb>=1:
            ab_total+=5*ab.sb
        if ab.sb==0 and ab.sb_att>=1:
            ab_total+=ab.sb_att


        if ab.rbi > 0:
            ab_total+=2*ab.rbi


        if ab.score==1:
            ab_total+=2
            

        if 18 <= ab_total:
            ab.result_stdev = 1
        elif 14 <= ab_total <= 17:
            ab.result_stdev = 0.95
        elif 10 <= ab_total <= 13:
            ab.result_stdev = 0.9
        elif 5 <= ab_total <= 9:
            ab.result_stdev = .78
        elif 3 <= ab_total <= 4:
            ab.result_stdev = .65
        elif ab_total == 2:
            ab.result_stdev = .5
        elif "Line" in ab.result:
            ab.result_stdev = .25
        elif "Strikeout" in ab.result:
            ab.result_stdev = 0
        else:
            ab.result_stdev = .15

        total_left -=1
        if total_left%100==0:
            print(f"{total_left} left")
    db.session.commit()
    print("Done")


    games = Game.query.all()
    games_left = len(games)

    for game in games:
        away_pitcher = [ab for ab in game.at_bats if ab.team==game.home][0].pitcher
        home_pitcher = [ab for ab in game.at_bats if ab.team==game.visitor][0].pitcher

        away_pitcher_abs = [ab for ab in game.at_bats if ab.pitcher==away_pitcher]
        home_pitcher_abs = [ab for ab in game.at_bats if ab.pitcher==home_pitcher]

        away_pitcher_value = 0
        away_pitcher_outs = 0
        away_pitcher_hits = 0
        for ab in away_pitcher_abs:
            if "Out" in ab.result or "out" in ab.result or "Pop" in ab.result or "Choice" in ab.result or "Fly" in ab.result:
                away_pitcher_value+=.75
                away_pitcher_outs+=1
            if "Strikeout" in ab.result:
                away_pitcher_value+=2
            if ab.score==1 and "Error" not in ab.result:
                away_pitcher_value-=2
            if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run":
                away_pitcher_value-=.6
                away_pitcher_hits+=1
            if ab.result=="Hit" or ab.result=="Walk":
                away_pitcher_value-=.6

        if game.away_score > game.home_score and away_pitcher_outs >= 15:
            away_pitcher_value +=4
        if away_pitcher_outs >= 27:
            away_pitcher_value+=2.5
            if away_pitcher_hits==0:
                away_pitcher_value+=5
            if game.home_score==0:
                away_pitcher_value+=2.5


        home_pitcher_value = 0
        home_pitcher_outs = 0
        home_pitcher_hits = 0
        for ab in home_pitcher_abs:
            if "Out" in ab.result or "out" in ab.result or "Pop" in ab.result or "Choice" in ab.result or "Fly" in ab.result:
                home_pitcher_value+=.75
                home_pitcher_outs+=1
            if "Strikeout" in ab.result:
                home_pitcher_value+=2
            if ab.score==1 and "Error" not in ab.result:
                home_pitcher_value-=2
            if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run":
                home_pitcher_value-=.6
                home_pitcher_hits+=1
            if ab.result=="Hit" or ab.result=="Walk":
                home_pitcher_value-=.6

        if game.home_score > game.away_score and home_pitcher_outs >= 15:
            home_pitcher_value +=4
        if home_pitcher_outs >= 27:
            home_pitcher_value+=2.5
            if home_pitcher_hits==0:
                home_pitcher_value+=5
            if game.away_score==0:
                home_pitcher_value+=2.5


    #     ipdb.set_trace()

    #     print("hi")
        
        #redo database. Add this and add winning pitcher value to game table

    

    #need to add stdev for sb, runs, rbi

        #hit should be at least 60%

        #points for things
        #hitter
            #single: 3
            #double: 5
            #triple: 8
            #homerun: 10
            #rbi: 2
            #run: 2
            #hbp/walk: 2
            #sb: 5
        #pitcher
            #out: .75
            #k: 2
            #win: 4
            #earned run: -2
            #hit: -.6
            #walk: -.6
            #complete game: 2.5
            #complete game shutout: 2.5
            #no hitter: 5


        #most possible points for hitter ab: 20
        #most possible points for pitcher game: 74.25

        #immaculate pitching day is 50, that'll be 1. Anything under 0 is 0
            #use a linear relationship between 50 and 0. This will need to be in the algo

        #for hitting, we'll spread them into tiers. This will be saved in the database
            #immaculate at bat is a 18-19 : 1
            #very good at bat is 10-17 : 0.9
            #solid ab is 5-9  : 0.78
            #ok ab is 3-4  : 0.65
            #decent ab is 2 : 0.5
            #give some slack for a hard hit out  : 0.25
            #give some slack for a ball in play  : 0.15
            #bad ab is 0   : 0

            
            


            
        # if "Strikeout" in ab.result:
        #     ab.result_stdev=0
        # elif "Popfly" in ab.result or "Groundout" in ab.result or "Choice" in ab.result or "Error" in ab.result:
        #     ab.result_stdev=.1
        # elif "Flyout" in ab.result:
        #     ab.result_stdev=.2
        # elif "Walk" in ab.result or "Sacrifice" in ab.result or "Interference" in ab.result or "Hit" in ab.result:
        #     ab.result_stdev=.5
        # elif "Lineout" in ab.result:
        #     ab.result_stdev=.4
        # elif "Home" in ab.result:
        #     ab.result_stdev=1
        # elif "Triple" in ab.result or "Double" in ab.result:
        #     ab.result_stdev=.95
        # else:
        #     ab.result_stdev=.9

         
       
