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


def mortgage(median_price):
    ir = .04/float(12)
    return float("{0:.2f}".format((.8*(median_price))*((ir*((1+ir)**360))/(((1+ir)**360)-1))+((median_price*.012)/12)+((median_price*.01)/12)))
try:
    craigs_url = line = column = 0

    overall_filename = 'cities_list.csv'

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
        RentStatusLastRun = cities_states[line][column+5]
        RentDateLastRun = cities_states[line][column+6]
        HomeStatusLastRun = cities_states[line][column+7]
        today_file = cities_states[line][column+8]
        today_file = str(today_file.replace("'",""))
        today_file_format = datetime.datetime.strptime(today_file, '%Y-%m-%d').date()
        today_minus_7 = datetime.date.today() - timedelta(days=7)


        if zipcode != '':
            folder_and_file_home = str("home_files/") + str(craigs_url) + str("/") + str(zipcode) + ".csv"
        elif neigh != '':
            folder_and_file_home = str("home_files/") +str(craigs_url) + str("/") + str(neigh) + ".csv"
        else:
            folder_and_file_home = str("home_files/") +str(craigs_url) + str("/") + str(city) + ".csv"
        print folder_and_file_home

        one_bed_home_list_c, two_bed_home_list_c, three_bed_home_list_c, four_bed_home_list_c, five_bed_home_list_c, six_bed_home_list_c = [],[],[],[],[],[]
        one_bed_home_list_h, two_bed_home_list_h, three_bed_home_list_h, four_bed_home_list_h, five_bed_home_list_h, six_bed_home_list_h = [],[],[],[],[],[]
        one_bed_home_list_th, two_bed_home_list_th, three_bed_home_list_th, four_bed_home_list_th, five_bed_home_list_th, six_bed_home_list_th = [],[],[],[],[],[]

        while True:
            try:
                line_neigh_city_home += 1
                neigh_city_file_home = open(folder_and_file_home,'rb')
                neigh_city_reader_home = csv.reader(neigh_city_file_home, delimiter = ',')
                group_home = []
                for row in neigh_city_reader_home:
                    group_home.append(row)

                if int(group_home[line_neigh_city_home][column_home+49]) >= int(minimum):
                    one_bed_home_list_c.append(int(group_home[line_neigh_city_home][column_home+48]))
                if int(group_home[line_neigh_city_home][column_home+56]) >= int(minimum):
                    two_bed_home_list_c.append(int(group_home[line_neigh_city_home][column_home+55]))
                if int(group_home[line_neigh_city_home][column_home+63]) >= int(minimum):
                    three_bed_home_list_c.append(int(group_home[line_neigh_city_home][column_home+62]))
                if int(group_home[line_neigh_city_home][column_home+70]) >= int(minimum):
                    four_bed_home_list_c.append(int(group_home[line_neigh_city_home][column_home+69]))
                if int(group_home[line_neigh_city_home][column_home+77]) >= int(minimum):
                    five_bed_home_list_c.append(int(group_home[line_neigh_city_home][column_home+76]))
                if int(group_home[line_neigh_city_home][column_home+84]) >= int(minimum):
                    six_bed_home_list_c.append(int(group_home[line_neigh_city_home][column_home+83]))

                if int(group_home[line_neigh_city_home][column_home+91]) >= int(minimum):
                    one_bed_home_list_h.append(int(group_home[line_neigh_city_home][column_home+90]))
                if int(group_home[line_neigh_city_home][column_home+98]) >= int(minimum):
                    two_bed_home_list_h.append(int(group_home[line_neigh_city_home][column_home+97]))
                if int(group_home[line_neigh_city_home][column_home+105]) >= int(minimum):
                    three_bed_home_list_h.append(int(group_home[line_neigh_city_home][column_home+104]))
                if int(group_home[line_neigh_city_home][column_home+112]) >= int(minimum):
                    four_bed_home_list_h.append(int(group_home[line_neigh_city_home][column_home+111]))
                if int(group_home[line_neigh_city_home][column_home+119]) >= int(minimum):
                    five_bed_home_list_h.append(int(group_home[line_neigh_city_home][column_home+118]))
                if int(group_home[line_neigh_city_home][column_home+126]) >= int(minimum):
                    six_bed_home_list_h.append(int(group_home[line_neigh_city_home][column_home+125]))

                if int(group_home[line_neigh_city_home][column_home+133]) >= int(minimum):
                    one_bed_home_list_th.append(int(group_home[line_neigh_city_home][column_home+132]))
                if int(group_home[line_neigh_city_home][column_home+140]) >= int(minimum):
                    two_bed_home_list_th.append(int(group_home[line_neigh_city_home][column_home+139]))
                if int(group_home[line_neigh_city_home][column_home+147]) >= int(minimum):
                    three_bed_home_list_th.append(int(group_home[line_neigh_city_home][column_home+146]))
                if int(group_home[line_neigh_city_home][column_home+154]) >= int(minimum):
                    four_bed_home_list_th.append(int(group_home[line_neigh_city_home][column_home+153]))
                if int(group_home[line_neigh_city_home][column_home+161]) >= int(minimum):
                    five_bed_home_list_th.append(int(group_home[line_neigh_city_home][column_home+160]))
                if int(group_home[line_neigh_city_home][column_home+168]) >= int(minimum):
                    six_bed_home_list_th.append(int(group_home[line_neigh_city_home][column_home+167]))

            except:
                break


        if one_bed_home_list_c != []:
            home_1_median_c = float(np.median(one_bed_home_list_c))
        else:
            home_1_median_c = 0
        if two_bed_home_list_c != []:
            home_2_median_c = float(np.median(two_bed_home_list_c))
        else:
            home_2_median_c = 0
        if three_bed_home_list_c != []:
            home_3_median_c = float(np.median(three_bed_home_list_c))
        else:
            home_3_median_c = 0
        if four_bed_home_list_c != []:
            home_4_median_c = float(np.median(four_bed_home_list_c))
        else:
            home_4_median_c = 0
        if five_bed_home_list_c != []:
            home_5_median_c = float(np.median(five_bed_home_list_c))
        else:
            home_5_median_c = 0
        if six_bed_home_list_c != []:
            home_6_median_c = float(np.median(six_bed_home_list_c))
        else:
            home_6_median_c = 0

        if one_bed_home_list_h != []:
            home_1_median_h = float(np.median(one_bed_home_list_h))
        else:
            home_1_median_h = 0
        if two_bed_home_list_h != []:
            home_2_median_h = float(np.median(two_bed_home_list_h))
        else:
            home_2_median_h = 0
        if three_bed_home_list_h != []:
            home_3_median_h = float(np.median(three_bed_home_list_h))
        else:
            home_3_median_h = 0
        if four_bed_home_list_h != []:
            home_4_median_h = float(np.median(four_bed_home_list_h))
        else:
            home_4_median_h = 0
        if five_bed_home_list_h != []:
            home_5_median_h = float(np.median(five_bed_home_list_h))
        else:
            home_5_median_h = 0
        if six_bed_home_list_h != []:
            home_6_median_h = float(np.median(six_bed_home_list_h))
        else:
            home_6_median_h = 0

        if one_bed_home_list_th != []:
            home_1_median_th = float(np.median(one_bed_home_list_th))
        else:
            home_1_median_th = 0
        if two_bed_home_list_th != []:
            home_2_median_th = float(np.median(two_bed_home_list_th))
        else:
            home_2_median_th = 0
        if three_bed_home_list_th != []:
            home_3_median_th = float(np.median(three_bed_home_list_th))
        else:
            home_3_median_th = 0
        if four_bed_home_list_th != []:
            home_4_median_th = float(np.median(four_bed_home_list_th))
        else:
            home_4_median_th = 0
        if five_bed_home_list_th != []:
            home_5_median_th = float(np.median(five_bed_home_list_th))
        else:
            home_5_median_th = 0
        if six_bed_home_list_th != []:
            home_6_median_th = float(np.median(six_bed_home_list_th))
        else:
            home_6_median_th = 0



        estate_url_1 = "http://www.estately.com/"

        if zipcode != '':
            estate_url = estate_url_1+state+'/'+zipcode+'?min_bed=1&order=price_asc'
        elif neigh != '':
            estate_url = estate_url_1+state+'/'+neigh.replace(' ','_')+ ',_'+city.replace(' ','_')+'?min_bed=1&order=price_asc'
        else:
            estate_url = estate_url_1+state+'/'+city.replace(' ','_')+'?min_bed=1&order=price_asc'
        print estate_url
        t = requests.get(estate_url)
        soup = BeautifulSoup(t.content,"html.parser")
        div = str(soup.find_all("div", {"class":"buffer"}))

        price_loc = div.find('<p class="result-price margin-bottom-10">')
        #if estately city found then not_found is found (not -1)
        not_found = meta.find('href="h')

        if not_found != -1:
            while price_loc != -1:
                property_url_loc = div.find('js-map-listing-result result-item clearfix js-must-be-removed" href="')
                property_url_loc_end = div.find('">',property_url_loc)
                property_url = str(div[property_url_loc+69:property_url_loc_end])
                print '***************************************************************'
                print property_url
                datetime.datetime.strptime(date_record, '%m/%d/%Y').date()
                property_type_loc = div.find('<small>')
                property_type_loc_end = div.find(' For Sale</small>',property_type_loc)
                property_type = str(div[property_type_loc+7:property_type_loc_end])
                print property_type
                price_loc = div.find('<p class="result-price margin-bottom-10">',date_loc_end)
                price_loc_end = div.find('</strong',price_loc)
                home_price = div[price_loc+52:price_loc_end]
                print 'Property Price: ' + str(home_price)
                home_price = float(home_price.replace(",", ""))
                bed_loc = div.find('<ul class="list-unstyled margin-0">',price_loc)
                bed_loc_end = div.find('</b',bed_loc)
                bed = div[bed_loc+46:bed_loc_end]
                div = div[price_loc+2:]
                price_loc = div.find('<p class="result-price margin-bottom-10">')
                FORMAT = '%(asctime)s %(message)s' + ' craigs_url: ' + str(craigs_url) + ' neigh: ' + str(neigh) + ' city: ' + str(city) + ' state: ' +str(state) + ' zipcode: ' + str(zipcode) + ' url: ' + str(url) + ' bedroom_no: ' + str(bedroom_no) + ' craigs_price: ' + str(craigs_price) + ' estate_url: ' + str(estate_url) + ' bed: ' + str(bed) + ' home_price: ' + str(home_price)
                b = requests.get(property_url)
                soup = BeautifulSoup(b.content,"html.parser")
                home_site = str(soup.find_all("div", {"class":"row margin-bottom-20"}))
                condo_fee_loc = home_site.find('Condo Coop Fee:')
                hoa_fee_loc = home_site.find('HOA Fees:')
                if condo_fee_loc == -1:
                    condo = 0
                if hoa_fee_loc == -1:
                    hoa = 0
                #time.sleep(2)
                if condo_fee_loc != -1:
                    condo_fee_loc_end = home_site.find('</p>',condo_fee_loc)
                    print 'condo_fee_loc' + str(home_site[condo_fee_loc+17:condo_fee_loc+18])
                    if home_site[condo_fee_loc+17:condo_fee_loc+18] == '$':
                        print home_site[condo_fee_loc+18:condo_fee_loc_end-2]
                        condo = float(home_site[condo_fee_loc+18:condo_fee_loc_end-2].replace(',',''))
                        print "Condo Fee: " + str(condo)
                    else:
                        condo_fee_loc = -1
                if hoa_fee_loc != -1:
                    hoa_fee_loc_end = home_site.find('</p>',hoa_fee_loc)

                    if home_site[hoa_fee_loc+11:hoa_fee_loc+12] == '$':
                        #print home_site[hoa_fee_loc+12:hoa_fee_loc_end-2]
                        hoa = float(home_site[hoa_fee_loc+12:hoa_fee_loc_end-2].replace(',',''))
                        print "HOA Fees: " + str(hoa)
                    #since I determine if it's condo fee by using condo fee loc, I set it to hoa fee loc so it's treated as the same
                        condo_fee_loc = hoa_fee_loc
                    else:
                        hoa_fee_loc = -1
                hoa = hoa + condo
                print 'Total sum HOA and Condo: ' + str(hoa)

                #condo
                #no HOA
                if bed == '1' and condo_fee_loc == -1 and property_type == 'Condo':
                    if home_1_median_c*.8 > mortgage(home_price):
                        print 'MEDIAN VALUE: ' + str(home_1_median_c)
                        print mortgage(home_price)


                if bed == '2' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'Condo':
                    home_2_bd_c.append(home_price)
                    home_2_bd_both_c.append(mortgage(home_price))
                    home_2_count_c +=1

                elif bed == '3' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'Condo':
                    home_3_bd_c.append(home_price)
                    home_3_bd_both_c.append(mortgage(home_price))
                    home_3_count_c +=1

                elif bed == '4' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'Condo':
                    home_4_bd_c.append(home_price)
                    home_4_bd_both_c.append(mortgage(home_price))
                    home_4_count_c +=1

                elif bed == '5' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'Condo':
                    home_5_bd_c.append(home_price)
                    home_5_bd_both_c.append(mortgage(home_price))
                    home_5_count_c +=1

                elif bed == '6' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'Condo':
                    home_6_bd_c.append(home_price)
                    home_6_bd_both_c.append(mortgage(home_price))
                    home_6_count_c +=1

                #HOA
                if bed == '1' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'Condo':
                    home_1_bd_hoa_c.append(home_price)
                    home_1_count_hoa_c +=1
                    hoa_1_bd_c.append(hoa)
                    home_1_bd_both_c.append(mortgage(home_price)+hoa)
                if bed == '2' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'Condo':
                    home_2_bd_hoa_c.append(home_price)
                    home_2_count_hoa_c +=1
                    hoa_2_bd_c.append(hoa)
                    home_2_bd_both_c.append(mortgage(home_price)+hoa)
                elif bed == '3' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'Condo':
                    home_3_bd_hoa_c.append(home_price)
                    home_3_count_hoa_c +=1
                    hoa_3_bd_c.append(hoa)
                    home_3_bd_both_c.append(mortgage(home_price)+hoa)
                elif bed == '4' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'Condo':
                    home_4_bd_hoa_c.append(home_price)
                    home_4_count_hoa_c +=1
                    hoa_4_bd_c.append(hoa)
                    home_4_bd_both_c.append(mortgage(home_price)+hoa)
                elif bed == '5' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'Condo':
                    home_5_bd_hoa_c.append(home_price)
                    home_5_count_hoa_c +=1
                    hoa_5_bd_c.append(hoa)
                    home_5_bd_both_c.append(mortgage(home_price)+hoa)
                elif bed == '6' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'Condo':
                    home_6_bd_hoa_c.append(home_price)
                    home_6_count_hoa_c +=1
                    hoa_6_bd_c.append(hoa)
                    home_6_bd_both_c.append(mortgage(home_price)+hoa)

                #house
                #no HOA
                if bed == '1' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'House':
                    home_1_bd_h.append(home_price)
                    home_1_bd_both_h.append(mortgage(home_price))
                    home_1_count_h +=1

                if bed == '2' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'House':
                    home_2_bd_h.append(home_price)
                    home_2_bd_both_h.append(mortgage(home_price))
                    home_2_count_h +=1

                elif bed == '3' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'House':
                    home_3_bd_h.append(home_price)
                    home_3_bd_both_h.append(mortgage(home_price))
                    home_3_count_h +=1

                elif bed == '4' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'House':
                    home_4_bd_h.append(home_price)
                    home_4_bd_both_h.append(mortgage(home_price))
                    home_4_count_h +=1

                elif bed == '5' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'House':
                    home_5_bd_h.append(home_price)
                    home_5_bd_both_h.append(mortgage(home_price))
                    home_5_count_h +=1

                elif bed == '6' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'House':
                    home_6_bd_h.append(home_price)
                    home_6_bd_both_h.append(mortgage(home_price))
                    home_6_count_h +=1

                #HOA
                if bed == '1' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'House':
                    home_1_bd_hoa_h.append(home_price)
                    home_1_count_hoa_h +=1
                    hoa_1_bd_h.append(hoa)
                    home_1_bd_both_h.append(mortgage(home_price)+hoa)
                if bed == '2' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'House':
                    home_2_bd_hoa_h.append(home_price)
                    home_2_count_hoa_h +=1
                    hoa_2_bd_h.append(hoa)
                    home_2_bd_both_h.append(mortgage(home_price)+hoa)
                elif bed == '3' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'House':
                    home_3_bd_hoa_h.append(home_price)
                    home_3_count_hoa_h +=1
                    hoa_3_bd_h.append(hoa)
                    home_3_bd_both_h.append(mortgage(home_price)+hoa)
                elif bed == '4' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'House':
                    home_4_bd_hoa_h.append(home_price)
                    home_4_count_hoa_h +=1
                    hoa_4_bd_h.append(hoa)
                    home_4_bd_both_h.append(mortgage(home_price)+hoa)
                elif bed == '5' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'House':
                    home_5_bd_hoa_h.append(home_price)
                    home_5_count_hoa_h +=1
                    hoa_5_bd_h.append(hoa)
                    home_5_bd_both_h.append(mortgage(home_price)+hoa)
                elif bed == '6' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'House':
                    home_6_bd_hoa_h.append(home_price)
                    home_6_count_hoa_h +=1
                    hoa_6_bd_h.append(hoa)
                    home_6_bd_both_h.append(mortgage(home_price)+hoa)


                #townhouse
                #no HOA
                if bed == '1' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'Townhouse':
                    home_1_bd_th.append(home_price)
                    home_1_bd_both_th.append(mortgage(home_price))
                    home_1_count_th +=1

                if bed == '2' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'Townhouse':
                    home_2_bd_th.append(home_price)
                    home_2_bd_both_th.append(mortgage(home_price))
                    home_2_count_th +=1

                elif bed == '3' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'Townhouse':
                    home_3_bd_th.append(home_price)
                    home_3_bd_both_th.append(mortgage(home_price))
                    home_3_count_th +=1

                elif bed == '4' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'Townhouse':
                    home_4_bd_th.append(home_price)
                    home_4_bd_both_th.append(mortgage(home_price))
                    home_4_count_th +=1

                elif bed == '5' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'Townhouse':
                    home_5_bd_th.append(home_price)
                    home_5_bd_both_th.append(mortgage(home_price))
                    home_5_count_th +=1

                elif bed == '6' and date_record > before_date_home and condo_fee_loc == -1 and property_type == 'Townhouse':
                    home_6_bd_th.append(home_price)
                    home_6_bd_both_th.append(mortgage(home_price))
                    home_6_count_th +=1

                #HOA
                if bed == '1' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'Townhouse':
                    home_1_bd_hoa_th.append(home_price)
                    home_1_count_hoa_th +=1
                    hoa_1_bd_th.append(hoa)
                    home_1_bd_both_th.append(mortgage(home_price)+hoa)
                if bed == '2' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'Townhouse':
                    home_2_bd_hoa_th.append(home_price)
                    home_2_count_hoa_th +=1
                    hoa_2_bd_th.append(hoa)
                    home_2_bd_both_th.append(mortgage(home_price)+hoa)
                elif bed == '3' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'Townhouse':
                    home_3_bd_hoa_th.append(home_price)
                    home_3_count_hoa_th +=1
                    hoa_3_bd_th.append(hoa)
                    home_3_bd_both_th.append(mortgage(home_price)+hoa)
                elif bed == '4' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'Townhouse':
                    home_4_bd_hoa_th.append(home_price)
                    home_4_count_hoa_th +=1
                    hoa_4_bd_th.append(hoa)
                    home_4_bd_both_th.append(mortgage(home_price)+hoa)
                elif bed == '5' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'Townhouse':
                    home_5_bd_hoa_th.append(home_price)
                    home_5_count_hoa_th +=1
                    hoa_5_bd_th.append(hoa)
                    home_5_bd_both_th.append(mortgage(home_price)+hoa)
                elif bed == '6' and date_record > before_date_home and condo_fee_loc != -1 and property_type == 'Townhouse':
                    home_6_bd_hoa_th.append(home_price)
                    home_6_count_hoa_th +=1
                    hoa_6_bd_th.append(hoa)
                    home_6_bd_both_th.append(mortgage(home_price)+hoa)
