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
handler = logging.FileHandler('logfile.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

craigs_url = neigh = city = state = url = bedroom_no = craigs_price = estate_url = bed = home_price = 0
FORMAT = 0
###setting values to 0 to see if they are set by the time they are logged


def mortgage(median_price):
    ir = .04/float(12)
    return float("{0:.2f}".format((.8*(median_price))*((ir*((1+ir)**360))/(((1+ir)**360)-1))+((median_price*.012)/12)+((median_price*.01)/12)))

def median_bd(list0,list0_median):
    if list0 != []:
        list0_median = int(np.median(list0))
        return int(list0_median)
    else:
        list0_median = 0
        return int(list0_median)

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
    overall_filename = 'cities_short.csv'

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
        today_file = cities_states[line][column+4]

        ##if there is today's date already on cities.csv, skip it and go to the next city
        if str(today_a) == str(today_file):
            print str(neigh) + " " + str(city) + " already completed for today"
            continue

        #### RENTAL
        rent_1_bd, rent_2_bd, rent_3_bd, rent_4_bd, rent_5_bd, rent_6_bd = [], [], [], [], [], []
        rent_1_count = rent_2_count = rent_3_count = rent_4_count = rent_5_count = rent_6_count = 0
        rent_1_median = rent_2_median = rent_3_median = rent_4_median = rent_5_median = rent_6_median = 0

        rent_count_list = [] #List of median_price and count for a bedroom number search

        i = 0

        if neigh == '':
            url3 = "&bedrooms=1&query=" + str(city.replace(' ','%20')) + "&sort=date"

        else:
            url3 = "&bedrooms=1&query=" + str(neigh.replace(' ','%20')) + "&sort=date"

        url = "http://" + str(craigs_url) + ".craigslist.org/search/apa?s=" + str(i) + url3
        print url

        r = requests.get(url)

        soup = BeautifulSoup(r.content, "html.parser")
        row = str(soup.find_all("ul", {"class":"rows"}))

        datestart = row.find(datestr)

        i=str(0)
        no_results = row.find('<pre id="moon">') #if found, no more results to display
        ##if we find date on first page
        while no_results == -1 and datestart != -1:
            nearby = row.find('<h4 class="ban nearby">')
            if nearby < datestart and nearby != -1:
                break
            price_start = row.find('<span class="result-price">$', datestart)
            price_end = row.find('<',price_start+1)
            craigs_price = row[price_start+28:price_end]
            bedroom_start = row.find('<span class="housing">',price_end)
            bedroom_end = row.find('br',bedroom_start)
            bedroom_no = row[bedroom_start+44:bedroom_end]
            FORMAT = '%(asctime)s %(message)s' + ' craigs_url: ' + str(craigs_url) + ' neigh: ' + str(neigh) + ' city: ' + str(city) + ' state: ' +str(state) + ' url: ' + str(url) + ' bedroom_no: ' + str(bedroom_no) + ' craigs_price: ' + str(craigs_price) + ' estate_url: ' + str(estate_url) + ' bed: ' + str(bed) + ' home_price: ' + str(home_price)
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
            row = row[price_end:]
            datestart = row.find(datestr)
            nearby = row.find('<h4 class="ban nearby">')
            if nearby < datestart and nearby != -1:
                break
        yesterday_date_loc = row.find(before_datestr)
        #finding the first page with prices

        while no_results == -1 and yesterday_date_loc == -1:
            while datestart ==-1 and no_results == -1:
                url = "http://" + str(craigs_url) + ".craigslist.org/search/apa?s=" + str(i) + url3
                time.sleep(2)
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
                FORMAT = '%(asctime)s %(message)s' + ' craigs_url: ' + str(craigs_url) + ' neigh: ' + str(neigh) + ' city: ' + str(city) + ' state: ' +str(state) + ' url: ' + str(url) + ' bedroom_no: ' + str(bedroom_no) + ' craigs_price: ' + str(craigs_price) + ' estate_url: ' + str(estate_url) + ' bed: ' + str(bed) + ' home_price: ' + str(home_price)

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

        #HOME PRICES

        estate_url_1 = "http://www.estately.com/"
        estate_url_bd = 1
        if neigh != '':
            estate_url = estate_url_1+state+'/'+neigh.replace(' ','_')+ ',_'+city.replace(' ','_')+'/sold?min_bed=1'
        else:
            estate_url = estate_url_1+state+'/'+city.replace(' ','_')+'/sold?min_bed=1'
        print estate_url
        t = requests.get(estate_url)
        soup = BeautifulSoup(t.content,"html.parser")
        div = str(soup.find_all("div", {"class":"buffer"}))

        #url generated did not find city
        z = requests.get(estate_url)
        soup = BeautifulSoup(z.content,"html.parser")
        meta = str(soup.find_all("li", {"itemscope":"itemscope"}))

        #general - no property type limitation
        #list of homes without hoas, their counts, and median
        home_1_bd, home_2_bd, home_3_bd, home_4_bd, home_5_bd, home_6_bd = [], [], [], [], [], []
        home_1_count = home_2_count = home_3_count = home_4_count = home_5_count = home_6_count = 0
        home_1_median = home_2_median = home_3_median = home_4_median = home_5_median = home_6_median = 0
        #list of homes with hoas, their counts, and median
        home_1_bd_hoa, home_2_bd_hoa, home_3_bd_hoa, home_4_bd_hoa, home_5_bd_hoa, home_6_bd_hoa = [], [], [], [], [], []
        home_1_count_hoa = home_2_count_hoa = home_3_count_hoa = home_4_count_hoa = home_5_count_hoa = home_6_count_hoa = 0
        home_1_median_hoa = home_2_median_hoa = home_3_median_hoa = home_4_median_hoa = home_5_median_hoa = home_6_median_hoa = 0
        #list of homes with and without hoas, and their counts
        home_1_bd_both, home_2_bd_both, home_3_bd_both, home_4_bd_both, home_5_bd_both, home_6_bd_both = [], [], [], [], [], []
        home_1_bd_both_count = home_2_bd_both_count = home_3_bd_both_count = home_4_bd_both_count = home_5_bd_both_count = home_6_bd_both_count = 0
        home_1_both_median = home_2_both_median = home_3_both_median = home_4_both_median = home_5_both_median = home_6_both_median = 0
        #list of hoas, and their counts
        hoa_1_bd, hoa_2_bd, hoa_3_bd, hoa_4_bd, hoa_5_bd, hoa_6_bd =  [], [], [], [], [], []
        hoa_1_bd_median = hoa_2_bd_median = hoa_3_bd_median = hoa_4_bd_median = hoa_5_bd_median = hoa_6_bd_median = 0


        #house
        #list of homes without hoas, their counts, and median
        home_1_bd_h, home_2_bd_h, home_3_bd_h, home_4_bd_h, home_5_bd_h, home_6_bd_h = [], [], [], [], [], []
        home_1_count_h = home_2_count_h = home_3_count_h = home_4_count_h = home_5_count_h = home_6_count_h = 0
        home_1_median_h = home_2_median_h = home_3_median_h = home_4_median_h = home_5_median_h = home_6_median_h = 0
        #list of homes with hoas, their counts, and median
        home_1_bd_hoa_h, home_2_bd_hoa_h, home_3_bd_hoa_h, home_4_bd_hoa_h, home_5_bd_hoa_h, home_6_bd_hoa_h = [], [], [], [], [], []
        home_1_count_hoa_h = home_2_count_hoa_h = home_3_count_hoa_h = home_4_count_hoa_h = home_5_count_hoa_h = home_6_count_hoa_h = 0
        home_1_median_hoa_h = home_2_median_hoa_h = home_3_median_hoa_h = home_4_median_hoa_h = home_5_median_hoa_h = home_6_median_hoa_h = 0
        #list of homes with and without hoas, and their counts
        home_1_bd_both_h, home_2_bd_both_h, home_3_bd_both_h, home_4_bd_both_h, home_5_bd_both_h, home_6_bd_both_h = [], [], [], [], [], []
        home_1_bd_both_count_h = home_2_bd_both_count_h = home_3_bd_both_count_h = home_4_bd_both_count_h = home_5_bd_both_count_h = home_6_bd_both_count_h = 0
        home_1_both_median_h = home_2_both_median_h = home_3_both_median_h = home_4_both_median_h = home_5_both_median_h = home_6_both_median_h = 0
        #list of hoas, and their counts
        hoa_1_bd_h, hoa_2_bd_h, hoa_3_bd_h, hoa_4_bd_h, hoa_5_bd_h, hoa_6_bd_h =  [], [], [], [], [], []
        hoa_1_bd_median_h = hoa_2_bd_median_h = hoa_3_bd_median_h = hoa_4_bd_median_h = hoa_5_bd_median_h = hoa_6_bd_median_h = 0

        #townhouse
        #list of homes without hoas, their counts, and median
        home_1_bd_th, home_2_bd_th, home_3_bd_th, home_4_bd_th, home_5_bd_th, home_6_bd_th = [], [], [], [], [], []
        home_1_count_th = home_2_count_th = home_3_count_th = home_4_count_th = home_5_count_th = home_6_count_th = 0
        home_1_median_th = home_2_median_th = home_3_median_th = home_4_median_th = home_5_median_th = home_6_median_th = 0
        #list of homes with hoas, their counts, and median
        home_1_bd_hoa_th, home_2_bd_hoa_th, home_3_bd_hoa_th, home_4_bd_hoa_th, home_5_bd_hoa_th, home_6_bd_hoa_th = [], [], [], [], [], []
        home_1_count_hoa_th = home_2_count_hoa_th = home_3_count_hoa_th = home_4_count_hoa_th = home_5_count_hoa_th = home_6_count_hoa_th = 0
        home_1_median_hoa_th = home_2_median_hoa_th = home_3_median_hoa_th = home_4_median_hoa_th = home_5_median_hoa_th = home_6_median_hoa_th = 0
        #list of homes with and without hoas, and their counts
        home_1_bd_both_th, home_2_bd_both_th, home_3_bd_both_th, home_4_bd_both_th, home_5_bd_both_th, home_6_bd_both_th = [], [], [], [], [], []
        home_1_bd_both_count_th = home_2_bd_both_count_th = home_3_bd_both_count_th = home_4_bd_both_count_th = home_5_bd_both_count_th = home_6_bd_both_count_th = 0
        home_1_both_median_th = home_2_both_median_th = home_3_both_median_th = home_4_both_median_th = home_5_both_median_th = home_6_both_median_th = 0
        #list of hoas, and their counts
        hoa_1_bd_th, hoa_2_bd_th, hoa_3_bd_th, hoa_4_bd_th, hoa_5_bd_th, hoa_6_bd_th =  [], [], [], [], [], []
        hoa_1_bd_median_th = hoa_2_bd_median_th = hoa_3_bd_median_th = hoa_4_bd_median_th = hoa_5_bd_median_th = hoa_6_bd_median_th = 0

        #condo
        #list of homes without hoas, their counts, and median
        home_1_bd_c, home_2_bd_c, home_3_bd_c, home_4_bd_c, home_5_bd_c, home_6_bd_c = [], [], [], [], [], []
        home_1_count_c = home_2_count_c = home_3_count_c = home_4_count_c = home_5_count_c = home_6_count_c = 0
        home_1_median_c = home_2_median_c = home_3_median_c = home_4_median_c = home_5_median_c = home_6_median_c = 0
        #list of homes with hoas, their counts, and median
        home_1_bd_hoa_c, home_2_bd_hoa_c, home_3_bd_hoa_c, home_4_bd_hoa_c, home_5_bd_hoa_c, home_6_bd_hoa_c = [], [], [], [], [], []
        home_1_count_hoa_c = home_2_count_hoa_c = home_3_count_hoa_c = home_4_count_hoa_c = home_5_count_hoa_c = home_6_count_hoa_c = 0
        home_1_median_hoa_c = home_2_median_hoa_c = home_3_median_hoa_c = home_4_median_hoa_c = home_5_median_hoa_c = home_6_median_hoa_c = 0
        #list of homes with and without hoas, and their counts
        home_1_bd_both_c, home_2_bd_both_c, home_3_bd_both_c, home_4_bd_both_c, home_5_bd_both_c, home_6_bd_both_c = [], [], [], [], [], []
        home_1_bd_both_count_c = home_2_bd_both_count_c = home_3_bd_both_count_c = home_4_bd_both_count_c = home_5_bd_both_count_c = home_6_bd_both_count_c = 0
        home_1_both_median_c = home_2_both_median_c = home_3_both_median_c = home_4_both_median_c = home_5_both_median_c = home_6_both_median_c = 0
        #list of hoas, and their counts
        hoa_1_bd_c, hoa_2_bd_c, hoa_3_bd_c, hoa_4_bd_c, hoa_5_bd_c, hoa_6_bd_c =  [], [], [], [], [], []
        hoa_1_bd_median_c = hoa_2_bd_median_c = hoa_3_bd_median_c = hoa_4_bd_median_c = hoa_5_bd_median_c = hoa_6_bd_median_c = 0

        date_loc = div.find('<b>Sold ')
        price_loc = div.find('<p class="result-price margin-bottom-10">')
        #if estately city found then not_found is found (not -1)
        not_found = meta.find('href="h')
        if not_found != -1:
            while price_loc != -1:
                property_url_loc = div.find('js-map-listing-result result-item clearfix js-must-be-removed" href="')
                property_url_loc_end = div.find('">',property_url_loc)
                property_url = str(div[property_url_loc+69:property_url_loc_end])
                print '***********************'
                print property_url
                date_loc = div.find('<b>Sold ')
                date_loc_end = div.find('</b>',date_loc)
                date_record = str(div[date_loc+8:date_loc_end])
                datetime.datetime.strptime(date_record, '%m/%d/%Y').date()
                property_type_loc = div.find('<small>Sold ')
                property_type_loc_end = div.find('</small>',property_type_loc)
                property_type = str(div[property_type_loc+12:property_type_loc_end])
                print property_type
                price_loc = div.find('<p class="result-price margin-bottom-10">',date_loc_end)
                price_loc_end = div.find('</strong',price_loc)
                home_price = div[price_loc+52:price_loc_end]
                print 'Home Price: ' + str(home_price)
                home_price = float(home_price.replace(",", ""))
                bed_loc = div.find('<ul class="list-unstyled margin-0">',price_loc)
                bed_loc_end = div.find('</b',bed_loc)
                bed = div[bed_loc+46:bed_loc_end]
                div = div[price_loc+2:]
                price_loc = div.find('<p class="result-price margin-bottom-10">')
                FORMAT = '%(asctime)s %(message)s' + ' craigs_url: ' + str(craigs_url) + ' neigh: ' + str(neigh) + ' city: ' + str(city) + ' state: ' +str(state) + ' url: ' + str(url) + ' bedroom_no: ' + str(bedroom_no) + ' craigs_price: ' + str(craigs_price) + ' estate_url: ' + str(estate_url) + ' bed: ' + str(bed) + ' home_price: ' + str(home_price)
                b = requests.get(property_url)
                soup = BeautifulSoup(b.content,"html.parser")
                home_site = str(soup.find_all("div", {"class":"row margin-bottom-20"}))
                hoa_loc = home_site.find('Condo Coop Fee:')
                if hoa_loc != -1:
                    hoa_loc_end = home_site.find('</p>',hoa_loc)
                    hoa = float(home_site[hoa_loc+18:hoa_loc_end-2].replace(',',''))
                    print "HOA: " + str(hoa)
                else:
                    print "No HOA found"

                #general
                #no HOA
                if bed == '1' and date_record > before_date_home and hoa_loc == -1:
                    home_1_bd.append(home_price)
                    home_1_bd_both.append(mortgage(home_price))
                    home_1_count +=1

                if bed == '2' and date_record > before_date_home and hoa_loc == -1:
                    home_2_bd.append(home_price)
                    home_2_bd_both.append(mortgage(home_price))
                    home_2_count +=1

                elif bed == '3' and date_record > before_date_home and hoa_loc == -1:
                    home_3_bd.append(home_price)
                    home_3_bd_both.append(mortgage(home_price))
                    home_3_count +=1

                elif bed == '4' and date_record > before_date_home and hoa_loc == -1:
                    home_4_bd.append(home_price)
                    home_4_bd_both.append(mortgage(home_price))
                    home_4_count +=1

                elif bed == '5' and date_record > before_date_home and hoa_loc == -1:
                    home_5_bd.append(home_price)
                    home_5_bd_both.append(mortgage(home_price))
                    home_5_count +=1

                elif bed == '6' and date_record > before_date_home and hoa_loc == -1:
                    home_6_bd.append(home_price)
                    home_6_bd_both.append(mortgage(home_price))
                    home_6_count +=1

                #HOA
                if bed == '1' and date_record > before_date_home and hoa_loc != -1:
                    home_1_bd_hoa.append(home_price)
                    home_1_count_hoa +=1
                    hoa_1_bd.append(hoa)
                    home_1_bd_both.append(mortgage(home_price)+hoa)
                if bed == '2' and date_record > before_date_home and hoa_loc != -1:
                    home_2_bd_hoa.append(home_price)
                    home_2_count_hoa +=1
                    hoa_2_bd.append(hoa)
                    home_2_bd_both.append(mortgage(home_price)+hoa)
                elif bed == '3' and date_record > before_date_home and hoa_loc != -1:
                    home_3_bd_hoa.append(home_price)
                    home_3_count_hoa +=1
                    hoa_3_bd.append(hoa)
                    home_3_bd_both.append(mortgage(home_price)+hoa)
                elif bed == '4' and date_record > before_date_home and hoa_loc != -1:
                    home_4_bd_hoa.append(home_price)
                    home_4_count_hoa +=1
                    hoa_4_bd.append(hoa)
                    home_4_bd_both.append(mortgage(home_price)+hoa)
                elif bed == '5' and date_record > before_date_home and hoa_loc != -1:
                    home_5_bd_hoa.append(home_price)
                    home_5_count_hoa +=1
                    hoa_5_bd.append(hoa)
                    home_5_bd_both.append(mortgage(home_price)+hoa)
                elif bed == '6' and date_record > before_date_home and hoa_loc != -1:
                    home_6_bd_hoa.append(home_price)
                    home_6_count_hoa +=1
                    hoa_6_bd.append(hoa)
                    home_6_bd_both.append(mortgage(home_price)+hoa)





                #condo
                #no HOA
                if bed == '1' and date_record > before_date_home and hoa_loc == -1 and property_type == 'Condo':
                    home_1_bd_c.append(home_price)
                    home_1_bd_both_c.append(mortgage(home_price))
                    home_1_count_c +=1

                if bed == '2' and date_record > before_date_home and hoa_loc == -1 and property_type == 'Condo':
                    home_2_bd_c.append(home_price)
                    home_2_bd_both_c.append(mortgage(home_price))
                    home_2_count_c +=1

                elif bed == '3' and date_record > before_date_home and hoa_loc == -1 and property_type == 'Condo':
                    home_3_bd_c.append(home_price)
                    home_3_bd_both_c.append(mortgage(home_price))
                    home_3_count_c +=1

                elif bed == '4' and date_record > before_date_home and hoa_loc == -1 and property_type == 'Condo':
                    home_4_bd_c.append(home_price)
                    home_4_bd_both_c.append(mortgage(home_price))
                    home_4_count_c +=1

                elif bed == '5' and date_record > before_date_home and hoa_loc == -1 and property_type == 'Condo':
                    home_5_bd_c.append(home_price)
                    home_5_bd_both_c.append(mortgage(home_price))
                    home_5_count_c +=1

                elif bed == '6' and date_record > before_date_home and hoa_loc == -1 and property_type == 'Condo':
                    home_6_bd_c.append(home_price)
                    home_6_bd_both_c.append(mortgage(home_price))
                    home_6_count_c +=1

                #HOA
                if bed == '1' and date_record > before_date_home and hoa_loc != -1 and property_type == 'Condo':
                    home_1_bd_hoa_c.append(home_price)
                    home_1_count_hoa_c +=1
                    hoa_1_bd_c.append(hoa)
                    home_1_bd_both_c.append(mortgage(home_price)+hoa)
                if bed == '2' and date_record > before_date_home and hoa_loc != -1 and property_type == 'Condo':
                    home_2_bd_hoa_c.append(home_price)
                    home_2_count_hoa_c +=1
                    hoa_2_bd_c.append(hoa)
                    home_2_bd_both_c.append(mortgage(home_price)+hoa)
                elif bed == '3' and date_record > before_date_home and hoa_loc != -1 and property_type == 'Condo':
                    home_3_bd_hoa_c.append(home_price)
                    home_3_count_hoa_c +=1
                    hoa_3_bd_c.append(hoa)
                    home_3_bd_both_c.append(mortgage(home_price)+hoa)
                elif bed == '4' and date_record > before_date_home and hoa_loc != -1 and property_type == 'Condo':
                    home_4_bd_hoa_c.append(home_price)
                    home_4_count_hoa_c +=1
                    hoa_4_bd_c.append(hoa)
                    home_4_bd_both_c.append(mortgage(home_price)+hoa)
                elif bed == '5' and date_record > before_date_home and hoa_loc != -1 and property_type == 'Condo':
                    home_5_bd_hoa_c.append(home_price)
                    home_5_count_hoa_c +=1
                    hoa_5_bd_c.append(hoa)
                    home_5_bd_both_c.append(mortgage(home_price)+hoa)
                elif bed == '6' and date_record > before_date_home and hoa_loc != -1 and property_type == 'Condo':
                    home_6_bd_hoa_c.append(home_price)
                    home_6_count_hoa_c +=1
                    hoa_6_bd_c.append(hoa)
                    home_6_bd_both_c.append(mortgage(home_price)+hoa)

                #house
                #no HOA
                if bed == '1' and date_record > before_date_home and hoa_loc == -1 and property_type == 'House':
                    home_1_bd_h.append(home_price)
                    home_1_bd_both_h.append(mortgage(home_price))
                    home_1_count_h +=1

                if bed == '2' and date_record > before_date_home and hoa_loc == -1 and property_type == 'House':
                    home_2_bd_h.append(home_price)
                    home_2_bd_both_h.append(mortgage(home_price))
                    home_2_count_h +=1

                elif bed == '3' and date_record > before_date_home and hoa_loc == -1 and property_type == 'House':
                    home_3_bd_h.append(home_price)
                    home_3_bd_both_h.append(mortgage(home_price))
                    home_3_count_h +=1

                elif bed == '4' and date_record > before_date_home and hoa_loc == -1 and property_type == 'House':
                    home_4_bd_h.append(home_price)
                    home_4_bd_both_h.append(mortgage(home_price))
                    home_4_count_h +=1

                elif bed == '5' and date_record > before_date_home and hoa_loc == -1 and property_type == 'House':
                    home_5_bd_h.append(home_price)
                    home_5_bd_both_h.append(mortgage(home_price))
                    home_5_count_h +=1

                elif bed == '6' and date_record > before_date_home and hoa_loc == -1 and property_type == 'House':
                    home_6_bd_h.append(home_price)
                    home_6_bd_both_h.append(mortgage(home_price))
                    home_6_count_h +=1

                #HOA
                if bed == '1' and date_record > before_date_home and hoa_loc != -1 and property_type == 'House':
                    home_1_bd_hoa_h.append(home_price)
                    home_1_count_hoa_h +=1
                    hoa_1_bd_h.append(hoa)
                    home_1_bd_both_h.append(mortgage(home_price)+hoa)
                if bed == '2' and date_record > before_date_home and hoa_loc != -1 and property_type == 'House':
                    home_2_bd_hoa_h.append(home_price)
                    home_2_count_hoa_h +=1
                    hoa_2_bd_h.append(hoa)
                    home_2_bd_both_h.append(mortgage(home_price)+hoa)
                elif bed == '3' and date_record > before_date_home and hoa_loc != -1 and property_type == 'House':
                    home_3_bd_hoa_h.append(home_price)
                    home_3_count_hoa_h +=1
                    hoa_3_bd_h.append(hoa)
                    home_3_bd_both_h.append(mortgage(home_price)+hoa)
                elif bed == '4' and date_record > before_date_home and hoa_loc != -1 and property_type == 'House':
                    home_4_bd_hoa_h.append(home_price)
                    home_4_count_hoa_h +=1
                    hoa_4_bd_h.append(hoa)
                    home_4_bd_both_h.append(mortgage(home_price)+hoa)
                elif bed == '5' and date_record > before_date_home and hoa_loc != -1 and property_type == 'House':
                    home_5_bd_hoa_h.append(home_price)
                    home_5_count_hoa_h +=1
                    hoa_5_bd_h.append(hoa)
                    home_5_bd_both_h.append(mortgage(home_price)+hoa)
                elif bed == '6' and date_record > before_date_home and hoa_loc != -1 and property_type == 'House':
                    home_6_bd_hoa_h.append(home_price)
                    home_6_count_hoa_h +=1
                    hoa_6_bd_h.append(hoa)
                    home_6_bd_both_h.append(mortgage(home_price)+hoa)


                #townhouse
                #no HOA
                if bed == '1' and date_record > before_date_home and hoa_loc == -1 and property_type == 'Townhouse':
                    home_1_bd_th.append(home_price)
                    home_1_bd_both_th.append(mortgage(home_price))
                    home_1_count_th +=1

                if bed == '2' and date_record > before_date_home and hoa_loc == -1 and property_type == 'Townhouse':
                    home_2_bd_th.append(home_price)
                    home_2_bd_both_th.append(mortgage(home_price))
                    home_2_count_th +=1

                elif bed == '3' and date_record > before_date_home and hoa_loc == -1 and property_type == 'Townhouse':
                    home_3_bd_th.append(home_price)
                    home_3_bd_both_th.append(mortgage(home_price))
                    home_3_count_th +=1

                elif bed == '4' and date_record > before_date_home and hoa_loc == -1 and property_type == 'Townhouse':
                    home_4_bd_th.append(home_price)
                    home_4_bd_both_th.append(mortgage(home_price))
                    home_4_count_th +=1

                elif bed == '5' and date_record > before_date_home and hoa_loc == -1 and property_type == 'Townhouse':
                    home_5_bd_th.append(home_price)
                    home_5_bd_both_th.append(mortgage(home_price))
                    home_5_count_th +=1

                elif bed == '6' and date_record > before_date_home and hoa_loc == -1 and property_type == 'Townhouse':
                    home_6_bd_th.append(home_price)
                    home_6_bd_both_th.append(mortgage(home_price))
                    home_6_count_th +=1

                #HOA
                if bed == '1' and date_record > before_date_home and hoa_loc != -1 and property_type == 'Townhouse':
                    home_1_bd_hoa_th.append(home_price)
                    home_1_count_hoa_th +=1
                    hoa_1_bd_th.append(hoa)
                    home_1_bd_both_th.append(mortgage(home_price)+hoa)
                if bed == '2' and date_record > before_date_home and hoa_loc != -1 and property_type == 'Townhouse':
                    home_2_bd_hoa_th.append(home_price)
                    home_2_count_hoa_th +=1
                    hoa_2_bd_th.append(hoa)
                    home_2_bd_both_th.append(mortgage(home_price)+hoa)
                elif bed == '3' and date_record > before_date_home and hoa_loc != -1 and property_type == 'Townhouse':
                    home_3_bd_hoa_th.append(home_price)
                    home_3_count_hoa_th +=1
                    hoa_3_bd_th.append(hoa)
                    home_3_bd_both_th.append(mortgage(home_price)+hoa)
                elif bed == '4' and date_record > before_date_home and hoa_loc != -1 and property_type == 'Townhouse':
                    home_4_bd_hoa_th.append(home_price)
                    home_4_count_hoa_th +=1
                    hoa_4_bd_th.append(hoa)
                    home_4_bd_both_th.append(mortgage(home_price)+hoa)
                elif bed == '5' and date_record > before_date_home and hoa_loc != -1 and property_type == 'Townhouse':
                    home_5_bd_hoa_th.append(home_price)
                    home_5_count_hoa_th +=1
                    hoa_5_bd_th.append(hoa)
                    home_5_bd_both_th.append(mortgage(home_price)+hoa)
                elif bed == '6' and date_record > before_date_home and hoa_loc != -1 and property_type == 'Townhouse':
                    home_6_bd_hoa_th.append(home_price)
                    home_6_count_hoa_th +=1
                    hoa_6_bd_th.append(hoa)
                    home_6_bd_both_th.append(mortgage(home_price)+hoa)

            #general - no property type constraint
            print 'home_1_bd   ' + str(home_1_bd)
            print 'home_2_bd   ' + str(home_2_bd)
            print 'home_3_bd   ' + str(home_3_bd)
            print 'home_4_bd   ' + str(home_4_bd)
            print 'home_5_bd   ' + str(home_5_bd)
            print 'home_6_bd   ' + str(home_6_bd)

            print 'home_1_bd_hoa   ' + str(home_1_bd_hoa)
            print 'hoa_1_bd   ' + str(hoa_1_bd)
            print 'home_2_bd_hoa   ' + str(home_2_bd_hoa)
            print 'hoa_2_bd   ' + str(hoa_2_bd)
            print 'home_3_bd_hoa   ' + str(home_3_bd_hoa)
            print 'hoa_3_bd   ' + str(hoa_3_bd)
            print 'home_4_bd_hoa   ' + str(home_4_bd_hoa)
            print 'hoa_4_bd   ' + str(hoa_4_bd)
            print 'home_5_bd_hoa   ' + str(home_5_bd_hoa)
            print 'hoa_5_bd   ' + str(hoa_5_bd)
            print 'home_6_bd_hoa   ' + str(home_6_bd_hoa)
            print 'hoa_6_bd   ' + str(hoa_6_bd)

            print 'home_1_bd_both   ' + str(home_1_bd_both)
            print 'home_2_bd_both   ' + str(home_2_bd_both)
            print 'home_3_bd_both   ' + str(home_3_bd_both)
            print 'home_4_bd_both   ' + str(home_4_bd_both)
            print 'home_5_bd_both   ' + str(home_5_bd_both)
            print 'home_6_bd_both   ' + str(home_6_bd_both)

            #using median_bd function, if list is not null median, elif equal to 0
            home_1_median = median_bd(home_1_bd,home_1_median)
            print 'home_1_median   ' + str(home_1_median)
            home_2_median = median_bd(home_2_bd,home_2_median)
            print 'home_2_median   ' + str(home_2_median)
            home_3_median = median_bd(home_3_bd,home_3_median)
            print 'home_3_median   ' + str(home_3_median)
            home_4_median = median_bd(home_4_bd,home_4_median)
            print 'home_4_median   ' + str(home_4_median)
            home_5_median = median_bd(home_5_bd,home_5_median)
            print 'home_5_median   ' + str(home_5_median)
            home_6_median = median_bd(home_6_bd,home_6_median)
            print 'home_6_median   ' + str(home_6_median)

            home_1_median_hoa = median_bd(home_1_bd_hoa,home_1_median_hoa)
            print 'home_1_median_hoa    ' + str(home_1_median_hoa)
            home_2_median_hoa = median_bd(home_2_bd_hoa,home_2_median_hoa)
            print 'home_2_median_hoa    ' + str(home_2_median_hoa)
            home_3_median_hoa = median_bd(home_3_bd_hoa,home_3_median_hoa)
            print 'home_3_median_hoa    ' + str(home_3_median_hoa)
            home_4_median_hoa = median_bd(home_4_bd_hoa,home_4_median_hoa)
            print 'home_4_median_hoa    ' + str(home_4_median_hoa)
            home_5_median_hoa = median_bd(home_5_bd_hoa,home_5_median_hoa)
            print 'home_5_median_hoa    ' + str(home_5_median_hoa)
            home_6_median_hoa = median_bd(home_6_bd_hoa,home_6_median_hoa)
            print 'home_6_median_hoa    ' + str(home_6_median_hoa)

            home_1_both_median = median_bd(home_1_bd_both,home_1_both_median)
            print 'home_1_both_median    ' + str(home_1_both_median)
            home_2_both_median = median_bd(home_2_bd_both,home_2_both_median)
            print 'home_2_both_median    ' + str(home_2_both_median)
            home_3_both_median = median_bd(home_3_bd_both,home_3_both_median)
            print 'home_3_both_median    ' + str(home_3_both_median)
            home_4_both_median = median_bd(home_4_bd_both,home_4_both_median)
            print 'home_4_both_median    ' + str(home_4_both_median)
            home_5_both_median = median_bd(home_5_bd_both,home_5_both_median)
            print 'home_5_both_median    ' + str(home_5_both_median)
            home_6_both_median = median_bd(home_6_bd_both,home_6_both_median)
            print 'home_6_both_median    ' + str(home_6_both_median)


            hoa_1_bd_median = median_bd(hoa_1_bd,hoa_1_bd_median)
            print 'hoa_1_bd_median    ' + str(hoa_1_bd_median)
            hoa_2_bd_median = median_bd(hoa_2_bd,hoa_2_bd_median)
            print 'hoa_2_bd_median    ' + str(hoa_2_bd_median)
            hoa_3_bd_median = median_bd(hoa_3_bd,hoa_3_bd_median)
            print 'hoa_3_bd_median    ' + str(hoa_3_bd_median)
            hoa_4_bd_median = median_bd(hoa_4_bd,hoa_4_bd_median)
            print 'hoa_4_bd_median    ' + str(hoa_4_bd_median)
            hoa_5_bd_median = median_bd(hoa_5_bd,hoa_5_bd_median)
            print 'hoa_5_bd_median    ' + str(hoa_5_bd_median)
            hoa_6_bd_median = median_bd(hoa_6_bd,hoa_6_bd_median)
            print 'hoa_6_bd_median    ' + str(hoa_6_bd_median)


            #condo
            print 'home_1_bd_c   ' + str(home_1_bd_c)
            print 'home_2_bd_c   ' + str(home_2_bd_c)
            print 'home_3_bd_c   ' + str(home_3_bd_c)
            print 'home_4_bd_c   ' + str(home_4_bd_c)
            print 'home_5_bd_c   ' + str(home_5_bd_c)
            print 'home_6_bd_c   ' + str(home_6_bd_c)

            print 'home_1_bd_hoa_c   ' + str(home_1_bd_hoa_c)
            print 'hoa_1_bd_c   ' + str(hoa_1_bd_c)
            print 'home_2_bd_hoa_c   ' + str(home_2_bd_hoa_c)
            print 'hoa_2_bd_c   ' + str(hoa_2_bd_c)
            print 'home_3_bd_hoa_c   ' + str(home_3_bd_hoa_c)
            print 'hoa_3_bd_c   ' + str(hoa_3_bd_c)
            print 'home_4_bd_hoa_c   ' + str(home_4_bd_hoa_c)
            print 'hoa_4_bd_c   ' + str(hoa_4_bd_c)
            print 'home_5_bd_hoa_c   ' + str(home_5_bd_hoa_c)
            print 'hoa_5_bd_c   ' + str(hoa_5_bd_c)
            print 'home_6_bd_hoa_c   ' + str(home_6_bd_hoa_c)
            print 'hoa_6_bd_c   ' + str(hoa_6_bd_c)

            print 'home_1_bd_both_c   ' + str(home_1_bd_both_c)
            print 'home_2_bd_both_c   ' + str(home_2_bd_both_c)
            print 'home_3_bd_both_c   ' + str(home_3_bd_both_c)
            print 'home_4_bd_both_c   ' + str(home_4_bd_both_c)
            print 'home_5_bd_both_c   ' + str(home_5_bd_both_c)
            print 'home_6_bd_both_c   ' + str(home_6_bd_both_c)

            #using median_bd function, if list is not null median, elif equal to 0
            home_1_median_c = median_bd(home_1_bd_c,home_1_median_c)
            print 'home_1_median_c   ' + str(home_1_median_c)
            home_2_median_c = median_bd(home_2_bd_c,home_2_median_c)
            print 'home_2_median_c   ' + str(home_2_median_c)
            home_3_median_c = median_bd(home_3_bd_c,home_3_median_c)
            print 'home_3_median_c   ' + str(home_3_median_c)
            home_4_median_c = median_bd(home_4_bd_c,home_4_median_c)
            print 'home_4_median_c   ' + str(home_4_median_c)
            home_5_median_c = median_bd(home_5_bd_c,home_5_median_c)
            print 'home_5_median_c   ' + str(home_5_median_c)
            home_6_median_c = median_bd(home_6_bd_c,home_6_median_c)
            print 'home_6_median_c   ' + str(home_6_median_c)

            home_1_median_hoa_c = median_bd(home_1_bd_hoa_c,home_1_median_hoa_c)
            print 'home_1_median_hoa_c    ' + str(home_1_median_hoa_c)
            home_2_median_hoa_c = median_bd(home_2_bd_hoa_c,home_2_median_hoa_c)
            print 'home_2_median_hoa_c    ' + str(home_2_median_hoa_c)
            home_3_median_hoa_c = median_bd(home_3_bd_hoa_c,home_3_median_hoa_c)
            print 'home_3_median_hoa_c    ' + str(home_3_median_hoa_c)
            home_4_median_hoa_c = median_bd(home_4_bd_hoa_c,home_4_median_hoa_c)
            print 'home_4_median_hoa_c    ' + str(home_4_median_hoa_c)
            home_5_median_hoa_c = median_bd(home_5_bd_hoa_c,home_5_median_hoa_c)
            print 'home_5_median_hoa_c    ' + str(home_5_median_hoa_c)
            home_6_median_hoa_c = median_bd(home_6_bd_hoa_c,home_6_median_hoa_c)
            print 'home_6_median_hoa_c    ' + str(home_6_median_hoa_c)

            home_1_both_median_c = median_bd(home_1_bd_both_c,home_1_both_median_c)
            print 'home_1_both_median_c    ' + str(home_1_both_median_c)
            home_2_both_median_c = median_bd(home_2_bd_both_c,home_2_both_median_c)
            print 'home_2_both_median_c    ' + str(home_2_both_median_c)
            home_3_both_median_c = median_bd(home_3_bd_both_c,home_3_both_median_c)
            print 'home_3_both_median_c    ' + str(home_3_both_median_c)
            home_4_both_median_c = median_bd(home_4_bd_both_c,home_4_both_median_c)
            print 'home_4_both_median_c    ' + str(home_4_both_median_c)
            home_5_both_median_c = median_bd(home_5_bd_both_c,home_5_both_median_c)
            print 'home_5_both_median_c    ' + str(home_5_both_median_c)
            home_6_both_median_c = median_bd(home_6_bd_both_c,home_6_both_median_c)
            print 'home_6_both_median_c    ' + str(home_6_both_median_c)


            hoa_1_bd_median_c = median_bd(hoa_1_bd_c,hoa_1_bd_median_c)
            print 'hoa_1_bd_median_c    ' + str(hoa_1_bd_median_c)
            hoa_2_bd_median_c = median_bd(hoa_2_bd_c,hoa_2_bd_median_c)
            print 'hoa_2_bd_median_c    ' + str(hoa_2_bd_median_c)
            hoa_3_bd_median_c = median_bd(hoa_3_bd_c,hoa_3_bd_median_c)
            print 'hoa_3_bd_median_c    ' + str(hoa_3_bd_median_c)
            hoa_4_bd_median_c = median_bd(hoa_4_bd_c,hoa_4_bd_median_c)
            print 'hoa_4_bd_median_c    ' + str(hoa_4_bd_median_c)
            hoa_5_bd_median_c = median_bd(hoa_5_bd_c,hoa_5_bd_median_c)
            print 'hoa_5_bd_median_c    ' + str(hoa_5_bd_median_c)
            hoa_6_bd_median_c = median_bd(hoa_6_bd_c,hoa_6_bd_median_c)
            print 'hoa_6_bd_median_c    ' + str(hoa_6_bd_median_c)


            #house
            print 'home_1_bd_h   ' + str(home_1_bd_h)
            print 'home_2_bd_h   ' + str(home_2_bd_h)
            print 'home_3_bd_h   ' + str(home_3_bd_h)
            print 'home_4_bd_h   ' + str(home_4_bd_h)
            print 'home_5_bd_h   ' + str(home_5_bd_h)
            print 'home_6_bd_h   ' + str(home_6_bd_h)

            print 'home_1_bd_hoa_h   ' + str(home_1_bd_hoa_h)
            print 'hoa_1_bd_h   ' + str(hoa_1_bd_h)
            print 'home_2_bd_hoa_h   ' + str(home_2_bd_hoa_h)
            print 'hoa_2_bd_h   ' + str(hoa_2_bd_h)
            print 'home_3_bd_hoa_h   ' + str(home_3_bd_hoa_h)
            print 'hoa_3_bd_h   ' + str(hoa_3_bd_h)
            print 'home_4_bd_hoa_h   ' + str(home_4_bd_hoa_h)
            print 'hoa_4_bd_h   ' + str(hoa_4_bd_h)
            print 'home_5_bd_hoa_h   ' + str(home_5_bd_hoa_h)
            print 'hoa_5_bd_h   ' + str(hoa_5_bd_h)
            print 'home_6_bd_hoa_h   ' + str(home_6_bd_hoa_h)
            print 'hoa_6_bd_h   ' + str(hoa_6_bd_h)

            print 'home_1_bd_both_h   ' + str(home_1_bd_both_h)
            print 'home_2_bd_both_h   ' + str(home_2_bd_both_h)
            print 'home_3_bd_both_h   ' + str(home_3_bd_both_h)
            print 'home_4_bd_both_h   ' + str(home_4_bd_both_h)
            print 'home_5_bd_both_h   ' + str(home_5_bd_both_h)
            print 'home_6_bd_both_h   ' + str(home_6_bd_both_h)

            #using median_bd function, if list is not null median, elif equal to 0
            home_1_median_h = median_bd(home_1_bd_h,home_1_median_h)
            print 'home_1_median_h   ' + str(home_1_median_h)
            home_2_median_h = median_bd(home_2_bd_h,home_2_median_h)
            print 'home_2_median_h   ' + str(home_2_median_h)
            home_3_median_h = median_bd(home_3_bd_h,home_3_median_h)
            print 'home_3_median_h   ' + str(home_3_median_h)
            home_4_median_h = median_bd(home_4_bd_h,home_4_median_h)
            print 'home_4_median_h   ' + str(home_4_median_h)
            home_5_median_h = median_bd(home_5_bd_h,home_5_median_h)
            print 'home_5_median_h   ' + str(home_5_median_h)
            home_6_median_h = median_bd(home_6_bd_h,home_6_median_h)
            print 'home_6_median_h   ' + str(home_6_median_h)

            home_1_median_hoa_h = median_bd(home_1_bd_hoa_h,home_1_median_hoa_h)
            print 'home_1_median_hoa_h    ' + str(home_1_median_hoa_h)
            home_2_median_hoa_h = median_bd(home_2_bd_hoa_h,home_2_median_hoa_h)
            print 'home_2_median_hoa_h    ' + str(home_2_median_hoa_h)
            home_3_median_hoa_h = median_bd(home_3_bd_hoa_h,home_3_median_hoa_h)
            print 'home_3_median_hoa_h    ' + str(home_3_median_hoa_h)
            home_4_median_hoa_h = median_bd(home_4_bd_hoa_h,home_4_median_hoa_h)
            print 'home_4_median_hoa_h    ' + str(home_4_median_hoa_h)
            home_5_median_hoa_h = median_bd(home_5_bd_hoa_h,home_5_median_hoa_h)
            print 'home_5_median_hoa_h    ' + str(home_5_median_hoa_h)
            home_6_median_hoa_h = median_bd(home_6_bd_hoa_h,home_6_median_hoa_h)
            print 'home_6_median_hoa_h    ' + str(home_6_median_hoa_h)

            home_1_both_median_h = median_bd(home_1_bd_both_h,home_1_both_median_h)
            print 'home_1_both_median_h    ' + str(home_1_both_median_h)
            home_2_both_median_h = median_bd(home_2_bd_both_h,home_2_both_median_h)
            print 'home_2_both_median_h    ' + str(home_2_both_median_h)
            home_3_both_median_h = median_bd(home_3_bd_both_h,home_3_both_median_h)
            print 'home_3_both_median_h    ' + str(home_3_both_median_h)
            home_4_both_median_h = median_bd(home_4_bd_both_h,home_4_both_median_h)
            print 'home_4_both_median_h    ' + str(home_4_both_median_h)
            home_5_both_median_h = median_bd(home_5_bd_both_h,home_5_both_median_h)
            print 'home_5_both_median_h    ' + str(home_5_both_median_h)
            home_6_both_median_h = median_bd(home_6_bd_both_h,home_6_both_median_h)
            print 'home_6_both_median_h    ' + str(home_6_both_median_h)


            hoa_1_bd_median_h = median_bd(hoa_1_bd_h,hoa_1_bd_median_h)
            print 'hoa_1_bd_median_h    ' + str(hoa_1_bd_median_h)
            hoa_2_bd_median_h = median_bd(hoa_2_bd_h,hoa_2_bd_median_h)
            print 'hoa_2_bd_median_h    ' + str(hoa_2_bd_median_h)
            hoa_3_bd_median_h = median_bd(hoa_3_bd_h,hoa_3_bd_median_h)
            print 'hoa_3_bd_median_h    ' + str(hoa_3_bd_median_h)
            hoa_4_bd_median_h = median_bd(hoa_4_bd_h,hoa_4_bd_median_h)
            print 'hoa_4_bd_median_h    ' + str(hoa_4_bd_median_h)
            hoa_5_bd_median_h = median_bd(hoa_5_bd_h,hoa_5_bd_median_h)
            print 'hoa_5_bd_median_h    ' + str(hoa_5_bd_median_h)
            hoa_6_bd_median_h = median_bd(hoa_6_bd_h,hoa_6_bd_median_h)
            print 'hoa_6_bd_median_h    ' + str(hoa_6_bd_median_h)


            #townhouse
            print 'home_1_bd_th   ' + str(home_1_bd_th)
            print 'home_2_bd_th   ' + str(home_2_bd_th)
            print 'home_3_bd_th   ' + str(home_3_bd_th)
            print 'home_4_bd_th   ' + str(home_4_bd_th)
            print 'home_5_bd_th   ' + str(home_5_bd_th)
            print 'home_6_bd_th   ' + str(home_6_bd_th)

            print 'home_1_bd_hoa_th   ' + str(home_1_bd_hoa_th)
            print 'hoa_1_bd_th   ' + str(hoa_1_bd_th)
            print 'home_2_bd_hoa_th   ' + str(home_2_bd_hoa_th)
            print 'hoa_2_bd_th   ' + str(hoa_2_bd_th)
            print 'home_3_bd_hoa_th   ' + str(home_3_bd_hoa_th)
            print 'hoa_3_bd_th   ' + str(hoa_3_bd_th)
            print 'home_4_bd_hoa_th   ' + str(home_4_bd_hoa_th)
            print 'hoa_4_bd_th   ' + str(hoa_4_bd_th)
            print 'home_5_bd_hoa_th   ' + str(home_5_bd_hoa_th)
            print 'hoa_5_bd_th   ' + str(hoa_5_bd_th)
            print 'home_6_bd_hoa_th   ' + str(home_6_bd_hoa_th)
            print 'hoa_6_bd_th   ' + str(hoa_6_bd_th)

            print 'home_1_bd_both_th   ' + str(home_1_bd_both_th)
            print 'home_2_bd_both_th   ' + str(home_2_bd_both_th)
            print 'home_3_bd_both_th   ' + str(home_3_bd_both_th)
            print 'home_4_bd_both_th   ' + str(home_4_bd_both_th)
            print 'home_5_bd_both_th   ' + str(home_5_bd_both_th)
            print 'home_6_bd_both_th   ' + str(home_6_bd_both_th)

            #using median_bd function, if list is not null median, elif equal to 0
            home_1_median_th = median_bd(home_1_bd_th,home_1_median_th)
            print 'home_1_median_th   ' + str(home_1_median_th)
            home_2_median_th = median_bd(home_2_bd_th,home_2_median_th)
            print 'home_2_median_th   ' + str(home_2_median_th)
            home_3_median_th = median_bd(home_3_bd_th,home_3_median_th)
            print 'home_3_median_th   ' + str(home_3_median_th)
            home_4_median_th = median_bd(home_4_bd_th,home_4_median_th)
            print 'home_4_median_th   ' + str(home_4_median_th)
            home_5_median_th = median_bd(home_5_bd_th,home_5_median_th)
            print 'home_5_median_th   ' + str(home_5_median_th)
            home_6_median_th = median_bd(home_6_bd_th,home_6_median_th)
            print 'home_6_median_th   ' + str(home_6_median_th)

            home_1_median_hoa_th = median_bd(home_1_bd_hoa_th,home_1_median_hoa_th)
            print 'home_1_median_hoa_th    ' + str(home_1_median_hoa_th)
            home_2_median_hoa_th = median_bd(home_2_bd_hoa_th,home_2_median_hoa_th)
            print 'home_2_median_hoa_th    ' + str(home_2_median_hoa_th)
            home_3_median_hoa_th = median_bd(home_3_bd_hoa_th,home_3_median_hoa_th)
            print 'home_3_median_hoa_th    ' + str(home_3_median_hoa_th)
            home_4_median_hoa_th = median_bd(home_4_bd_hoa_th,home_4_median_hoa_th)
            print 'home_4_median_hoa_th    ' + str(home_4_median_hoa_th)
            home_5_median_hoa_th = median_bd(home_5_bd_hoa_th,home_5_median_hoa_th)
            print 'home_5_median_hoa_th    ' + str(home_5_median_hoa_th)
            home_6_median_hoa_th = median_bd(home_6_bd_hoa_th,home_6_median_hoa_th)
            print 'home_6_median_hoa_th    ' + str(home_6_median_hoa_th)

            home_1_both_median_th = median_bd(home_1_bd_both_th,home_1_both_median_th)
            print 'home_1_both_median_th    ' + str(home_1_both_median_th)
            home_2_both_median_th = median_bd(home_2_bd_both_th,home_2_both_median_th)
            print 'home_2_both_median_th    ' + str(home_2_both_median_th)
            home_3_both_median_th = median_bd(home_3_bd_both_th,home_3_both_median_th)
            print 'home_3_both_median_th    ' + str(home_3_both_median_th)
            home_4_both_median_th = median_bd(home_4_bd_both_th,home_4_both_median_th)
            print 'home_4_both_median_th    ' + str(home_4_both_median_th)
            home_5_both_median_th = median_bd(home_5_bd_both_th,home_5_both_median_th)
            print 'home_5_both_median_th    ' + str(home_5_both_median_th)
            home_6_both_median_th = median_bd(home_6_bd_both_th,home_6_both_median_th)
            print 'home_6_both_median_th    ' + str(home_6_both_median_th)


            hoa_1_bd_median_th = median_bd(hoa_1_bd_th,hoa_1_bd_median_th)
            print 'hoa_1_bd_median_th    ' + str(hoa_1_bd_median_th)
            hoa_2_bd_median_th = median_bd(hoa_2_bd_th,hoa_2_bd_median_th)
            print 'hoa_2_bd_median_th    ' + str(hoa_2_bd_median_th)
            hoa_3_bd_median_th = median_bd(hoa_3_bd_th,hoa_3_bd_median_th)
            print 'hoa_3_bd_median_th    ' + str(hoa_3_bd_median_th)
            hoa_4_bd_median_th = median_bd(hoa_4_bd_th,hoa_4_bd_median_th)
            print 'hoa_4_bd_median_th    ' + str(hoa_4_bd_median_th)
            hoa_5_bd_median_th = median_bd(hoa_5_bd_th,hoa_5_bd_median_th)
            print 'hoa_5_bd_median_th    ' + str(hoa_5_bd_median_th)
            hoa_6_bd_median_th = median_bd(hoa_6_bd_th,hoa_6_bd_median_th)
            print 'hoa_6_bd_median_th    ' + str(hoa_6_bd_median_th)




            #list saved in overall
            overall_list = [craigs_url,neigh,city,state,today_a,'Successfully Processed','','','','','','','','','','','','','']
            #list saved for individual cities
            city_rent_home = [today_a,rent_1_median,rent_1_count,rent_2_median,rent_2_count,rent_3_median,rent_3_count,rent_4_median,rent_4_count,rent_5_median,rent_5_count,rent_6_median,rent_6_count,home_1_median,home_1_count,home_1_median_hoa,hoa_1_bd_median,home_1_count_hoa,home_1_both_median,home_1_count+home_1_count_hoa,home_2_median,home_2_count,home_2_median_hoa,hoa_2_bd_median,home_2_count_hoa,home_2_both_median,home_2_count+home_2_count_hoa,home_3_median,home_3_count,home_3_median_hoa,hoa_3_bd_median,home_3_count_hoa,home_3_both_median,home_3_count+home_3_count_hoa,home_4_median,home_4_count,home_4_median_hoa,hoa_4_bd_median,home_4_count_hoa,home_4_both_median,home_4_count+home_4_count_hoa,home_5_median,home_5_count,home_5_median_hoa,hoa_5_bd_median,home_5_count_hoa,home_5_both_median,home_5_count+home_5_count_hoa,home_6_median,home_6_count,home_6_median_hoa,hoa_6_bd_median,home_6_count_hoa,home_6_both_median,home_6_count+home_6_count_hoa,home_1_median_c,home_1_count_c,home_1_median_hoa_c,hoa_1_bd_median_c,home_1_count_hoa_c,home_1_both_median_c,home_1_count_c+home_1_count_hoa_c,home_2_median_c,home_2_count_c,home_2_median_hoa_c,hoa_2_bd_median_c,home_2_count_hoa_c,home_2_both_median_c,home_2_count_c+home_2_count_hoa_c,home_3_median_c,home_3_count_c,home_3_median_hoa_c,hoa_3_bd_median_c,home_3_count_hoa_c,home_3_both_median_c,home_3_count_c+home_3_count_hoa_c,home_4_median_c,home_4_count_c,home_4_median_hoa_c,hoa_4_bd_median_c,home_4_count_hoa_c,home_4_both_median_c,home_4_count_c+home_4_count_hoa_c,home_5_median_c,home_5_count_c,home_5_median_hoa_c,hoa_5_bd_median_c,home_5_count_hoa_c,home_5_both_median_c,home_5_count_c+home_5_count_hoa_c,home_6_median_c,home_6_count_c,home_6_median_hoa_c,hoa_6_bd_median_c,home_6_count_hoa_c,home_6_both_median_c,home_6_count_c+home_6_count_hoa_c,home_1_median_h,home_1_count_h,home_1_median_hoa_h,hoa_1_bd_median_h,home_1_count_hoa_h,home_1_both_median_h,home_1_count_h+home_1_count_hoa_h,home_2_median_h,home_2_count_h,home_2_median_hoa_h,hoa_2_bd_median_h,home_2_count_hoa_h,home_2_both_median_h,home_2_count_h+home_2_count_hoa_h,home_3_median_h,home_3_count_h,home_3_median_hoa_h,hoa_3_bd_median_h,home_3_count_hoa_h,home_3_both_median_h,home_3_count_h+home_3_count_hoa_h,home_4_median_h,home_4_count_h,home_4_median_hoa_h,hoa_4_bd_median_h,home_4_count_hoa_h,home_4_both_median_h,home_4_count_h+home_4_count_hoa_h,home_5_median_h,home_5_count_h,home_5_median_hoa_h,hoa_5_bd_median_h,home_5_count_hoa_h,home_5_both_median_h,home_5_count_h+home_5_count_hoa_h,home_6_median_h,home_6_count_h,home_6_median_hoa_h,hoa_6_bd_median_h,home_6_count_hoa_h,home_6_both_median_h,home_6_count_h+home_6_count_hoa_h,home_1_median_th,home_1_count_th,home_1_median_hoa_th,hoa_1_bd_median_th,home_1_count_hoa_th,home_1_both_median_th,home_1_count_th+home_1_count_hoa_th,home_2_median_th,home_2_count_th,home_2_median_hoa_th,hoa_2_bd_median_th,home_2_count_hoa_th,home_2_both_median_th,home_2_count_th+home_2_count_hoa_th,home_3_median_th,home_3_count_th,home_3_median_hoa_th,hoa_3_bd_median_th,home_3_count_hoa_th,home_3_both_median_th,home_3_count_th+home_3_count_hoa_th,home_4_median_th,home_4_count_th,home_4_median_hoa_th,hoa_4_bd_median_th,home_4_count_hoa_th,home_4_both_median_th,home_4_count_th+home_4_count_hoa_th,home_5_median_th,home_5_count_th,home_5_median_hoa_th,hoa_5_bd_median_th,home_5_count_hoa_th,home_5_both_median_th,home_5_count_th+home_5_count_hoa_th,home_6_median_th,home_6_count_th,home_6_median_hoa_th,hoa_6_bd_median_th,home_6_count_hoa_th,home_6_both_median_th,home_6_count_th+home_6_count_hoa_th]

            #setting folder/file to save city's file
            if neigh != '':
                folder_and_file = craigs_url + str("/") + neigh + ".csv"
            else:
                folder_and_file = craigs_url + str("/") + city + ".csv"
            print folder_and_file

            #adding city_rent_home values to each city's csv


            with open(folder_and_file,"a") as f:
                 writer = csv.writer(f, lineterminator='\n')
                 writer.writerow(city_rent_home )
                 f.close()

        else:
            overall_list = [craigs_url,neigh,city,state,today_a,'FAILED','','','','','','','','','','','','','']

        #adding overall_list to main csv
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

        #time.sleep(10)

except (SystemExit, KeyboardInterrupt):
    raise
except Exception, e:
    logger.error(FORMAT, exc_info=True)


os.system('updating_cities_test.py')
'''
content = 'This is an automatic email sent to notify the Real Estate Python Job ran successfully'
mail = smtplib.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
mail.login('onenefautomation@gmail.com','!Password1')
mail.sendmail('x','gianbustillo@gmail.com',content)
mail.close()
'''
