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

    

    pitchers_left = [player for player in Pitcher.query.all() if player.arm!="L" and player.arm!="R" and player.arm!="B" and player.arm!="S"]

    total_players = len(pitchers_left)

    counter = 0

    for player in pitchers_left:

        counter+=1

        print(player.name)
        print(f"{total_players - counter} left")

        name_array = player.name.replace("Jr.",'').replace("Sr.",'').replace("'",'').replace('.','').split(" ")
        first_name = name_array[0].lower()
        if len(name_array) > 2:
            last_name = ('').join(name_array[1:]).lower()
        else:
            last_name = name_array[-1].lower()

        string = f"{last_name[0]}/{last_name[0:5]}{first_name[0:2]}0"

        numbers = [1,2,3,4,5,6,7,8,9,10]

        for number in numbers:


            if number == 10:
                string = string[:len(string)-1]

            # ipdb.set_trace()

            site_url = f"https://www.baseball-reference.com/players/{string}{number}.shtml"


            depth_page = requests.get(site_url, headers = {'User-Agent':"Mozilla/5.0"})
            depth_chart = BeautifulSoup(depth_page.text, 'html.parser')

            if depth_page.status_code==404:
                time.sleep(3.2)
                if number==10:
                    if len(name_array) > 2:
                        first_name = ('').join(name_array[0:1]).lower()
                        last_name = name_array[-1].lower()
                    else:
                        last_name = name_array[-1].lower()

                    string = f"{last_name[0]}/{last_name[0:5]}{first_name[0:2]}0"

                    for number in numbers:
                        if number == 10:
                            string = string[:len(string)-1]
                        site_url = f"https://www.baseball-reference.com/players/{string}{number}.shtml"


                        depth_page = requests.get(site_url, headers = {'User-Agent':"Mozilla/5.0"})
                        depth_chart = BeautifulSoup(depth_page.text, 'html.parser')

                        if depth_page.status_code==404:
                            time.sleep(3.2)
                            continue

                        else:
                            last_year = depth_chart.select('table.row_summable')[0].select('tbody')[0].select('tr.full')[-1].select('th')[0].text

                            if last_year == "2021" or last_year == "2022" or last_year == "2023":

                                handedness_array = depth_chart.select('div.players')[0].select('p')[1].text.replace('\n','').replace('\xa0','').replace('•\t','').split(' ')
                                for index,value in enumerate(handedness_array):
                                    if value=="Throws:":
                                        arm = handedness_array[index+1][0]
                                        break
                                player.arm=arm
                                db.session.commit()

                                break

                            else: 
                                time.sleep(3.2)

                continue

            else:

                last_year = depth_chart.select('table.row_summable')[0].select('tbody')[0].select('tr.full')[-1].select('th')[0].text

                if last_year == "2021" or last_year == "2022" or last_year == "2023":

                    handedness_array = depth_chart.select('div.players')[0].select('p')[1].text.replace('\n','').replace('\xa0','').replace('•\t','').split(' ')
                    for index,value in enumerate(handedness_array):
                        if value=="Throws:":
                            arm = handedness_array[index+1][0]
                            break
                    player.arm=arm
                    db.session.commit()

                    break

                else: 
                    time.sleep(3.2)



        time.sleep(3.2)






    hitters_left = [player for player in Hitter.query.all() if player.bat!="L" and player.bat!="R" and player.bat!="B" and player.bat!="S"]

    ipdb.set_trace()

    total_players = len(hitters_left)

    counter = 0

    for player in hitters_left:

        counter+=1

        print(player.name)
        print(f"{total_players - counter} left")

        name_array = player.name.replace("Jr.",'').replace("Sr.",'').replace("'",'').replace('.','').split(" ")
        first_name = name_array[0].lower()
        if len(name_array) > 2:
            last_name = ('').join(name_array[1:]).lower()
        else:
            last_name = name_array[-1].lower()

        string = f"{last_name[0]}/{last_name[0:5]}{first_name[0:2]}0"

        numbers = [1,2,3,4,5,6,7,8,9,10]

        for number in numbers:


            if number == 10:
                string = string[:len(string)-1]

            # ipdb.set_trace()

            site_url = f"https://www.baseball-reference.com/players/{string}{number}.shtml"

            depth_page = requests.get(site_url, headers = {'User-Agent':"Mozilla/5.0"})
            depth_chart = BeautifulSoup(depth_page.text, 'html.parser')

            if depth_page.status_code==404:
                time.sleep(3.2)
                if number==10:
                    if len(name_array) > 2:
                        first_name = ('').join(name_array[0:1]).lower()
                        last_name = name_array[-1].lower()
                    else:
                        last_name = name_array[-1].lower()

                    string = f"{last_name[0]}/{last_name[0:5]}{first_name[0:2]}0"

                    for number in numbers:
                        if number == 10:
                            string = string[:len(string)-1]
                        site_url = f"https://www.baseball-reference.com/players/{string}{number}.shtml"


                        depth_page = requests.get(site_url, headers = {'User-Agent':"Mozilla/5.0"})
                        depth_chart = BeautifulSoup(depth_page.text, 'html.parser')

                        if depth_page.status_code==404:
                            time.sleep(3.2)
                            continue

                        else:
                            last_year = depth_chart.select('table.row_summable')[0].select('tbody')[0].select('tr.full')[-1].select('th')[0].text

                            if last_year == "2021" or last_year == "2022" or last_year == "2023":

                                handedness_array = depth_chart.select('div.players')[0].select('p')[1].text.replace('\n','').replace('\xa0','').replace('•\t','').split(' ')
                                for index,value in enumerate(handedness_array):
                                    if value=="Bats:":
                                        bat = handedness_array[index+1][0]
                                        break
                                player.bat=bat
                                db.session.commit()

                                break
                            else: 
                                time.sleep(3.2)

                continue

            else:

                try:
                    last_year = depth_chart.select('table.row_summable')[0].select('tbody')[0].select('tr.full')[-1].select('th')[0].text
                except IndexError:
                    time.sleep(3.2)
                    first_name = name_array[0:2].lower()
                    last_name = name_array[-1].lower()
                    string = f"{last_name[0]}/{last_name[0:5]}{first_name[0:2]}01"
                    site_url = f"https://www.baseball-reference.com/players/{string}{number}.shtml"

                    depth_page = requests.get(site_url, headers = {'User-Agent':"Mozilla/5.0"})
                    depth_chart = BeautifulSoup(depth_page.text, 'html.parser')
                    last_year = depth_chart.select('table.row_summable')[0].select('tbody')[0].select('tr.full')[-1].select('th')[0].text



                if last_year == "2021" or last_year == "2022" or last_year == "2023":

                    handedness_array = depth_chart.select('div.players')[0].select('p')[1].text.replace('\n','').replace('\xa0','').replace('•\t','').split(' ')
                    for index,value in enumerate(handedness_array):
                        if value=="Bats:":
                            bat = handedness_array[index+1][0]
                            break
                    player.bat=bat
                    db.session.commit()

                    break

                else: 
                    time.sleep(3.2)



        time.sleep(3.2)

       












