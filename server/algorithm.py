from app import *
from statistics import mean,mode,median,stdev
from bs4 import BeautifulSoup
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


    def random_number(salary):
        counter = 20
        try:
            value = round(float(salary),2)
            array = []
            while counter > value:
                final_value = round(counter/20,2)
                array.append(round(float(final_value),2))
                counter-=.5
        except ValueError:
            array = [0,0,0]
        

        return sample(array,1)[0]



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
        "Arizona D'Backs":"Chase Field",
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
            

    #get game data


    #find league average babip over last 100k abs

    league_abs = AtBat.query.all()[-100000:]
    thousand_games = Game.query.all()[-100:]

    league_avg_babip_numerator = len([ab for ab in league_abs if ab.result=="Triple" or ab.result=="Double" or ab.result=="Single"])
    league_avg_babip_denominator = len([ab for ab in league_abs if "Strikeout" not in ab.result and ab.result!="Home Run" and ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result])
    league_babip = league_avg_babip_numerator/league_avg_babip_denominator

    league_avg_abs = [ab for ab in league_abs if ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result]
    league_avg_hits = len([ab for ab in league_avg_abs if ab.result=="Home Run" or ab.result=="Triple" or ab.result=="Double" or ab.result=="Single"])

    league_avg = league_avg_hits/len(league_avg_abs)

    # league_avg_ks
    list_of_ks = []
    for a_game in thousand_games:
        abs_to_count = [ab for ab in a_game.at_bats if ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result]
        ks = [ab for ab in a_game.at_bats if "Strikeout" in ab.result]
        list_of_ks.append(len(ks)/len(abs_to_count))
    league_avg_ks = mean(list_of_ks)

    # league_avg_innings_pitched
    # list_of_outs = []
    # for a_game in thousand_games:
    #     home = a_game.home
    #     away = a_game.visitor
    #     ab1_home = [ab for ab in a_game.at_bats if away==ab.team][0]
    #     ab1_away = [ab for ab in a_game.at_bats if home==ab.team][0]
    #     outs = [ab for ab in a_game.at_bats if "Out" in ab.result or "out" in ab.result or "Pop" in ab.result or "Choice" in ab.result or "Fly" in ab.result]
    #     pitcher_1_outs = len([ab for ab in outs if ab.pitcher==ab1_home.pitcher])
    #     pitcher_2_outs = len([ab for ab in outs if ab.pitcher==ab1_away.pitcher])
    #     list_of_outs.append(pitcher_1_outs)
    #     list_of_outs.append(pitcher_2_outs)
    # league_avg_outs = mean(list_of_outs)


    league_in_play_percentage = league_avg_babip_denominator/len(league_abs)


    league_on_first_abs = [ab for ab in league_abs if ab.result=="Single" or ab.result=="Walk" or ab.result=="Hit" or "Reached" in ab.result or "Choice" in ab.result]

    league_sb_abs = len([ab for ab in league_on_first_abs if ab.sb_att>=1])

    league_sb_perc = league_sb_abs/len(league_on_first_abs)

    league_sb_attempts = [ab for ab in AtBat.query.all() if ab.sb_att > 0]
    league_sb_abs = len([ab for ab in league_sb_attempts if ab.sb > 0])

    league_sb_success = league_sb_abs/len(league_sb_attempts)





    #schedule_page_url = f"https://rotogrinders.com/lineups/mlb?date={year_string}-{month_string}-{day_string}&site=draftkings"
    schedule_page_url = "https://rotogrinders.com/lineups/mlb?site=draftkings"
    schedule_page = requests.get(schedule_page_url, headers = {'User-Agent':"Mozilla/5.0"})
    schedule = BeautifulSoup(schedule_page.text, 'html.parser')
    
    games = schedule.select('div.module')

    hitter_list = []
    pitcher_list = []
    game_list = []
    team_list = []

    for game in games:


        try:
            header = game.select('div.module-header')[0]
        except IndexError:
            continue

        away_team = header.select('div.team-nameplate')[0].select('span')[0]
        home_team = header.select('div.team-nameplate')[1].select('span')[0]
        away = away_team.select('span')[0].text + ' ' + away_team.select('span')[1].text
        if away=="Arizona Diamondbacks":
            away="Arizona D'Backs"
        home = home_team.select('span')[0].text + ' ' + home_team.select('span')[1].text
        if home=="Arizona Diamondbacks":
            home="Arizona D'Backs"

        if home=="Detroit Tigers":
            continue
        

        time = header.select('span')[1].text
        time_hour = time.split(":")[0]
        try:
            final_time = datetime.strptime(date_string + (' ') + (' ').join(time.split(' ')[0:2]),"%A, %B %d, %Y %I:%M %p")
        except ValueError:
            time = header.select('span')[0].text
            time_hour = time.split(":")[0]
            final_time = datetime.strptime(date_string + (' ') + (' ').join(time.split(' ')[0:2]),"%A, %B %d, %Y %I:%M %p")
        # if final_time > datetime(2024,4,3,16,6) or (datetime(2024,4,3,15,00) <= final_time <= datetime(2024,4,3,15,50)):
        #     continue

        

       


        # if final_time > datetime(2024,4,5,14,30):
        #     continue

        team_list.append(away)
        team_list.append(home)
        stadium = stadiums[home]

        weather_thing = "stuff"

        sun = header.select("i.sunny")
        if len(sun) > 0:
                cloud_or_sun = "Sunny"
        else:
            cloud_or_sun = "Cloudy"

        weather = game.select('.weather-bar')[0]
        try:
            wind_temps = weather.select('.weather-bar-temps')[0]
        except IndexError:
            weather_thing = "in a dome"
        if "in a dome" in weather.text or weather_thing == "in a dome":
            final_wind_direction = 400
            temperature = 70
            precipitation = "No Precipitation"
            wind_speed = 0
            cloud_or_sun = "In Dome"
        else:
            temperature = int(wind_temps.select('span')[3].text.replace('°',''))
            wind_direction = wind_temps.select('span')[0].select('span')[0].text
            wind_speed = int(wind_temps.select('span')[0].select('span')[1].text.split(' ')[1])
            wind_factor = wind_correction_factors[stadium]
            hours_list = weather.select('div.weather-bar-item')
            sun = game.select('.icn-sunny')
            


            #wind directions are out towards these directions
                # 0 = South
                # 90 = West
                # 180 = North
                # 270 = East


            if wind_direction == "N":
                wind_value = 0
            elif wind_direction == "NNE":
                wind_value = 22.5
            elif wind_direction == "NE":
                wind_value = 45
            elif wind_direction == "ENE":
                wind_value = 67.5
            elif wind_direction == "E":
                wind_value = 90
            elif wind_direction == "ESE":
                wind_value = 112.5
            elif wind_direction == "SE":
                wind_value = 135
            elif wind_direction == "SSE":
                wind_value = 157.5
            elif wind_direction == "S":
                wind_value = 180
            elif wind_direction == "SSW":
                wind_value = 202.5
            elif wind_direction =="SW":
                wind_value = 225
            elif wind_direction == "WSW":
                wind_value = 247.5
            elif wind_direction == "W":
                wind_value = 270
            elif wind_direction == "WNW":
                wind_value = 292.5
            elif wind_direction =="NW":
                wind_value = 315
            elif wind_direction == "NNW":
                wind_value = 337.5



            if wind_factor=="Dome":
                final_wind_direction = 400
            else:
                final_wind_direction = wind_value - wind_factor
                if final_wind_direction < 0:
                    final_wind_direction = 360 + final_wind_direction

            

            for hour in hours_list:
                percent = int(hour.select('span')[0].text.replace("%",""))
                game_time = (hour.select('span')[1].text.replace('m','').replace('a','').replace('p',''))
                if game_time==time_hour:
                    if percent >= 40 and temperature > 35:
                        precipitation = "Rain"
                    elif percent >= 40 and temperature <=35:
                        precipitation = "Snow"
                    else:
                        precipitation = "No Precipitation"


        match = Game(
            date = final_time,
            home = home,
            visitor = away,
            precipitation = precipitation,
            wind_direction = int(final_wind_direction),
            wind_speed = int(wind_speed),
            temperature = int(temperature),
            cloud_or_sun = cloud_or_sun,
            location = stadium
        )
        game_list.append(match)

        

        #away players

        away_lineup = game.select('div.lineup-card')[0]
        home_lineup = game.select('div.lineup-card')[1]
        away_pitcher = away_lineup.select('div.lineup-card-header')[0]
        home_pitcher = home_lineup.select('div.lineup-card-header')[0]
        away_hitters = away_lineup.select('ul.lineup-card-players')[0].select('li')
        home_hitters = home_lineup.select('ul.lineup-card-players')[0].select('li')



        def add_pitcher(pitcher_object,home_or_away):
            pitcher_object.salary = salary
            pitcher_object.team = home_or_away
            hitter_array = []
            sb_modifier_array = []
            for ab in pitcher_object.at_bats:
                hitter = ab.hitter.name
                try:
                    hitter_object = Hitter.query.filter(Hitter.name==hitter)[0]
                except IndexError:
                    ipdb.set_trace()
                if hitter not in hitter_array:
                    hitter_array.append(hitter)
                    sb_modifier_abs = [ab for ab in pitcher_object.at_bats if ab.hitter.name==hitter]
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
            pitcher_sb_attempts = [ab for ab in pitcher_object.at_bats if ab.sb_att > 0]
            pitcher_sb_abs = len([ab for ab in pitcher_sb_attempts if ab.sb > 0])
            if len(pitcher_sb_attempts) > 0:
                pitcher_sb_success = (pitcher_sb_abs/len(pitcher_sb_attempts))/league_sb_success
            else: 
                pitcher_sb_success = 1
            sb_modifier = pitcher_sb_success*.7 + sb_modifier_final*.3
            pitcher_object.sb_modifier = sb_modifier
            pitcher_object.position = "SP"
            pitcher_list.append(pitcher_object)

        name = unidecode(away_pitcher.select('a')[0].text)
        
        salary = away_pitcher.select('span')[4].text.replace(' ','').replace('\n','').replace('$','').replace('K','')
       
        # arm = away_pitcher.select('.stats')[0].text.replace(' ','').replace('\n','')[0]

        #pitcher sb modifier data
        try:
            pitcher_object = Pitcher.query.filter(Pitcher.name==name)[0]
            add_pitcher(pitcher_object,away)
        except IndexError:
            try:
                pitcher_object = [pitcher for pitcher in Pitcher.query.all() if name in pitcher.name][0]
                add_pitcher(pitcher_object,away)
            except IndexError:
                pass
        

        

        for hitter in away_hitters:
            name = unidecode(hitter.select('a')[0].text)
            stat_group = hitter.select('span.player-nameplate-stats')[0]
            # bat = stat_group.select('span.stats')[0].text.replace('\n','').replace(' ','')
            #make an array of positions
            positions = stat_group.select('span')[1].text.replace('\n','').replace(' ','').split('/')
            salary = stat_group.select('span')[2].text.replace('\n','').replace(' ','').replace('$','').replace('K','')
            if len(salary) < 1:
                continue
            try:
                player_object = Hitter.query.filter(Hitter.name==name)[0]
                player_object.salary = salary
                player_object.team = away
                player_object.position = positions
                hitter_list.append(player_object)
            except IndexError:
                try:
                    player_object = [hitter for hitter in Hitter.query.all() if name in hitter.name][0]
                    player_object.salary = salary
                    player_object.team = away
                    player_object.position = positions
                    hitter_list.append(player_object)
                except IndexError:
                    continue
            


        #home players

        name = unidecode(home_pitcher.select('a')[0].text)
        salary = home_pitcher.select('span')[4].text.replace(' ','').replace('\n','').replace('$','').replace('K','')
        # arm = home_pitcher.select('.stats')[0].text.replace(' ','').replace('\n','')[0]



        try:
            pitcher_object = Pitcher.query.filter(Pitcher.name==name)[0]
            add_pitcher(pitcher_object,home)
        except IndexError:
            try:
                pitcher_object = [pitcher for pitcher in Pitcher.query.all() if name in pitcher.name][0]
                add_pitcher(pitcher_object,home)
            except IndexError:
                pass
            
        
        
        

        for hitter in home_hitters:
            name = unidecode(hitter.select('a')[0].text)
            stat_group = hitter.select('span.player-nameplate-stats')[0]
            # bat = stat_group.select('span.stats')[0].text.replace('\n','').replace(' ','')
            #make an array of positions
            positions = stat_group.select('span')[1].text.replace('\n','').replace(' ','').split('/')
            salary = stat_group.select('span')[2].text.replace('\n','').replace(' ','').replace('$','').replace('K','')
            if len(salary) < 1:
                continue
            try:
                player_object = Hitter.query.filter(Hitter.name==name)[0]
                player_object.salary = salary
                player_object.team = home
                player_object.position = positions
                hitter_list.append(player_object)
            except IndexError:
                try:
                    player_object = [hitter for hitter in Hitter.query.all() if name in hitter.name][0]
                    player_object.salary = salary
                    player_object.team = home
                    player_object.position = positions
                    hitter_list.append(player_object)
                except IndexError:
                    continue

        print(f"{away} @ {home}")
    # ipdb.set_trace()


    team_ks_list = []
    for team in team_list:
        team_k_rate_list = []
        games = [game for game in Game.query.all() if game.home==team or game.visitor==team][-50:]
        for game in games:
            total_abs = [ab for ab in game.at_bats if ab.team==team and ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result]
            strikeout_abs = len([ab for ab in total_abs if "Strikeout" in ab.result])
            strikeout_rate = strikeout_abs/len(total_abs)
            team_k_rate_list.append(strikeout_rate)
        team_ks_list.append({"team":team,"strikeout_rate":(mean(team_k_rate_list))/league_avg_ks})


    #find_player_values
    bets = []
    number_of_abs = -150
    first_value_comparer = .55
    how_many_abs = 10
    how_many_games = 8
    max_stdev = .35
    bags = []
    homers = []
    strikeouts = []
    total_bases = []

    total_bases.append({"name":"New Guy","total_bases":0})
    # print("Made it to the loop")
    for player in hitter_list:

        player_name = player.name
        player_team = player.team
        game = [game for game in game_list if game.home==player_team or game.visitor==player_team][0]
        if game.home==player_team:
            other_team = game.visitor
        else:
            other_team = game.home
        
        #collect my own data about every game they've played in

        pitcher_object_list = [player for player in pitcher_list if player.team==other_team]
        print(f"{player_name} ({player_team})")

        abs = [ab for ab in player.at_bats if ab.game]
        if len(pitcher_object_list) > 0:
            pitcher_object = pitcher_object_list[0]
            pitcher_name=pitcher_object.name
            # hitter = 1
        


            # specific_time = datetime(2024,1,21,16,30,00)
            #and specific_time.time() < [game["time"] for game in game_list if game["home"]==player_team or game["away"]==player_team][0]

            # if ([game.date.time() for game in game_list if game.home==player_team or game.visitor==player_team][0] > format_time)

            

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

        else: 
            result_modifier = 1
            babip_modifier = 1
            in_play_modifier = 1
            
            
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

        # sb modifier

        # pitchers abs where a player gets onto first

        on_first_abs = [ab for ab in all_pitcher_abs if ab.result=="Single" or ab.result=="Walk" or ab.result=="Hit" or "Reached" in ab.result or "Choice" in ab.result]

        sb_abs = len([ab for ab in on_first_abs if ab.sb>=1])

        sb_perc = league_sb_abs/len(league_on_first_abs)

        #how likely they are to steal compared to the rest of the league
        sb_modifier = sb_perc/league_sb_perc


        #how bad the pitcher is against sb's (higher number means more steals)
        pitcher_sb_modifier = pitcher_object.sb_modifier

        final_sb_modifier = .8*pitcher_sb_modifier + .2*sb_modifier
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

        if game.precipitation!="In Dome":
            try:
                wind_speed_high = int(game.wind_speed) + 2
            except ValueError:
                ipdb.set_trace()
            wind_speed_low = int(game.wind_speed) - 2

            try:
                wind_speed_abs = [ab for ab in abs if wind_speed_low <= ab.game.wind_speed <= wind_speed_high][number_of_abs:]
            except TypeError:
                ipdb.set_trace()

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


        try:
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
        except TypeError:
            ipdb.set_trace()


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
            if value["stdev"] < max_stdev:
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


            if len(new_stdev_list)==1:
                first_value = 1.15 * mean(ab.result_stdev for ab in new_stdev_list[0]["array"])
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

                



                # sorted_sb_stdev_list = sorted(sb_stdev_array,key=itemgetter('stdev'))

                # sb_value = mean(game.sb for game in sorted_sb_stdev_list[0]["array"])

                # sb_total_value = sb_value * total_sb_modifier


                hit_values = (first_value + second_value + third_value + fourth_value + fifth_value + sixth_value + seventh_value + eigth_value + ninth_value + tenth_value)
            
                if len(new_sorted_abs_in_common)>0:

                    most_similar = []
                    item_one = new_sorted_abs_in_common[0]["how_many"]

                    for item in new_sorted_abs_in_common:
                        if item["how_many"]==item_one:
                            most_similar.append(item["item"].result_stdev)
                    most_similar_value = mean(most_similar)
                    hit_formula = 1.5*(hit_values) + .5 * most_similar_value
                else:
                    hit_formula = 2*hit_values
                player.value = round(hit_formula * result_modifier,4)

                # ab_total = player.actual_value

                # if 26 <= ab_total:
                #     result_stdev = 1.3
                # elif 18 <= ab_total <= 25:
                #     result_stdev = 1
                # elif 14 <= ab_total <= 17:
                #     result_stdev = 0.95
                # elif 10 <= ab_total <= 13:
                #     result_stdev = 0.9
                # elif 5 <= ab_total <= 9:
                #     result_stdev = .78
                # elif 3 <= ab_total <= 4:
                #     result_stdev = .65
                # elif ab_total == 2:
                #     result_stdev = .5
                # elif "Line" in ab.result:
                #     result_stdev = .25
                # elif "Strikeout" in ab.result:
                #     result_stdev = 0
                # else:
                #     result_stdev = .15

                homers_value = mean([1 if ab.result=="Home Run" else 0 for ab in new_stdev_list[0]["array"]]) 
                bags_value = final_sb_modifier * mean([sb_modifier*ab.sb for ab in new_stdev_list[0]["array"]]) 

                bags.append({"name":player_name,"amount":bags_value}) 
                homers.append({"name":player_name,"amount":homers_value})

                # player_total_bases = []
                # total_bases_games = []
                # for ab in new_stdev_list[0]["array"]:
                #     total_bases_games.append(ab.game)
                # total_bases_games = list(set(total_bases_games))

                # for game in total_bases_games:
                #     total_bases_value = 0
                #     player_abs_in_game = [ab for ab in game.at_bats if ab.hitter.name==player_name]
                #     for ab in player_abs_in_game:
                #         if ab.result=="Home Run":
                #             total_bases_value+=4
                #         elif ab.result=="Triple":
                #             total_bases_value+=3
                #         elif ab.result=="Double":
                #             total_bases_value+=2
                #         elif ab.result=="Single":
                #             total_bases_value+=1
                #     player_total_bases.append(total_bases_value)
                # total_bases_value_final = mean(player_total_bases)

                # total_bases.append({"name":player_name,"total_bases":total_bases_value_final})

                bets.append({"name":player_name,"position":player.position,"salary":player.salary,"compare_value":player.value/(float(player.salary)/10),"team":player.team,"object":player,"value":player.value,"first":new_stdev_list[0]["name"],"first_array":new_stdev_list[0]["array"],"stdev_1":new_stdev_list[0]["stdev"],"second":new_stdev_list[1]["name"],"stdev_2":new_stdev_list[1]["stdev"]})

                # print("Nice. On to the next")


    # bets_sorted = sorted(bets,key=itemgetter('value'))
    # for bet in bets_sorted:
    #     value = bet["value"]
    #     actual_value = bet["actual_value"]
    #     print(f"Value: {value}, actual_value: {actual_value}")
    # ipdb.set_trace()
    for player in pitcher_list:

        player_name = player.name
        player_team = player.team
        main_game = [game for game in game_list if game.home==player_team or game.visitor==player_team][0]
        if main_game.home==player_team:
            other_team = main_game.visitor
        else:
            other_team = main_game.home
    


        # specific_time = datetime(2024,1,21,16,30,00)
        #and specific_time.time() < [game["time"] for game in game_list if game["home"]==player_team or game["away"]==player_team][0]

        # if ([game.date.time() for game in game_list if game.home==player_team or game.visitor==player_team][0] > format_time)

        print(f"{player_name} ({player_team})")


        games = list(set(player.games))
        abs = [ab for ab in player.at_bats if ab.game]

        # print("Start Modifiers")

        #find k modifier, have league_k_perc
        #will also need innings pitched modifier
        #already have sb_modifier

        # ks_list = []
        # for game in games:
        #     pitcher_counted_abs = [ab for ab in abs if ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result]
        #     pitcher_strikeout_abs = len([ab for ab in pitcher_counted_abs if "Strikeout" in ab.result])
        #     ks_list.append(pitcher_strikeout_abs/len(pitcher_counted_abs))
        # pitcher_strikeout_rate = mean(ks_list)

        # #innings pitched modifier
        #     #loop through each game and find total abs where an out was recorded
        #     #compare it to league average innings pitched

        # #league_avg_outs
        # #find player avg outs

        # list_of_outs = []
        # for out_game in games:
        #     outs = [ab for ab in out_game.at_bats if "Out" in ab.result or "out" in ab.result or "Pop" in ab.result or "Choice" in ab.result or "Fly" in ab.result]
        #     pitcher_outs = len([ab for ab in outs if ab.pitcher==player])
        #     list_of_outs.append(pitcher_outs)
        # pitcher_outs_modifier = mean(list_of_outs)

        # outs_modifier = pitcher_outs_modifier/league_avg_outs

        pitcher_amount = 25
        pitcher_number_of_games = -32
       
        
        #latest 25 games at time
        upper_hour = main_game.date.hour+1
        lower_hour = main_game.date.hour-1
        minutes = main_game.date.minute
        upper_time = datetime(2023,2,1,upper_hour,minutes).time()
        lower_time = datetime(2023,2,1,lower_hour,minutes).time()
        games_at_time = [game for game in games if game.date.time()<=upper_time and game.date.time()>=lower_time][pitcher_number_of_games:]
        games_at_time_list = []
        for game in games_at_time:
            first_ab = [ab for ab in game.at_bats if ab.pitcher==player][0]
            if first_ab.team==game.home:
                games_at_time_list.append({"game":game, "stdev":game.away_pitcher_result/pitcher_amount})
            else:
                games_at_time_list.append({"game":game, "stdev":game.home_pitcher_result/pitcher_amount})
        

        #last 25 games on specific day
        current_day = current_date.weekday()
        games_on_day = [game for game in games if game.date.weekday()==current_day][pitcher_number_of_games:]
        games_on_day_list = []
        for game in games_on_day:
            first_ab = [ab for ab in game.at_bats if ab.pitcher==player][0]
            if first_ab.team==game.home:
                games_on_day_list.append({"game":game, "stdev":game.away_pitcher_result/pitcher_amount})
            else:
                games_on_day_list.append({"game":game, "stdev":game.home_pitcher_result/pitcher_amount})


    
        #latest_games
        latest_games = [game for game in games][pitcher_number_of_games:]
        latest_games_list = []
        for game in latest_games:
            first_ab = [ab for ab in game.at_bats if ab.pitcher==player][0]
            if first_ab.team==game.home:
                latest_games_list.append({"game":game, "stdev":game.away_pitcher_result/pitcher_amount})
            else:
                latest_games_list.append({"game":game, "stdev":game.home_pitcher_result/pitcher_amount})



        #home/away games
        if main_game.home==player_team:
            latest_home_or_away_games = [game for game in games if game.home==player_team][pitcher_number_of_games:]
        else:
            latest_home_or_away_games = [game for game in games if game.visitor==player_team][pitcher_number_of_games:]
        latest_home_or_away_games_list = []
        for game in latest_home_or_away_games:
            first_ab = [ab for ab in game.at_bats if ab.pitcher==player][0]
            if first_ab.team==game.home:
                latest_home_or_away_games_list.append({"game":game, "stdev":game.away_pitcher_result/pitcher_amount})
            else:
                latest_home_or_away_games_list.append({"game":game, "stdev":game.home_pitcher_result/pitcher_amount})




        #last 50 at stadium
        at_stadium = [game for game in games if game.location == main_game.location][pitcher_number_of_games:]
        at_stadium_list = []
        for game in at_stadium:
            first_ab = [ab for ab in game.at_bats if ab.pitcher==player][0]
            if first_ab.team==game.home:
                at_stadium_list.append({"game":game, "stdev":game.away_pitcher_result/pitcher_amount})
            else:
                at_stadium_list.append({"game":game, "stdev":game.home_pitcher_result/pitcher_amount})

        #last 50 with wind direction

        if game.wind_direction == 400:
            wind_direction_games = [game for game in games if game.precipitation=="In Dome"][pitcher_number_of_games:]

        else:
            wind_high = main_game.wind_direction + 22.5
            wind_low = main_game.wind_direction - 22.5

            wind_direction_games = [game for game in games if wind_low <= game.wind_direction <= wind_high][pitcher_number_of_games:]

        wind_direction_games_list = []
        for game in wind_direction_games:
            first_ab = [ab for ab in game.at_bats if ab.pitcher==player][0]
            if first_ab.team==game.home:
                wind_direction_games_list.append({"game":game, "stdev":game.away_pitcher_result/pitcher_amount})
            else:
                wind_direction_games_list.append({"game":game, "stdev":game.home_pitcher_result/pitcher_amount})


        #wind speed

        if main_game.wind_speed!="In Dome":
            try:
                wind_speed_high = int(main_game.wind_speed) + 2
            except ValueError:
                ipdb.set_trace()
            wind_speed_low = int(main_game.wind_speed) - 2

            wind_speed_games = [game for game in games if wind_speed_low <= game.wind_speed <= wind_speed_high][pitcher_number_of_games:]

        else:
            wind_speed_games = []

        wind_speed_games_list = []
        for game in wind_speed_games:
            first_ab = [ab for ab in game.at_bats if ab.pitcher==player][0]
            if first_ab.team==game.home:
                wind_speed_games_list.append({"game":game, "stdev":game.away_pitcher_result/pitcher_amount})
            else:
                wind_speed_games_list.append({"game":game, "stdev":game.home_pitcher_result/pitcher_amount})

        #sunny/cloudy
        #Overcast, Sunny, Cloudy, In Dome
        if main_game.cloud_or_sun=="Cloudy" or main_game.cloud_or_sun=="Overcast":
            cloud_or_sun_games = [games for games in games if game.cloud_or_sun=="Cloudy" or game.cloud_or_sun=="Overcast"][pitcher_number_of_games:]
        elif main_game.cloud_or_sun=="Sunny":
            cloud_or_sun_games = [game for game in games if game.cloud_or_sun=="Sunny"][pitcher_number_of_games:]
        else:
            cloud_or_sun_games = []

        cloud_or_sun_games_list = []
        for game in cloud_or_sun_games:
            first_ab = [ab for ab in game.at_bats if ab.pitcher==player][0]
            if first_ab.team==game.home:
                cloud_or_sun_games_list.append({"game":game, "stdev":game.away_pitcher_result/pitcher_amount})
            else:
                cloud_or_sun_games_list.append({"game":game, "stdev":game.home_pitcher_result/pitcher_amount})


        #precipitation
        if main_game.precipitation=="Rain":
            precipitation_games = [game for game in games if game.precipitation=="Rain" or game.precipitation=="Drizzle"][pitcher_number_of_games:]
        elif main_game.precipitation=="Snow":
            precipitation_games = [game for game in games if game.precipitation=="Snow"][pitcher_number_of_games:]
        else:
            precipitation_games = []

        precipitation_games_list = []
        for game in precipitation_games:
            first_ab = [ab for ab in game.at_bats if ab.pitcher==player][0]
            if first_ab.team==game.home:
                precipitation_games_list.append({"game":game, "stdev":game.away_pitcher_result/pitcher_amount})
            else:
                precipitation_games_list.append({"game":game, "stdev":game.home_pitcher_result/pitcher_amount})


        #temperature
        freezing = 35
        real_cold = 42
        very_cold = 47
        cold = 62
        nice = 78
        hot = 88
        too_hot = 97

        the_temperature = int(main_game.temperature)

        if the_temperature <= freezing:
            temperature_games = [game for game in games if the_temperature <= freezing][pitcher_number_of_games:]
        elif freezing < the_temperature <= real_cold:
            temperature_games = [game for game in games if freezing < the_temperature <= real_cold][pitcher_number_of_games:]
        elif real_cold < the_temperature <= very_cold:
            temperature_games = [game for game in games if real_cold < the_temperature <= very_cold][pitcher_number_of_games:]
        elif very_cold < the_temperature <= cold:
            temperature_games = [game for game in games if very_cold < the_temperature <= cold][pitcher_number_of_games:]
        elif cold < the_temperature <= nice:
            temperature_games = [game for game in games if cold < the_temperature <= nice][pitcher_number_of_games:]
        elif nice < the_temperature <= hot:
            temperature_games = [game for game in games if nice < the_temperature <= hot][pitcher_number_of_games:]
        elif hot < the_temperature <= too_hot:
            temperature_games = [game for game in games if hot < the_temperature <= too_hot][pitcher_number_of_games:]
        else:
            temperature_games = [game for game in games if the_temperature > too_hot][pitcher_number_of_games:]


        temperature_games_list = []
        for game in temperature_games:
            first_ab = [ab for ab in game.at_bats if ab.pitcher==player][0]
            if first_ab.team==game.home:
                temperature_games_list.append({"game":game, "stdev":game.away_pitcher_result/pitcher_amount})
            else:
                temperature_games_list.append({"game":game, "stdev":game.home_pitcher_result/pitcher_amount})

        #vs team
        games_vs_team = [game for game in games if game.home==other_team or game.visitor==other_team][pitcher_number_of_games:]
        games_vs_team_list = []
        for game in games_vs_team:
            first_ab = [ab for ab in game.at_bats if ab.pitcher==player][0]
            if first_ab.team==game.home:
                games_vs_team_list.append({"game":game, "stdev":game.away_pitcher_result/pitcher_amount})
            else:
                games_vs_team_list.append({"game":game, "stdev":game.home_pitcher_result/pitcher_amount})


        ks_stdev_array = [{"name":"temperature_games_list","array":temperature_games_list,"stdev":stdev([game["stdev"] for game in temperature_games_list]) if len(temperature_games_list)>how_many_games else 500},
                {"name":"games_vs_team_list","array":games_vs_team_list,"stdev":stdev([game["stdev"] for game in games_vs_team_list]) if len(games_vs_team_list)>how_many_games else 500},
                {"name":"precipitation_games_list","array":precipitation_games_list,"stdev":stdev([game["stdev"] for game in precipitation_games_list]) if len(precipitation_games_list)>how_many_games else 500},
                {"name":"cloud_or_sun_games_list","array":cloud_or_sun_games_list,"stdev":stdev([game["stdev"] for game in cloud_or_sun_games_list]) if len(cloud_or_sun_games_list)>how_many_games else 500},
                {"name":"wind_speed_games_list","array":wind_speed_games_list,"stdev":stdev([game["stdev"] for game in wind_speed_games_list]) if len(wind_speed_games_list)>how_many_games else 500},
                {"name":"wind_direction_games_list","array":wind_direction_games_list,"stdev":stdev([game["stdev"] for game in wind_direction_games_list]) if len(wind_direction_games_list)>how_many_games else 500},
                {"name":"at_stadium_list","array":at_stadium_list,"stdev":stdev([game["stdev"] for game in at_stadium_list]) if len(at_stadium_list)>how_many_games else 500},
                {"name":"games_at_time_list","array":games_at_time_list,"stdev":stdev([game["stdev"] for game in games_at_time_list]) if len(games_at_time_list)>how_many_games else 500},
                {"name":"games_on_day_list","array":games_on_day_list,"stdev":stdev([game["stdev"] for game in games_on_day_list]) if len(games_on_day_list)>how_many_games else 500},
                {"name":"latest_games_list","array":latest_games_list,"stdev":stdev([game["stdev"] for game in latest_games_list]) if len(latest_games_list)>how_many_games else 500},
                {"name":"latest_home_or_away_games_list","array":latest_home_or_away_games_list,"stdev":stdev([game["stdev"] for game in latest_home_or_away_games_list]) if len(latest_home_or_away_games_list)>how_many_games else 500},
            ]

        # innings_stdev_array = [{"name":"temperature_games_list","array":temperature_games_list,"stdev":stdev([game["innings_pitched"]/14 for game in temperature_games_list]) if len(temperature_games_list)>how_many_abs else 500},
        #     {"name":"games_vs_team_list","array":games_vs_team_list,"stdev":stdev([game["innings_pitched"]/14 for game in games_vs_team_list]) if len(games_vs_team_list)>how_many_abs else 500},
        #     {"name":"precipitation_games_list","array":precipitation_games_list,"stdev":stdev([game["innings_pitched"]/14 for game in precipitation_games_list]) if len(precipitation_games_list)>how_many_abs else 500},
        #     {"name":"cloud_or_sun_games_list","array":cloud_or_sun_games_list,"stdev":stdev([game["innings_pitched"]/14 for game in cloud_or_sun_games_list]) if len(cloud_or_sun_games_list)>how_many_abs else 500},
        #     {"name":"wind_speed_games_list","array":wind_speed_games_list,"stdev":stdev([game["innings_pitched"]/14 for game in wind_speed_games_list]) if len(wind_speed_games_list)>how_many_abs else 500},
        #     {"name":"wind_direction_games_list","array":wind_direction_games_list,"stdev":stdev([game["innings_pitched"]/14 for game in wind_direction_games_list]) if len(wind_direction_games_list)>how_many_abs else 500},
        #     {"name":"at_stadium_list","array":at_stadium_list,"stdev":stdev([game["innings_pitched"]/14 for game in at_stadium_list]) if len(at_stadium_list)>how_many_abs else 500},
        #     {"name":"games_at_time_list","array":games_at_time_list,"stdev":stdev([game["innings_pitched"]/14 for game in games_at_time_list]) if len(games_at_time_list)>how_many_abs else 500},
        #     {"name":"games_on_day_list","array":games_on_day_list,"stdev":stdev([game["innings_pitched"]/14 for game in games_on_day_list]) if len(games_on_day_list)>how_many_abs else 500},
        #     {"name":"latest_games_list","array":latest_games_list,"stdev":stdev([game["innings_pitched"]/14 for game in latest_games_list]) if len(latest_games_list)>how_many_abs else 500},
        #     {"name":"latest_home_or_away_games_list","array":latest_home_or_away_games_list,"stdev":stdev([game["innings_pitched"]/14 for game in latest_home_or_away_games_list]) if len(latest_home_or_away_games_list)>how_many_abs else 500},
        #    ]

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

        # first_inn_value = 0
        # second_inn_value = 0
        # third_inn_value = 0
        # fourth_inn_value = 0
        # fifth_inn_value = 0
        # sixth_inn_value = 0
        # seventh_inn_value = 0
        # eigth_inn_value = 0
        # ninth_inn_value = 0
        # tenth_inn_value = 0

        # print("made a sorted list")

    

        new_ks_stdev_list = []
        for value in ks_stdev_array:
            if value["stdev"] < 1:
                new_ks_stdev_list.append(value)

        # new_innings_stdev_list = []
        # for value in innings_stdev_array:
        #     if value["stdev"] < 300:
        #         new_innings_stdev_list.append(value)

        if len(new_ks_stdev_list) > 0:

            # print("We've got the new one. Start big giant")

            # ipdb.set_trace()

            big_giant = temperature_games_list.copy()
            big_giant.extend(latest_home_or_away_games_list)
            big_giant.extend(latest_games_list)
            big_giant.extend(games_on_day_list)
            big_giant.extend(games_at_time_list)
            big_giant.extend(at_stadium_list)
            big_giant.extend(wind_direction_games_list)
            big_giant.extend(wind_speed_games_list)
            big_giant.extend(cloud_or_sun_games_list)
            big_giant.extend(precipitation_games_list)
            big_giant.extend(games_vs_team_list)
        

            abs_in_common = []
            for item in big_giant:
                i = 0
                if item not in abs_in_common:
                    for secondary in big_giant:
                        if item["game"]==secondary["game"]:
                            i+=1
                    if i > 4:
                        abs_in_common.append({"item":item,"how_many":i})
                



            if len(abs_in_common) < how_many_abs:
                continue
            
            sorted_abs_in_common = sorted(abs_in_common,key=itemgetter('how_many'))
            sorted_abs_in_common.reverse()

            high_ab_in_common = sorted_abs_in_common[0]["how_many"]
            diffy = high_ab_in_common-.4*high_ab_in_common

            new_sorted_abs_in_common = [game["item"] for game in sorted_abs_in_common if game["how_many"] > diffy][number_of_abs:]
            try:
                final_ks_sorted_abs_in_common = {"name":"abs_in_common","array":[game for game in new_sorted_abs_in_common],"stdev":stdev([item["stdev"] for item in new_sorted_abs_in_common])}
            except TypeError:
                ipdb.set_trace()
            # final_innings_sorted_abs_in_common = {"name":"abs_in_common","array":[game["item"] for game in new_sorted_abs_in_common],"stdev":stdev([game["item"]["innings_pitched"] for game in new_sorted_abs_in_common])}
            if len(sorted_abs_in_common) > 5:
                # new_innings_stdev_list.insert(0,final_innings_sorted_abs_in_common)
                new_ks_stdev_list.insert(0,final_ks_sorted_abs_in_common)

            new_ks_stdev_list = sorted(new_ks_stdev_list,key=itemgetter('stdev'))
            # new_innings_stdev_list = sorted(new_innings_stdev_list,key=itemgetter('stdev'))

            # print("Big giant done. Create player_value")

            if len(new_ks_stdev_list)==1:
                first_value = 1.15 * mean(game["stdev"] for game in new_ks_stdev_list[0]["array"])
            elif len(new_ks_stdev_list)>1:
                if len(new_ks_stdev_list)==2:
                    first_value = .65 * mean(game["stdev"] for game in new_ks_stdev_list[0]["array"])
                    second_value = .3 * mean(game["stdev"] for game in new_ks_stdev_list[1]["array"]) 
                elif len(new_ks_stdev_list)==3:
                    first_value = first_value_comparer * mean(game["stdev"] for game in new_ks_stdev_list[0]["array"])
                    second_value = .25 * mean(game["stdev"] for game in new_ks_stdev_list[1]["array"]) 
                    third_value = .15 * mean(game["stdev"] for game in new_ks_stdev_list[2]["array"]) 
                elif len(new_ks_stdev_list)==4:
                    first_value = first_value_comparer * mean(game["stdev"] for game in new_ks_stdev_list[0]["array"])
                    second_value = .25 * mean(game["stdev"] for game in new_ks_stdev_list[1]["array"]) 
                    third_value = .1 * mean(game["stdev"] for game in new_ks_stdev_list[2]["array"]) 
                    fourth_value = .05 * mean(game["stdev"] for game in new_ks_stdev_list[3]["array"])
                elif len(new_ks_stdev_list)==5:
                    first_value = first_value_comparer * mean(game["stdev"] for game in new_ks_stdev_list[0]["array"])
                    second_value = .225 * mean(game["stdev"] for game in new_ks_stdev_list[1]["array"]) 
                    third_value = .1 * mean(game["stdev"] for game in new_ks_stdev_list[2]["array"]) 
                    fourth_value = .05 * mean(game["stdev"] for game in new_ks_stdev_list[3]["array"])
                    fifth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[4]["array"])
                elif len(new_ks_stdev_list)==6:
                    first_value = first_value_comparer * mean(game["stdev"] for game in new_ks_stdev_list[0]["array"])
                    second_value = .2 * mean(game["stdev"] for game in new_ks_stdev_list[1]["array"]) 
                    third_value = .1 * mean(game["stdev"] for game in new_ks_stdev_list[2]["array"]) 
                    fourth_value = .05 * mean(game["stdev"] for game in new_ks_stdev_list[3]["array"])
                    fifth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[4]["array"])
                    sixth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[5]["array"])
                elif len(new_ks_stdev_list)==7:
                    first_value = first_value_comparer * mean(game["stdev"] for game in new_ks_stdev_list[0]["array"])
                    second_value = .175 * mean(game["stdev"] for game in new_ks_stdev_list[1]["array"]) 
                    third_value = .1 * mean(game["stdev"] for game in new_ks_stdev_list[2]["array"]) 
                    fourth_value = .05 * mean(game["stdev"] for game in new_ks_stdev_list[3]["array"])
                    fifth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[4]["array"])
                    sixth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[5]["array"])
                    seventh_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[6]["array"])
                elif len(new_ks_stdev_list)==8:
                    first_value = first_value_comparer * mean(game["stdev"] for game in new_ks_stdev_list[0]["array"])
                    second_value = .175 * mean(game["stdev"] for game in new_ks_stdev_list[1]["array"]) 
                    third_value = .1 * mean(game["stdev"] for game in new_ks_stdev_list[2]["array"]) 
                    fourth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[3]["array"])
                    fifth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[4]["array"])
                    sixth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[5]["array"])
                    seventh_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[6]["array"])
                    eigth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[7]["array"])
                elif len(new_ks_stdev_list)==9:
                    first_value = first_value_comparer * mean(game["stdev"] for game in new_ks_stdev_list[0]["array"])
                    second_value = .175 * mean(game["stdev"] for game in new_ks_stdev_list[1]["array"]) 
                    third_value = .05 * mean(game["stdev"] for game in new_ks_stdev_list[2]["array"]) 
                    fourth_value = .05 * mean(game["stdev"] for game in new_ks_stdev_list[3]["array"])
                    fifth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[4]["array"])
                    sixth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[5]["array"])
                    seventh_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[6]["array"])
                    eigth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[7]["array"])
                    ninth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[8]["array"])
                elif len(new_ks_stdev_list)>=10:
                    first_value = first_value_comparer * mean(game["stdev"] for game in new_ks_stdev_list[0]["array"])
                    second_value = .175 * mean(game["stdev"] for game in new_ks_stdev_list[1]["array"]) 
                    third_value = .05 * mean(game["stdev"] for game in new_ks_stdev_list[2]["array"]) 
                    fourth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[3]["array"])
                    fifth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[4]["array"])
                    sixth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[5]["array"])
                    seventh_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[6]["array"])
                    eigth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[7]["array"])
                    ninth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[8]["array"])
                    tenth_value = .025 * mean(game["stdev"] for game in new_ks_stdev_list[9]["array"])
                else:
                    continue
            

            # if len(new_ks_stdev_list)==1:
            #     first_inn_value = 1.15 * mean(game["innings_pitched"] for game in new_innings_stdev_list[0]["array"])
            # elif len(new_ks_stdev_list)>1:
            #     if len(new_ks_stdev_list)==2:
            #         first_inn_value = .65 * mean(game["innings_pitched"] for game in new_innings_stdev_list[0]["array"])
            #         second_inn_value = .3 * mean(game["innings_pitched"] for game in new_innings_stdev_list[1]["array"]) 
            #     elif len(new_ks_stdev_list)==3:
            #         first_inn_value = first_value_comparer * mean(game["innings_pitched"] for game in new_innings_stdev_list[0]["array"])
            #         second_inn_value = .25 * mean(game["innings_pitched"] for game in new_innings_stdev_list[1]["array"]) 
            #         third_inn_value = .15 * mean(game["innings_pitched"] for game in new_innings_stdev_list[2]["array"]) 
            #     elif len(new_ks_stdev_list)==4:
            #         first_inn_value = first_value_comparer * mean(game["innings_pitched"] for game in new_innings_stdev_list[0]["array"])
            #         second_inn_value = .25 * mean(game["innings_pitched"] for game in new_innings_stdev_list[1]["array"]) 
            #         third_inn_value = .1 * mean(game["innings_pitched"] for game in new_innings_stdev_list[2]["array"]) 
            #         fourth_inn_value = .05 * mean(game["innings_pitched"] for game in new_innings_stdev_list[3]["array"])
            #     elif len(new_ks_stdev_list)==5:
            #         first_inn_value = first_value_comparer * mean(game["innings_pitched"] for game in new_innings_stdev_list[0]["array"])
            #         second_inn_value = .225 * mean(game["innings_pitched"] for game in new_innings_stdev_list[1]["array"]) 
            #         third_inn_value = .1 * mean(game["innings_pitched"] for game in new_innings_stdev_list[2]["array"]) 
            #         fourth_inn_value = .05 * mean(game["innings_pitched"] for game in new_innings_stdev_list[3]["array"])
            #         fifth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[4]["array"])
            #     elif len(new_ks_stdev_list)==6:
            #         first_inn_value = first_value_comparer * mean(game["innings_pitched"] for game in new_innings_stdev_list[0]["array"])
            #         second_inn_value = .2 * mean(game["innings_pitched"] for game in new_innings_stdev_list[1]["array"]) 
            #         third_inn_value = .1 * mean(game["innings_pitched"] for game in new_innings_stdev_list[2]["array"]) 
            #         fourth_inn_value = .05 * mean(game["innings_pitched"] for game in new_innings_stdev_list[3]["array"])
            #         fifth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[4]["array"])
            #         sixth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[5]["array"])
            #     elif len(new_ks_stdev_list)==7:
            #         first_inn_value = first_value_comparer * mean(game["innings_pitched"] for game in new_innings_stdev_list[0]["array"])
            #         second_inn_value = .175 * mean(game["innings_pitched"] for game in new_innings_stdev_list[1]["array"]) 
            #         third_inn_value = .1 * mean(game["innings_pitched"] for game in new_innings_stdev_list[2]["array"]) 
            #         fourth_inn_value = .05 * mean(game["innings_pitched"] for game in new_innings_stdev_list[3]["array"])
            #         fifth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[4]["array"])
            #         sixth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[5]["array"])
            #         seventh_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[6]["array"])
            #     elif len(new_ks_stdev_list)==8:
            #         first_inn_value = first_value_comparer * mean(game["innings_pitched"] for game in new_innings_stdev_list[0]["array"])
            #         second_inn_value = .175 * mean(game["innings_pitched"] for game in new_innings_stdev_list[1]["array"]) 
            #         third_inn_value = .1 * mean(game["innings_pitched"] for game in new_innings_stdev_list[2]["array"]) 
            #         fourth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[3]["array"])
            #         fifth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[4]["array"])
            #         sixth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[5]["array"])
            #         seventh_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[6]["array"])
            #         eigth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[7]["array"])
            #     elif len(new_ks_stdev_list)==9:
            #         first_inn_value = first_value_comparer * mean(game["innings_pitched"] for game in new_innings_stdev_list[0]["array"])
            #         second_inn_value = .175 * mean(game["innings_pitched"] for game in new_innings_stdev_list[1]["array"]) 
            #         third_inn_value = .05 * mean(game["innings_pitched"] for game in new_innings_stdev_list[2]["array"]) 
            #         fourth_inn_value = .05 * mean(game["innings_pitched"] for game in new_innings_stdev_list[3]["array"])
            #         fifth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[4]["array"])
            #         sixth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[5]["array"])
            #         seventh_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[6]["array"])
            #         eigth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[7]["array"])
            #         ninth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[8]["array"])
            #     elif len(new_ks_stdev_list)>=10:
            #         first_inn_value = first_value_comparer * mean(game["innings_pitched"] for game in new_innings_stdev_list[0]["array"])
            #         second_inn_value = .175 * mean(game["innings_pitched"] for game in new_innings_stdev_list[1]["array"]) 
            #         third_inn_value = .05 * mean(game["innings_pitched"] for game in new_innings_stdev_list[2]["array"]) 
            #         fourth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[3]["array"])
            #         fifth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[4]["array"])
            #         sixth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[5]["array"])
            #         seventh_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[6]["array"])
            #         eigth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[7]["array"])
            #         ninth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[8]["array"])
            #         tenth_inn_value = .025 * mean(game["innings_pitched"] for game in new_innings_stdev_list[9]["array"])
            #     else:
            #         continue


                team_ks_modifier = [item for item in team_ks_list if item["team"]==other_team][0]["strikeout_rate"]

                if len(sorted_abs_in_common)>0:

                    most_similar = []
                    item_one = sorted_abs_in_common[0]["how_many"]

                    for item in sorted_abs_in_common:
                        if item["how_many"]==item_one:
                            most_similar.append(item["item"])
                    try:
                        most_similar_list = [item["stdev"] for item in most_similar]
                    except TypeError:
                        ipdb.set_trace()
                    most_similar_value = mean(most_similar_list)
                    ks_formula =  .5 * mean(game["stdev"] for game in new_ks_stdev_list[0]["array"]) + .5 * most_similar_value
                else:
                    ks_formula = mean(game["stdev"] for game in new_ks_stdev_list[0]["array"])
                player.value = round(hit_formula * result_modifier,4)

                list_of_ks_in_similar = []
                for game in most_similar:
                    total_game_ks = len([ab for ab in game["game"].at_bats if ab.pitcher.name==player_name and "Strikeout" in ab.result])
                    list_of_ks_in_similar.append(total_game_ks)
                similar_ks = mean(list_of_ks_in_similar)

                
                # innings_formula = first_inn_value + second_inn_value + third_inn_value + fourth_inn_value + fifth_inn_value + sixth_inn_value + seventh_inn_value + eigth_inn_value + ninth_inn_value + tenth_inn_value
                # ks_formula = (first_value + second_value + third_value + fourth_value + fifth_value + sixth_value + seventh_value + eigth_value + ninth_value + tenth_value)
                list_of_ks_in_player = []
                for game in new_ks_stdev_list[0]["array"]:
                    total_game_ks = len([ab for ab in game["game"].at_bats if ab.pitcher.name==player_name and "Strikeout" in ab.result])
                    list_of_ks_in_player.append(total_game_ks)
                player_ks = round(mean(list_of_ks_in_player),1)
                strikeouts.append({"name":player_name,"ks":(.25*(player_ks)+ (.75*similar_ks)) * team_ks_modifier})

                player.value = round(ks_formula,4)
        

                bets.append({"name":player_name,"object":player,"position":"P","salary":player.salary,"compare_value":player.value/(float(player.salary)/10),"team":player.team,"value":player.value,"first":new_ks_stdev_list[0]["name"],"first_array":new_ks_stdev_list[0]["array"],"stdev_1":new_ks_stdev_list[0]["stdev"],"second":new_ks_stdev_list[1]["name"],"stdev_2":new_ks_stdev_list[1]["stdev"]})

                # print("Nice. On to the next")


    # pitcher_bet = [bet for bet in bets if bet["position"]=="P"]
    # bets_sorted = sorted(pitcher_bet,key=itemgetter('value'))

    # for bet in bets_sorted:
    #     value = bet["value"]
    #     actual_value = bet["actual_value"]
    #     print(f"Value: {value}, actual_value: {actual_value}")
    # ipdb.set_trace()

    sorted_bets = sorted(bets,key=itemgetter('stdev_1'))
    sorted_by_value_bets = sorted(bets,key=itemgetter('value'))
    sorted_compare_value_bets = sorted(bets,key=itemgetter('compare_value'))
    sorted_compare_value_bets.reverse()
    sorted_by_value_bets.reverse()
    sorted_bets.reverse()

    highest_value = [bet["value"] for bet in sorted_by_value_bets][0]

    try:
        higher_value = 2*highest_value/3
    except TypeError:
        ipdb.set_trace()
    low_value = 1*highest_value/3
    mid_value = .5

    
    # sorted_bets.reverse()

    iterator = 0
    list_value = 0

    # if len([bet for bet in sorted_by_value_bets if bet["stdev_1"] <.26]) > 25:
    #     sorted_by_value_bets = [bet for bet in sorted_by_value_bets if bet["stdev_1"] <.26]
    # elif len([bet for bet in sorted_by_value_bets if bet["stdev_1"] <.3]) > 25:
    #     sorted_by_value_bets = [bet for bet in sorted_by_value_bets if bet["stdev_1"] <.3]
    # elif len([bet for bet in sorted_by_value_bets if bet["stdev_1"] <.35]) > 25:
    #     sorted_by_value_bets = [bet for bet in sorted_by_value_bets if bet["stdev_1"] <.35]


    for bet in sorted_by_value_bets:
    #     if bet["value"] > mid_value:
    #         if list_value<=30:
    #             list_value+=1
    #         if bet["actual_value"] > mid_value:
    #             response = "⬆️✅"
    #             if list_value <= 30:
    #                 iterator+=1
    #         else:
    #             response = "⬆️❌"
    #     else:
    #         if bet["actual_value"] < mid_value:
    #             response = "👇🏽✅"
    #         else:
    #             response = "👇🏽❌"
            
                
        if bet["value"] > mid_value:
            name = bet["name"]
            value = bet["value"]
            first = bet["first"]
            second = bet["second"]
            team = bet["team"]
            position = bet["position"]
            salary = bet["salary"]
            stdev_1 = bet["stdev_1"]
            stdev_2 = bet["stdev_2"]
            string_beginning = (f"{name} {team}: {salary}").ljust(40,' ')
            string_middle = (f"- Proj: {value} ").ljust(10,' ')
            string_late_middle = (f"Position: {position}").ljust(20,' ')
            string_end = (f"{first}:{round(stdev_1,4)}, {second}:{round(stdev_2,4)}").ljust(25,' ')
            print(f"{string_beginning} {string_middle} {string_late_middle} {string_end}")


    sorted_bags = sorted(bags,key=itemgetter('amount'))
    sorted_bags.reverse()
    sorted_homers = sorted(homers,key=itemgetter('amount'))
    sorted_homers.reverse()
    sorted_strikeouts = sorted(strikeouts,key=itemgetter('ks'))
    sorted_strikeouts.reverse()
    sorted_total_bases = sorted(total_bases,key=itemgetter('total_bases'))
    sorted_total_bases.reverse()

    print('\nBags')
    for item in sorted_bags[0:25]:
        name = item["name"]
        amount = item["amount"]
        if float(amount) > 0:
            print(f"{name} Value: {amount}")
    print('\nHomers')
    for item in sorted_homers[0:25]:
        name = item["name"]
        amount = item["amount"]
        if float(amount) > 0:
            print(f"{name} Value: {amount}")
    print('\nStrikeouts')
    for item in sorted_strikeouts:
        name = item["name"]
        ks = item["ks"]
        print(f"{name}: {ks}")
    print('\n')

    for item in sorted_total_bases[0:50]:
        name= item["name"]
        total_bases = item["total_bases"]
        print(f"{name}: {total_bases}")

    # if list_value==31:
    #         list_value=30
    # percentage = round(100*iterator/list_value,3)
    # print(f"Top 30 are at {percentage}%")
   
    # ipdb.set_trace()

    #to make sure the totals of each position are there the right amount of times

    pitchers = 0
    catchers = 0
    first = 0
    second = 0
    short = 0
    third = 0
    outfielders = 0

    dk_players = []
    dk_counter = 0

    #build the original 10 player list

    sorted_bets = [bet for bet in sorted_by_value_bets if bet["value"] > mid_value]

    sorted_players = [player["object"] for player in sorted_bets]

    for player in sorted_players:
        if "SP" in player.position and pitchers<2:
            player.dk_position="SP"
            dk_players.append(player)
            pitchers+=1
            continue
        if "C" in player.position and catchers==0:
            player.dk_position="C"
            dk_players.append(player)
            catchers+=1
            continue
        if "1B" in player.position and first==0:
            player.dk_position="1B"
            dk_players.append(player)
            first+=1
            continue
        if "2B" in player.position and second==0:
            player.dk_position="2B"
            dk_players.append(player)
            second+=1
            continue
        if "3B" in player.position and third==0:
            player.dk_position="3B"
            dk_players.append(player)
            third+=1
            continue
        if "SS" in player.position and short==0:
            player.dk_position="SS"
            dk_players.append(player)
            short+=1
            continue
        if ("RF" in player.position or "LF" in player.position or "CF" in player.position or "OF" in player.position) and outfielders<3:
            player.dk_position="OF"
            dk_players.append(player)
            outfielders+=1
            continue
        if len(dk_players)==10:
            break

    

    #if the 10 players salary is acceptable then end the algo there
    #if not, check the next few players

    total_salary = sum([float(player.salary) for player in dk_players])
    if total_salary > 50:
        print("Too High")
        print(total_salary)
        removed_players = []
        # new_list = sorted_players[counter:]      
        for player in sorted_players:
            if player not in dk_players:
                if "SP" in player.position:
                    pitcher_array = [player for player in dk_players if player.dk_position=="SP"]
                    for last_loss in pitcher_array:
                        if float(player.salary) < float(last_loss.salary):
                            dk_players.remove(last_loss)
                            removed_players.append(last_loss)
                            player.dk_position="SP"
                            dk_players.append(player)
                            break
                if "C" in player.position:
                    last_loss = [player for player in dk_players if player.dk_position=="C"]
                    last_loss = last_loss[0]
                    if float(player.salary) < float(last_loss.salary):
                        dk_players.remove(last_loss)
                        removed_players.append(last_loss)
                        player.dk_position="C"
                        dk_players.append(player)
                        continue
                if "1B" in player.position:
                    last_loss = [player for player in dk_players if player.dk_position=="1B"]
                    last_loss = last_loss[0]
                    if float(player.salary) < float(last_loss.salary):
                        dk_players.remove(last_loss)
                        removed_players.append(last_loss)
                        player.dk_position="1B"
                        dk_players.append(player)
                        continue
                if "2B" in player.position:
                    last_loss = [player for player in dk_players if player.dk_position=="2B"]
                    last_loss = last_loss[0]
                    if float(player.salary) < float(last_loss.salary):
                        dk_players.remove(last_loss)
                        removed_players.append(last_loss)
                        player.dk_position="2B"
                        dk_players.append(player)
                        continue
                if "3B" in player.position:
                    last_loss = [player for player in dk_players if player.dk_position=="3B"]
                    last_loss = last_loss[0]
                    if float(player.salary) < float(last_loss.salary):
                        dk_players.remove(last_loss)
                        removed_players.append(last_loss)
                        player.dk_position="3B"
                        dk_players.append(player)
                        continue
                if "SS" in player.position:
                    last_loss = [player for player in dk_players if player.dk_position=="SS"]
                    last_loss = last_loss[0]
                    if float(player.salary) < float(last_loss.salary):
                        dk_players.remove(last_loss)
                        removed_players.append(last_loss)
                        player.dk_position="SS"
                        dk_players.append(player)
                        continue
                if "RF" in player.position or "LF" in player.position or "CF" in player.position or "OF" in player.position:
                    outfielder_array =  [player for player in dk_players if player.dk_position=="OF"]
                    for last_loss in outfielder_array:
                        if float(player.salary) < float(last_loss.salary):
                            dk_players.remove(last_loss)
                            removed_players.append(last_loss)
                            player.dk_position="OF"
                            dk_players.append(player)
                            break
                total_salary = sum([float(player.salary) for player in dk_players])
                if total_salary < 50:
                    break  

        #I've gotta add this to commitW

        #now that we replaced a few players until we got the salary below the max,
        #we have a list of removed players who may be able to go back in
        
        if len(removed_players) > 0:
            for player in removed_players:
                if "SP" in player.position:
                    pitcher_array = [player for player in dk_players if player.dk_position=="SP"]
                    for last_loss in pitcher_array:
                        everyone_else = [player for player in dk_players if player.name!=last_loss.name]
                        salary_with_nine = sum([float(player.salary) for player in everyone_else])
                        new_total_salary = salary_with_nine + float(player.salary)
                        if  new_total_salary <=50 and float(player.value) > float(last_loss.value):
                            dk_players.remove(last_loss)
                            player.dk_position="SP"
                            dk_players.append(player)
                            break
                if "C" in player.position:
                    last_loss = [player for player in dk_players if player.dk_position=="C"]
                    try:
                        last_loss = last_loss[0]
                    except IndexError:
                        ipdb.set_trace()
                    everyone_else = [player for player in dk_players if player.name!=last_loss.name]
                    salary_with_nine = sum([float(player.salary) for player in everyone_else])
                    new_total_salary = salary_with_nine + float(player.salary)
                    if new_total_salary <=50 and float(player.value) > float(last_loss.value):
                        dk_players.remove(last_loss)
                        player.dk_position="C"
                        dk_players.append(player)
                        continue
                if "1B" in player.position:
                    last_loss = [player for player in dk_players if player.dk_position=="1B"]
                    try:
                        last_loss = last_loss[0]
                    except IndexError:
                        ipdb.set_trace()
                    everyone_else = [player for player in dk_players if player.name!=last_loss.name]
                    salary_with_nine = sum([float(player.salary) for player in everyone_else])
                    new_total_salary = salary_with_nine + float(player.salary)
                    if new_total_salary <=50 and float(player.value) > float(last_loss.value):
                        dk_players.remove(last_loss)
                        player.dk_position="1B"
                        dk_players.append(player)
                        continue
                if "2B" in player.position:
                    last_loss = [player for player in dk_players if player.dk_position=="2B"]
                    try:
                        last_loss = last_loss[0]
                    except IndexError:
                        ipdb.set_trace()
                    everyone_else = [player for player in dk_players if player.name!=last_loss.name]
                    salary_with_nine = sum([float(player.salary) for player in everyone_else])
                    new_total_salary = salary_with_nine + float(player.salary)
                    if new_total_salary <=50 and float(player.value) > float(last_loss.value):
                        dk_players.remove(last_loss)
                        player.dk_position="2B"
                        dk_players.append(player)
                        continue
                if "3B" in player.position:
                    last_loss = [player for player in dk_players if player.dk_position=="3B"]
                    try:
                        last_loss = last_loss[0]
                    except IndexError:
                        ipdb.set_trace()
                    everyone_else = [player for player in dk_players if player.name!=last_loss.name]
                    salary_with_nine = sum([float(player.salary) for player in everyone_else])
                    new_total_salary = salary_with_nine + float(player.salary)
                    if new_total_salary <=50 and float(player.value) > float(last_loss.value):
                        dk_players.remove(last_loss)
                        player.dk_position="3B"
                        dk_players.append(player)
                        continue
                if "SS" in player.position:
                    last_loss = [player for player in dk_players if player.dk_position=="SS"]
                    try:
                        last_loss = last_loss[0]
                    except IndexError:
                        ipdb.set_trace()
                    everyone_else = [player for player in dk_players if player.name!=last_loss.name]
                    salary_with_nine = sum([float(player.salary) for player in everyone_else])
                    new_total_salary = salary_with_nine + float(player.salary)
                    if new_total_salary <=50 and float(player.value) > float(last_loss.value):
                        dk_players.remove(last_loss)
                        player.dk_position="SS"
                        dk_players.append(player)
                        continue
                if "RF" in player.position or "LF" in player.position or "CF" in player.position or "OF" in player.position:
                    outfielder_array = [player for player in dk_players if player.dk_position=="OF"]
                    for last_loss in outfielder_array:
                        everyone_else = [player for player in dk_players if player.name!=last_loss.name]
                        salary_with_nine = sum([float(player.salary) for player in everyone_else])
                        new_total_salary = salary_with_nine + float(player.salary)
                        if new_total_salary <=50 and float(player.value) > float(last_loss.value):
                            dk_players.remove(last_loss)
                            player.dk_position="OF"
                            dk_players.append(player)
                            break


    for player in dk_players:
        print(f"{player.name}, {player.dk_position}: ${player.salary}K")
    

    ipdb.set_trace()

    print("Hi")



   