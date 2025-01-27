from turtle import ht
from datetime import datetime
from bs4 import BeautifulSoup, Comment
from app import app
from urllib.request import Request, urlopen
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, Game, Pitcher, Hitter, AtBat, Outing
from unidecode import unidecode
import time
import requests
import ipdb





with app.app_context():
    
    years = ["2024"]

    for year in years:

        
        # headers = {'user-agent': 'my-app/0.0.1'}
        html = requests.get(f"https://www.baseball-reference.com/leagues/majors/{year}-schedule.shtml", headers={'User-Agent':"Mozilla/5.0"})
        # date = html.select('div.ScheduleDay_sd_GFE_w')[0]


        doc = BeautifulSoup(html.text, 'html.parser')
        rows = doc.select('p.game')
        rows = [row for row in rows if "Spring" not in row.text]
        #games that year in database
        games_that_year = len([game for game in Game.query.all() if game.date.year==int(year)])


        for game in rows[games_that_year:]:

            if "Spring" in game.text:
                continue
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

            pitching_data = box_score_data.select('.section_wrapper')[1]
            pitching_data_comment = pitching_data.find(string=lambda string:isinstance(string, Comment))
            pitching_data_soup = BeautifulSoup(pitching_data_comment , 'lxml')

            date = box_score_data.select('.scorebox_meta')[0].select('div')[0].text
            the_time = box_score_data.select('.scorebox_meta')[0].select('div')[1].text

            # ipdb.set_trace()

            the_time_list = the_time.split(' ')

            
            if the_time_list[3][0]=='p':
                ending_of_date="PM"
            else:
                ending_of_date="AM"

            total_date = date+" "+the_time_list[2]+" "+ending_of_date

            try:
                the_time_string = datetime.strptime(total_date,"%A, %B %d, %Y %I:%M %p")
            except ValueError:
                the_time = box_score_data.select('.scorebox_meta')[0].select('div')[2].text
                the_time_list = the_time.split(' ')
                if the_time_list[3][0]=='p':
                    ending_of_date="PM"
                else:
                    ending_of_date="AM"

                total_date = date+" "+the_time_list[2]+" "+ending_of_date
                the_time_string = datetime.strptime(total_date,"%A, %B %d, %Y %I:%M %p")

            if the_time_string > datetime(2024,4,10,23,00):
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

            ipdb.set_trace()
            umpire_string = weather_info.select('div')[0].text.split(' ')[3:]
            umpire_list = []
            for word in umpire_string:
                if word=="1B":
                    break
                else:
                    umpire_list.append(word)
            umpire = (' ').join(umpire_list)



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
                cloud_or_sun = weather.replace('.','').split(',')[2][1:]
            else: 
                precipitation = "In Dome"
                cloud_or_sun = "In Dome"
            

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
                seperated_results = result.replace('-',' ').replace('/',' ').replace(';',' ').replace(':',' ').replace('\xa0',' ').split(' ')
                sb=0
                sb_att = 0
                rbi = 0


                if "Scores" in result:
                    if "R" in player.select('td')[4].text:
                            for index, word in enumerate(seperated_results):
                                if word=="Scores":
                                    scored = seperated_results[index-1]
                                    person_who_scored_list = [scorer for scorer in AtBat.query.order_by(AtBat.id.desc()).limit(9).all() if scored in scorer.hitter.name]
                                    if len(person_who_scored_list) > 0:
                                        person_who_scored = person_who_scored_list[0]
                                        person_who_scored.score = True
                                        db.session.commit()

                if "Wild Pitch" in result or "Steals" in result or "Caught" in result or "Passed" in result or "Picked" in result or "Defensive" in result or "Advancing" in result:
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
                    else:
                        pass

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

                    if "Line" in result  or "Lineout" in result or "Flyball" in result or "Fly Ball" in result:
                        strength = "Strong"
                    elif "Weak" in result or "Groundout" in result or "Ground" in result or "Popfly" in result:
                        strength = "Weak"
                    else:
                        strength = "None"

                    if "Sacrifice" in result:
                        play = "Sacrifice"
                    elif "Strikeout" in result:
                        play = result.replace(';','').split(' ')
                        if len(play) > 1:
                            play = play[0]+(' ')+play[1]
                        else:
                            play = play[0]
                    elif "Single" in result:
                        play = "Single"
                    elif "Ground" in result:
                        play = "Groundout"
                        strength = "Weak"
                    elif "Reached on" in result:
                        if "Interference" in result:
                            play = "Catcher Interference"
                        else:
                            play = "Error"
                    elif "Home Run" in result:
                        play = "Home Run"
                        score = 1
                        rbi+=1
                        strength = "Strong"
                    elif "Popfly" in result:
                        play = "Popfly"
                    elif "Lineout" in result:
                        play = "Lineout"
                        strength = "Strong"
                    elif "Choice" in result:
                        play = "Fielder Choice"
                    elif "Walk" in result:
                        play = "Walk"
                    elif "Triple" in result:
                        play = "Triple"
                        strength = "Strong"
                    elif "Double" in result:
                        play = "Double"
                        strength = "Strong"
                    elif "Hit By Pitch" in result:
                        play = "Hit By Pitch"
                    else:
                        play = seperated_results[0]


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

                    outs = len([value for value in player.select('td')[4].text if value=="O"])


                    
                    if int(sb)>0:
                        ipdb.set_trace()

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
                        team = team,
                        outs = outs
                    )

                    at_bat.pitcher = assoc_pitcher
                    at_bat.hitter = assoc_hitter
                    at_bat.game = match
                    db.session.add(at_bat)
                    db.session.commit()

            away_pitcher = [ab for ab in match.at_bats if ab.team==match.home][0].pitcher
            home_pitcher = [ab for ab in match.at_bats if ab.team==match.visitor][0].pitcher

            away_pitcher_with_w_l = pitching_data_soup.select('tbody')[0].select('tr')[0].select('th')[0].text.split(',')
            home_pitcher_with_w_l = pitching_data_soup.select('tbody')[1].select('tr')[0].select('th')[0].text.split(',')
            

            away_pitcher_abs = [ab for ab in match.at_bats if ab.pitcher==away_pitcher]
            home_pitcher_abs = [ab for ab in match.at_bats if ab.pitcher==home_pitcher]

            away_pitcher_value = 0
            away_pitcher_outs = 0
            away_pitcher_hits = 0
            for ab in away_pitcher_abs:
                away_pitcher_outs += ab.outs
                if "Strikeout" in ab.result:
                    away_pitcher_value+=2
                if ab.score==1 and "Error" not in ab.result:
                    away_pitcher_value-=2
                if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run":
                    away_pitcher_value-=.6
                    away_pitcher_hits+=1
                if ab.result=="Hit" or ab.result=="Walk":
                    away_pitcher_value-=.6

            
            away_pitcher_value += away_pitcher_outs * .75
            if len(away_pitcher_with_w_l) > 1:
                if "W" in away_pitcher_with_w_l[1]:
                    away_pitcher_value +=4
            if away_pitcher_outs >= 27:
                away_pitcher_value+=2.5
                if away_pitcher_hits==0:
                    away_pitcher_value+=5
                if match.home_score==0:
                    away_pitcher_value+=2.5


            home_pitcher_value = 0
            home_pitcher_outs = 0
            home_pitcher_hits = 0
            for ab in home_pitcher_abs:
                home_pitcher_outs += ab.outs
                if "Strikeout" in ab.result:
                    home_pitcher_value+=2
                if ab.score==1 and "Error" not in ab.result:
                    home_pitcher_value-=2
                if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run":
                    home_pitcher_value-=.6
                    home_pitcher_hits+=1
                if ab.result=="Hit" or ab.result=="Walk":
                    home_pitcher_value-=.6


            home_pitcher_value += home_pitcher_outs * .75
            if len(home_pitcher_with_w_l) > 1:
                if "W" in home_pitcher_with_w_l[1]:
                    home_pitcher_value +=4
            if home_pitcher_outs >= 27:
                home_pitcher_value+=2.5
                if home_pitcher_hits==0:
                    home_pitcher_value+=5
                if match.away_score==0:
                    home_pitcher_value+=2.5


            match.home_pitcher_result = home_pitcher_value
            match.away_pitcher_result = away_pitcher_value


            abs = match.at_bats

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
                    

                if 25 <=ab_total:
                    ab.result_stdev = 1.3
                if 18 <= ab_total <=24:
                    ab.result_stdev = 1
                elif 14 <= ab_total <= 17:
                    ab.result_stdev = .95
                elif 10 <= ab_total <= 13:
                    ab.result_stdev = .9
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
                db.session.commit()
                        
            print(date)
            time.sleep(3.2)
                

        time.sleep(3.2)

    print("Done")