# ________________________________________________________


#  bets = []
#     high_value_teasers = []
#     low_value_teasers = []
#     games_in_a_row = []
#     weekday_games = []
#     counter = 0 


#     #find league average babip over last 100k abs

#     league_abs = AtBat.query.all()[-100000:]
#     thousand_games = Game.query.all()[-100:]

#     league_avg_babip_numerator = len([ab for ab in league_abs if ab.result=="Triple" or ab.result=="Double" or ab.result=="Single"])
#     league_avg_babip_denominator = len([ab for ab in league_abs if "Strikeout" not in ab.result and ab.result!="Home Run" and ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result])
#     league_babip = league_avg_babip_numerator/league_avg_babip_denominator

#     league_avg_abs = [ab for ab in league_abs if ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result]
#     league_avg_hits = len([ab for ab in league_avg_abs if ab.result=="Home Run" or ab.result=="Triple" or ab.result=="Double" or ab.result=="Single"])

#     league_avg = league_avg_hits/len(league_avg_abs)

#     # league_avg_ks
#     list_of_ks = []
#     for a_game in thousand_games:
#         home = a_game.home
#         away = a_game.visitor
#         ab1_home = [ab for ab in a_game.at_bats if away==ab.team][0]
#         ab1_away = [ab for ab in a_game.at_bats if home==ab.team][0]
#         abs_to_count = [ab for ab in a_game.at_bats if ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result]
#         ks = [ab for ab in a_game.at_bats if "Strikeout" in ab.result]
#         pitcher_1_ks = len([ab for ab in ks if ab.pitcher==ab1_home.pitcher])
#         pitcher_2_ks = len([ab for ab in ks if ab.pitcher==ab1_away.pitcher])
#         list_of_ks.append(pitcher_1_ks)
#         list_of_ks.append(pitcher_2_ks)
#     league_avg_ks = mean(list_of_ks)

