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

       
