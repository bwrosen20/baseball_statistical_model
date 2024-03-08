from app import *
from statistics import mean,mode,median,stdev
from bs4 import BeautifulSoup, Comment
from datetime import datetime, date, timedelta
from operator import itemgetter
from sqlalchemy import or_
from unidecode import unidecode
from random import sample
import calendar
import itertools
import time
import requests
import ipdb


with app.app_context():


    # def random_number(salary):
    #     counter = 20
    #     try:
    #         value = round(float(salary),2)
    #         array = []
    #         while counter > value:
    #             final_value = round(counter/20,2)
    #             array.append(round(float(final_value),2))
    #             counter-=.5
    #     except ValueError:
    #         array = [0,0,0]
        

    #     return sample(array,1)[0]



    time_url = "https://time.is/"
    time_page = requests.get(time_url, headers = {'User-Agent':"Mozilla/5.0"})
    time_doc = BeautifulSoup(time_page.text, 'html.parser')
    date_string = time_doc.select("#dd")[0].text
    time_string = time_doc.select('#clock')[0].text 
    format_time = datetime.strptime(time_string,"%I:%M:%S%p").time()

    #set current date to todays date and run the algorithm to see projections
    full_date = datetime.strptime(date_string, "%A, %B %d, %Y")
    current_date = full_date.date()

    # current_date = datetime(2023,11,27).date()


    yesterday = current_date - timedelta(1)
    most_recent_game_date = Game.query.all()[-1].date.date()
    time_list = date_string.replace(",","").split()
    month = time_list[1].lower()
    year = int(time_list[3])
    if len(str(full_date.month))<2:
        month_string = ('0' + str(full_date.month))
    else:
        month_string = str(full_date.month)
    if len(str(full_date.day))<2:
        day_string = ('0' + str(full_date.day))
    else:
        day_string = str(full_date.day)


    

    month_of_yesterday = calendar.month_name[yesterday.month].lower()
    year_of_yesterday = yesterday.year
    year_of_yesterday_string = str(year_of_yesterday)



    stadium_orientations = {
        "American Family Field":"SE",
        "Angel Stadium of Anaheim":"NE",
        "Busch Stadium III":"ENE",
        "Chase Field":"Dome",
        "Citi Field":"NNE",
        "Citizens Bank Park":"NNE",
        "Comerica Park":"SSE",
        "Coors Field":"N",
        "Dodger Stadium":"NNE",
        "Fenway Park":"NE",
        "Globe Life Field":"Dome",
        "Great American Ball Park":"SE",
        "Guaranteed Rate Field":"SE",
        "Kauffman Stadium":"NE",
        "loanDepot Park":"Dome",
        "Minute Maid Park":"N",
        "Nationals Park":"NNE",
        "RingCentral Coliseum":"ENE",
        "Oakland Coliseum":"ENE",
        "Oracle Park":"E",
        "Oriole Park at Camden Yards":"NNE",
        "Petco Park":"N",
        "PNC Park":"ESE",
        "Progressive Field":"N",
        "Rogers Centre":"Dome",
        "T-Mobile Park":"NNE",
        "Target Field":"E",
        "Tropicana Field":"Dome",
        "Truist Park":"SSE",
        "Wrigley Field":"NNE",
        "Yankee Stadium III":"ENE"
    }

   

    wind_correction_factors = {
        "American Family Field":135,
        "Angel Stadium of Anaheim":45,
        "Busch Stadium III":67.5,
        "Chase Field":"Dome",
        "Citi Field":22.5,
        "Citizens Bank Park":22.5,
        "Comerica Park":157.5,
        "Coors Field":0,
        "Dodger Stadium":22.5,
        "Fenway Park":45,
        "Globe Life Field":"Dome",
        "Great American Ball Park":135,
        "Guaranteed Rate Field":135,
        "Kauffman Stadium":45,
        "loanDepot Park":"Dome",
        "Minute Maid Park":0,
        "Nationals Park":22.5,
        "RingCentral Coliseum":67.5,
        "Oakland Coliseum":67.5,
        "Oracle Park":90,
        "Oriole Park at Camden Yards":22.5,
        "Petco Park":0,
        "PNC Park":112.5,
        "Progressive Field":0,
        "Rogers Centre":"Dome",
        "T-Mobile Park":22.5,
        "Target Field":90,
        "Tropicana Field":"Dome",
        "Truist Park":157.5,
        "Wrigley Field":22.5,
        "Yankee Stadium III":67.5
    }


    stadiums = {
        "Milwaukee Brewers":"American Family Field",
        "Los Angeles Angels":"Angel Stadium of Anaheim",
        "St. Louis Cardinals":"Busch Stadium III",
        "Arizona Diamondbacks":"Chase Field",
        "New York Mets":"Citi Field",
        "Philadelphia Phillies":"Citizens Bank Park",
        "Detroit Tigers":"Comerica Park",
        "Colorado Rockies":"Coors Field",
        "Los Angeles Dodgers":"Dodger Stadium",
        "Boston Red Sox":"Fenway Park",
        "Texas Rangers":"Globe Life Field",
        "Cincinnati Reds":"Great American Ball Park",
        "Chicago White Sox":"Guaranteed Rate Field",
        "Kansas City Royals":"Kauffman Stadium",
        "Miami Marlins":"loanDepot Park",
        "Houston Astros":"Minute Maid Park",
        "Washington Nationals":"Nationals Park",
        "Oakland Athletics":"Oakland Coliseum",
        "San Francisco Giants":"Oracle Park",
        "Baltimore Orioles":"Oriole Park at Camden Yards",
        "San Diego Padres":"Petco Park",
        "Pittsburgh Pirates":"PNC Park",
        "Cleveland Guardians":"Progressive Field",
        "Toronto Blue Jays":"Rogers Centre",
        "Seattle Mariners":"T-Mobile Park",
        "Minnesota Twins":"Target Field",
        "Tampa Bay Rays":"Tropicana Field",
        "Atlanta Braves":"Truist Park",
        "Chicago Cubs":"Wrigley Field",
        "New York Yankees":"Yankee Stadium III"
    }

    # if most_recent_game_date != yesterday:
    #     scrape_a_day(yesterday,month_of_yesterday,year_of_yesterday)

    # else:
    #     print("All games have been downloaded\n")

    # algo_b_bets = FinalBet.query.filter(FinalBet.algorithm=="B").all()
    
    # if len(algo_b_bets) > 0:
    #     last_algo_b_bet = algo_b_bets[-1]
    #     if last_algo_b_bet.date.date()!=current_date:
    #         yesterdays_bets = FinalBet.query.filter(FinalBet.date==full_date-timedelta(1),FinalBet.algorithm=="B").all()
    #         high_value = [bet for bet in yesterdays_bets if bet.category=="high_value"]
    #         low_value = [bet for bet in yesterdays_bets if bet.category=="low_value"]
    #         total_value = [bet for bet in yesterdays_bets if bet.category=="total_value"]
    #         games_in_a_row = [bet for bet in yesterdays_bets if bet.category=="games_in_a_row"]

    #         print("\nHigh value teasers\n")
    #         for item in high_value:
    #             name = item.name
    #             prop = item.prop
    #             teaser = item.line
    #             index = item.category_value
    #             player_who_played = Player.query.filter(Player.name==name).first()
    #             yesterdays_game = player_who_played.games[-1]
    #             if yesterdays_game.game.date.date()==(full_date-timedelta(1)).date():
    #                 if prop=="rebounds":
    #                     actual_score = yesterdays_game.trb
    #                 elif prop=="points":
    #                     actual_score = yesterdays_game.points
    #                 else:
    #                     actual_score = yesterdays_game.assists
    #                 if actual_score >= teaser:
    #                     did_they_do_it = "✅"
    #                 else:
    #                     did_they_do_it = "❌"
    #             else:
    #                 did_they_do_it = "🏖️"
    #                 actual_score = "NA"

    #             string_output = f"{index}: {name} {teaser} {prop} Actual: {actual_score}"
    #             string_output = string_output.ljust(55,'.')

    #             print(f"{string_output} {did_they_do_it}")

    #         print("\nLow value teasers\n")
    #         for item in low_value:
    #             name = item.name
    #             prop = item.prop
    #             teaser = item.line
    #             index = item.category_value
    #             player_who_played = Player.query.filter(Player.name==name).first()
    #             yesterdays_game = player_who_played.games[-1]
    #             if yesterdays_game.game.date.date()==(full_date-timedelta(1)).date():
    #                 if prop=="rebounds":
    #                     actual_score = yesterdays_game.trb
    #                 elif prop=="points":
    #                     actual_score = yesterdays_game.points
    #                 else:
    #                     actual_score = yesterdays_game.assists
    #                 if actual_score >= teaser:
    #                     did_they_do_it = "✅"
    #                 else:
    #                     did_they_do_it = "❌"
    #             else:
    #                 did_they_do_it = "🏖️"
    #                 actual_score = "NA"

    #             string_output = f"{index}: {name} {teaser} {prop} Actual: {actual_score}"
    #             string_output = string_output.ljust(55,'.')

    #             print(f"{string_output} {did_they_do_it}")

    #         print("\nTotal value\n")
    #         for item in total_value:
    #             name = item.name
    #             prop = item.prop
    #             teaser = item.line
    #             index = item.category_value
    #             player_who_played = Player.query.filter(Player.name==name).first()
    #             yesterdays_game = player_who_played.games[-1]
    #             if yesterdays_game.game.date.date()==(full_date-timedelta(1)).date():
    #                 if prop=="rebounds":
    #                     actual_score = yesterdays_game.trb
    #                 elif prop=="points":
    #                     actual_score = yesterdays_game.points
    #                 else:
    #                     actual_score = yesterdays_game.assists
    #                 if actual_score >= teaser:
    #                     did_they_do_it = "✅"
    #                 else:
    #                     did_they_do_it = "❌"
    #             else:
    #                 did_they_do_it = "🏖️"
    #                 actual_score = "NA"

    #             string_output = f"{index}: {name} {teaser} {prop} Actual: {actual_score}"
    #             string_output = string_output.ljust(55,'.')

    #             print(f"{string_output} {did_they_do_it}")


    #         print("\nGames in a Row\n")
    #         for item in games_in_a_row:
    #             name = item.name
    #             prop = item.prop
    #             teaser = item.line
    #             index = item.category_value
    #             player_who_played = Player.query.filter(Player.name==name).first()
    #             yesterdays_game = player_who_played.games[-1]
    #             if yesterdays_game.game.date.date()==(full_date-timedelta(1)).date():
    #                 if prop=="rebounds":
    #                     actual_score = yesterdays_game.trb
    #                 elif prop=="points":
    #                     actual_score = yesterdays_game.points
    #                 else:
    #                     actual_score = yesterdays_game.assists
    #                 if actual_score >= teaser:
    #                     did_they_do_it = "✅"
    #                 else:
    #                     did_they_do_it = "❌"
    #             else:
    #                 did_they_do_it = "🏖️"
    #                 actual_score = "NA"

    #             string_output = f"{index}: {name} {teaser} {prop} Actual: {actual_score}"
    #             string_output = string_output.ljust(55,'.')

    #             print(f"{string_output} {did_they_do_it}")
    #         print('\n')
            



    #find league average babip over last 100k abs

    league_abs = AtBat.query.all()[-100000:]

    league_avg_babip_numerator = len([ab for ab in league_abs if ab.result=="Triple" or ab.result=="Double" or ab.result=="Single"])
    league_avg_babip_denominator = len([ab for ab in league_abs if "Strikeout" not in ab.result and ab.result!="Home Run" and ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result])
    league_babip = league_avg_babip_numerator/league_avg_babip_denominator

    league_avg_abs = [ab for ab in league_abs if ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result]
    league_avg_hits = len([ab for ab in league_avg_abs if ab.result=="Home Run" or ab.result=="Triple" or ab.result=="Double" or ab.result=="Single"])

    league_avg = league_avg_hits/len(league_avg_abs)

    league_ks = len([ab for ab in league_avg_abs if "Strikeout" in ab.result])
    league_k_perc = league_ks/len(league_avg_abs)

    league_in_play_percentage = league_avg_babip_denominator/len(league_abs)


    league_on_first_abs = [ab for ab in league_abs if ab.result=="Single" or ab.result=="Walk" or ab.result=="Hit" or "Reached" in ab.result or "Choice" in ab.result]

    league_sb_abs = len([ab for ab in league_on_first_abs if ab.sb_att>=1])

    league_sb_perc = league_sb_abs/len(league_on_first_abs)

    league_sb_attempts = [ab for ab in AtBat.query.all() if ab.sb_att > 0]
    league_sb_abs = len([ab for ab in league_sb_attempts if ab.sb > 0])

    league_sb_success = league_sb_abs/len(league_sb_attempts)



    #get game data



    year=2022

    #schedule_page_url = f"https://rotogrinders.com/lineups/mlb?date={year_string}-{month_string}-{day_string}&site=draftkings"
    schedule_page_url = f"https://www.baseball-reference.com/leagues/majors/{year}-schedule.shtml"
    html = requests.get(schedule_page_url, headers={'User-Agent':"Mozilla/5.0"})
    doc = BeautifulSoup(html.text, 'html.parser')
    rows = doc.select('p.game')
    
    games_that_year = [game for game in Game.query.all() if game.date.year==int(year)]

   

    url_ending = rows[len(games_that_year)].select('a')[2].get("href")
    box_score_url = f"https://www.baseball-reference.com/{url_ending}"
    box_score = requests.get(box_score_url)
    box_score_data = BeautifulSoup(box_score.text, 'lxml')

    
    date = box_score_data.select('.scorebox_meta')[0].select('div')[0].text
    the_time = box_score_data.select('.scorebox_meta')[0].select('div')[1].text

    # ipdb.set_trace()

    the_time_list = the_time.split(' ')

    
    if the_time_list[3][0]=='p':
        ending_of_date="PM"
    else:
        ending_of_date="AM"

    total_date = date+" "+the_time_list[2]+" "+ending_of_date


    todays_time_string = datetime.strptime(total_date,"%A, %B %d, %Y %I:%M %p")




    todays_games = []
    hitter_list = []
    pitcher_list = []

    for game in rows[(len(games_that_year)):]:

        url_ending = game.select('a')[2].get("href")
        box_score_url = f"https://www.baseball-reference.com/{url_ending}"
        box_score = requests.get(box_score_url)
        box_score_data = BeautifulSoup(box_score.text, 'lxml')

        date = box_score_data.select('.scorebox_meta')[0].select('div')[0].text
        the_time = box_score_data.select('.scorebox_meta')[0].select('div')[1].text

        the_time_list = the_time.split(' ')

        
        if the_time_list[3][0]=='p':
            ending_of_date="PM"
        else:
            ending_of_date="AM"

        total_date = date+" "+the_time_list[2]+" "+ending_of_date


        the_time_string = datetime.strptime(total_date,"%A, %B %d, %Y %I:%M %p")

        if the_time_string.date()!=todays_time_string.date():
            break



        home = game.select('a')[1].text
        away = game.select('a')[0].text

        
        play_by_play = box_score_data.select('#all_play_by_play')[0]

        comment = play_by_play.find(string=lambda string:isinstance(string, Comment))
        commentsoup = BeautifulSoup(comment , 'lxml')
        tops = commentsoup.select('tr.top_inning')
        bottoms= commentsoup.select('tr.bottom_inning')
        tops.extend(bottoms)

        date = box_score_data.select('.scorebox_meta')[0].select('div')[0].text
        the_time = box_score_data.select('.scorebox_meta')[0].select('div')[1].text

        # ipdb.set_trace()

        the_time_list = the_time.split(' ')

        
        if the_time_list[3][0]=='p':
            ending_of_date="PM"
        else:
            ending_of_date="AM"

        total_date = date+" "+the_time_list[2]+" "+ending_of_date


        the_time_string = datetime.strptime(total_date,"%A, %B %d, %Y %I:%M %p")

        # if the_time_string > datetime(2021,9,6,22,00):
        #     break
            

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

        todays_games.append(match)


        players_data = box_score_data.select('#all_lineups')[0]
        players_comment = players_data.find(string=lambda string:isinstance(string, Comment))
        players_soup = BeautifulSoup(players_comment , 'lxml')

        away_players_data = players_soup.select('#lineups_1')[0]
        home_players_data = players_soup.select('#lineups_2')[0]

        away_players = away_players_data.select('tr')
        home_players = home_players_data.select('tr')

        #find the player objects and add a temporary team column


        for player in away_players:
            name = unidecode(player.select('td')[1].text)
            if name[0]==" ":
                name=name[1:]
            position = player.select('td')[2].text
            if "P" in position:
                pitcher_options = Pitcher.query.filter(Pitcher.name==name).all()
                if len(pitcher_options)>0:
                    starting_lineup_player = pitcher_options[0]
                    starting_lineup_player.team=away
                    hitter_array = []
                    sb_modifier_array = []
                    for ab in starting_lineup_player.at_bats:
                        hitter = ab.hitter.name
                        try:
                            hitter_object = Hitter.query.filter(Hitter.name==hitter)[0]
                        except IndexError:
                            ipdb.set_trace()
                        if hitter not in hitter_array:
                            hitter_array.append(hitter)
                            sb_modifier_abs = [ab for ab in starting_lineup_player.at_bats if ab.hitter.name==hitter]
                            if len(sb_modifier_abs)>5 and len([ab for ab in sb_modifier_abs if ab.result=="Single" or ab.result=="Walk" or "Reached" in ab.result or "Choice" in ab.result])>0:
                                #sb percentage against this pitcher
                                abs_on_first = [ab for ab in sb_modifier_abs if ab.result=="Single" or ab.result=="Walk" or "Reached" in ab.result or "Choice" in ab.result]
                                abs_where_he_stole = [ab for ab in abs_on_first if ab.sb>=1]
                                try: 
                                    pitcher_sb_modifier = len(abs_where_he_stole)/len(abs_on_first)
                                except ZeroDivisionError:
                                    ipdb.set_trace()

                                #how often people try to steal on them
                                total_abs_on_first = [ab for ab in hitter_object.at_bats if ab.result=="Single" or ab.result=="Walk" or "Reached" in ab.result or "Choice" in ab.result]
                                total_abs_where_he_stole = [ab for ab in total_abs_on_first if ab.sb_att>=1]
                                total_sb_modifier = (len(total_abs_where_he_stole)/len(total_abs_on_first))/league_sb_perc

                                #total modifier will be around 1, higher if pitcher allows more sb
                                
                                sb_modifier_array.append(total_sb_modifier)
                                
                    if len(sb_modifier_array) > 0:            
                        sb_modifier_final = mean(sb_modifier_array)
                    else:
                        sb_modifier_final = 1
                    #how likely he is to let up sb attempts in the first place
                    pitcher_sb_attempts = [ab for ab in starting_lineup_player.at_bats if ab.sb_att > 0]
                    pitcher_sb_abs = len([ab for ab in pitcher_sb_attempts if ab.sb > 0])
                    if len(pitcher_sb_attempts) > 0:
                        pitcher_sb_success = (pitcher_sb_abs/len(pitcher_sb_attempts))/league_sb_success
                    else: 
                        pitcher_sb_success = 1
                    sb_modifier = pitcher_sb_success*.7 + sb_modifier_final*.3
                    starting_lineup_player.sb_modifier = sb_modifier

                    pitcher_list.append(starting_lineup_player)
                # else:
                #     ipdb.set_trace()
            else:
                hitter_options = Hitter.query.filter(Hitter.name==name).all()
                if len(hitter_options)>0:
                    starting_lineup_player = hitter_options[0]
                    starting_lineup_player.team=away
                    hitter_list.append(starting_lineup_player)
                # else:
                #     ipdb.set_trace()

        for player in home_players:
            name = unidecode(player.select('td')[1].text)
            if name[0]==" ":
                name=name[1:]
            position = player.select('td')[2].text
            if "P" in position:
                pitcher_options = Pitcher.query.filter(Pitcher.name==name).all()
                if len(pitcher_options)>0:
                    starting_lineup_player = pitcher_options[0]
                    starting_lineup_player.team=home
                    hitter_array = []
                    sb_modifier_array = []
                    for ab in starting_lineup_player.at_bats:
                        hitter = ab.hitter.name
                        try:
                            hitter_object = Hitter.query.filter(Hitter.name==hitter)[0]
                        except IndexError:
                            ipdb.set_trace()
                        if hitter not in hitter_array:
                            hitter_array.append(hitter)
                            sb_modifier_abs = [ab for ab in starting_lineup_player.at_bats if ab.hitter.name==hitter]
                            if len(sb_modifier_abs)>5 and len([ab for ab in sb_modifier_abs if ab.result=="Single" or ab.result=="Walk" or "Reached" in ab.result or "Choice" in ab.result])>0:
                                #sb percentage against this pitcher
                                abs_on_first = [ab for ab in sb_modifier_abs if ab.result=="Single" or ab.result=="Walk" or "Reached" in ab.result or "Choice" in ab.result]
                                abs_where_he_stole = [ab for ab in abs_on_first if ab.sb>=1]
                                pitcher_sb_modifier = len(abs_where_he_stole)/len(abs_on_first)
                                 #how often people try to steal on them
                                total_abs_on_first = [ab for ab in hitter_object.at_bats if ab.result=="Single" or ab.result=="Walk" or "Reached" in ab.result or "Choice" in ab.result]
                                total_abs_where_he_stole = [ab for ab in total_abs_on_first if ab.sb_att>=1]
                                total_sb_modifier = (len(total_abs_where_he_stole)/len(total_abs_on_first))/league_sb_perc

                                #total modifier will be around 1, higher if pitcher allows more sb
                                
                                sb_modifier_array.append(total_sb_modifier)

                    if len(sb_modifier_array) > 0:            
                        sb_modifier_final = mean(sb_modifier_array)
                    else:
                        sb_modifier_final = 1
                    #how likely he is to let up sb attempts in the first place
                    pitcher_sb_attempts = [ab for ab in starting_lineup_player.at_bats if ab.sb_att > 0]
                    pitcher_sb_abs = len([ab for ab in pitcher_sb_attempts if ab.sb > 0])
                    if len(pitcher_sb_attempts) > 0:
                        pitcher_sb_success = (pitcher_sb_abs/len(pitcher_sb_attempts))/league_sb_success
                    else: 
                        pitcher_sb_success = 1
                    
                    sb_modifier = pitcher_sb_success*.7 + sb_modifier_final*.3
                    starting_lineup_player.sb_modifier = sb_modifier

                    pitcher_list.append(starting_lineup_player)
                # else:
                #     ipdb.set_trace()
            else:
                hitter_options = Hitter.query.filter(Hitter.name==name).all()
                if len(hitter_options)>0:
                    starting_lineup_player = hitter_options[0]
                    starting_lineup_player.team=home
                    hitter_list.append(starting_lineup_player)
                # else:
                #     ipdb.set_trace()
    

  

    bets = []
    high_value_teasers = []
    low_value_teasers = []
    games_in_a_row = []
    weekday_games = []
    counter = 0 


    
    print("Made it to the loop")

    for player in hitter_list:

        player_name = player.name
        player_team = player.team
        game = [game for game in todays_games if game.home==player_team or game.visitor==player_team][0]
        if game.home==player_team:
            other_team = game.visitor
        else:
            other_team = game.home
        
        #collect my own data about every game they've played in

        pitcher_object = [player for player in pitcher_list if player.team==other_team][0]
        pitcher_name=pitcher_object.name
        # hitter = 1
    


        # specific_time = datetime(2024,1,21,16,30,00)
        #and specific_time.time() < [game["time"] for game in todays_games if game["home"]==player_team or game["away"]==player_team][0]

        # if ([game.date.time() for game in game_list if game.home==player_team or game.visitor==player_team][0] > format_time):
        if 1>0:

            print(f"{player_name} ({player_team})")

            abs = player.at_bats


            #find info for babip modifier

            hitter_total_abs = [ab for ab in abs if ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result]
            hitter_balls_in_play = [ab for ab in hitter_total_abs if "Strikeout" not in ab.result and ab.result!="Home Run"]
            hitter_babip_numerator = len([ab for ab in hitter_balls_in_play if ab.result=="Triple" or ab.result=="Double" or ab.result=="Single"])


            hitter_in_play_percentage = len(hitter_balls_in_play)/len(hitter_total_abs)
            hitter_babip = hitter_babip_numerator/len(hitter_balls_in_play)

            #find percentage of balls in play by pitcher


            all_pitcher_abs = pitcher_object.at_bats
            pitcher_total_abs = [ab for ab in all_pitcher_abs if ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result]
            pitcher_balls_in_play = [ab for ab in pitcher_total_abs if "Strikeout" not in ab.result and ab.result!="Home Run"]
            pitcher_babip_numerator = len([ab for ab in pitcher_balls_in_play if ab.result=="Triple" or ab.result=="Double" or ab.result=="Single"])


            #pitcher in play % and babip

            pitcher_in_play_percentage = len(pitcher_balls_in_play)/len(pitcher_total_abs)
            pitcher_babip = pitcher_babip_numerator/len(pitcher_balls_in_play)

            
            
            #latest 25 abs at time
            upper_hour = game.date.hour+1
            lower_hour = game.date.hour-1
            minutes = game.date.minute
            upper_time = datetime(2023,2,1,upper_hour,minutes).time()
            lower_time = datetime(2023,2,1,lower_hour,minutes).time()
            abs_at_time = [ab for ab in abs if ab.game.date.time()<=upper_time and ab.game.date.time()>=lower_time][-50:]
            
            #last 25 abs on specific day
            current_day = current_date.weekday()
            abs_on_day = []
            for ab in abs:
                if ab.game.date.weekday()==current_day:
                    abs_on_day.append(ab)

            abs_on_day = abs_on_day[-50:]


        
            #last 50 abs
            latest_games = [ab for ab in abs][-50:]


            #home/away games
            if game.home==player_team:
                latest_home_or_away_abs = [ab for ab in abs if ab.game.home==player_team][-50:]
            else:
                latest_home_or_away_abs = [ab for ab in abs if ab.game.visitor==player_team][-50:]
            

            
            #get latest matchups vs pitcher
            abs_vs_opponent = [ab for ab in abs if (ab.pitcher.name==pitcher_name)][-50:]

            #other things I need

            #abs vs lefty/righty 

            abs_vs_left_right = [ab for ab in abs if ab.pitcher.arm==pitcher_object.arm][-50:]

            #right-left modifier

            #pitchers average when facing opposite side batter

            total_abs_opp = [ab for ab in all_pitcher_abs if ab.hitter.bat!=pitcher_object.arm and "Walk" not in ab.result and "Sacrifice" not in ab.result and "Interference" not in ab.result and "Hit" not in ab.result]
            abs_with_hit_opp = len([ab for ab in total_abs_opp if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run"])

            pitcher_opposite_avg = abs_with_hit_opp/len(total_abs_opp)


            #pitchers avg when facing same side batter

            total_abs_same = [ab for ab in all_pitcher_abs if ab.hitter.bat==pitcher_object.arm and "Walk" not in ab.result and "Sacrifice" not in ab.result and "Interference" not in ab.result and "Hit" not in ab.result]
            abs_with_hit_same = len([ab for ab in total_abs_same if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run"])

            pitcher_same_avg = abs_with_hit_same/len(total_abs_same)



            #hitters average when facing opposite side pitcher

            oppo_taco_abs = [ab for ab in abs if ab.pitcher.arm!=player.bat and "Walk" not in ab.result and "Sacrifice" not in ab.result and "Interference" not in ab.result and "Hit" not in ab.result]
            oppo_taco_hits = len([ab for ab in oppo_taco_abs if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run"])

            hitter_opposite_avg = oppo_taco_hits/len(oppo_taco_abs)


            #hitters avg when facing same side pitcher

            same_side_abs = [ab for ab in abs if ab.pitcher.arm==player.bat and "Walk" not in ab.result and "Sacrifice" not in ab.result and "Interference" not in ab.result and "Hit" not in ab.result]
            same_side_hits = len([ab for ab in same_side_abs if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run"])
            

            hitter_same_avg = same_side_hits/len(same_side_abs)

            if pitcher_object.arm==player.bat:
                batter_side_modifier = (0.35 * pitcher_same_avg/league_avg ) + (0.65 * hitter_same_avg/league_avg)

            else:
                batter_side_modifier = (0.35 * pitcher_opposite_avg/league_avg ) + (0.65 * hitter_opposite_avg/league_avg)

            #babip modifier)
            
            #find percentage of balls in play compared to pitchers at bats
            #find hitter babip in last 150 abs 

            #hitter_babip
            #pitcher_babip
            #league_babip
            #league_in_play_percentage
            #pitcher_in_play_percentage
            #hitter_in_play_percentage

            babip_modifier = (pitcher_babip + hitter_babip) / (2 * league_babip)
            in_play_modifier = (pitcher_in_play_percentage + hitter_in_play_percentage) / (2 * league_in_play_percentage)


            result_modifier = (0.275 * babip_modifier + 0.05 * in_play_modifier + 0.675 * batter_side_modifier)

            
            #need a sb modifier, maybe more. We'll see

            #sb modifier

            #pitchers abs where a player gets onto first

            on_first_abs = [ab for ab in all_pitcher_abs if ab.result=="Single" or ab.result=="Walk" or ab.result=="Hit" or "Reached" in ab.result or "Choice" in ab.result]

            sb_abs = len([ab for ab in on_first_abs if ab.sb>=1])

            sb_perc = league_sb_abs/len(league_on_first_abs)

            #how likely they are to steal compared to the rest of the league
            sb_modifier = sb_perc/league_sb_perc


            #how bad the pitcher is against sb's (higher number means more steals)
            pitcher_sb_modifier = pitcher_object.sb_modifier

            #strikeout percentage (for pitchers)


            #create new implied batting average by multipying hitter 

            #babip
                #compare pitchers allowed babip to hitter's babip



            #both pitchers and hitters



            #last 50 at stadium
            at_stadium = [ab for ab in abs if ab.game.location == game.location][-50:]

            #last 50 with wind direction

            if final_wind_direction == 400:
                wind_direction_abs = [ab for ab in abs if ab.game.precipitation=="In Dome"][-50:]

            else:
                wind_high = final_wind_direction + 22.5
                wind_low = final_wind_direction - 22.5

                wind_direction_abs = [ab for ab in abs if wind_low <= ab.game.wind_direction <= wind_high][-50:]

                #wind speed
                wind_speed_high = wind_speed + 2
                wind_speed_low = wind_speed - 2

                wind_speed_abs = [ab for ab in abs if wind_speed_low <= ab.game.wind_speed <= wind_speed_high][-50:]

            #sunny/cloudy
            #Overcast, Sunny, Cloudy, In Dome
            if game.cloud_or_sun=="Cloudy" or game.cloud_or_sun=="Overcast":
                cloud_or_sun_abs = [ab for ab in abs if ab.game.cloud_or_sun=="Cloudy" or ab.game.cloud_or_sun=="Overcast"][-50:]
            elif game.cloud_or_sun=="Sunny":
                cloud_or_sun_abs = [ab for ab in abs if ab.game.cloud_or_sun=="Sunny"][-50:]
            else:
                cloud_or_sun_abs = []


            #precipitation
            if game.precipitation=="Rain":
                precipitation_abs = [ab for ab in abs if ab.game.precipitation=="Rain" or ab.game.precipitation=="Drizzle"][-50:]
            elif game.precipitation=="Snow":
                precipitation_abs = [ab for ab in abs if ab.game.precipitation=="Snow"][-50:]
            else:
                precipitation_abs = []


            #temperature
            freezing = 35
            real_cold = 42
            very_cold = 47
            cold = 62
            nice = 78
            hot = 88
            too_hot = 97

            if game.temperature <= freezing:
                temperature_abs = [ab for ab in abs if ab.game.temperature <= freezing][50:]
            elif freezing < game.temperature <= real_cold:
                temperature_abs = [ab for ab in abs if freezing < ab.game.temperature <= real_cold][-50:]
            elif real_cold < game.temperature <= very_cold:
                temperature_abs = [ab for ab in abs if real_cold < ab.game.temperature <= very_cold][-50:]
            elif very_cold < game.temperature <= cold:
                temperature_abs = [ab for ab in abs if very_cold < ab.game.temperature <= cold][-50:]
            elif cold < game.temperature <= nice:
                temperature_abs = [ab for ab in abs if cold < ab.game.temperature <= nice][-50:]
            elif nice < game.temperature <= hot:
                temperature_abs = [ab for ab in abs if nice < ab.game.temperature <= hot][-50:]
            elif hot < game.temperature <= too_hot:
                temperature_abs = [ab for ab in abs if hot < ab.game.temperature <= too_hot][-50:]
            else:
                temperature_abs = [ab for ab in abs if ab.game.temperature > too_hot][-50:]

            #vs team
            abs_vs_team = [ab for ab in abs if ab.game.home==other_team or ab.game.visitor==other_team][-50:]



                #stats to measure
                    #for hitters
                        #hits
                        #walks
                        #strikeouts
                        #rbi
                        #runs
                        #sbs

                    #for pitchers
                        #innings pitched
                        #strikeouts
                        #walks
                        #earned runs


                #find if people steal more often against that pitcher than the league average
                    #grab at bats where someone gets on first with a clear path to second and steals vs doesn't
                #find what correlates best with standard deviation. 
                #lowest stdev will be worth most and vice versa




                #make a big array of games
                # latest_home_or_away_games.extend(games_at_time)
                # latest_home_or_away_games.extend(games_vs_opponent)
                # if injury:
                #     latest_home_or_away_games.extend(games_with_injury[-3:])
                # if opponent_injury:
                #     latest_home_or_away_games.extend(games_with_opp_injury[-3:])
                # latest_home_or_away_games.extend(games_on_day)
                # latest_home_or_away_games.extend(rest_days)

                # latest_home_or_away_games.reverse()

                #find most similar game


                # new_game_list = set(latest_home_or_away_games)

                # uniq_game_list = list(new_game_list)


                # uniq_game_list = [game for game in uniq_game_list]


            #values to put into stdev formula

            #temperature_abs
            if len(temperature_abs)<5:
                temperature_abs = [ab for ab in AtBat.query.all() if ab.team=="Dummy"]
            #abs_vs_team
            if len(abs_vs_team)<5:
                abs_vs_team = [ab for ab in AtBat.query.all() if ab.team=="Dummy"]
            #precipitation_abs (if greater than 0)
            if len(precipitation_abs)<5:
                precipitation_abs = [ab for ab in AtBat.query.all() if ab.team=="Dummy"]
            #cloud_or_sun_abs
            if len(cloud_or_sun_abs)<5:
                cloud_or_sun_abs = [ab for ab in AtBat.query.all() if ab.team=="Dummy"]
            #wind_speed_abs
            if len(wind_speed_abs)<5:
                wind_speed_abs = [ab for ab in AtBat.query.all() if ab.team=="Dummy"]
            #wind_direction_abs
            if len(wind_direction_abs)<5:
                wind_direction_abs = [ab for ab in AtBat.query.all() if ab.team=="Dummy"]
            #at_stadium
            if len(at_stadium)<5:
                at_stadium = [ab for ab in AtBat.query.all() if ab.team=="Dummy"]
            #abs_at_time
            if len(abs_at_time)<5:
                abs_at_time = [ab for ab in AtBat.query.all() if ab.team=="Dummy"]
            #abs_on_day
            if len(abs_on_day)<5:
                abs_on_day = [ab for ab in AtBat.query.all() if ab.team=="Dummy"]
            #latest_games
            if len(latest_games)<5:
                latest_games = [ab for ab in AtBat.query.all() if ab.team=="Dummy"]
            #latest_home_or_away_games
            if len(latest_home_or_away_games)<5:
                latest_home_or_away_games = [ab for ab in AtBat.query.all() if ab.team=="Dummy"]
            #abs_vs_opponent
            if len(abs_vs_opponent)<5:
                abs_vs_opponent = [ab for ab in AtBat.query.all() if ab.team=="Dummy"]
            #abs_vs_left_or_right
            if len(abs_vs_left_or_right)<5:
                abs_vs_left_or_right = [ab for ab in AtBat.query.all() if ab.team=="Dummy"]
            

            hit_stdev_array = [{"temperature_abs":{"array":temperature_abs,"stdev":stdev([ab.result_stdev for ab in temperature_abs])}},
                {"abs_vs_team":{"array":abs_vs_team,"stdev":stdev([ab.result_stdev for ab in abs_vs_team])}},
                {"precipitation_abs":{"array":precipitation_abs,"stdev":stdev([ab.result_stdev for ab in precipitation_abs])}},
                {"cloud_or_sun_abs":{"array":cloud_or_sun_abs,"stdev":stdev([ab.result_stdev for ab in cloud_or_sun_abs])}},
                {"wind_speed_abs":{"array":wind_speed_abs,"stdev":stdev([ab.result_stdev for ab in wind_speed_abs])}},
                {"wind_direction_abs":{"array":wind_direction_abs,"stdev":stdev([ab.result_stdev for ab in wind_direction_abs])}},
                {"at_stadium":{"array":at_stadium,"stdev":stdev([ab.result_stdev for ab in at_stadium])}},
                {"abs_at_time":{"array":abs_at_time,"stdev":stdev([ab.result_stdev for ab in abs_at_time])}},
                {"abs_on_day":{"array":abs_on_day,"stdev":stdev([ab.result_stdev for ab in abs_on_day])}},
                {"latest_games":{"array":latest_games,"stdev":stdev([ab.result_stdev for ab in latest_games])}},
                {"latest_home_or_away_games":{"array":latest_home_or_away_games,"stdev":stdev([ab.result_stdev for ab in latest_home_or_away_games])}},
                {"abs_vs_opponent":{"array":abs_vs_opponent,"stdev":stdev([ab.result_stdev for ab in abs_vs_opponent])}},
                {"abs_vs_left_or_right":{"array":abs_vs_left_or_right,"stdev":stdev([ab.result_stdev for ab in abs_vs_left_or_right])}}
                ]

            ipdb.set_trace()



    #make a draftkings algorithm

        #roster
            #2 P
            #1 C
            #1 1B
            #1 2B
            #1 SS
            #1 3B
            #3 OF
        
        #Salary Cap = $50,000

    
                    
   

    

    # sorted_bets = sorted(bets,key=itemgetter('perc'))[-10:]
    # sort_by_diff = sorted(bets,key=itemgetter('diff'))[-10:]
    # sorted_by_total_value = sorted(games_in_a_row,key=itemgetter('total_value'))[-20:]
    # sorted_by_total_value = [item for item in sorted_by_total_value if item["total_value"]>.8]
    # sorted_by_total_value.reverse()
    # sorted_by_games_straight = sorted(games_in_a_row,key=itemgetter('games_straight'))[-20:]
    # sorted_by_games_straight.reverse()
    # sorted_by_games_straight = [item for item in sorted_by_games_straight if item["games_straight"]>4]

    # weekday_games_sorted = sorted(weekday_games,key=itemgetter("value"))[-20:]
    # weekday_games_sorted.reverse()
        
    # for item in sorted_bets:
    #     name = item["name"]
    #     prop = item["prop"]
    #     line = item["line"]
    #     projected = item["projected"]
    #     bet = item["bet"]
    #     print(f"{name} {bet} in {prop}. Projected: {projected}, Line: {line}")

    # print("\nBets sorted by difference\n")

    # for item in sort_by_diff:
    #     name = item["name"]
    #     prop = item["prop"]
    #     line = item["line"]
    #     projected = item["projected"]
    #     bet = item["bet"]
    #     print(f"{name} {bet} in {prop}. Projected: {projected}, Line: {line}")


    # print("\nBets with lowest consistency")

    # for item in lowest_consistency:
    #     name=item["name"]
    #     stat = item["stat"]
    #     value = item["value"]
    #     line = item["line"]
    #     print(f"{name} {line} {stat}: {value}")

    # print("\nBets with highest consistency")

    # for item in highest_consistency:
    #     name=item["name"]
    #     stat = item["stat"]
    #     value = item["value"]
    #     line = item["line"]
    #     print(f"{name} {line} {stat}: {value}")


    # print("\nHigh value teasers\n")

    # for index, item in enumerate(sorted_high_value_teasers):
    #     name=item["name"]
    #     prop = item["prop"]
    #     value = item["value"]
    #     teaser = item["teaser"]
    #     modifier = item["modifier"]
    #     proj = item["proj"]
    #     data_points = item["data_points"]
    #     games_straight = item["games_straight"]

    #     player_data_list = FinalBet.query.filter(FinalBet.date==full_date,FinalBet.algorithm=="B",FinalBet.category=="high_value",FinalBet.category_value==(index+1)).all()

    #     if len(player_data_list) > 0:
    #         player_data = player_data_list[0]
    #         player_data.name = name
    #         player_data.prop = prop
    #         player_data.line = teaser
    #     else:
    #         player = FinalBet(
    #             category = "high_value",
    #             algorithm = "B",
    #             category_value = index+1,
    #             date = full_date,
    #             name = name,
    #             prop = prop,
    #             line = teaser
    #         )
    #         db.session.add(player)
    #     db.session.commit()

    #     print(f"{index+1}: {name} {teaser} {prop}: {value} (Modifier:{modifier}, Projection:{proj}, Data Points:{data_points}, Games Straight:{games_straight})")

    # print("\nLow value teasers\n")

    # for index, item in enumerate(sorted_low_value_teasers):
    #     name=item["name"]
    #     prop = item["prop"]
    #     value = item["value"]
    #     teaser = item["teaser"]
    #     modifier = item["modifier"]
    #     proj = item["proj"]
    #     data_points = item["data_points"]
    #     games_straight = item["games_straight"]

    #     player_data_list = FinalBet.query.filter(FinalBet.date==full_date,FinalBet.algorithm=="B",FinalBet.category=="low_value",FinalBet.category_value==(index+1)).all()
    #     if len(player_data_list) > 0:
    #         player_data = player_data_list[0]
    #         player_data.name = name
    #         player_data.prop = prop
    #         player_data.line = teaser
    #     else:
    #         player = FinalBet(
    #             category = "low_value",
    #             algorithm = "B",
    #             category_value = index+1,
    #             date = full_date,
    #             name = name,
    #             prop = prop,
    #             line = teaser
    #         )
    #         db.session.add(player)
    #     db.session.commit()

    #     print(f"{index+1}: {name} {teaser} {prop}: {value} (Modifier:{modifier}, Projection:{proj}, Data Points:{data_points}, Games Straight:{games_straight})")


    # print("\nMost Games in a Row\n")

    # for index, item in enumerate(sorted_by_games_straight):
    #     name=item["name"]
    #     prop = item["prop"]
    #     value = item["value"]
    #     teaser = item["teaser"]
    #     modifier = item["modifier"]
    #     proj = item["proj"]
    #     data_points = item["data_points"]
    #     games_straight = item["games_straight"]

    #     player_data_list = FinalBet.query.filter(FinalBet.date==full_date,FinalBet.algorithm=="B",FinalBet.category=="games_in_a_row",FinalBet.category_value==(index+1)).all()
    #     if len(player_data_list) > 0:
    #         player_data = player_data_list[0]
    #         player_data.name = name
    #         player_data.prop = prop
    #         player_data.line = teaser
    #     else:
    #         player = FinalBet(
    #             category = "games_in_a_row",
    #             algorithm = "B",
    #             category_value = index+1,
    #             date = full_date,
    #             name = name,
    #             prop = prop,
    #             line = teaser
    #         )
    #         db.session.add(player)
    #     db.session.commit()

    #     print(f"{index+1}: {name} {teaser} {prop}: {value} (Modifier:{modifier}, Projection:{proj}, Data Points:{data_points}, Games Straight:{games_straight})")



    # print("\nRanked by Total Value\n")

    # for index, item in enumerate(sorted_by_total_value):
    #     name=item["name"]
    #     prop = item["prop"]
    #     value = item["value"]
    #     teaser = item["teaser"]
    #     modifier = item["modifier"]
    #     proj = item["proj"]
    #     data_points = item["data_points"]
    #     games_straight = item["games_straight"]
    #     total_value = item["total_value"]

    #     player_data_list = FinalBet.query.filter(FinalBet.date==full_date,FinalBet.algorithm=="B",FinalBet.category=="total_value",FinalBet.category_value==(index+1)).all()
    #     if len(player_data_list) > 0:
    #         player_data = player_data_list[0]
    #         player_data.name = name
    #         player_data.prop = prop
    #         player_data.line = teaser
    #     else:
    #         player = FinalBet(
    #             category = "total_value",
    #             algorithm = "B",
    #             category_value = index+1,
    #             date = full_date,
    #             name = name,
    #             prop = prop,
    #             line = teaser
    #         )
    #         db.session.add(player)
    #     db.session.commit()

    #     print(f"{index+1}: {name} {teaser} {prop}: {value} (Modifier:{modifier}, Projection:{proj}, Data Points:{data_points}, Games Straight:{games_straight}, Total Value:{total_value})")
        
        
    # print("\nWeekday Comparisons\n")

    # for index, item in enumerate(weekday_games_sorted):
    #     name = item["name"]
    #     prop = item["prop"]
    #     value = item["value"]
    #     line = item["line"]
    #     print(f"{index+1}: {name} {line} {prop}: {value}")

    # print("Injuries:")

    # for team,injuries in injured_list.items():
    #     if team in list_of_teams:
    #         print(f"{team}: {injuries}")

    # print("\nAlgo B")
    # print(time_string)
    # print('✅')

            



# category (high teaser, low teaser, games in a row, total value)
# category value (1,2,3,etc...)
# date
# player name
# prop (trb, points, assists)
# line