#     # league_avg_innings_pitched
#     list_of_outs = []
#     for a_game in thousand_games:
#         home = a_game.home
#         away = a_game.visitor
#         ab1_home = [ab for ab in a_game.at_bats if away==ab.team][0]
#         ab1_away = [ab for ab in a_game.at_bats if home==ab.team][0]
#         outs = [ab for ab in a_game.at_bats if "Out" in ab.result or "out" in ab.result or "Pop" in ab.result or "Choice" in ab.result or "Fly" in ab.result]
#         pitcher_1_outs = len([ab for ab in outs if ab.pitcher==ab1_home.pitcher])
#         pitcher_2_outs = len([ab for ab in outs if ab.pitcher==ab1_away.pitcher])
#         list_of_outs.append(pitcher_1_outs)
#         list_of_outs.append(pitcher_2_outs)
#     league_avg_outs = mean(list_of_outs)


#     league_in_play_percentage = league_avg_babip_denominator/len(league_abs)


#     league_on_first_abs = [ab for ab in league_abs if ab.result=="Single" or ab.result=="Walk" or ab.result=="Hit" or "Reached" in ab.result or "Choice" in ab.result]

#     league_sb_abs = len([ab for ab in league_on_first_abs if ab.sb_att>=1])

#     league_sb_perc = league_sb_abs/len(league_on_first_abs)

#     league_sb_attempts = [ab for ab in AtBat.query.all() if ab.sb_att > 0]
#     league_sb_abs = len([ab for ab in league_sb_attempts if ab.sb > 0])

#     league_sb_success = league_sb_abs/len(league_sb_attempts)
   

#     for player in player_list:

#         player_name = player.name
#         player_team = player["team"]
#         game = [game for game in game_list if game["home"]==player_team or game["away"]==player_team][0]
#         if game["home"]==player_team:
#             other_team = game["away"]
#         else:
#             other_team = game["home"]
        
#         #collect my own data about every game they've played in

#         if "SP" in player.position:
#             current_player = Pitcher.query.filter(Pitcher.name==player_name).first()
#             hitter = 0
#         else:
#             current_player = Hitter.query.filter(Hitter.name==player_name).first()
#             pitcher_name = [player.name for player in player_list if "SP" in player.position and player["team"]==other_team][0]
#             pitcher_object = Pitcher.query.filter(Pitcher.name==pitcher_name).first()
#             hitter = 1


        
        
#         if current_player:    


#             # specific_time = datetime(2024,1,21,16,30,00)
#             #and specific_time.time() < [game["time"] for game in game_list if game["home"]==player_team or game["away"]==player_team][0]

#             if ([game["time"].time() for game in game_list if game["home"]==player_team or game["away"]==player_team][0] > format_time):

#                 print(f"{player_name} ({player_team})")

#                 abs = current_player.at_bats

#                 if hitter:

#                     #find info for babip modifier

