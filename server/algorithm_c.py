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
            


    # print("Start league wide stats")

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

    # dummy_abs = [ab for ab in AtBat.query.all() if ab.team=="Dummy"]


    #get game data

    # print("Finish League Wide Stats")


    # print("Start game data")

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



    teams = []
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

        if the_time_string.date()!=todays_time_string.date():
            break



        home = game.select('a')[1].text
        away = game.select('a')[0].text

        if home in teams or away in teams:
            continue

        print(f"{away} at {home}")

        
        play_by_play = box_score_data.select('#all_play_by_play')[0]

        comment = play_by_play.find(string=lambda string:isinstance(string, Comment))
        commentsoup = BeautifulSoup(comment , 'lxml')
        tops = commentsoup.select('tr.top_inning')
        bottoms= commentsoup.select('tr.bottom_inning')
        tops.extend(bottoms)

        
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

        todays_games.append(match)
        teams.append(home)
        teams.append(away)


        players_data = box_score_data.select('#all_lineups')[0]
        players_comment = players_data.find(string=lambda string:isinstance(string, Comment))
        players_soup = BeautifulSoup(players_comment , 'lxml')

        away_players_data = players_soup.select('#lineups_1')[0]
        home_players_data = players_soup.select('#lineups_2')[0]

        away_players = away_players_data.select('tr')
        home_players = home_players_data.select('tr')

        away_player_tables = box_score_data.select('.table_wrapper')[0]
        away_players_tables_comment = away_player_tables.find(string=lambda string:isinstance(string, Comment))
        away_players_tables_soup = BeautifulSoup(away_players_tables_comment , 'lxml')
        list_of_away_player_stats = away_players_tables_soup.select('tbody')[0].select('tr')

        home_player_tables = box_score_data.select('.table_wrapper')[1]
        home_players_tables_comment = home_player_tables.find(string=lambda string:isinstance(string, Comment))
        home_players_tables_soup = BeautifulSoup(home_players_tables_comment , 'lxml')
        list_of_home_player_stats = home_players_tables_soup.select('tbody')[0].select('tr')

        #find the player objects and add a temporary team column


        for player in away_players:
            name = unidecode(player.select('td')[1].text)
            try:
                if name[0]==" ":
                    name=name[1:]
            except IndexError:
                continue
                
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

                    for item in list_of_away_player_stats:
                        try:
                            item_name = unidecode(item.select('th')[0].select('a')[0].text)
                        except IndexError:
                            ipdb.set_trace()
                        if item_name==name:
                            item_abs = item.select('td')[0].text
                            item_hits = item.select('td')[2].text
                            if ("SB") in item.select('td')[-1].text:
                                starting_lineup_player.sbs = 1
                            else:
                                starting_lineup_player.sbs = 0
                            starting_lineup_player.hits = item_hits
                            starting_lineup_player.abs = item_abs
                            break
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
                    for item in list_of_home_player_stats:
                        item_name = unidecode(item.select('th')[0].select('a')[0].text)
                        if item_name==name:
                            item_abs = item.select('td')[0].text
                            item_hits = item.select('td')[2].text
                            if ("SB") in item.select('td')[-1].text:
                                starting_lineup_player.sbs = 1
                            else:
                                starting_lineup_player.sbs = 0
                            starting_lineup_player.hits = item_hits
                            starting_lineup_player.abs = item_abs
                            break
                    hitter_list.append(starting_lineup_player)
                # else:
                #     ipdb.set_trace()

    

    #values tested:
        # 1. Babip modifier : .1
        # 2. in play modifier : .7
        # 3. batter side modifier : 0 (then )
        # 4. number of abs : 30 (50,40)
        # 5. how many abs : 20
        # 6. first value comparer : .75

    test_range= [i/100 for i in range(5,51,5)]

    # test_range = [.01,.02,.03]
    test_values = []

    for test_value in test_range:

        bets = []
        number_of_abs = -140

        print(f'\n{test_value}\n')

    
        # print("Made it to the loop")
        for player in hitter_list:

            player_name = player.name
            player_team = player.team
            game = [game for game in todays_games if game.home==player_team or game.visitor==player_team][0]
            if game.home==player_team:
                other_team = game.visitor
            else:
                other_team = game.home
            
            #collect my own data about every game they've played in

            pitcher_object_list = [player for player in pitcher_list if player.team==other_team]
            if len(pitcher_object_list) > 0:
                pitcher_object = pitcher_object_list[0]
                pitcher_name=pitcher_object.name
                # hitter = 1
            


                # specific_time = datetime(2024,1,21,16,30,00)
                #and specific_time.time() < [game["time"] for game in todays_games if game["home"]==player_team or game["away"]==player_team][0]

                # if ([game.date.time() for game in game_list if game.home==player_team or game.visitor==player_team][0] > format_time)

                print(f"{player_name} ({player_team})")

                abs = [ab for ab in player.at_bats if ab.game]

                # print("Player abs collected")


                # print("Start Modifiers")

                #find info for babip modifier

                hitter_total_abs = [ab for ab in abs if ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result]
                hitter_balls_in_play = [ab for ab in hitter_total_abs if "Strikeout" not in ab.result and ab.result!="Home Run"]
                hitter_babip_numerator = len([ab for ab in hitter_balls_in_play if ab.result=="Triple" or ab.result=="Double" or ab.result=="Single"])

                try:
                    hitter_in_play_percentage = len(hitter_balls_in_play)/len(hitter_total_abs)
                except ZeroDivisionError:
                    hitter_in_play_percentage = league_in_play_percentage

                try:
                    hitter_babip = hitter_babip_numerator/len(hitter_balls_in_play)
                except ZeroDivisionError:
                    hitter_babip = league_babip

                #find percentage of balls in play by pitcher


                all_pitcher_abs = pitcher_object.at_bats
                pitcher_total_abs = [ab for ab in all_pitcher_abs if ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result]
                pitcher_balls_in_play = [ab for ab in pitcher_total_abs if "Strikeout" not in ab.result and ab.result!="Home Run"]
                pitcher_babip_numerator = len([ab for ab in pitcher_balls_in_play if ab.result=="Triple" or ab.result=="Double" or ab.result=="Single"])


                #pitcher in play % and babip


                try:
                    pitcher_in_play_percentage = len(pitcher_balls_in_play)/len(pitcher_total_abs)
                except ZeroDivisionError:
                    pitcher_in_play_percentage = league_in_play_percentage

                try:
                    pitcher_babip = pitcher_babip_numerator/len(pitcher_balls_in_play)
                except ZeroDivisionError:
                    pitcher_babip = league_babip


                if pitcher_object.arm==player.bat:

                    #pitchers avg when facing same side batter

                    total_abs_same = [ab for ab in all_pitcher_abs if ab.hitter.bat==pitcher_object.arm and "Walk" not in ab.result and "Sacrifice" not in ab.result and "Interference" not in ab.result and "Hit" not in ab.result]
                    abs_with_hit_same = len([ab for ab in total_abs_same if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run"])

                    try:
                        pitcher_same_avg = abs_with_hit_same/len(total_abs_same)
                    except ZeroDivisionError:
                        pitcher_same_avg = league_avg
                    #hitters avg when facing same side pitcher

                    same_side_abs = [ab for ab in abs if ab.pitcher.arm==player.bat and "Walk" not in ab.result and "Sacrifice" not in ab.result and "Interference" not in ab.result and "Hit" not in ab.result]
                    same_side_hits = len([ab for ab in same_side_abs if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run"])
                    
                    try:
                        hitter_same_avg = same_side_hits/len(same_side_abs)
                    except ZeroDivisionError:
                        hitter_same_avg = league_avg
                    batter_side_modifier = (0.9 * pitcher_same_avg/league_avg ) + (0.1 * hitter_same_avg/league_avg)

                else:

                    #pitchers average when facing opposite side batter

                    total_abs_opp = [ab for ab in all_pitcher_abs if ab.hitter.bat!=pitcher_object.arm and "Walk" not in ab.result and "Sacrifice" not in ab.result and "Interference" not in ab.result and "Hit" not in ab.result]
                    abs_with_hit_opp = len([ab for ab in total_abs_opp if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run"])

                    try:
                        pitcher_opposite_avg = abs_with_hit_opp/len(total_abs_opp)
                    except ZeroDivisionError:
                        pitcher_opposite_avg = league_avg
                    #hitters average when facing opposite side pitcher

                    oppo_taco_abs = [ab for ab in abs if ab.pitcher.arm!=player.bat and "Walk" not in ab.result and "Sacrifice" not in ab.result and "Interference" not in ab.result and "Hit" not in ab.result]
                    oppo_taco_hits = len([ab for ab in oppo_taco_abs if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run"])
                    try:
                        hitter_opposite_avg = oppo_taco_hits/len(oppo_taco_abs)
                    except ZeroDivisionError:
                        hitter_opposite_avg = league_avg
                    batter_side_modifier = (0.9 * pitcher_opposite_avg/league_avg ) + (0.1 * hitter_opposite_avg/league_avg)

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


                result_modifier = (.1 * babip_modifier + .7 * in_play_modifier + 0.1 * batter_side_modifier)
                # result_modifier = (babip_modifier + in_play_modifier + batter_side_modifier)/3


                # print("Got em")

                # print("Start collecting abs")
                
                
                #latest 25 abs at time
                upper_hour = game.date.hour+1
                lower_hour = game.date.hour-1
                minutes = game.date.minute
                upper_time = datetime(2023,2,1,upper_hour,minutes).time()
                lower_time = datetime(2023,2,1,lower_hour,minutes).time()
                abs_at_time = [ab for ab in abs if ab.game.date.time()<=upper_time and ab.game.date.time()>=lower_time][number_of_abs:]
                
                #last 25 abs on specific day
                current_day = current_date.weekday()
                abs_on_day = []
                for ab in abs:
                    if ab.game.date.weekday()==current_day:
                        abs_on_day.append(ab)

                abs_on_day = abs_on_day[number_of_abs:]


            
                #last 50 abs
                latest_games = [ab for ab in abs][number_of_abs:]


                #home/away games
                if game.home==player_team:
                    latest_home_or_away_abs = [ab for ab in abs if ab.game.home==player_team][number_of_abs:]
                else:
                    latest_home_or_away_abs = [ab for ab in abs if ab.game.visitor==player_team][number_of_abs:]
                

                
                #get latest matchups vs pitcher
                abs_vs_opponent = [ab for ab in abs if (ab.pitcher.name==pitcher_name)][number_of_abs:]

                #other things I need

                #abs vs lefty/righty 

                abs_vs_left_right = [ab for ab in abs if ab.pitcher.arm==pitcher_object.arm][number_of_abs:]

                #right-left modifier


                

                
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

                total_sb_modifier = .65 * sb_modifier + .35 * pitcher_sb_modifier

                #strikeout percentage (for pitchers)


                #create new implied batting average by multipying hitter 

                #babip
                    #compare pitchers allowed babip to hitter's babip



                #both pitchers and hitters



                #last 50 at stadium
                at_stadium = [ab for ab in abs if ab.game.location == game.location][number_of_abs:]

                #last 50 with wind direction

                if game.wind_direction == 400:
                    wind_direction_abs = [ab for ab in abs if ab.game.precipitation=="In Dome"][number_of_abs:]

                else:
                    wind_high = game.wind_direction + 22.5
                    wind_low = game.wind_direction - 22.5

                    wind_direction_abs = [ab for ab in abs if wind_low <= ab.game.wind_direction <= wind_high][number_of_abs:]

                    # ipdb.set_trace()

                #wind speed
                if len(game.wind_speed) > 0:
                    wind_speed_high = int(game.wind_speed) + 2
                    wind_speed_low = int(game.wind_speed) - 2

                    wind_speed_abs = [ab for ab in abs if wind_speed_low <= ab.game.wind_speed <= wind_speed_high][number_of_abs:]

                else:
                    wind_speed_abs = []

                #sunny/cloudy
                #Overcast, Sunny, Cloudy, In Dome
                if game.cloud_or_sun=="Cloudy" or game.cloud_or_sun=="Overcast":
                    cloud_or_sun_abs = [ab for ab in abs if ab.game.cloud_or_sun=="Cloudy" or ab.game.cloud_or_sun=="Overcast"][number_of_abs:]
                elif game.cloud_or_sun=="Sunny":
                    cloud_or_sun_abs = [ab for ab in abs if ab.game.cloud_or_sun=="Sunny"][number_of_abs:]
                else:
                    cloud_or_sun_abs = []


                #precipitation
                if game.precipitation=="Rain":
                    precipitation_abs = [ab for ab in abs if ab.game.precipitation=="Rain" or ab.game.precipitation=="Drizzle"][number_of_abs:]
                elif game.precipitation=="Snow":
                    precipitation_abs = [ab for ab in abs if ab.game.precipitation=="Snow"][number_of_abs:]
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

                the_temperature = int(game.temperature)

                if the_temperature <= freezing:
                    temperature_abs = [ab for ab in abs if the_temperature <= freezing][number_of_abs:]
                elif freezing < the_temperature <= real_cold:
                    temperature_abs = [ab for ab in abs if freezing < the_temperature <= real_cold][number_of_abs:]
                elif real_cold < the_temperature <= very_cold:
                    temperature_abs = [ab for ab in abs if real_cold < the_temperature <= very_cold][number_of_abs:]
                elif very_cold < the_temperature <= cold:
                    temperature_abs = [ab for ab in abs if very_cold < the_temperature <= cold][number_of_abs:]
                elif cold < the_temperature <= nice:
                    temperature_abs = [ab for ab in abs if cold < the_temperature <= nice][number_of_abs:]
                elif nice < the_temperature <= hot:
                    temperature_abs = [ab for ab in abs if nice < the_temperature <= hot][number_of_abs:]
                elif hot < the_temperature <= too_hot:
                    temperature_abs = [ab for ab in abs if hot < the_temperature <= too_hot][number_of_abs:]
                else:
                    temperature_abs = [ab for ab in abs if the_temperature > too_hot][number_of_abs:]

                #vs team
                abs_vs_team = [ab for ab in abs if ab.game.home==other_team or ab.game.visitor==other_team][number_of_abs:]



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
                # latest_home_or_away_abs.extend(games_at_time)
                # latest_home_or_away_abs.extend(games_vs_opponent)
                # if injury:
                #     latest_home_or_away_abs.extend(games_with_injury[-3:])
                # if opponent_injury:
                #     latest_home_or_away_abs.extend(games_with_opp_injury[-3:])
                # latest_home_or_away_abs.extend(games_on_day)
                # latest_home_or_away_abs.extend(rest_days)

                # latest_home_or_away_abs.reverse()

                #find most similar game


                # new_game_list = set(latest_home_or_away_abs)

                # uniq_game_list = list(new_game_list)


                # uniq_game_list = [game for game in uniq_game_list]


                # print("Start on big list of games")

                #values to put into stdev formula

                # #temperature_abs
                # if len(temperature_abs)<4:
                #     temperature_abs = dummy_abs
                # #abs_vs_team
                # if len(abs_vs_team)<4:
                #     abs_vs_team = dummy_abs
                # #precipitation_abs (if greater than 0)
                # if len(precipitation_abs)<4:
                #     precipitation_abs = dummy_abs
                # #cloud_or_sun_abs
                # if len(cloud_or_sun_abs)<4:
                #     cloud_or_sun_abs = dummy_abs
                # #wind_speed_abs
                # if len(wind_speed_abs)<4:
                #     wind_speed_abs = dummy_abs
                # #wind_direction_abs
                # if len(wind_direction_abs)<4:
                #     wind_direction_abs = dummy_abs
                # #at_stadium
                # if len(at_stadium)<4:
                #     at_stadium = dummy_abs
                # #abs_at_time
                # if len(abs_at_time)<4:
                #     abs_at_time = dummy_abs
                # #abs_on_day
                # if len(abs_on_day)<4:
                #     abs_on_day = dummy_abs
                # #latest_games
                # if len(latest_games)<4:
                #     latest_games = dummy_abs
                # #latest_home_or_away_abs
                # if len(latest_home_or_away_abs)<4:
                #     latest_home_or_away_abs = dummy_abs
                # #abs_vs_opponent
                # if len(abs_vs_opponent)<4:
                #     abs_vs_opponent = dummy_abs
                # #abs_vs_left_right
                # if len(abs_vs_left_right)<4:
                #     abs_vs_left_right = dummy_abs

                # print("Cancelled out the dummies")
                

                # hit_stdev_array = [{"temperature_abs":{"array":temperature_abs,"stdev":stdev([ab.result_stdev for ab in temperature_abs])}},
                #     {"abs_vs_team":{"array":abs_vs_team,"stdev":stdev([ab.result_stdev for ab in abs_vs_team])}},
                #     {"precipitation_abs":{"array":precipitation_abs,"stdev":stdev([ab.result_stdev for ab in precipitation_abs])}},
                #     {"cloud_or_sun_abs":{"array":cloud_or_sun_abs,"stdev":stdev([ab.result_stdev for ab in cloud_or_sun_abs])}},
                #     {"wind_speed_abs":{"array":wind_speed_abs,"stdev":stdev([ab.result_stdev for ab in wind_speed_abs])}},
                #     {"wind_direction_abs":{"array":wind_direction_abs,"stdev":stdev([ab.result_stdev for ab in wind_direction_abs])}},
                #     {"at_stadium":{"array":at_stadium,"stdev":stdev([ab.result_stdev for ab in at_stadium])}},
                #     {"abs_at_time":{"array":abs_at_time,"stdev":stdev([ab.result_stdev for ab in abs_at_time])}},
                #     {"abs_on_day":{"array":abs_on_day,"stdev":stdev([ab.result_stdev for ab in abs_on_day])}},
                #     {"latest_games":{"array":latest_games,"stdev":stdev([ab.result_stdev for ab in latest_games])}},
                #     {"latest_home_or_away_abs":{"array":latest_home_or_away_abs,"stdev":stdev([ab.result_stdev for ab in latest_home_or_away_abs])}},
                #     {"abs_vs_opponent":{"array":abs_vs_opponent,"stdev":stdev([ab.result_stdev for ab in abs_vs_opponent])}},
                #     {"abs_vs_left_right":{"array":abs_vs_left_right,"stdev":stdev([ab.result_stdev for ab in abs_vs_left_right])}}
                #     ]

                how_many_abs = 8


                hit_stdev_array = [{"name":"temperature_abs","array":temperature_abs,"stdev":stdev([ab.result_stdev for ab in temperature_abs]) if len(temperature_abs)>how_many_abs else 500},
                    {"name":"abs_vs_team","array":abs_vs_team,"stdev":stdev([ab.result_stdev for ab in abs_vs_team]) if len(abs_vs_team)>how_many_abs else 500},
                    {"name":"precipitation_abs","array":precipitation_abs,"stdev":stdev([ab.result_stdev for ab in precipitation_abs]) if len(precipitation_abs)>how_many_abs else 500},
                    {"name":"cloud_or_sun_abs","array":cloud_or_sun_abs,"stdev":stdev([ab.result_stdev for ab in cloud_or_sun_abs]) if len(cloud_or_sun_abs)>how_many_abs else 500},
                    {"name":"wind_speed_abs","array":wind_speed_abs,"stdev":stdev([ab.result_stdev for ab in wind_speed_abs]) if len(wind_speed_abs)>how_many_abs else 500},
                    {"name":"wind_direction_abs","array":wind_direction_abs,"stdev":stdev([ab.result_stdev for ab in wind_direction_abs]) if len(wind_direction_abs)>how_many_abs else 500},
                    {"name":"at_stadium","array":at_stadium,"stdev":stdev([ab.result_stdev for ab in at_stadium]) if len(at_stadium)>how_many_abs else 500},
                    {"name":"abs_at_time","array":abs_at_time,"stdev":stdev([ab.result_stdev for ab in abs_at_time]) if len(abs_at_time)>how_many_abs else 500},
                    {"name":"abs_on_day","array":abs_on_day,"stdev":stdev([ab.result_stdev for ab in abs_on_day]) if len(abs_on_day)>how_many_abs else 500},
                    {"name":"latest_games","array":latest_games,"stdev":stdev([ab.result_stdev for ab in latest_games]) if len(latest_games)>how_many_abs else 500},
                    {"name":"latest_home_or_away_abs","array":latest_home_or_away_abs,"stdev":stdev([ab.result_stdev for ab in latest_home_or_away_abs]) if len(latest_home_or_away_abs)>how_many_abs else 500},
                    {"name":"abs_vs_opponent","array":abs_vs_opponent,"stdev":stdev([ab.result_stdev for ab in abs_vs_opponent]) if len(abs_vs_opponent)>how_many_abs else 500},
                    {"name":"abs_vs_left_right","array":abs_vs_left_right,"stdev":stdev([ab.result_stdev for ab in abs_vs_left_right]) if len(abs_vs_left_right)>how_many_abs else 500}
                    ]

                sb_stdev_array = [{"name":"temperature_abs","array":temperature_abs,"stdev":stdev([ab.sb for ab in temperature_abs]) if len(temperature_abs)>how_many_abs else 500},
                    {"name":"abs_vs_team","array":abs_vs_team,"stdev":stdev([ab.sb for ab in abs_vs_team]) if len(abs_vs_team)>how_many_abs else 500},
                    {"name":"precipitation_abs","array":precipitation_abs,"stdev":stdev([ab.sb for ab in precipitation_abs]) if len(precipitation_abs)>how_many_abs else 500},
                    {"name":"cloud_or_sun_abs","array":cloud_or_sun_abs,"stdev":stdev([ab.sb for ab in cloud_or_sun_abs]) if len(cloud_or_sun_abs)>how_many_abs else 500},
                    {"name":"wind_speed_abs","array":wind_speed_abs,"stdev":stdev([ab.sb for ab in wind_speed_abs]) if len(wind_speed_abs)>how_many_abs else 500},
                    {"name":"wind_direction_abs","array":wind_direction_abs,"stdev":stdev([ab.sb for ab in wind_direction_abs]) if len(wind_direction_abs)>how_many_abs else 500},
                    {"name":"at_stadium","array":at_stadium,"stdev":stdev([ab.sb for ab in at_stadium]) if len(at_stadium)>how_many_abs else 500},
                    {"name":"abs_at_time","array":abs_at_time,"stdev":stdev([ab.sb for ab in abs_at_time]) if len(abs_at_time)>how_many_abs else 500},
                    {"name":"abs_on_day","array":abs_on_day,"stdev":stdev([ab.sb for ab in abs_on_day]) if len(abs_on_day)>how_many_abs else 500},
                    {"name":"latest_games","array":latest_games,"stdev":stdev([ab.sb for ab in latest_games]) if len(latest_games)>how_many_abs else 500},
                    {"name":"latest_home_or_away_abs","array":latest_home_or_away_abs,"stdev":stdev([ab.sb for ab in latest_home_or_away_abs]) if len(latest_home_or_away_abs)>how_many_abs else 500},
                    {"name":"abs_vs_opponent","array":abs_vs_opponent,"stdev":stdev([ab.sb for ab in abs_vs_opponent]) if len(abs_vs_opponent)>how_many_abs else 500},
                    {"name":"abs_vs_left_right","array":abs_vs_left_right,"stdev":stdev([ab.sb for ab in abs_vs_left_right]) if len(abs_vs_left_right)>how_many_abs else 500}
                    ]

                # if player_name=="Connor Wong" or player_name=="Christian Arroyo":
                #     ipdb.set_trace()   
            

                first_value = 0
                second_value = 0
                third_value = 0
                fourth_value = 0
                fifth_value = 0
                sixth_value = 0
                seventh_value = 0
                eigth_value = 0
                ninth_value = 0
                tenth_value = 0

                # print("made a sorted list")

            

                new_stdev_list = []
                for value in hit_stdev_array:
                    if value["stdev"] < .45:
                        new_stdev_list.append(value)

                if len(new_stdev_list) > 0:

                    # print("We've got the new one. Start big giant")

                    # ipdb.set_trace()

                    big_giant = abs_vs_opponent.copy()
                    big_giant.extend(abs_vs_left_right)
                    big_giant.extend(latest_home_or_away_abs)
                    big_giant.extend(latest_games)
                    big_giant.extend(abs_on_day)
                    big_giant.extend(abs_at_time)
                    big_giant.extend(at_stadium)
                    big_giant.extend(wind_direction_abs)
                    big_giant.extend(wind_speed_abs)
                    big_giant.extend(cloud_or_sun_abs)
                    big_giant.extend(precipitation_abs)
                    big_giant.extend(abs_vs_team)
                    big_giant.extend(temperature_abs)
                

                    abs_in_common = []
                    for item in big_giant:
                        i = 0
                        if item not in abs_in_common and item.hitter.name==player_name:
                            for secondary in big_giant:
                                if item==secondary:
                                    i+=1
                            if i > 4:
                                abs_in_common.append({"item":item,"how_many":i})

                    if len(abs_in_common) > how_many_abs:
                    
                        sorted_abs_in_common = sorted(abs_in_common,key=itemgetter('how_many'))
                        sorted_abs_in_common.reverse()

                        high_ab_in_common = sorted_abs_in_common[0]["how_many"]
                        diffy = high_ab_in_common-.4*high_ab_in_common

                        new_sorted_abs_in_common = [ab for ab in sorted_abs_in_common if ab["how_many"] > diffy][number_of_abs:]
                        final_sorted_abs_in_common = {"name":"abs_in_common","array":[ab["item"] for ab in new_sorted_abs_in_common],"stdev":stdev([ab["item"].result_stdev for ab in new_sorted_abs_in_common])}
                        if len(sorted_abs_in_common) > 5:
                            new_stdev_list.insert(0,final_sorted_abs_in_common)

                    new_stdev_list = sorted(new_stdev_list,key=itemgetter('stdev'))

                    # print("Big giant done. Create player_value")

                    first_value_comparer = .55


                    if len(new_stdev_list)==1:
                        first_value = 1.15 * mean([ab.result_stdev for ab in new_stdev_list[0]["array"]])
                    elif len(new_stdev_list)>1:
                        if len(new_stdev_list)==2:
                            first_value = .65 * mean(ab.result_stdev for ab in new_stdev_list[0]["array"])
                            second_value = .3 * mean(ab.result_stdev for ab in new_stdev_list[1]["array"]) 
                        elif len(new_stdev_list)==3:
                            first_value = first_value_comparer * mean(ab.result_stdev for ab in new_stdev_list[0]["array"])
                            second_value = .25 * mean(ab.result_stdev for ab in new_stdev_list[1]["array"]) 
                            third_value = .15 * mean(ab.result_stdev for ab in new_stdev_list[2]["array"]) 
                        elif len(new_stdev_list)==4:
                            first_value = first_value_comparer * mean(ab.result_stdev for ab in new_stdev_list[0]["array"])
                            second_value = .25 * mean(ab.result_stdev for ab in new_stdev_list[1]["array"]) 
                            third_value = .1 * mean(ab.result_stdev for ab in new_stdev_list[2]["array"]) 
                            fourth_value = .05 * mean(ab.result_stdev for ab in new_stdev_list[3]["array"])
                        elif len(new_stdev_list)==5:
                            first_value = first_value_comparer * mean(ab.result_stdev for ab in new_stdev_list[0]["array"])
                            second_value = .225 * mean(ab.result_stdev for ab in new_stdev_list[1]["array"]) 
                            third_value = .1 * mean(ab.result_stdev for ab in new_stdev_list[2]["array"]) 
                            fourth_value = .05 * mean(ab.result_stdev for ab in new_stdev_list[3]["array"])
                            fifth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[4]["array"])
                        elif len(new_stdev_list)==6:
                            first_value = first_value_comparer * mean(ab.result_stdev for ab in new_stdev_list[0]["array"])
                            second_value = .2 * mean(ab.result_stdev for ab in new_stdev_list[1]["array"]) 
                            third_value = .1 * mean(ab.result_stdev for ab in new_stdev_list[2]["array"]) 
                            fourth_value = .05 * mean(ab.result_stdev for ab in new_stdev_list[3]["array"])
                            fifth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[4]["array"])
                            sixth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[5]["array"])
                        elif len(new_stdev_list)==7:
                            first_value = first_value_comparer * mean(ab.result_stdev for ab in new_stdev_list[0]["array"])
                            second_value = .175 * mean(ab.result_stdev for ab in new_stdev_list[1]["array"]) 
                            third_value = .1 * mean(ab.result_stdev for ab in new_stdev_list[2]["array"]) 
                            fourth_value = .05 * mean(ab.result_stdev for ab in new_stdev_list[3]["array"])
                            fifth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[4]["array"])
                            sixth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[5]["array"])
                            seventh_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[6]["array"])
                        elif len(new_stdev_list)==8:
                            first_value = first_value_comparer * mean(ab.result_stdev for ab in new_stdev_list[0]["array"])
                            second_value = .175 * mean(ab.result_stdev for ab in new_stdev_list[1]["array"]) 
                            third_value = .1 * mean(ab.result_stdev for ab in new_stdev_list[2]["array"]) 
                            fourth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[3]["array"])
                            fifth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[4]["array"])
                            sixth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[5]["array"])
                            seventh_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[6]["array"])
                            eigth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[7]["array"])
                        elif len(new_stdev_list)==9:
                            first_value = first_value_comparer * mean(ab.result_stdev for ab in new_stdev_list[0]["array"])
                            second_value = .175 * mean(ab.result_stdev for ab in new_stdev_list[1]["array"]) 
                            third_value = .05 * mean(ab.result_stdev for ab in new_stdev_list[2]["array"]) 
                            fourth_value = .05 * mean(ab.result_stdev for ab in new_stdev_list[3]["array"])
                            fifth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[4]["array"])
                            sixth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[5]["array"])
                            seventh_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[6]["array"])
                            eigth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[7]["array"])
                            ninth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[8]["array"])
                        elif len(new_stdev_list)>=10:
                            first_value = first_value_comparer * mean(ab.result_stdev for ab in new_stdev_list[0]["array"])
                            second_value = .175 * mean(ab.result_stdev for ab in new_stdev_list[1]["array"]) 
                            third_value = .05 * mean(ab.result_stdev for ab in new_stdev_list[2]["array"]) 
                            fourth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[3]["array"])
                            fifth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[4]["array"])
                            sixth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[5]["array"])
                            seventh_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[6]["array"])
                            eigth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[7]["array"])
                            ninth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[8]["array"])
                            tenth_value = .025 * mean(ab.result_stdev for ab in new_stdev_list[9]["array"])
                        else:
                            continue

                    sb_stdev_list = sorted(sb_stdev_array,key=itemgetter('stdev'))

                    sb_value = mean(game.sb for game in sb_stdev_list[0]["array"])

                    sb_total_value = sb_value * total_sb_modifier


                    hit_formula = first_value + second_value + third_value + fourth_value + fifth_value + sixth_value + seventh_value + eigth_value + ninth_value + tenth_value
                    # hit_formula = mean(ab.result_stdev for ab in new_stdev_list[0]["array"])
                
                    player_value = 1-test_value * hit_formula * result_modifier + test_value * sb_total_value

                    bets.append({"name":player_name,"value":round(player_value,4),"hits":player.hits,"abs":player.abs,"sbs":player.sbs,"first":new_stdev_list[0]["name"],"stdev_1":new_stdev_list[0]["stdev"],"second":new_stdev_list[1]["name"],"stdev_2":new_stdev_list[1]["stdev"]})

                    # print("Nice. On to the next")

        sorted_bets = sorted(bets,key=itemgetter('stdev_1'))
        sorted_by_value_bets = sorted(bets,key=itemgetter('value'))
        mid_value = median([a_value["value"] for a_value in sorted_by_value_bets])
        iterator = 0
        list_value = 0

        for bet in sorted_bets:
            if bet["value"] > mid_value:
                list_value+=1
            if (int(bet["abs"]) == 0):
                response = "🏖️"
            elif ((bet["value"]) > mid_value and int(bet["hits"]) > 0 or int(bet["sbs"]) > 0) or ((bet["value"]) < mid_value and int(bet["hits"]) == 0):
                if (int(bet["hits"]) > 0 or int(bet["sbs"]) > 0) and bet["value"] > mid_value:
                    response = "⬆️✅"
                    if list_value <= 30:
                        iterator+=1
                else:
                    response = "👇🏽✅"
            else:
                if int(bet["hits"]) == 0 and bet["value"] > mid_value:
                    response = "⬆️❌"
                else:
                    response = "👇🏽❌"

            if bet["value"] > mid_value:
                name = bet["name"]
                value = bet["value"]
                hits = bet["hits"]
                at_bats = bet["abs"]
                sbs = bet["sbs"]
                first = bet["first"]
                second = bet["second"]
                stdev_1 = bet["stdev_1"]
                stdev_2 = bet["stdev_2"]
                string_beginning = (f"{name} : {value} ({hits}/{at_bats}) Sb's: {sbs} {first}:{round(stdev_1,4)}, {second}:{round(stdev_2,4)}")
                string_output = string_beginning.ljust(100,'.')
                print(f"{string_output}{response}")
                    
        percentage = round((iterator/30)*100,3)

        test_value_dict = {"value":test_value, "percentage":percentage}

        test_values.append(test_value_dict)

    sorted_test_values = sorted(test_values,key=itemgetter('percentage'))
    sorted_test_values.reverse()
    for item in sorted_test_values:
        value = item["value"]
        percentage = item["percentage"]
        print(f'{value} : {percentage}%')


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