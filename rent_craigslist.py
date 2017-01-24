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
        rent_1_bd_th, rent_2_bd_th, rent_3_bd_th, rent_4_bd_th, rent_5_bd_th, rent_6_bd_th = [], [], [], [], [], []
        rent_1_count_th = rent_2_count_th = rent_3_count_th = rent_4_count_th = rent_5_count_th = rent_6_count_th = 0
        rent_1_bd_c, rent_2_bd_c, rent_3_bd_c, rent_4_bd_c, rent_5_bd_c, rent_6_bd_c = [], [], [], [], [], []
        rent_1_count_c = rent_2_count_c = rent_3_count_c = rent_4_count_c = rent_5_count_c = rent_6_count_c = 0
        rent_1_bd_h, rent_2_bd_h, rent_3_bd_h, rent_4_bd_h, rent_5_bd_h, rent_6_bd_h = [], [], [], [], [], []
        rent_1_count_h = rent_2_count_h = rent_3_count_h = rent_4_count_h = rent_5_count_h = rent_6_count_h = 0
        rent_1_bd_th_c, rent_2_bd_th_c, rent_3_bd_th_c, rent_4_bd_th_c, rent_5_bd_th_c, rent_6_bd_th_c = [], [], [], [], [], []
        rent_1_count_th_c = rent_2_count_th_c = rent_3_count_th_c = rent_4_count_th_c = rent_5_count_th_c = rent_6_count_th_c = 0

        rent_1_median = rent_2_median = rent_3_median = rent_4_median = rent_5_median = rent_6_median = 0
        rent_1_median_th = rent_2_median_th = rent_3_median_th = rent_4_median_th = rent_5_median_th = rent_6_median_th = 0
        rent_1_median_c = rent_2_median_c = rent_3_median_c = rent_4_median_c = rent_5_median_c = rent_6_median_c = 0
        rent_1_median_h = rent_2_median_h = rent_3_median_h = rent_4_median_h = rent_5_median_h = rent_6_median_h = 0
        rent_1_median_th_c = rent_2_median_th_c = rent_3_median_th_c = rent_4_median_th_c = rent_5_median_th_c = rent_6_median_th_c = 0


        rent_count_list = [] #List of median_price and count for a bedroom number search

        i = 0

        if zipcode != '':
            url3 = "&bedrooms=1&query=" + str(zipcode) + "&sort=date"
            url3_th = "&bedrooms=1&query=" + str(zipcode) + "+%22town+house%22+%7C+%22townhouse%22+%7C+%22town+home%22&sort=date"
            url3_c = "&bedrooms=1&query=" + str(zipcode) + "+%22condo%22+%7C+%22condominium%22&sort=date"
            url3_th_c = "&bedrooms=1&query=" + str(zipcode) + "+%22town+house%22+%7C+%22townhouse%22+%7C+%22town+home%22+%22condo%22+%7C+%22condominium%22&sort=date"
        elif neigh == '':
            url3 = "&bedrooms=1&query=" + str(city.replace(' ','%20')) + "&sort=date"
            url3_th = "&bedrooms=1&query=" + str(city.replace(' ','%20')) + "+%22town+house%22+%7C+%22townhouse%22+%7C+%22town+home%22&sort=date"
            url3_c = "&bedrooms=1&query=" + str(city.replace(' ','%20')) + "+%22condo%22+%7C+%22condominium%22&sort=date"
            url3_th_c = "&bedrooms=1&query=" + str(city.replace(' ','%20')) + "+%22town+house%22+%7C+%22townhouse%22+%7C+%22town+home%22+%22condo%22+%7C+%22condominium%22&sort=date"
        else:
            url3 = "&bedrooms=1&query=" + str(neigh.replace(' ','%20')) + "&sort=date"
            url3_th = "&bedrooms=1&query=" + str(neigh.replace(' ','%20')) + "+%22town+house%22+%7C+%22townhouse%22+%7C+%22town+home%22&sort=date"
            url3_c = "&bedrooms=1&query=" + str(neigh.replace(' ','%20')) + "+%22condo%22+%7C+%22condominium%22&sort=date"
            url3_th_c = "&bedrooms=1&query=" + str(neigh.replace(' ','%20')) + "+%22town+house%22+%7C+%22townhouse%22+%7C+%22town+home%22+%22condo%22+%7C+%22condominium%22&sort=date"


        url = "http://" + str(craigs_url) + ".craigslist.org/search/apa?s=" + str(i) + url3
        url_th = "http://" + str(craigs_url) + ".craigslist.org/search/apa?s=" + str(i) + url3_th
        url_c = "http://" + str(craigs_url) + ".craigslist.org/search/apa?s=" + str(i) + url3_c
        url_th_c = "http://" + str(craigs_url) + ".craigslist.org/search/apa?s=" + str(i) + url3_th_c

        print 'ALL'
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
                url = "http://" + str(craigs_url) + ".craigslist.org/search/apa?s=" + str(i) + url3
                print url
                r = requests.get(url)
                soup = BeautifulSoup(r.content, "html.parser")
                row = str(soup.find_all("ul", {"class":"rows"}))
                datestart = row.find(datestr)
                no_results = row.find('<pre id="moon">')
                price_start = 0
                time.sleep(1)
            price_start = 0

            while datestart !=-1  and yesterday_date_loc == -1 and price_start != -1:
                nearby = row.find('<h4 class="ban nearby">')
                if nearby < datestart and nearby != -1:
                    break
                price_start = row.find('<span class="result-price">$', datestart)
                price_end = row.find('<',price_start+1)
                craigs_price = row[price_start+28:price_end]
                print craigs_price
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

        i = 0
        print 'TH'
        r_th = requests.get(url_th)
        soup_th = BeautifulSoup(r_th.content, "html.parser")
        row_th = str(soup_th.find_all("ul", {"class":"rows"}))

        datestart_th = row_th.find(datestr)

        i=str(0)
        no_results_th = row_th.find('<pre id="moon">') #if found, no more results to display
        ##if we find date on first page

        while no_results_th == -1 and datestart_th != -1:
            nearby_th = row_th.find('<h4 class="ban nearby">')
            #print nearby
            if nearby_th < datestart_th and nearby_th != -1:
                break
            price_start_th = row_th.find('<span class="result-price">$', datestart_th)
            price_end_th = row_th.find('<',price_start_th+1)
            craigs_price_th = row_th[price_start_th+28:price_end_th]
            print craigs_price_th
            bedroom_start_th = row_th.find('<span class="housing">',datestart_th)
            bedroom_end_th = row_th.find('br',bedroom_start_th)
            bedroom_no_th = row_th[bedroom_start_th+44:bedroom_end_th]
            FORMAT = '%(asctime)s %(message)s' + ' craigs_url: ' + str(craigs_url) + ' neigh: ' + str(neigh) + ' city: ' + str(city) + ' state: ' +str(state) + ' zipcode: ' +str(zipcode) + ' url: ' + str(url) + ' bedroom_no: ' + str(bedroom_no) + ' craigs_price: ' + str(craigs_price)
            if bedroom_no_th == '1' and craigs_price_th != '':
                rent_1_bd_th.append(int(craigs_price_th))
                rent_1_count_th +=1
            if bedroom_no_th == '2' and craigs_price_th != '':
                rent_2_bd_th.append(int(craigs_price_th))
                rent_2_count_th +=1
            if bedroom_no_th == '3' and craigs_price_th != '':
                rent_3_bd_th.append(int(craigs_price_th))
                rent_3_count_th +=1
            if bedroom_no_th == '4' and craigs_price_th != '':
                rent_4_bd_th.append(int(craigs_price_th))
                rent_4_count_th +=1
            if bedroom_no_th == '5' and craigs_price_th != '':
                rent_5_bd_th.append(int(craigs_price_th))
                rent_5_count_th +=1
            if bedroom_no_th == '6' and craigs_price_th != '':
                rent_6_bd_th.append(int(craigs_price_th))
                rent_6_count_th +=1
            row_th = row_th[price_end_th:]
            datestart_th = row_th.find(datestr)
            nearby_th = row_th.find('<h4 class="ban nearby">')

            if nearby_th < datestart_th and nearby_th != -1:
                break
            if craigs_price_th == '':
                break

        yesterday_date_loc_th = row_th.find(before_datestr)
        #finding the first page with prices

        while no_results_th == -1 and yesterday_date_loc_th == -1:
            while datestart_th ==-1 and no_results_th == -1:
                url_th = "http://" + str(craigs_url) + ".craigslist.org/search/apa?s=" + str(i) + url3_th
                i = int(i)
                i = i + 100
                i = str(i)
                url_th = "http://" + str(craigs_url) + ".craigslist.org/search/apa?s=" + str(i) + url3_th
                print url_th
                r_th = requests.get(url_th)
                soup_th = BeautifulSoup(r_th.content, "html.parser")
                row_th = str(soup_th.find_all("ul", {"class":"rows"}))
                datestart_th = row_th.find(datestr)
                no_results_th = row_th.find('<pre id="moon">')
                price_start = 0
                time.sleep(1)
            price_start = 0

            while datestart_th !=-1  and yesterday_date_loc_th == -1 and price_start_th != -1:
                nearby_th = row_th.find('<h4 class="ban nearby">')
                if nearby_th < datestart_th and nearby_th != -1:
                    break
                price_start_th = row_th.find('<span class="result-price">$', datestart_th)
                price_end_th = row_th.find('<',price_start_th+1)
                craigs_price_th = row_th[price_start_th+28:price_end_th]
                print craigs_price_th
                bedroom_start_th = row_th.find('<span class="housing">',price_end_th)
                bedroom_end_th = row_th.find('br',bedroom_start_th)
                bedroom_no_th = row_th[bedroom_start_th+44:bedroom_end_th]
                FORMAT = '%(asctime)s %(message)s' + ' craigs_url: ' + str(craigs_url) + ' neigh: ' + str(neigh) + ' city: ' + str(city) + ' state: ' + str(state) + ' zipcode: ' + str(zipcode) + ' url: ' + str(url) + ' bedroom_no: ' + str(bedroom_no) + ' craigs_price: ' + str(craigs_price)
                if craigs_price_th != '':
                    if bedroom_no_th == '1':
                        rent_1_bd_th.append(int(craigs_price_th))
                        rent_1_count_th +=1
                    if bedroom_no_th == '2':
                        rent_2_bd_th.append(int(craigs_price_th))
                        rent_2_count_th +=1
                    if bedroom_no_th == '3':
                        rent_3_bd_th.append(int(craigs_price_th))
                        rent_3_count_th +=1
                    if bedroom_no_th == '4':
                        rent_4_bd_th.append(int(craigs_price_th))
                        rent_4_count_th +=1
                    if bedroom_no_th == '5':
                        rent_5_bd_th.append(int(craigs_price_th))
                        rent_5_count_th +=1
                    if bedroom_no_th == '6':
                        rent_6_bd_th.append(int(craigs_price_th))
                        rent_6_count_th +=1
                else:
                    datestart_th = -1
                    no_results_th = -1

                row_th = row_th[price_end_th:]
                datestart_th = row_th.find(datestr)

            ##POSSIBLE ISSUE HERE - DATESTART TWO ROWS ABOVE MAKES IT -1????
            yesterday_date_loc_th = row_th.find(before_datestr)
            if yesterday_date_loc_th != -1:
                break
            no_results_th == -1
            datestart_th = -1

        i = 0
        print 'condo'
        r_c = requests.get(url_c)
        soup_c = BeautifulSoup(r_c.content, "html.parser")
        row_c = str(soup_c.find_all("ul", {"class":"rows"}))

        datestart_c = row_c.find(datestr)

        i=str(0)
        no_results_c = row_c.find('<pre id="moon">') #if found, no more results to display
        ##if we find date on first page

        while no_results_c == -1 and datestart_c != -1:
            nearby_c = row_c.find('<h4 class="ban nearby">')
            #print nearby
            if nearby_c < datestart_c and nearby_c != -1:
                break
            price_start_c = row_c.find('<span class="result-price">$', datestart_c)
            price_end_c = row_c.find('<',price_start_c+1)
            craigs_price_c = row_c[price_start_c+28:price_end_c]
            print craigs_price_c
            bedroom_start_c = row_c.find('<span class="housing">',datestart_c)
            bedroom_end_c = row_c.find('br',bedroom_start_c)
            bedroom_no_c = row_c[bedroom_start_c+44:bedroom_end_c]
            FORMAT = '%(asctime)s %(message)s' + ' craigs_url: ' + str(craigs_url) + ' neigh: ' + str(neigh) + ' city: ' + str(city) + ' state: ' +str(state) + ' zipcode: ' +str(zipcode) + ' url: ' + str(url) + ' bedroom_no: ' + str(bedroom_no) + ' craigs_price: ' + str(craigs_price)
            if bedroom_no_c == '1' and craigs_price_c != '':
                rent_1_bd_c.append(int(craigs_price_c))
                rent_1_count_c +=1
            if bedroom_no_c == '2' and craigs_price_c != '':
                rent_2_bd_c.append(int(craigs_price_c))
                rent_2_count_c +=1
            if bedroom_no_c == '3' and craigs_price_c != '':
                rent_3_bd_c.append(int(craigs_price_c))
                rent_3_count_c +=1
            if bedroom_no_c == '4' and craigs_price_c != '':
                rent_4_bd_c.append(int(craigs_price_c))
                rent_4_count_c +=1
            if bedroom_no_c == '5' and craigs_price_c != '':
                rent_5_bd_c.append(int(craigs_price_c))
                rent_5_count_c +=1
            if bedroom_no_c == '6' and craigs_price_c != '':
                rent_6_bd_c.append(int(craigs_price_c))
                rent_6_count_c +=1
            row_c = row_c[price_end_c:]
            datestart_c = row_c.find(datestr)
            nearby_c = row_c.find('<h4 class="ban nearby">')

            if nearby_c < datestart_c and nearby_c != -1:
                break
            if craigs_price_c == '':
                break

        yesterday_date_loc_c = row_c.find(before_datestr)
        #finding the first page with prices

        while no_results_c == -1 and yesterday_date_loc_c == -1:
            while datestart_c ==-1 and no_results_c == -1:
                url_c = "http://" + str(craigs_url) + ".craigslist.org/search/apa?s=" + str(i) + url3_c
                i = int(i)
                i = i + 100
                i = str(i)
                url_c = "http://" + str(craigs_url) + ".craigslist.org/search/apa?s=" + str(i) + url3_c
                print url_c
                r_c = requests.get(url_c)
                soup_c = BeautifulSoup(r_c.content, "html.parser")
                row_c = str(soup_c.find_all("ul", {"class":"rows"}))
                datestart_c = row_c.find(datestr)
                no_results_c = row_c.find('<pre id="moon">')
                price_start = 0
                time.sleep(1)
            price_start = 0

            while datestart_c !=-1  and yesterday_date_loc_c == -1 and price_start_c != -1:
                nearby_c = row_c.find('<h4 class="ban nearby">')
                if nearby_c < datestart_c and nearby_c != -1:
                    break
                price_start_c = row_c.find('<span class="result-price">$', datestart_c)
                price_end_c = row_c.find('<',price_start_c+1)
                craigs_price_c = row_c[price_start_c+28:price_end_c]
                print craigs_price_c
                bedroom_start_c = row_c.find('<span class="housing">',price_end_c)
                bedroom_end_c = row_c.find('br',bedroom_start_c)
                bedroom_no_c = row_c[bedroom_start_c+44:bedroom_end_c]
                FORMAT = '%(asctime)s %(message)s' + ' craigs_url: ' + str(craigs_url) + ' neigh: ' + str(neigh) + ' city: ' + str(city) + ' state: ' + str(state) + ' zipcode: ' + str(zipcode) + ' url: ' + str(url) + ' bedroom_no: ' + str(bedroom_no) + ' craigs_price: ' + str(craigs_price)
                if craigs_price_c != '':
                    if bedroom_no_c == '1':
                        rent_1_bd_c.append(int(craigs_price_c))
                        rent_1_count_c +=1
                    if bedroom_no_c == '2':
                        rent_2_bd_c.append(int(craigs_price_c))
                        rent_2_count_c +=1
                    if bedroom_no_c == '3':
                        rent_3_bd_c.append(int(craigs_price_c))
                        rent_3_count_c +=1
                    if bedroom_no_c == '4':
                        rent_4_bd_c.append(int(craigs_price_c))
                        rent_4_count_c +=1
                    if bedroom_no_c == '5':
                        rent_5_bd_c.append(int(craigs_price_c))
                        rent_5_count_c +=1
                    if bedroom_no_c == '6':
                        rent_6_bd_c.append(int(craigs_price_c))
                        rent_6_count_c +=1
                else:
                    datestart_c = -1
                    no_results_c = -1

                row_c = row_c[price_end_c:]
                datestart_c = row_c.find(datestr)

            ##POSSIBLE ISSUE HERE - DATESTART TWO ROWS ABOVE MAKES IT -1????
            yesterday_date_loc_c = row_c.find(before_datestr)
            if yesterday_date_loc_c != -1:
                break
            no_results_c == -1
            datestart_c = -1


        i = 0
        print 'townhouse and condo'
        r_th_c = requests.get(url_th_c)
        soup_th_c = BeautifulSoup(r_th_c.content, "html.parser")
        row_th_c = str(soup_th_c.find_all("ul", {"class":"rows"}))

        datestart_th_c = row_th_c.find(datestr)

        i=str(0)
        no_results_th_c = row_th_c.find('<pre id="moon">') #if found, no more results to display
        ##if we find date on first page

        while no_results_th_c == -1 and datestart_th_c != -1:
            nearby_th_c = row_th_c.find('<h4 class="ban nearby">')
            #print nearby
            if nearby_th_c < datestart_th_c and nearby_th_c != -1:
                break
            price_start_th_c = row_th_c.find('<span class="result-price">$', datestart_th_c)
            price_end_th_c = row_th_c.find('<',price_start_th_c+1)
            craigs_price_th_c = row_th_c[price_start_th_c+28:price_end_th_c]
            print craigs_price_th_c
            bedroom_start_th_c = row_th_c.find('<span class="housing">',datestart_th_c)
            bedroom_end_th_c = row_th_c.find('br',bedroom_start_th_c)
            bedroom_no_th_c = row_th_c[bedroom_start_th_c+44:bedroom_end_th_c]
            FORMAT = '%(asctime)s %(message)s' + ' craigs_url: ' + str(craigs_url) + ' neigh: ' + str(neigh) + ' city: ' + str(city) + ' state: ' +str(state) + ' zipcode: ' +str(zipcode) + ' url: ' + str(url) + ' bedroom_no: ' + str(bedroom_no) + ' craigs_price: ' + str(craigs_price)
            if bedroom_no_th_c == '1' and craigs_price_th_c != '':
                rent_1_bd_th_c.append(int(craigs_price_th_c))
                rent_1_count_th_c +=1
            if bedroom_no_th_c == '2' and craigs_price_th_c != '':
                rent_2_bd_th_c.append(int(craigs_price_th_c))
                rent_2_count_th_c +=1
            if bedroom_no_th_c == '3' and craigs_price_th_c != '':
                rent_3_bd_th_c.append(int(craigs_price_th_c))
                rent_3_count_th_c +=1
            if bedroom_no_th_c == '4' and craigs_price_th_c != '':
                rent_4_bd_th_c.append(int(craigs_price_th_c))
                rent_4_count_th_c +=1
            if bedroom_no_th_c == '5' and craigs_price_th_c != '':
                rent_5_bd_th_c.append(int(craigs_price_th_c))
                rent_5_count_th_c +=1
            if bedroom_no_th_c == '6' and craigs_price_th_c != '':
                rent_6_bd_th_c.append(int(craigs_price_th_c))
                rent_6_count_th_c +=1
            row_th_c = row_th_c[price_end_th_c:]
            datestart_th_c = row_th_c.find(datestr)
            nearby_th_c = row_th_c.find('<h4 class="ban nearby">')

            if nearby_th_c < datestart_th_c and nearby_th_c != -1:
                break
            if craigs_price_th_c == '':
                break

        yesterday_date_loc_th_c = row_th_c.find(before_datestr)
        #finding the first page with prices

        while no_results_th_c == -1 and yesterday_date_loc_th_c == -1:
            while datestart_th_c ==-1 and no_results_th_c == -1:
                url_th_c = "http://" + str(craigs_url) + ".craigslist.org/search/apa?s=" + str(i) + url3_th_c
                i = int(i)
                i = i + 100
                i = str(i)
                url_th_c = "http://" + str(craigs_url) + ".craigslist.org/search/apa?s=" + str(i) + url3_th_c
                print url_th_c
                r_th_c = requests.get(url_th_c)
                soup_th_c = BeautifulSoup(r_th_c.content, "html.parser")
                row_th_c = str(soup_th_c.find_all("ul", {"class":"rows"}))
                datestart_th_c = row_th_c.find(datestr)
                no_results_th_c = row_th_c.find('<pre id="moon">')
                price_start = 0
                time.sleep(1)
            price_start = 0

            while datestart_th_c !=-1  and yesterday_date_loc_th_c == -1 and price_start_th_c != -1:
                nearby_th_c = row_th_c.find('<h4 class="ban nearby">')
                if nearby_th_c < datestart_th_c and nearby_th_c != -1:
                    break
                price_start_th_c = row_th_c.find('<span class="result-price">$', datestart_th_c)
                price_end_th_c = row_th_c.find('<',price_start_th_c+1)
                craigs_price_th_c = row_th_c[price_start_th_c+28:price_end_th_c]
                print craigs_price_th_c
                bedroom_start_th_c = row_th_c.find('<span class="housing">',price_end_th_c)
                bedroom_end_th_c = row_th_c.find('br',bedroom_start_th_c)
                bedroom_no_th_c = row_th_c[bedroom_start_th_c+44:bedroom_end_th_c]
                FORMAT = '%(asctime)s %(message)s' + ' craigs_url: ' + str(craigs_url) + ' neigh: ' + str(neigh) + ' city: ' + str(city) + ' state: ' + str(state) + ' zipcode: ' + str(zipcode) + ' url: ' + str(url) + ' bedroom_no: ' + str(bedroom_no) + ' craigs_price: ' + str(craigs_price)
                if craigs_price_th_c != '':
                    if bedroom_no_th_c == '1':
                        rent_1_bd_th_c.append(int(craigs_price_th_c))
                        rent_1_count_th_c +=1
                    if bedroom_no_th_c == '2':
                        rent_2_bd_th_c.append(int(craigs_price_th_c))
                        rent_2_count_th_c +=1
                    if bedroom_no_th_c == '3':
                        rent_3_bd_th_c.append(int(craigs_price_th_c))
                        rent_3_count_th_c +=1
                    if bedroom_no_th_c == '4':
                        rent_4_bd_th_c.append(int(craigs_price_th_c))
                        rent_4_count_th_c +=1
                    if bedroom_no_th_c == '5':
                        rent_5_bd_th_c.append(int(craigs_price_th_c))
                        rent_5_count_th_c +=1
                    if bedroom_no_th_c == '6':
                        rent_6_bd_th_c.append(int(craigs_price_th_c))
                        rent_6_count_th_c +=1
                else:
                    datestart_th_c = -1
                    no_results_th_c = -1

                row_th_c = row_th_c[price_end_th_c:]
                datestart_th_c = row_th_c.find(datestr)

            ##POSSIBLE ISSUE HERE - DATESTART TWO ROWS ABOVE MAKES IT -1????
            yesterday_date_loc_th_c = row_th_c.find(before_datestr)
            if yesterday_date_loc_th_c != -1:
                break
            no_results_th_c == -1
            datestart_th_c = -1

        rent_1_bd_h = list(set(rent_1_bd + rent_1_bd_th_c) - set(rent_1_bd_c + rent_1_bd_th))
        rent_2_bd_h = list(set(rent_2_bd + rent_2_bd_th_c) - set(rent_2_bd_c + rent_2_bd_th))
        rent_3_bd_h = list(set(rent_3_bd + rent_3_bd_th_c) - set(rent_3_bd_c + rent_3_bd_th))
        rent_4_bd_h = list(set(rent_4_bd + rent_4_bd_th_c) - set(rent_4_bd_c + rent_4_bd_th))
        rent_5_bd_h = list(set(rent_5_bd + rent_5_bd_th_c) - set(rent_5_bd_c + rent_5_bd_th))
        rent_6_bd_h = list(set(rent_6_bd + rent_6_bd_th_c) - set(rent_6_bd_c + rent_6_bd_th))

        rent_1_count_h = rent_1_count - rent_1_count_c - rent_1_count_th  + rent_1_count_th_c
        rent_2_count_h = rent_2_count - rent_2_count_c - rent_2_count_th  + rent_2_count_th_c
        rent_3_count_h = rent_3_count - rent_3_count_c - rent_3_count_th  + rent_3_count_th_c
        rent_4_count_h = rent_4_count - rent_4_count_c - rent_4_count_th  + rent_4_count_th_c
        rent_5_count_h = rent_5_count - rent_5_count_c - rent_5_count_th  + rent_5_count_th_c
        rent_6_count_h = rent_6_count - rent_6_count_c - rent_6_count_th  + rent_6_count_th_c

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

        if rent_1_bd_c != []:
            rent_1_median_c = int(np.median(rent_1_bd_c))
        else:
            rent_1_median_c = 0

        if rent_2_bd_c != []:
            rent_2_median_c = int(np.median(rent_2_bd_c))
        else:
            rent_2_median_c = 0

        if rent_3_bd_c != []:
            rent_3_median_c = int(np.median(rent_3_bd_c))
        else:
            rent_3_median_c = 0

        if rent_4_bd_c != []:
            rent_4_median_c = int(np.median(rent_4_bd_c))
        else:
            rent_4_median_c = 0

        if rent_5_bd_c != []:
            rent_5_median_c = int(np.median(rent_5_bd_c))
        else:
            rent_5_median_c = 0

        if rent_6_bd_c != []:
            rent_6_median_c = int(np.median(rent_6_bd_c))
        else:
            rent_6_median_c = 0


        if rent_1_bd_th != []:
            rent_1_median_th = int(np.median(rent_1_bd_th))
        else:
            rent_1_median_th = 0

        if rent_2_bd_th != []:
            rent_2_median_th = int(np.median(rent_2_bd_th))
        else:
            rent_2_median_th = 0

        if rent_3_bd_th != []:
            rent_3_median_th = int(np.median(rent_3_bd_th))
        else:
            rent_3_median_th = 0

        if rent_4_bd_th != []:
            rent_4_median_th = int(np.median(rent_4_bd_th))
        else:
            rent_4_median_th = 0

        if rent_5_bd_th != []:
            rent_5_median_th = int(np.median(rent_5_bd_th))
        else:
            rent_5_median_th = 0

        if rent_6_bd_th != []:
            rent_6_median_th = int(np.median(rent_6_bd_th))
        else:
            rent_6_median_th = 0


        if rent_1_bd_h != []:
            rent_1_median_h = int(np.median(rent_1_bd_h))
        else:
            rent_1_median_h = 0

        if rent_2_bd_h != []:
            rent_2_median_h = int(np.median(rent_2_bd_h))
        else:
            rent_2_median_h = 0

        if rent_3_bd_h != []:
            rent_3_median_h = int(np.median(rent_3_bd_h))
        else:
            rent_3_median_h = 0

        if rent_4_bd_h != []:
            rent_4_median_h = int(np.median(rent_4_bd_h))
        else:
            rent_4_median_h = 0

        if rent_5_bd_h != []:
            rent_5_median_h = int(np.median(rent_5_bd_h))
        else:
            rent_5_median_h = 0

        if rent_6_bd_h != []:
            rent_6_median_h = int(np.median(rent_6_bd_h))
        else:
            rent_6_median_h = 0

        rent_price_count = [rent_1_median, rent_1_count,rent_2_median, rent_2_count, rent_3_median, rent_3_count, rent_4_median, rent_4_count, rent_5_median, rent_5_count, rent_6_median, rent_6_count,rent_1_median_c, rent_1_count_c,rent_2_median_c, rent_2_count_c, rent_3_median_c, rent_3_count_c, rent_4_median_c, rent_4_count_c, rent_5_median_c, rent_5_count_c, rent_6_median_c, rent_6_count_c,rent_1_median_h, rent_1_count_h,rent_2_median_h, rent_2_count_h, rent_3_median_h, rent_3_count_h, rent_4_median_h, rent_4_count_h, rent_5_median_h, rent_5_count_h, rent_6_median_h, rent_6_count_h,rent_1_median_th, rent_1_count_th,rent_2_median_th, rent_2_count_th, rent_3_median_th, rent_3_count_th, rent_4_median_th, rent_4_count_th, rent_5_median_th, rent_5_count_th, rent_6_median_th, rent_6_count_th]


        print rent_price_count

        overall_list = [craigs_url,neigh,city,state,zipcode,'Successful',today_a,HomeStatusLastRun,HomeDateLastRun]
        #list saved for individual cities
        city_rent_list = [today_a,rent_1_median, rent_1_count,rent_2_median, rent_2_count, rent_3_median, rent_3_count, rent_4_median, rent_4_count, rent_5_median, rent_5_count, rent_6_median, rent_6_count,rent_1_median_c, rent_1_count_c,rent_2_median_c, rent_2_count_c, rent_3_median_c, rent_3_count_c, rent_4_median_c, rent_4_count_c, rent_5_median_c, rent_5_count_c, rent_6_median_c, rent_6_count_c,rent_1_median_h, rent_1_count_h,rent_2_median_h, rent_2_count_h, rent_3_median_h, rent_3_count_h, rent_4_median_h, rent_4_count_h, rent_5_median_h, rent_5_count_h, rent_6_median_h, rent_6_count_h,rent_1_median_th, rent_1_count_th,rent_2_median_th, rent_2_count_th, rent_3_median_th, rent_3_count_th, rent_4_median_th, rent_4_count_th, rent_5_median_th, rent_5_count_th, rent_6_median_th, rent_6_count_th]

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


#os.system('updating_cities.py')

content = 'rent_craigslist.py - COMPLETED'
mail = smtplib.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
mail.login('onenefautomation@gmail.com','!Password1')
mail.sendmail('x','gianbustillo@gmail.com',content)
mail.close()