#                     hitter_total_abs = [ab for ab in abs if ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result]
#                     hitter_balls_in_play = [ab for ab in hitter_total_abs if "Strikeout" not in ab.result and ab.result!="Home Run"]
#                     hitter_babip_numerator = len([ab for ab in hitter_balls_in_play if ab.result=="Triple" or ab.result=="Double" or ab.result=="Single"])


#                     hitter_in_play_percentage = len(hitter_balls_in_play)/len(hitter_total_abs)
#                     hitter_babip = hitter_babip_numerator/len(hitter_balls_in_play)

#                     #find percentage of balls in play by pitcher


#                     all_pitcher_abs = pitcher_object.at_bats
#                     pitcher_total_abs = [ab for ab in all_pitcher_abs if ab.result!="Sacrifice" and ab.result!="Walk" and ab.result!="Hit" and "Interference" not in ab.result]
#                     pitcher_balls_in_play = [ab for ab in pitcher_total_abs if "Strikeout" not in ab.result and ab.result!="Home Run"]
#                     pitcher_babip_numerator = len([ab for ab in pitcher_balls_in_play if ab.result=="Triple" or ab.result=="Double" or ab.result=="Single"])


#                     #pitcher in play % and babip

#                     pitcher_in_play_percentage = len(pitcher_balls_in_play)/len(pitcher_total_abs)
#                     pitcher_babip = pitcher_babip_numerator/len(pitcher_balls_in_play)

                    
                    
#                     #latest 25 abs at time
#                     upper_hour = game["time"].hour+1
#                     lower_hour = game["time"].hour-1
#                     minutes = game["time"].minute
#                     upper_time = datetime(2023,2,1,upper_hour,minutes).time()
#                     lower_time = datetime(2023,2,1,lower_hour,minutes).time()
#                     abs_at_time = [ab for ab in abs if ab.game.date.time()<=upper_time and ab.game.date.time()>=lower_time][-25:]
                   
#                     #last 25 abs on specific day
#                     current_day = current_date.weekday()
#                     abs_on_day = []
#                     for ab in abs:
#                         if ab.game.date.weekday()==current_day:
#                             abs_on_day.append(ab)

#                     abs_on_day = abs_on_day[-25:]


                
#                     #last 30 abs
#                     latest_games = [ab for ab in abs][-30:]


#                     #home/away games
#                     if game["home"]==player_team:
#                         latest_home_or_away_abs = [ab for ab in abs if ab.game.home==player_team][-50:]
#                     else:
#                         latest_home_or_away_abs = [ab for ab in abs if ab.game.visitor==player_team][-50:]
                    

                    
#                     #get latest matchups vs pitcher
#                     abs_vs_opponent = [ab for ab in abs if (ab.pitcher.name==pitcher_name)][-15:]

#                     #other things I need

#                     #abs vs lefty/righty 

#                     abs_vs_left_right = [ab for ab in abs if ab.pitcher.arm==pitcher_object.arm][-50:]

#                     #right-left modifier

#                     #pitchers average when facing opposite side batter

#                     total_abs_opp = [ab for ab in all_pitcher_abs if ab.hitter.bat!=pitcher_object.arm and "Walk" not in ab.result and "Sacrifice" not in ab.result and "Interference" not in ab.result and "Hit" not in ab.result]
#                     abs_with_hit_opp = len([ab for ab in total_abs_opp if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run"])

#                     pitcher_opposite_avg = abs_with_hit_opp/len(total_abs_opp)


#                     #pitchers avg when facing same side batter

#                     total_abs_same = [ab for ab in all_pitcher_abs if ab.hitter.bat==pitcher_object.arm and "Walk" not in ab.result and "Sacrifice" not in ab.result and "Interference" not in ab.result and "Hit" not in ab.result]
#                     abs_with_hit_same = len([ab for ab in total_abs_same if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run"])

#                     pitcher_same_avg = abs_with_hit_same/len(total_abs_same)



#                     #hitters average when facing opposite side pitcher

