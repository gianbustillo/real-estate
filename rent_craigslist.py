import requests
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import time
import numpy as np
import csv
import logging
import os
import smtplib

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logfile_rent.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

craigs_url = neigh = city = state = zipcode = url = bedroom_no = craigs_price = 0
FORMAT = 0
###setting values to 0 to see if they are set by the time they are logged


try:
    line = column = 0
    today = datetime.date.today()
    today_a = "'" + str(today) + "'"
    ##dates for home prices
    before_date_home = datetime.date.today() - timedelta(days=180)
    before_date_home = before_date_home.strftime('%m/%d/%Y')

    #dates for rent price
    #from datetime import timedelta
    before_yesterday_date_rent = str(datetime.date.today() - timedelta(days=2))
    yesterday_date_rent = str(datetime.date.today() - timedelta(days=1))
    today_date_rent =  str(datetime.date.today() - timedelta(days=0))
    datestr = '<time class="result-date" datetime="'+yesterday_date_rent+' '
    before_datestr = '<time class="result-date" datetime="'+before_yesterday_date_rent+' '
    overall_filename = 'cities_list.csv'

    #as long as there are values in the next row to process
    while craigs_url != '':
        rent_price_count = 0
        line += 1
        csv_file = open(overall_filename,'rb')
        csv_reader = csv.reader(csv_file, delimiter = ',')
        cities_states = []
        for row in csv_reader:
            cities_states.append(row)
        craigs_url = cities_states[line][column]
        neigh = cities_states[line][column+1]
        city = cities_states[line][column+2]
        state = cities_states[line][column+3]
        zipcode = cities_states[line][column+4]
        today_file = cities_states[line][column+6]
        HomeStatusLastRun = cities_states[line][column+7]
        HomeDateLastRun = cities_states[line][column+8]
        #today_file = str(today_file.replace("'",""))


        ##if there is today's date already on cities.csv, skip it and go to the next city
        if str(today_a) == str(today_file):
            print str(zipcode) + " " + str(neigh) + " " + str(city) + " already completed for today"
            continue

        #### RENTAL
        rent_1_bd, rent_2_bd, rent_3_bd, rent_4_bd, rent_5_bd, rent_6_bd = [], [], [], [], [], []
        rent_1_count = rent_2_count = rent_3_count = rent_4_count = rent_5_count = rent_6_count = 0
        rent_1_median = rent_2_median = rent_3_median = rent_4_median = rent_5_median = rent_6_median = 0

        rent_count_list = [] #List of median_price and count for a bedroom number search

        i = 0

        if zipcode != '':
            url3 = "&bedrooms=1&query=" + str(zipcode) + "&sort=date"
        elif neigh == '':
            url3 = "&bedrooms=1&query=" + str(city.replace(' ','%20')) + "&sort=date"
        else:
            url3 = "&bedrooms=1&query=" + str(neigh.replace(' ','%20')) + "&sort=date"

        url = "http://" + str(craigs_url) + ".craigslist.org/search/apa?s=" + str(i) + url3

        r = requests.get(url)

        soup = BeautifulSoup(r.content, "html.parser")
        row = str(soup.find_all("ul", {"class":"rows"}))

        datestart = row.find(datestr)

        i=str(0)
        no_results = row.find('<pre id="moon">') #if found, no more results to display
        ##if we find date on first page


        while no_results == -1 and datestart != -1:
            nearby = row.find('<h4 class="ban nearby">')
            #print nearby
            if nearby < datestart and nearby != -1:
                break
            price_start = row.find('<span class="result-price">$', datestart)
            price_end = row.find('<',price_start+1)
            craigs_price = row[price_start+28:price_end]
            print craigs_price
            bedroom_start = row.find('<span class="housing">',datestart)
            bedroom_end = row.find('br',bedroom_start)
            bedroom_no = row[bedroom_start+44:bedroom_end]
            FORMAT = '%(asctime)s %(message)s' + ' craigs_url: ' + str(craigs_url) + ' neigh: ' + str(neigh) + ' city: ' + str(city) + ' state: ' +str(state) + ' zipcode: ' +str(zipcode) + ' url: ' + str(url) + ' bedroom_no: ' + str(bedroom_no) + ' craigs_price: ' + str(craigs_price)
            if bedroom_no == '1' and craigs_price != '':
                rent_1_bd.append(int(craigs_price))
                rent_1_count +=1
            if bedroom_no == '2' and craigs_price != '':
                rent_2_bd.append(int(craigs_price))
                rent_2_count +=1
            if bedroom_no == '3' and craigs_price != '':
                rent_3_bd.append(int(craigs_price))
                rent_3_count +=1
            if bedroom_no == '4' and craigs_price != '':
                rent_4_bd.append(int(craigs_price))
                rent_4_count +=1
            if bedroom_no == '5' and craigs_price != '':
                rent_5_bd.append(int(craigs_price))
                rent_5_count +=1
            if bedroom_no == '6' and craigs_price != '':
                rent_6_bd.append(int(craigs_price))
                rent_6_count +=1
            row = row[price_end:]
            datestart = row.find(datestr)
            nearby = row.find('<h4 class="ban nearby">')

            if nearby < datestart and nearby != -1:
                break
            if craigs_price == '':
                break

        yesterday_date_loc = row.find(before_datestr)
        #finding the first page with prices

        while no_results == -1 and yesterday_date_loc == -1:
            while datestart ==-1 and no_results == -1:
                url = "http://" + str(craigs_url) + ".craigslist.org/search/apa?s=" + str(i) + url3
                i = int(i)
                i = i + 100
                i = str(i)
                print url
                r = requests.get(url)
                soup = BeautifulSoup(r.content, "html.parser")
                row = str(soup.find_all("ul", {"class":"rows"}))
                datestart = row.find(datestr)
                no_results = row.find('<pre id="moon">')
                price_start = 0
                time.sleep(5)
            price_start = 0

            while datestart !=-1  and yesterday_date_loc == -1 and price_start != -1:
                nearby = row.find('<h4 class="ban nearby">')
                if nearby < datestart and nearby != -1:
                    break
                price_start = row.find('<span class="result-price">$', datestart)
                price_end = row.find('<',price_start+1)
                craigs_price = row[price_start+28:price_end]
                bedroom_start = row.find('<span class="housing">',price_end)
                bedroom_end = row.find('br',bedroom_start)
                bedroom_no = row[bedroom_start+44:bedroom_end]
                FORMAT = '%(asctime)s %(message)s' + ' craigs_url: ' + str(craigs_url) + ' neigh: ' + str(neigh) + ' city: ' + str(city) + ' state: ' + str(state) + ' zipcode: ' + str(zipcode) + ' url: ' + str(url) + ' bedroom_no: ' + str(bedroom_no) + ' craigs_price: ' + str(craigs_price)
                if craigs_price != '':
                    if bedroom_no == '1':
                        rent_1_bd.append(int(craigs_price))
                        rent_1_count +=1
                    if bedroom_no == '2':
                        rent_2_bd.append(int(craigs_price))
                        rent_2_count +=1
                    if bedroom_no == '3':
                        rent_3_bd.append(int(craigs_price))
                        rent_3_count +=1
                    if bedroom_no == '4':
                        rent_4_bd.append(int(craigs_price))
                        rent_4_count +=1
                    if bedroom_no == '5':
                        rent_5_bd.append(int(craigs_price))
                        rent_5_count +=1
                    if bedroom_no == '6':
                        rent_6_bd.append(int(craigs_price))
                        rent_6_count +=1
                else:
                    datestart = -1
                    no_results = -1

                row = row[price_end:]
                datestart = row.find(datestr)

            ##POSSIBLE ISSUE HERE - DATESTART TWO ROWS ABOVE MAKES IT -1????
            yesterday_date_loc = row.find(before_datestr)
            if yesterday_date_loc != -1:
                break
            no_results == -1
            datestart = -1

        if rent_1_bd != []:
            rent_1_median = int(np.median(rent_1_bd))
        else:
            rent_1_median = 0

        if rent_2_bd != []:
            rent_2_median = int(np.median(rent_2_bd))
        else:
            rent_2_median = 0

        if rent_3_bd != []:
            rent_3_median = int(np.median(rent_3_bd))
        else:
            rent_3_median = 0

        if rent_4_bd != []:
            rent_4_median = int(np.median(rent_4_bd))
        else:
            rent_4_median = 0

        if rent_5_bd != []:
            rent_5_median = int(np.median(rent_5_bd))
        else:
            rent_5_median = 0

        if rent_6_bd != []:
            rent_6_median = int(np.median(rent_6_bd))
        else:
            rent_6_median = 0


        rent_price_count = [rent_1_median, rent_1_count,rent_2_median, rent_2_count, rent_3_median, rent_3_count, rent_4_median, rent_4_count, rent_5_median, rent_5_count, rent_6_median, rent_6_count]

        print rent_price_count

        overall_list = [craigs_url,neigh,city,state,zipcode,'Successful',today_a,HomeStatusLastRun,HomeDateLastRun]
        #list saved for individual cities
        city_rent_list = [today_a,rent_1_median,rent_1_count,rent_2_median,rent_2_count,rent_3_median,rent_3_count,rent_4_median,rent_4_count,rent_5_median,rent_5_count,rent_6_median,rent_6_count]

        if zipcode != '':
            folder_and_file = str("rent_files/") + craigs_url + str("/") + zipcode + ".csv"
        elif neigh != '':
            folder_and_file = str("rent_files/") + craigs_url + str("/") + neigh + ".csv"
        else:
            folder_and_file = str("rent_files/") + craigs_url + str("/") + city + ".csv"
        print folder_and_file

        #adding city_rent_home values to each city's csv

        with open(folder_and_file,"a") as f:
             writer = csv.writer(f, lineterminator='\n')
             writer.writerow(city_rent_list)
             f.close()

        csv_list = []
        with open(overall_filename, 'rb') as b:
            no_clue = csv.reader(b)
            csv_list.extend(no_clue)
        line_to_override = {line:overall_list }
        with open(overall_filename, 'wb') as b:
            writer = csv.writer(b)
            for line2, row in enumerate(csv_list):
                 data = line_to_override.get(line2, row)
                 writer.writerow(data)
        time.sleep(5)

except (SystemExit, KeyboardInterrupt):
    raise
except Exception, e:
    logger.error(FORMAT, exc_info=True)


os.system('updating_cities.py')

content = 'rent_craigslist.py - COMPLETED'
mail = smtplib.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
mail.login('onenefautomation@gmail.com','!Password1')
mail.sendmail('x','gianbustillo@gmail.com',content)
mail.close()
