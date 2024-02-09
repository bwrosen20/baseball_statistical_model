from app import *
from statistics import mean,mode
from bs4 import BeautifulSoup
from datetime import datetime, date
from operator import itemgetter
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
                    arm = player.select('span')[1].text[-1]
                    print(f"{name}: Arm- {arm}")
                else: 
                    #he's a hitter. Get bat handedness
                    bat = player.select('span')[1].text[-3]
                    print(f'{name}: Bat- {bat}')

            pitcher_counter+=1
            print(f"Pitch counter has been raised to {pitcher_counter}")

        time.sleep(3.2)

       