#                     oppo_taco_abs = [ab for ab in abs if ab.pitcher.arm!=current_player.bat and "Walk" not in ab.result and "Sacrifice" not in ab.result and "Interference" not in ab.result and "Hit" not in ab.result]
#                     oppo_taco_hits = len([ab for ab in oppo_taco_abs if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run"])

#                     hitter_opposite_avg = oppo_taco_hits/len(oppo_taco_abs)


#                     #hitters avg when facing same side pitcher

#                     same_side_abs = [ab for ab in abs if ab.pitcher.arm==current_player.bat and "Walk" not in ab.result and "Sacrifice" not in ab.result and "Interference" not in ab.result and "Hit" not in ab.result]
#                     same_side_hits = len([ab for ab in same_side_abs if ab.result=="Single" or ab.result=="Double" or ab.result=="Triple" or ab.result=="Home Run"])
                    

#                     hitter_same_avg = same_side_hits/len(same_side_abs)

#                     if pitcher_object.arm==current_player.bat:
#                         batter_side_modifier = (0.35 * pitcher_same_avg/league_avg ) + (0.65 * hitter_same_avg/league_avg)

#                     else:
#                         batter_side_modifier = (0.35 * pitcher_opposite_avg/league_avg ) + (0.65 * hitter_opposite_avg/league_avg)

#                     #babip modifier)
                    
#                     #find percentage of balls in play compared to pitchers at bats
#                     #find hitter babip in last 150 abs 

#                     #hitter_babip
#                     #pitcher_babip
#                     #league_babip
#                     #league_in_play_percentage
#                     #pitcher_in_play_percentage
#                     #hitter_in_play_percentage

#                     babip_modifier = (pitcher_babip + hitter_babip) / (2 * league_babip)
#                     in_play_modifier = (pitcher_in_play_percentage + hitter_in_play_percentage) / (2 * league_in_play_percentage)


#                     result_modifier = (0.275 * babip_modifier + 0.05 * in_play_modifier + 0.675 * batter_side_modifier)

                    
#                     #need a sb modifier, maybe more. We'll see

#                     #sb modifier

#                     #pitchers abs where a player gets onto first

#                     on_first_abs = [ab for ab in all_pitcher_abs if ab.result=="Single" or ab.result=="Walk" or ab.result=="Hit" or "Reached" in ab.result or "Choice" in ab.result]

#                     sb_abs = len([ab for ab in on_first_abs if ab.sb>=1])

#                     sb_perc = league_sb_abs/len(league_on_first_abs)

#                     #how likely they are to steal compared to the rest of the league
#                     sb_modifier = sb_perc/league_sb_perc

#                     pitcher_list_object = [player for player in player_list if player.name==pitcher_name][0]


#                     #how bad the pitcher is against sb's (higher number means more steals)
#                     pitcher_sb_modifier = pitcher_list_object["sb_modifier"]

#                     #strikeout percentage (for pitchers)


#                     #create new implied batting average by multipying hitter 

#                     #babip
#                         #compare pitchers allowed babip to hitter's babip


#                 else:
#                     pass
#                     #pitcher algorithm





#                 #at stadium
#                 at_stadium = [ab for ab in abs if ab.game.location == game["stadium"]] 

#                 #with wind direction

#                 if final_wind_direction == 400:
#                     wind_direction_abs = [ab for ab in abs if ab.game.precipitation=="In Dome"]

#                 else:
#                     wind_high = final_wind_direction + 22.5
#                     wind_low = final_wind_direction - 22.5

#                     wind_direction_abs = [ab for ab in abs if wind_low <= ab.game.wind_direction <= wind_high]

#                     #wind speed
#                     wind_speed_high = wind_speed + 2
#                     wind_speed_low = wind_speed - 2

#                     wind_speed_abs = [ab for ab in abs if wind_speed_low <= ab.game.wind_speed <= wind_speed_high]

