from turtle import ht
from datetime import datetime
from bs4 import BeautifulSoup, Comment
from app import app
from urllib.request import Request, urlopen
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, Game, Pitcher, Hitter, AtBat
from unidecode import unidecode
import time
import requests
import ipdb





with app.app_context():
    
    years = ["2021,2022,2023"]

    for year in years:

        
        # headers = {'user-agent': 'my-app/0.0.1'}
        html = requests.get(f"https://www.baseball-reference.com/leagues/majors/{year}-schedule.shtml", headers={'User-Agent':"Mozilla/5.0"})
        # date = html.select('div.ScheduleDay_sd_GFE_w')[0]


        doc = BeautifulSoup(html.text, 'html.parser')
        rows = doc.select('p.game')

        for game in rows:

            home = game.select('a')[1].text
            away = game.select('a')[0].text

            
            url_ending = game.select('a')[2].get("href")

            box_score_url = f"https://www.baseball-reference.com/{url_ending}"

            box_score = requests.get(box_score_url)

            box_score_data = BeautifulSoup(box_score.text, 'lxml')
            play_by_play = box_score_data.select('#all_play_by_play')[0]

            comment = play_by_play.find(string=lambda string:isinstance(string, Comment))
            commentsoup = BeautifulSoup(comment , 'lxml')
            tops = commentsoup.select('tr.top_inning')
            bottoms= commentsoup.select('tr.bottom_inning')
            tops.extend(bottoms)

            date = box_score_data.select('.scorebox_meta')[0].select('div')[0].text
            the_time = box_score_data.select('.scorebox_meta')[0].select('div')[1].text

            the_time_list = the_time.split(' ')
            total_date = date+" "+the_time_list[2]+" "+'PM' if the_time_list[3][0]=='p' else 'AM'
            the_time_string = datetime.strptime(total_date,"%A, %B %d, %Y %I:%M %p")

            if the_time_string > datetime(2021,4,30,22,00):
                break

            


            location = (box_score_data.select('.scorebox_meta')[0].select('div')[3].text)[7:]
            try:
                truth = int(location[-2:])
                if truth > 0:
                    location = (box_score_data.select('.scorebox_meta')[0].select('div')[2].text)[7:]
            except (ValueError,TypeError):
                pass

            type_of_field = box_score_data.select('.scorebox_meta')[0].select('div')[5].text

            away_score = box_score_data.select('.scores')[0].select('div')[0].text
            home_score = box_score_data.select('.scores')[1].select('div')[0].text

            weather_data = box_score_data.select('div.section_wrapper')[2]

            weather_comment = weather_data.find(string=lambda string:isinstance(string, Comment))
            weathersoup = BeautifulSoup(weather_comment , 'lxml')
            
            weather_info = weathersoup.select('div.section_content')[0]

            try:
                weather = weather_info.select('div')[4].text
            except IndexError:
                weather = weather_info.select('div')[3].text

            temperature = weather.split(',')[0].split(':')[1][1:3]
            wind = weather.split(',')[1][6:]
            wind_speed = wind.split(' ')[0].split('m')[0]

            if "out to Centerfield" in wind:
                wind_value = 180
            elif "Left to Right" in wind:
                wind_value = 270
            elif "out to Rightfield" in wind:
                wind_value = 225
            elif "in from Rightfield" in wind:
                wind_value = 22.5
            elif "out to Leftfield" in wind:
                wind_value = 135
            elif "Right to Left" in wind:
                wind_value = 90
            elif "in from Leftfield" in wind:
                wind_value = 315
            elif "in from Centerfield" in wind:
                wind_value = 0
            else:
                wind_value = 400



            if len(weather.split(',')) > 3:
                precipitation = weather.replace('.','').split(',')[3][1:]
            else: 
                precipitation = "In Dome"
            cloud_or_sun = weather.replace('.','').split(',')[2][1:]

            match = Game(
                visitor= away,
                home= home,
                location= location,
                temperature = temperature,
                wind_direction = wind_value,
                wind_speed = wind_speed,
                precipitation = precipitation,
                cloud_or_sun = cloud_or_sun,
                home_score= home_score,
                away_score= away_score,
                date= the_time_string
            )
            
            db.session.add(match)
            db.session.commit()

            for index, player in enumerate(tops):

                result = player.select('td')[10].text
                seperated_results = result.replace('-',' ').replace('/',' ').replace(';',' ').replace(':',' ').split(' ')
                sb=0
                sb_att = 0
                rbi = 0
                if "Wild Pitch" in result or "Steals" in result or "Caught" in result or "Passed" in result or "Picked" in result or "Defensive" in result:
                    #we're gonna find the person who stole or scored on a wp 
                    if "Steals" in result:
                        for index, word in enumerate(seperated_results):
                            if word=="Steals":
                                stole = seperated_results[index-1]
                                person_who_stole_list = [stealer for stealer in AtBat.query.order_by(AtBat.id.desc()).limit(9).all() if stole in stealer.hitter.name]
                                if len(person_who_stole_list) > 0:
                                    person_who_stole = person_who_stole_list[0]
                                    person_who_stole.sb = person_who_stole.sb+1
                                    person_who_stole.sb_att = person_who_stole.sb_att+1
                                    db.session.commit()
                                    # break
                    elif "Caught" in result:
                        for index, word in enumerate(seperated_results):
                            if word=="Caught":
                                stole = seperated_results[index-1]
                                person_who_stole_list = [stealer for stealer in AtBat.query.order_by(AtBat.id.desc()).limit(9).all() if stole in stealer.hitter.name]
                                if len(person_who_stole_list) > 0:
                                    person_who_stole = person_who_stole_list[0]
                                    person_who_stole.sb_att = person_who_stole.sb_att+1
                                    db.session.commit()
                                    # break
                    elif "Picked" in result or "Defensive" in result:
                        pass
                    else:
                        if "R" in player.select('td')[4].text:
                            for index, word in enumerate(seperated_results):
                                if word=="Scores":
                                    scored = seperated_results[index-1]
                                    person_who_scored_list = [scorer for scorer in AtBat.query.order_by(AtBat.id.desc()).limit(9).all() if scored in scorer.hitter.name]
                                    if len(person_who_scored_list) > 0:
                                        person_who_scored = person_who_scored_list[0]
                                        person_who_scored.score = True
                                        db.session.commit()
                                    
                               

                else:
                
                    #Find associations in Player and Hitter data sets

                    hitter = unidecode(player.select('td')[6].text.replace('\xa0',' '))
                    pitcher = unidecode(player.select('td')[7].text.replace('\xa0',' '))
                    if (pitcher in [person.name for person in Pitcher.query.all()]):
                        assoc_pitcher = Pitcher.query.filter(Pitcher.name == pitcher).first()
                    else:
                        assoc_pitcher = Pitcher(name=pitcher)
                        db.session.add(assoc_pitcher)
                        db.session.commit()

                    if (hitter in [person.name for person in Hitter.query.all()]):
                        assoc_hitter = Hitter.query.filter(Hitter.name == hitter).first()
                    else:
                        assoc_hitter = Hitter(name=hitter)
                        db.session.add(assoc_hitter)
                        db.session.commit()

                    score = 0

                    if "Strikeout" in result:
                        play = result.replace(';','').split(' ')
                        play = play[0]+(' ')+play[1]
                    elif "Groundout" in result:
                        play = "Groundout"
                    elif "Reached on" in result:
                        if "Interference" in result:
                            play = "Catcher Interference"
                        else:
                            play = "Error"
                    elif "Home Run" in result:
                        play = "Home Run"
                        score = 1
                        rbi+=1
                    elif "Double" in result:
                        play = "Double"
                    elif "Popfly" in result:
                        play = "Popfly"
                    elif "Lineout" in result:
                        play = "Lineout"
                    elif "Choice" in result:
                        play = "Fielder Choice"
                    elif "Walk" in result:
                        play = "Walk"
                    else:
                        play = seperated_results[0]

                    if "Weak" in result:
                        strength = "Weak"
                    elif "Line" in result or "Deep" in result:
                        strength = "Strong"
                    else:
                        strength = "None"

                    #check location of contact. Defaults to "None"

                    position_list = ['P','C','1B','2B','3B','SS','LF','CF','RF']
                    location = "None"

                    for possible_position in seperated_results:
                        if possible_position in position_list:
                            location = possible_position
                            # break


                    #check RBI's. Download score onto previous at bats

                    if "R" in player.select('td')[4].text:
                        for index, word in enumerate(seperated_results):
                            if word=="Scores":
                                scored = seperated_results[index-1]
                                person_who_scored_list = [scorer for scorer in AtBat.query.order_by(AtBat.id.desc()).limit(9).all() if scored in scorer.hitter.name]
                                if len(person_who_scored_list) > 0:
                                    person_who_scored = person_who_scored_list[0]
                                    person_who_scored.score = True
                                    db.session.commit()
                                rbi+=1
                               


                
                    inning = player.select('th')[0].text[1:]
                    if player.select('th')[0].text[0] == "t":
                        team = away
                    else:
                        team = home
                    pitches = player.select('td')[3].text.split(',')[0]
                    balls = player.select('td')[3].text.split(',')[1][1]
                    strikes = player.select('td')[3].text.split(',')[1][3]


                    at_bat = AtBat(
                        inning= inning,
                        pitches = pitches,
                        balls = balls,
                        strikes = strikes,
                        result = play,
                        strength = strength,
                        location = location,
                        rbi = rbi,
                        score = score,
                        sb = sb,
                        sb_att = sb_att,
                        team = team
                    )

                    at_bat.pitcher = assoc_pitcher
                    at_bat.hitter = assoc_hitter
                    at_bat.game = match
                    db.session.add(at_bat)
                    db.session.commit()
                        
            print(date)
            time.sleep(3.2)
                

        time.sleep(3.2)

    print("Done")