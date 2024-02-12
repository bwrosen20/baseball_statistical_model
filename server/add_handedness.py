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

    teams = ["bluejays","orioles","rays","redsox","yankees",
                "guardians","royals","tigers","twins","whitesox",
                "angels","astros","athletics","mariners","rangers",
                "braves","marlins","mets","nationals","phillies",
                "brewers","cardinals","cubs","pirates","reds",
                "dbacks","dodgers","giants","padres","rockies"]

    for team in teams:

        site_url = f"https://www.mlb.com/{team}/roster/depth-chart"

        depth_page = requests.get(site_url, headers = {'User-Agent':"Mozilla/5.0"})
        depth_chart = BeautifulSoup(depth_page.text, 'html.parser')

        pitcher_counter = 0

        position_groups = depth_chart.select('div.players')[0].select('table.roster__table')


        for position in position_groups:
            players = position.select('tbody')[0].select('tr')

            for player in players:

                name = unidecode(player.select('a')[0].text)

                if pitcher_counter < 2:
                    #he's a pitcher. Get his arm handedness
                    pitcher_object = Pitcher.query.filter(Pitcher.name==name).first()
                    if pitcher_object:
                        if pitcher_object.arm != "R" and pitcher_object.arm != "L" and pitcher_object.arm != "S":
                            arm = player.select('span')[1].text[-1]
                            pitcher_object.arm=arm
                            db.session.commit()
                            print(f"{name}: Arm- {arm}")
                else: 
                    #he's a hitter. Get bat handedness
                    hitter_object = Hitter.query.filter(Hitter.name==name).first()
                    if hitter_object:
                        if hitter_object.bat != "R" and hitter_object.bat != "L" and hitter_object.bat != "S":
                            bat = player.select('span')[1].text[-3]
                            hitter_object.bat = bat
                            db.session.commit()
                            print(f'{name}: Bat- {bat}')

            pitcher_counter+=1

        time.sleep(3.2)

       