#                 #sunny/cloudy
#                 #Overcast, Sunny, Cloudy, In Dome
#                 if game["cloud_or_sun"]=="Cloudy":
#                     cloud_or_sun_abs = [ab for ab in abs if ab.game.cloud_or_sun=="Cloudy" or ab.game.cloud_or_sun=="Overcast"]
#                 elif game["cloud_or_sun"]=="Sunny":
#                     cloud_or_sun_abs = [ab for ab in abs if ab.game.cloud_or_sun=="Sunny"]
#                 else:
#                     cloud_or_sun_abs = []


#                 #precipitation
#                 if game["precipitation"]=="Rain":
#                     precipitation_abs = [ab for ab in abs if ab.game.precipitation=="Rain" or ab.game.precipitation=="Drizzle"]
#                 elif game["precipitation"]=="Snow":
#                     precipitation_abs = [ab for ab in abs if ab.game.precipitation=="Snow"]
#                 else:
#                     precipitation_abs = []


#                 #temperature
#                 freezing = 35
#                 real_cold = 42
#                 very_cold = 47
#                 cold = 62
#                 nice = 78
#                 hot = 88
#                 too_hot = 97

#                 if game["temperature"] <= freezing:
#                     temperature_abs = [ab for ab in abs if ab.game.temperature <= freezing]
#                 elif freezing < game["temperature"] <= real_cold:
#                     temperature_abs = [ab for ab in abs if freezing < ab.game.temperature <= real_cold]
#                 elif real_cold < game["temperature"] <= very_cold:
#                     temperature_abs = [ab for ab in abs if real_cold < ab.game.temperature <= very_cold]
#                 elif very_cold < game["temperature"] <= cold:
#                     temperature_abs = [ab for ab in abs if very_cold < ab.game.temperature <= cold]
#                 elif cold < game["temperature"] <= nice:
#                     temperature_abs = [ab for ab in abs if cold < ab.game.temperature <= nice]
#                 elif nice < game["temperature"] <= hot:
#                     temperature_abs = [ab for ab in abs if nice < ab.game.temperature <= hot]
#                 elif hot < game["temperature"] <= too_hot:
#                     temperature_abs = [ab for ab in abs if hot < ab.game.temperature <= too_hot]
#                 else:
#                     temperature_abs = [ab for ab in abs if ab.game.temperature > too_hot]

#                 #vs team
#                 abs_vs_team = [ab for ab in abs if ab.game.home==other_team or ab.game.visitor==other_team]



#                     #stats to measure
#                         #for hitters
#                             #hits
#                             #walks
#                             #strikeouts
#                             #rbi
#                             #runs
#                             #sbs

#                         #for pitchers
#                             #innings pitched
#                             #strikeouts
#                             #walks
#                             #earned runs


#                     #find if people steal more often against that pitcher than the league average
#                         #grab at bats where someone gets on first with a clear path to second and steals vs doesn't
#                     #find what correlates best with standard deviation. 
#                     #lowest stdev will be worth most and vice versa




#                     #make a big array of games
#                     # latest_home_or_away_games.extend(games_at_time)
#                     # latest_home_or_away_games.extend(games_vs_opponent)
#                     # if injury:
#                     #     latest_home_or_away_games.extend(games_with_injury[-3:])
#                     # if opponent_injury:
#                     #     latest_home_or_away_games.extend(games_with_opp_injury[-3:])
#                     # latest_home_or_away_games.extend(games_on_day)
#                     # latest_home_or_away_games.extend(rest_days)

#                     # latest_home_or_away_games.reverse()

#                     #find most similar game


#                     # new_game_list = set(latest_home_or_away_games)

#                     # uniq_game_list = list(new_game_list)


#                     # uniq_game_list = [game for game in uniq_game_list]

#                 ipdb.set_trace()



#     #make a draftkings algorithm

#         #roster
#             #2 P
#             #1 C
#             #1 1B
#             #1 2B
#             #1 SS
#             #1 3B
#             #3 OF
        
#         #Salary Cap = $50,000

    
                    
   

    

