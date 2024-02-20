from app import *
from statistics import mean,mode,median
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
            

    #get game data




    #schedule_page_url = f"https://rotogrinders.com/lineups/mlb?date={year_string}-{month_string}-{day_string}&site=draftkings"
    schedule_page_url = f"https://rotogrinders.com/lineups/mlb?date=2021-05-24&site=draftkings"
    schedule_page = requests.get(schedule_page_url, headers = {'User-Agent':"Mozilla/5.0"})
    schedule = BeautifulSoup(schedule_page.text, 'html.parser')
    
    games = schedule.select('li[data-role="lineup-card"]')

    player_list = []
    game_list = []

    for game in games:


        header = game.select('header')[0]

        time = header.select('time')[0].text
        time_hour = time.split(":")[0]
        final_time = datetime.strptime(date_string + (' ') + (' ').join(time.split(' ')[0:2]),"%A, %B %d, %Y %I:%M %p")
        away = header.select('div.teams')[0].select('span')[1].text + ' ' + header.select('div.teams')[0].select('span')[3].text
        home = header.select('div.teams')[0].select('span')[5].text + ' ' + header.select('div.teams')[0].select('span')[7].text
        stadium = stadiums[home]
        

        if len(game.select('.wind-status')) > 0:
            temperature = int(game.select('.wind-status')[0].select('span.humidity')[0].text.replace('°',''))
            wind = game.select('.wind-status')[0].select('li')[0].select('span')[0].text.split(' ')
            wind_direction = wind[0]
            wind_speed = wind[2]
            wind_factor = wind_correction_factors[stadium]
            hours_list = game.select('.precip-status')[0].select('.precip')[0].select('li')
            sun = game.select('.icn-sunny')
            if len(sun) > 0:
                cloud_or_sun = "Sunny"
            else:
                cloud_or_sun = "Cloudy"


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
                game_time = hour.select('span')[1].text.split(' ')[0]
                if game_time==time_hour:
                    if percent >= 40 and temperature > 35:
                        precipitation = "Rain"
                    elif percent >= 40 and temperature <=35:
                        precipitation = "Snow"
                    else:
                        precipitation = "No Precipitation"
                    
        else:
            final_wind_direction = 400
            temperature = 70
            precipitation = "No Precipitation"
            wind_speed = 0
            cloud_or_sun = "In Dome"

        

        game_list.append({"time":final_time,
            "home":home,
            "away":away,
            "precipitation":precipitation,
            "wind_direction":final_wind_direction,
            "wind_speed":wind_speed,
            "temperature":temperature,
            "cloud_or_sun":cloud_or_sun,
            "stadium":stadium})

        #away players

        away_pitcher = game.select('div.pitcher')[0]
        away_hitters = game.select('ul.players')[0].select('li')

        name = unidecode(away_pitcher.select('a')[0].text)
        salary = away_pitcher.select('span.salary')[0].text.replace(' ','').replace('\n','').replace('$','').replace('K','')
        arm = away_pitcher.select('.stats')[0].text.replace(' ','').replace('\n','')[0]
        player_dict = {"name":name,
                "position":["SP"],
                "salary":salary,
                "team":away,
                "side":arm,
                "value":random_number(salary)}
        player_list.append(player_dict)

        for hitter in away_hitters:
            name = unidecode(hitter.select('a')[0].text)
            stat_group = hitter.select('span.stats')[0]
            bat = stat_group.select('span.stats')[0].text.replace('\n','').replace(' ','')
            #make an array of positions
            positions = stat_group.select('span.position')[0].text.replace('\n','').replace(' ','').split('/')
            salary = stat_group.select('span.salary')[0].text.replace('\n','').replace(' ','').replace('$','').replace('K','')
            player_dict = {"name":name,
                "position":positions,
                "salary":salary,
                "team":away,
                "side":bat,
                "value":random_number(salary)}
            player_list.append(player_dict)


        #home players

        home_pitcher = game.select('div.pitcher')[1]
        home_hitters = game.select('ul.players')[1].select('li')

        name = unidecode(home_pitcher.select('a')[0].text)
        salary = home_pitcher.select('span.salary')[0].text.replace(' ','').replace('\n','').replace('$','').replace('K','')
        arm = home_pitcher.select('.stats')[0].text.replace(' ','').replace('\n','')[0]
        player_dict = {"name":name,
                "position":["SP"],
                "salary":salary,
                "team":home,
                "side":arm,
                "value":random_number(salary)}
        player_list.append(player_dict)
        
        

        for hitter in home_hitters:
            name = unidecode(hitter.select('a')[0].text)
            stat_group = hitter.select('span.stats')[0]
            bat = stat_group.select('span.stats')[0].text.replace('\n','').replace(' ','')
            #make an array of positions
            positions = stat_group.select('span.position')[0].text.replace('\n','').replace(' ','').split('/')
            salary = stat_group.select('span.salary')[0].text.replace('\n','').replace(' ','').replace('$','').replace('K','')
            player_dict = {"name":name,
                "position":positions,
                "salary":salary,
                "team":home,
                "side":bat,
                "value":random_number(salary)}
            player_list.append(player_dict)


    #using value just to test DK algorithm

    sorted_players = sorted(player_list,key=itemgetter('value'))
    sorted_players.reverse()

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

    for player in sorted_players:
        if "SP" in player["position"] and pitchers<2:
            player["dk_position"]="SP"
            dk_players.append(player)
            pitchers+=1
            continue
        if "C" in player["position"] and catchers==0:
            player["dk_position"]="C"
            dk_players.append(player)
            catchers+=1
            continue
        if "1B" in player["position"] and first==0:
            player["dk_position"]="1B"
            dk_players.append(player)
            first+=1
            continue
        if "2B" in player["position"] and second==0:
            player["dk_position"]="2B"
            dk_players.append(player)
            second+=1
            continue
        if "3B" in player["position"] and third==0:
            player["dk_position"]="3B"
            dk_players.append(player)
            third+=1
            continue
        if "SS" in player["position"] and short==0:
            player["dk_position"]="SS"
            dk_players.append(player)
            short+=1
            continue
        if ("RF" in player["position"] or "LF" in player["position"] or "CF" in player["position"] or "OF" in player["position"]) and outfielders<3:
            player["dk_position"]="OF"
            dk_players.append(player)
            outfielders+=1
            continue
        if len(dk_players)==10:
            break

    [print(player) for player in dk_players]

    #if the 10 players salary is acceptable then end the algo there
    #if not, check the next few players

    total_salary = sum([float(player["salary"]) for player in dk_players])
    if total_salary > 50:
        print("Too High")
        print(total_salary)
        removed_players = []
        # new_list = sorted_players[counter:]      
        for player in sorted_players:
            if player not in dk_players:
                if "SP" in player["position"]:
                    pitcher_array = [player for player in dk_players if player["dk_position"]=="SP"]
                    for last_loss in pitcher_array:
                        if float(player["salary"]) < float(last_loss["salary"]):
                            dk_players.remove(last_loss)
                            removed_players.append(last_loss)
                            player["dk_position"]="SP"
                            dk_players.append(player)
                            break
                if "C" in player["position"]:
                    last_loss = [player for player in dk_players if player["dk_position"]=="C"]
                    last_loss = last_loss[0]
                    if float(player["salary"]) < float(last_loss["salary"]):
                        dk_players.remove(last_loss)
                        removed_players.append(last_loss)
                        player["dk_position"]="C"
                        dk_players.append(player)
                        continue
                if "1B" in player["position"]:
                    last_loss = [player for player in dk_players if player["dk_position"]=="1B"]
                    last_loss = last_loss[0]
                    if float(player["salary"]) < float(last_loss["salary"]):
                        dk_players.remove(last_loss)
                        removed_players.append(last_loss)
                        player["dk_position"]="1B"
                        dk_players.append(player)
                        continue
                if "2B" in player["position"]:
                    last_loss = [player for player in dk_players if player["dk_position"]=="2B"]
                    last_loss = last_loss[0]
                    if float(player["salary"]) < float(last_loss["salary"]):
                        dk_players.remove(last_loss)
                        removed_players.append(last_loss)
                        player["dk_position"]="2B"
                        dk_players.append(player)
                        continue
                if "3B" in player["position"]:
                    last_loss = [player for player in dk_players if player["dk_position"]=="3B"]
                    last_loss = last_loss[0]
                    if float(player["salary"]) < float(last_loss["salary"]):
                        dk_players.remove(last_loss)
                        removed_players.append(last_loss)
                        player["dk_position"]="3B"
                        dk_players.append(player)
                        continue
                if "SS" in player["position"]:
                    last_loss = [player for player in dk_players if player["dk_position"]=="SS"]
                    last_loss = last_loss[0]
                    if float(player["salary"]) < float(last_loss["salary"]):
                        dk_players.remove(last_loss)
                        removed_players.append(last_loss)
                        player["dk_position"]="SS"
                        dk_players.append(player)
                        continue
                if "RF" in player["position"] or "LF" in player["position"] or "CF" in player["position"] or "OF" in player["position"]:
                    outfielder_array =  [player for player in dk_players if player["dk_position"]=="OF"]
                    for last_loss in outfielder_array:
                        if float(player["salary"]) < float(last_loss["salary"]):
                            dk_players.remove(last_loss)
                            removed_players.append(last_loss)
                            player["dk_position"]="OF"
                            dk_players.append(player)
                            break
                total_salary = sum([float(player["salary"]) for player in dk_players])
                if total_salary < 50:
                    break   

        #now that we replaced a few players until we got the salary below the max,
        #we have a list of removed players who may be able to go back in
        
        if len(removed_players) > 0:
            for player in removed_players:
                if "SP" in player["position"]:
                    pitcher_array = [player for player in dk_players if player["dk_position"]=="SP"]
                    for last_loss in pitcher_array:
                        everyone_else = [player for player in dk_players if player["name"]!=last_loss["name"]]
                        salary_with_nine = sum([float(player["salary"]) for player in everyone_else])
                        new_total_salary = salary_with_nine + float(player["salary"])
                        if  new_total_salary <=50 and float(player["value"]) > float(last_loss["value"]):
                            dk_players.remove(last_loss)
                            player["dk_position"]="SP"
                            dk_players.append(player)
                            break
                if "C" in player["position"]:
                    last_loss = [player for player in dk_players if player["dk_position"]=="C"]
                    try:
                        last_loss = last_loss[0]
                    except IndexError:
                        ipdb.set_trace()
                    everyone_else = [player for player in dk_players if player["name"]!=last_loss["name"]]
                    salary_with_nine = sum([float(player["salary"]) for player in everyone_else])
                    new_total_salary = salary_with_nine + float(player["salary"])
                    if new_total_salary <=50 and float(player["value"]) > float(last_loss["value"]):
                        dk_players.remove(last_loss)
                        player["dk_position"]="C"
                        dk_players.append(player)
                        continue
                if "1B" in player["position"]:
                    last_loss = [player for player in dk_players if player["dk_position"]=="1B"]
                    try:
                        last_loss = last_loss[0]
                    except IndexError:
                        ipdb.set_trace()
                    everyone_else = [player for player in dk_players if player["name"]!=last_loss["name"]]
                    salary_with_nine = sum([float(player["salary"]) for player in everyone_else])
                    new_total_salary = salary_with_nine + float(player["salary"])
                    if new_total_salary <=50 and float(player["value"]) > float(last_loss["value"]):
                        dk_players.remove(last_loss)
                        player["dk_position"]="1B"
                        dk_players.append(player)
                        continue
                if "2B" in player["position"]:
                    last_loss = [player for player in dk_players if player["dk_position"]=="2B"]
                    try:
                        last_loss = last_loss[0]
                    except IndexError:
                        ipdb.set_trace()
                    everyone_else = [player for player in dk_players if player["name"]!=last_loss["name"]]
                    salary_with_nine = sum([float(player["salary"]) for player in everyone_else])
                    new_total_salary = salary_with_nine + float(player["salary"])
                    if new_total_salary <=50 and float(player["value"]) > float(last_loss["value"]):
                        dk_players.remove(last_loss)
                        player["dk_position"]="2B"
                        dk_players.append(player)
                        continue
                if "3B" in player["position"]:
                    last_loss = [player for player in dk_players if player["dk_position"]=="3B"]
                    try:
                        last_loss = last_loss[0]
                    except IndexError:
                        ipdb.set_trace()
                    everyone_else = [player for player in dk_players if player["name"]!=last_loss["name"]]
                    salary_with_nine = sum([float(player["salary"]) for player in everyone_else])
                    new_total_salary = salary_with_nine + float(player["salary"])
                    if new_total_salary <=50 and float(player["value"]) > float(last_loss["value"]):
                        dk_players.remove(last_loss)
                        player["dk_position"]="3B"
                        dk_players.append(player)
                        continue
                if "SS" in player["position"]:
                    last_loss = [player for player in dk_players if player["dk_position"]=="SS"]
                    try:
                        last_loss = last_loss[0]
                    except IndexError:
                        ipdb.set_trace()
                    everyone_else = [player for player in dk_players if player["name"]!=last_loss["name"]]
                    salary_with_nine = sum([float(player["salary"]) for player in everyone_else])
                    new_total_salary = salary_with_nine + float(player["salary"])
                    if new_total_salary <=50 and float(player["value"]) > float(last_loss["value"]):
                        dk_players.remove(last_loss)
                        player["dk_position"]="SS"
                        dk_players.append(player)
                        continue
                if "RF" in player["position"] or "LF" in player["position"] or "CF" in player["position"] or "OF" in player["position"]:
                    outfielder_array = [player for player in dk_players if player["dk_position"]=="OF"]
                    for last_loss in outfielder_array:
                        everyone_else = [player for player in dk_players if player["name"]!=last_loss["name"]]
                        salary_with_nine = sum([float(player["salary"]) for player in everyone_else])
                        new_total_salary = salary_with_nine + float(player["salary"])
                        if new_total_salary <=50 and float(player["value"]) > float(last_loss["value"]):
                            dk_players.remove(last_loss)
                            player["dk_position"]="OF"
                            dk_players.append(player)
                            break

        

    #parse espn injury page
    injury_url = "https://www.espn.com/mlb/injuries"
    injury_page = requests.get(injury_url, headers={'User-Agent':"Mozilla/5.0"})
    injuries = BeautifulSoup(injury_page.text, 'html.parser')
    injury_page = injuries.select('.ResponsiveTable')

    #collect injury dictionary
    injured_list = {}


    for injured in injury_page:
        team_name = injured.select('.Table__Title')[0].text
        
        players = injured.select('tbody')[0].select('tr')
        injured_players = []
        for player in players:
            player_info = player.select('td')[4].text
            if player.select('td')[3].text=='Out' and "is expected to be cleared" not in player_info and "will play" not in player_info and "plans to play" not in player_info:
                injured_players.append(player.select('td')[0].text)
                
        injured_list[team_name] = injured_players


    #collect player prop data

    #create empty odds dictionary

    # odds_dict = {}
    # all_players = Player.query.all()
    # for player in all_players:
    #     odds_dict[player.name]={}


    # #draftkings player props

    # action_network_points_url = 'https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/42648/categories/1215?format=json'
    # action_network_assists_url = 'https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/42648/categories/1217?format=json'
    # action_network_rebounds_url = 'https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/42648/categories/1216?format=json'
   

    # #action network player props

    # # action_network_points_url = 'https://www.actionnetwork.com/nba/props/points'
    # # action_network_assists_url = 'https://www.actionnetwork.com/nba/props/assists'
    # # action_network_rebounds_url = 'https://www.actionnetwork.com/nba/props/rebounds'

    # action_network_points = requests.get(action_network_points_url, headers={'User-Agent':"Mozilla/5.0"}, allow_redirects=False)
    # action_network_assists = requests.get(action_network_assists_url, headers={'User-Agent':"Mozilla/5.0"}, allow_redirects=False)
    # action_network_rebounds = requests.get(action_network_rebounds_url, headers={'User-Agent':"Mozilla/5.0"}, allow_redirects=False)

    # try: 
    #     points_page = action_network_points.json()["eventGroup"]["offerCategories"][2]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    # except KeyError:
    #     try:
    #         points_page = action_network_points.json()["eventGroup"]["offerCategories"][3]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #     except KeyError:
    #         try:
    #             points_page = action_network_points.json()["eventGroup"]["offerCategories"][4]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #         except KeyError:
    #             try:
    #                 points_page = action_network_points.json()["eventGroup"]["offerCategories"][5]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #             except KeyError:
    #                 try:
    #                     points_page = action_network_points.json()["eventGroup"]["offerCategories"][6]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #                 except KeyError:
    #                     try:
    #                         points_page = action_network_points.json()["eventGroup"]["offerCategories"][7]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #                     except KeyError:
    #                         try:
    #                             points_page = action_network_points.json()["eventGroup"]["offerCategories"][8]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #                         except KeyError:
    #                             points_page = action_network_points.json()["eventGroup"]["offerCategories"][9]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]

    # try: 
    #     rebounds_page = action_network_rebounds.json()["eventGroup"]["offerCategories"][2]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    # except KeyError:
    #     try:
    #         rebounds_page = action_network_rebounds.json()["eventGroup"]["offerCategories"][3]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #     except KeyError:
    #         try:
    #             rebounds_page = action_network_rebounds.json()["eventGroup"]["offerCategories"][4]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #         except KeyError:
    #             try:
    #                 rebounds_page = action_network_rebounds.json()["eventGroup"]["offerCategories"][5]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #             except KeyError:
    #                 try:
    #                     rebounds_page = action_network_rebounds.json()["eventGroup"]["offerCategories"][6]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #                 except KeyError:
    #                     try:
    #                         rebounds_page = action_network_rebounds.json()["eventGroup"]["offerCategories"][7]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #                     except KeyError:
    #                         try:
    #                             rebounds_page = action_network_rebounds.json()["eventGroup"]["offerCategories"][8]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #                         except KeyError:
    #                             rebounds_page = action_network_rebounds.json()["eventGroup"]["offerCategories"][9]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]


    # try: 
    #     assists_page = action_network_assists.json()["eventGroup"]["offerCategories"][2]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    # except KeyError:
    #     try:
    #         assists_page = action_network_assists.json()["eventGroup"]["offerCategories"][3]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #     except KeyError:
    #         try:
    #             assists_page = action_network_assists.json()["eventGroup"]["offerCategories"][4]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #         except KeyError:
    #             try:
    #                 assists_page = action_network_assists.json()["eventGroup"]["offerCategories"][5]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #             except KeyError:
    #                 try:
    #                     assists_page = action_network_assists.json()["eventGroup"]["offerCategories"][6]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #                 except KeyError:
    #                     try:
    #                         assists_page = action_network_assists.json()["eventGroup"]["offerCategories"][7]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #                     except KeyError:
    #                         try:
    #                             assists_page = action_network_assists.json()["eventGroup"]["offerCategories"][8]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    #                         except KeyError:
    #                             assists_page = action_network_assists.json()["eventGroup"]["offerCategories"][9]["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"]
    
    # for offer in points_page:
    #     for inside in offer:
    #         name = inside["outcomes"][0]["participant"]
    #         if name.endswith(" "):
    #             name = name.rstrip(name[-1])
    #         if name.startswith(" "):
    #             name = name[1:]
    #         line = inside["outcomes"][0]["line"]
    #         if name in odds_dict:
    #             odds_dict[name]["points"] = line
    #         else:
    #             odds_dict[name] = {}
    #             odds_dict[name]["points"] = line

    # for offer in rebounds_page:
    #     for inside in offer:
    #         name = inside["outcomes"][0]["participant"]
    #         if name.endswith(" "):
    #             name = name.rstrip(name[-1])
    #         if name.startswith(" "):
    #             name = name[1:]
    #         line = inside["outcomes"][0]["line"]
    #         if name in odds_dict:
    #             odds_dict[name]["rebounds"] = line
    #         else:
    #             odds_dict[name] = {}
    #             odds_dict[name]["rebounds"] = line

    # for offer in assists_page:
    #     for inside in offer:
    #         name = inside["outcomes"][0]["participant"]
    #         if name.endswith(" "):
    #             name = name.rstrip(name[-1])
    #         if name.startswith(" "):
    #             name = name[1:]
    #         line = inside["outcomes"][0]["line"]
    #         if name in odds_dict:
    #             odds_dict[name]["assists"] = line
    #         else:
    #             odds_dict[name] = {}
    #             odds_dict[name]["assists"] = line


    # new_odds_dict = odds_dict.copy()

    # for item in odds_dict:
    #     if odds_dict[item] == {}:
    #         del(new_odds_dict[item])


    # new_odds_dict = sorted(new_odds_dict.items(),key=lambda kv: kv)
    # new_odds_dict = dict(sorted(new_odds_dict.items()))

    #new_odds_dict is a dicitonary of all today's props

    bets = []
    high_value_teasers = []
    low_value_teasers = []
    games_in_a_row = []
    weekday_games = []
    counter = 0 


    #find league average babip over last 100k abs

    league_abs = AtBat.query.all()[-100000:]

    league_avg_babip_numerator = len([ab for ab in league_abs if ab.result=="Triple" or ab.result=="Double" or ab.result=="Single"])
    league_avg_babip_denominator = len([ab for ab in league_abs if "Strikeout" not in ab.result and ab.result!="Home Run" and ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result])
    league_babip = league_avg_babip_numerator/league_avg_babip_denominator


    league_in_play_percentage = league_avg_babip_denominator/len(league_abs)
   

    for player in player_list:

        player_name = player["name"]
        player_team = player["team"]
        game = [game for game in game_list if game["home"]==player_team or game["away"]==player_team][0]
        if game["home"]==player_team:
            other_team = game["away"]
        else:
            other_team = game["home"]
        
        #collect my own data about every game they've played in

        if "SP" in player["position"]:
            current_player = Pitcher.query.filter(Pitcher.name==player_name).first()
            hitter = 0
        else:
            current_player = Hitter.query.filter(Hitter.name==player_name).first()
            pitcher_name = [player["name"] for player in player_list if "SP" in player["position"] and player["team"]==other_team][0]
            pitcher_object = Pitcher.query.filter(Pitcher.name==pitcher_name).first()
            hitter = 1


        
        
        if current_player:    


            # specific_time = datetime(2024,1,21,16,30,00)
            #and specific_time.time() < [game["time"] for game in todays_games if game["home"]==player_team or game["away"]==player_team][0]

            if ([game["time"].time() for game in game_list if game["home"]==player_team or game["away"]==player_team][0] > format_time):

                print(f"{player_name} ({player_team})")


                if hitter:

                    abs = current_player.at_bats

                    #find info for babip modifier

                    hitter_total_abs = [ab for ab in abs if ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result]
                    hitter_balls_in_play = [ab for ab in hitter_total_abs if "Strikeout" not in ab.result and ab.result!="Home Run"]
                    hitter_babip_numerator = len([ab for ab in hitter_balls_in_play if ab.result=="Triple" or ab.result=="Double" or ab.result=="Single"])


                    hitter_in_play_percentage = len(hitter_balls_in_play)/len(hitter_total_abs)
                    hitter_babip = hitter_babip_numerator/len(hitter_balls_in_play)

                    #find percentage of balls in play by pitcher


                    all_pitcher_abs = pitcher_object.at_bats
                    pitcher_total_abs = [ab for ab in pitcher_object.at_bats if ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result]
                    pitcher_balls_in_play = [ab for ab in pitcher_total_abs if "Strikeout" not in ab.result and ab.result!="Home Run"]
                    pitcher_babip_numerator = len([ab for ab in pitcher_balls_in_play if ab.result=="Triple" or ab.result=="Double" or ab.result=="Single"])


                    pitcher_in_play_percentage = len(pitcher_balls_in_play)/len(pitcher_total_abs)
                    pitcher_babip = pitcher_babip_numerator/len(pitcher_balls_in_play)

                    
                    
                    #latest 25 abs at time
                    upper_hour = game["time"].hour+1
                    lower_hour = game["time"].hour-1
                    minutes = game["time"].minute
                    upper_time = datetime(2023,2,1,upper_hour,minutes).time()
                    lower_time = datetime(2023,2,1,lower_hour,minutes).time()
                    abs_at_time = [ab for ab in abs if ab.game.date.time()<=upper_time and ab.game.date.time()>=lower_time][-25:]
                   
                    #last 25 abs on specific day
                    current_day = current_date.weekday()
                    abs_on_day = []
                    for ab in abs:
                        if ab.game.date.weekday()==current_day:
                            abs_on_day.append(ab)

                    abs_on_day = abs_on_day[-25:]


                
                    #last 30 abs
                    latest_games = [ab for ab in abs][-30:]


                    #home/away games
                    if game["home"]==player_team:
                        latest_home_or_away_abs = [ab for ab in abs if ab.game.home==player_team][-50:]
                    else:
                        latest_home_or_away_abs = [ab for ab in abs if ab.game.visitor==player_team][-50:]
                    

                    
                    # #get latest matchups vs pitcher
                    # abs_vs_opponent = [ab for ab in abs if (ab.pitcher.name==pitcher_name)][-15:]

                    # #other things I need

                    # #abs vs lefty/righty 

                    # abs_vs_left_right = [ab for ab in abs if ab.pitcher.arm==pitcher_object.arm][-50:]

                    # #right-left modifier

                    # #pitchers average when facing opposite side batter

                    # total_abs_opp = [ab for ab in pitcher_object.at_bats if ab.hitter.bat!=pitcher_object.arm]
                    # abs_with_hit_opp = len([ab for ab in total_abs_opp if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run"])

                    # pitcher_opposite_avg = abs_with_hit_opp/len(total_abs_opp)


                    # #pitchers avg when facing same side batter

                    # total_abs_same = [ab for ab in pitcher_object.at_bats if ab.hitter.bat==pitcher_object.arm]
                    # abs_with_hit_same = len([ab for ab in total_abs_same if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run"])

                    # pitcher_same_avg = abs_with_hit_same/len(total_abs_same)


                    # #modifier will likely be around 1
                    # #above 1 if pitcher is better against opposite
                    # #less than 1 if pitcher is worse against opposite

                    # batter_side_modifier = pitcher_opposite_avg/pitcher_same_avg


                    

                    #babip modifier
                    
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

                    
                    ipdb.set_trace()



                    #create new implied batting average by multipying hitter 

                    #babip
                        #compare pitchers allowed babip to hitter's babip

                    #at stadium
                    at_stadium = [ab for ab in abs if ab.game.location == game["stadium"]] 

                    #with wind direction
                    wind_high = wind_direction + 22.5
                    wind_low = wind_direction - 22.5

                    wind_direction_abs = [ab for ab in abs if wind_low <= ab.game.wind_direction <= wind_high]

                    #wind speed
                    wind_speed_high = wind_speed + 2
                    wind_speed_low = wind_speed - 2

                    wind_speed_abs = [ab for ab in abs if wind_speed_low <= ab.game.wind_speed <= wind_speed_high]




                    #sunny/cloudy
                    #Overcast, Sunny, Cloudy, In Dome
                    if game["cloud_or_sun"]=="Cloudy":
                        cloud_or_sun_abs = [ab for ab in abs if ab.game.cloud_or_sun=="Cloudy" or ab.game.cloud_or_sun=="Overcast"]
                    elif game["cloud_or_sun"]=="Sunny":
                        cloud_or_sun_abs = [ab for ab in abs if ab.game.cloud_or_sun=="Sunny"]
                    else:
                        cloud_or_sun_abs = []


                    #precipitation
                    if game["precipitation"]=="Rain":
                        precipitation_abs = [ab for ab in abs if ab.game.precipitation=="Rain" or ab.game.precipitation=="Drizzle"]
                    elif game["precipitation"]=="Snow":
                        precipitation_abs = [ab for ab in abs if ab.game.precipitation=="Snow"]
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

                    if game["temperature"] <= freezing:
                        temperature_abs = [ab for ab in abs if ab.game.temperature <= freezing]
                    elif freezing < game["temperature"] <= real_cold:
                        temperature_abs = [ab for ab in abs if freezing < ab.game.temperature <= real_cold]
                    elif real_cold < game["temperature"] <= very_cold:
                        temperature_abs = [ab for ab in abs if real_cold < ab.game.temperature <= very_cold]
                    elif very_cold < game["temperature"] <= cold:
                        temperature_abs = [ab for ab in abs if very_cold < ab.game.temperature <= cold]
                    elif cold < game["temperature"] <= nice:
                        temperature_abs = [ab for ab in abs if cold < ab.game.temperature <= nice]
                    elif nice < game["temperature"] <= hot:
                        temperature_abs = [ab for ab in abs if nice < ab.game.temperature <= hot]
                    elif hot < game["temperature"] <= too_hot:
                        temperature_abs = [ab for ab in abs if hot < ab.game.temperature <= too_hot]
                    else:
                        temperature_abs = [ab for ab in abs if ab.game.temperature > too_hot]

                    #vs team
                    abs_vs_team = [ab for ab in abs if ab.game.home==other_team or ab.game.visitor==other_team]



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
                    latest_home_or_away_games.extend(games_at_time)
                    latest_home_or_away_games.extend(games_vs_opponent)
                    if injury:
                        latest_home_or_away_games.extend(games_with_injury[-3:])
                    if opponent_injury:
                        latest_home_or_away_games.extend(games_with_opp_injury[-3:])
                    latest_home_or_away_games.extend(games_on_day)
                    latest_home_or_away_games.extend(rest_days)

                    latest_home_or_away_games.reverse()

                    #find most similar game
                    most_similar = mode(latest_home_or_away_games)
                    assists_similar = most_similar.assists
                    points_similar = most_similar.points
                    trb_similar = most_similar.trb


                    new_game_list = set(latest_home_or_away_games)

                    uniq_game_list = list(new_game_list)


                    uniq_game_list = [game for game in uniq_game_list]



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