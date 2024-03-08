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

    abs = AtBat.query.all()
    total_left = len(abs)

    for ab in abs:

        if "Strikeout" in ab.result:
            ab.result_stdev=0
        elif "Popfly" in ab.result or "Groundout" in ab.result or "Choice" in ab.result or "Error" in ab.result:
            ab.result_stdev=.15
        elif "Flyout" in ab.result:
            ab.result_stdev=.35
        elif "Walk" in ab.result or "Sacrifice" in ab.result or "Interference" in ab.result or "Hit" in ab.result:
            ab.result_stdev=.5
        elif "Lineout" in ab.result:
            ab.result_stdev=.75
        else:
            ab.result_stdev=1
        total_left -=1
        if total_left%100==0:
            print(f"{total_left} left")
    db.session.commit()
    print("Done")
   

       