#     # sorted_bets = sorted(bets,key=itemgetter('perc'))[-10:]
#     # sort_by_diff = sorted(bets,key=itemgetter('diff'))[-10:]
#     # sorted_by_total_value = sorted(games_in_a_row,key=itemgetter('total_value'))[-20:]
#     # sorted_by_total_value = [item for item in sorted_by_total_value if item["total_value"]>.8]
#     # sorted_by_total_value.reverse()
#     # sorted_by_games_straight = sorted(games_in_a_row,key=itemgetter('games_straight'))[-20:]
#     # sorted_by_games_straight.reverse()
#     # sorted_by_games_straight = [item for item in sorted_by_games_straight if item["games_straight"]>4]

#     # weekday_games_sorted = sorted(weekday_games,key=itemgetter("value"))[-20:]
#     # weekday_games_sorted.reverse()
        
#     # for item in sorted_bets:
#     #     name = item["name"]
#     #     prop = item["prop"]
#     #     line = item["line"]
#     #     projected = item["projected"]
#     #     bet = item["bet"]
#     #     print(f"{name} {bet} in {prop}. Projected: {projected}, Line: {line}")

#     # print("\nBets sorted by difference\n")

#     # for item in sort_by_diff:
#     #     name = item["name"]
#     #     prop = item["prop"]
#     #     line = item["line"]
#     #     projected = item["projected"]
#     #     bet = item["bet"]
#     #     print(f"{name} {bet} in {prop}. Projected: {projected}, Line: {line}")


#     # print("\nBets with lowest consistency")

#     # for item in lowest_consistency:
#     #     name=item["name"]
#     #     stat = item["stat"]
#     #     value = item["value"]
#     #     line = item["line"]
#     #     print(f"{name} {line} {stat}: {value}")

#     # print("\nBets with highest consistency")

#     # for item in highest_consistency:
#     #     name=item["name"]
#     #     stat = item["stat"]
#     #     value = item["value"]
#     #     line = item["line"]
#     #     print(f"{name} {line} {stat}: {value}")


#     # print("\nHigh value teasers\n")

#     # for index, item in enumerate(sorted_high_value_teasers):
#     #     name=item["name"]
#     #     prop = item["prop"]
#     #     value = item["value"]
#     #     teaser = item["teaser"]
#     #     modifier = item["modifier"]
#     #     proj = item["proj"]
#     #     data_points = item["data_points"]
#     #     games_straight = item["games_straight"]

#     #     player_data_list = FinalBet.query.filter(FinalBet.date==full_date,FinalBet.algorithm=="B",FinalBet.category=="high_value",FinalBet.category_value==(index+1)).all()

#     #     if len(player_data_list) > 0:
#     #         player_data = player_data_list[0]
#     #         player_data.name = name
#     #         player_data.prop = prop
#     #         player_data.line = teaser
#     #     else:
#     #         player = FinalBet(
#     #             category = "high_value",
#     #             algorithm = "B",
#     #             category_value = index+1,
#     #             date = full_date,
#     #             name = name,
#     #             prop = prop,
#     #             line = teaser
#     #         )
#     #         db.session.add(player)
#     #     db.session.commit()

#     #     print(f"{index+1}: {name} {teaser} {prop}: {value} (Modifier:{modifier}, Projection:{proj}, Data Points:{data_points}, Games Straight:{games_straight})")

#     # print("\nLow value teasers\n")

#     # for index, item in enumerate(sorted_low_value_teasers):
#     #     name=item["name"]
#     #     prop = item["prop"]
#     #     value = item["value"]
#     #     teaser = item["teaser"]
#     #     modifier = item["modifier"]
#     #     proj = item["proj"]
#     #     data_points = item["data_points"]
#     #     games_straight = item["games_straight"]

#     #     player_data_list = FinalBet.query.filter(FinalBet.date==full_date,FinalBet.algorithm=="B",FinalBet.category=="low_value",FinalBet.category_value==(index+1)).all()
#     #     if len(player_data_list) > 0:
#     #         player_data = player_data_list[0]
#     #         player_data.name = name
#     #         player_data.prop = prop
#     #         player_data.line = teaser
#     #     else:
#     #         player = FinalBet(
#     #             category = "low_value",
#     #             algorithm = "B",
#     #             category_value = index+1,
#     #             date = full_date,
#     #             name = name,
#     #             prop = prop,
#     #             line = teaser
#     #         )
#     #         db.session.add(player)
#     #     db.session.commit()

#     #     print(f"{index+1}: {name} {teaser} {prop}: {value} (Modifier:{modifier}, Projection:{proj}, Data Points:{data_points}, Games Straight:{games_straight})")


#     # print("\nMost Games in a Row\n")

#     # for index, item in enumerate(sorted_by_games_straight):
#     #     name=item["name"]
#     #     prop = item["prop"]
#     #     value = item["value"]
#     #     teaser = item["teaser"]
#     #     modifier = item["modifier"]
#     #     proj = item["proj"]
#     #     data_points = item["data_points"]
#     #     games_straight = item["games_straight"]

#     #     player_data_list = FinalBet.query.filter(FinalBet.date==full_date,FinalBet.algorithm=="B",FinalBet.category=="games_in_a_row",FinalBet.category_value==(index+1)).all()
#     #     if len(player_data_list) > 0:
#     #         player_data = player_data_list[0]
#     #         player_data.name = name
#     #         player_data.prop = prop
#     #         player_data.line = teaser
#     #     else:
#     #         player = FinalBet(
#     #             category = "games_in_a_row",
#     #             algorithm = "B",
#     #             category_value = index+1,
#     #             date = full_date,
#     #             name = name,
#     #             prop = prop,
#     #             line = teaser
#     #         )
#     #         db.session.add(player)
#     #     db.session.commit()

#     #     print(f"{index+1}: {name} {teaser} {prop}: {value} (Modifier:{modifier}, Projection:{proj}, Data Points:{data_points}, Games Straight:{games_straight})")



#     # print("\nRanked by Total Value\n")

#     # for index, item in enumerate(sorted_by_total_value):
#     #     name=item["name"]
#     #     prop = item["prop"]
#     #     value = item["value"]
#     #     teaser = item["teaser"]
#     #     modifier = item["modifier"]
#     #     proj = item["proj"]
#     #     data_points = item["data_points"]
#     #     games_straight = item["games_straight"]
#     #     total_value = item["total_value"]

#     #     player_data_list = FinalBet.query.filter(FinalBet.date==full_date,FinalBet.algorithm=="B",FinalBet.category=="total_value",FinalBet.category_value==(index+1)).all()
#     #     if len(player_data_list) > 0:
#     #         player_data = player_data_list[0]
#     #         player_data.name = name
#     #         player_data.prop = prop
#     #         player_data.line = teaser
#     #     else:
#     #         player = FinalBet(
#     #             category = "total_value",
#     #             algorithm = "B",
#     #             category_value = index+1,
#     #             date = full_date,
#     #             name = name,
#     #             prop = prop,
#     #             line = teaser
#     #         )
#     #         db.session.add(player)
#     #     db.session.commit()

#     #     print(f"{index+1}: {name} {teaser} {prop}: {value} (Modifier:{modifier}, Projection:{proj}, Data Points:{data_points}, Games Straight:{games_straight}, Total Value:{total_value})")
        
        
#     # print("\nWeekday Comparisons\n")

#     # for index, item in enumerate(weekday_games_sorted):
#     #     name = item["name"]
#     #     prop = item["prop"]
#     #     value = item["value"]
#     #     line = item["line"]
#     #     print(f"{index+1}: {name} {line} {prop}: {value}")

#     # print("Injuries:")

#     # for team,injuries in injured_list.items():
#     #     if team in list_of_teams:
#     #         print(f"{team}: {injuries}")

#     # print("\nAlgo B")
#     # print(time_string)
#     # print('✅')

            



# category (high teaser, low teaser, games in a row, total value)
# category value (1,2,3,etc...)
# date
# player name
# prop (trb, points, assists)
# line