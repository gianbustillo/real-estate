import os
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import time
import numpy as np
import csv
import logging
##SET PARAMETERS##
minimum = 0




#minimum number count

overall_filename = 'cities_list2.csv'

craigs_url = line = column = 0

today = datetime.date.today()
today_a = "'" + str(today) + "'"

while craigs_url != '':
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
    rent_import_status = str(cities_states[line][column+5])
    home_import_status = str(cities_states[line][column+7])

    if rent_import_status != 'FAILED' and home_import_status != 'FAILED':
        if zipcode != '':
            folder_and_file_rent = str("rent_files/") + str(craigs_url) + str("/") + str(zipcode) + ".csv"
        elif neigh != '':
            folder_and_file_rent = str("rent_files/") +str(craigs_url) + str("/") + str(neigh) + ".csv"
        else:
            folder_and_file_rent = str("rent_files/") +str(craigs_url) + str("/") + str(city) + ".csv"
        print folder_and_file_rent

        if zipcode != '':
            folder_and_file_home = str("home_files/") + str(craigs_url) + str("/") + str(zipcode) + ".csv"
        elif neigh != '':
            folder_and_file_home = str("home_files/") +str(craigs_url) + str("/") + str(neigh) + ".csv"
        else:
            folder_and_file_home = str("home_files/") +str(craigs_url) + str("/") + str(city) + ".csv"
        print folder_and_file_home


        datestamp = 0
        line_neigh_city_rent = line_neigh_city_home = 0
        column_rent = column_home  = 0


        one_bed_rent_list, two_bed_rent_list, three_bed_rent_list, four_bed_rent_list, five_bed_rent_list, six_bed_rent_list = [],[],[],[],[],[]
        one_bed_home_list, two_bed_home_list, three_bed_home_list, four_bed_home_list, five_bed_home_list, six_bed_home_list = [],[],[],[],[],[]
        one_bed_home_list_c, two_bed_home_list_c, three_bed_home_list_c, four_bed_home_list_c, five_bed_home_list_c, six_bed_home_list_c = [],[],[],[],[],[]
        one_bed_home_list_h, two_bed_home_list_h, three_bed_home_list_h, four_bed_home_list_h, five_bed_home_list_h, six_bed_home_list_h = [],[],[],[],[],[]
        one_bed_home_list_th, two_bed_home_list_th, three_bed_home_list_th, four_bed_home_list_th, five_bed_home_list_th, six_bed_home_list_th = [],[],[],[],[],[]


        while True:
            try:
                line_neigh_city_rent += 1
                neigh_city_file_rent = open(folder_and_file_rent,'rb')
                neigh_city_reader_rent = csv.reader(neigh_city_file_rent, delimiter = ',')
                group_rent = []
                for row in neigh_city_reader_rent:
                    group_rent.append(row)


                line_neigh_city_home += 1
                neigh_city_file_home = open(folder_and_file_home,'rb')
                neigh_city_reader_home = csv.reader(neigh_city_file_home, delimiter = ',')
                group_home = []
                for row in neigh_city_reader_home:
                    group_home.append(row)


                date_rent = group_rent[line_neigh_city_rent][column_rent]
                if int(group_rent[line_neigh_city_rent][column_rent+2]) >= int(minimum):
                    one_bed_rent_list.append(int(group_rent[line_neigh_city_rent][column_rent+1]))
                if int(group_rent[line_neigh_city_rent][column_rent+4]) >= int(minimum):
                    two_bed_rent_list.append(int(group_rent[line_neigh_city_rent][column_rent+3]))
                if int(group_rent[line_neigh_city_rent][column_rent+6]) >= int(minimum):
                    three_bed_rent_list.append(int(group_rent[line_neigh_city_rent][column_rent+5]))
                if int(group_rent[line_neigh_city_rent][column_rent+8]) >= int(minimum):
                    four_bed_rent_list.append(int(group_rent[line_neigh_city_rent][column_rent+7]))
                if int(group_rent[line_neigh_city_rent][column_rent+10]) >= int(minimum):
                    five_bed_rent_list.append(int(group_rent[line_neigh_city_rent][column_rent+9]))
                if int(group_rent[line_neigh_city_rent][column_rent+12]) >= int(minimum):
                    six_bed_rent_list.append(int(group_rent[line_neigh_city_rent][column_rent+11]))


                date_home = group_home[line_neigh_city_home][column_home]
                if int(group_home[line_neigh_city_home][column_home+7]) >= int(minimum):
                    one_bed_home_list.append(int(group_home[line_neigh_city_home][column_home+6]))
                if int(group_home[line_neigh_city_home][column_home+14]) >= int(minimum):
                    two_bed_home_list.append(int(group_home[line_neigh_city_home][column_home+13]))
                if int(group_home[line_neigh_city_home][column_home+21]) >= int(minimum):
                    three_bed_home_list.append(int(group_home[line_neigh_city_home][column_home+20]))
                if int(group_home[line_neigh_city_home][column_home+28]) >= int(minimum):
                    four_bed_home_list.append(int(group_home[line_neigh_city_home][column_home+27]))
                if int(group_home[line_neigh_city_home][column_home+35]) >= int(minimum):
                    five_bed_home_list.append(int(group_home[line_neigh_city_home][column_home+34]))
                if int(group_home[line_neigh_city_home][column_home+42]) >= int(minimum):
                    six_bed_home_list.append(int(group_home[line_neigh_city_home][column_home+41]))

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


        if one_bed_rent_list != []:
            rent_1_median = int(np.median(one_bed_rent_list))
        else:
            rent_1_median = 0
        if two_bed_rent_list != []:
            rent_2_median = int(np.median(two_bed_rent_list))
        else:
            rent_2_median = 0
        if three_bed_rent_list != []:
            rent_3_median = int(np.median(three_bed_rent_list))
        else:
            rent_3_median = 0
        if four_bed_rent_list != []:
            rent_4_median = int(np.median(four_bed_rent_list))
        else:
            rent_4_median = 0
        if five_bed_rent_list != []:
            rent_5_median = int(np.median(five_bed_rent_list))
        else:
            rent_5_median = 0
        if six_bed_rent_list != []:
            rent_6_median = int(np.median(six_bed_rent_list))
        else:
            rent_6_median = 0

        if one_bed_home_list != []:
            home_1_median = float(np.median(one_bed_home_list))
        else:
            home_1_median = 0
        if two_bed_home_list != []:
            home_2_median = float(np.median(two_bed_home_list))
        else:
            home_2_median = 0
        if three_bed_home_list != []:
            home_3_median = float(np.median(three_bed_home_list))
        else:
            home_3_median = 0
        if four_bed_home_list != []:
            home_4_median = float(np.median(four_bed_home_list))
        else:
            home_4_median = 0
        if five_bed_home_list != []:
            home_5_median = float(np.median(five_bed_home_list))
        else:
            home_5_median = 0
        if six_bed_home_list != []:
            home_6_median = float(np.median(six_bed_home_list))
        else:
            home_6_median = 0


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
        '''
        print str(rent_1_median) + ' rent_1_median'
        print str(rent_2_median) + ' rent_2_median'
        print str(rent_3_median) + ' rent_3_median'
        print str(rent_4_median) + ' rent_4_median'
        print str(rent_5_median) + ' rent_5_median'
        print str(rent_6_median) + ' rent_6_median'

        print str(home_1_median) + ' home_1_median'
        print str(home_2_median) + ' home_2_median'
        print str(home_3_median) + ' home_3_median'
        print str(home_4_median) + ' home_4_median'
        print str(home_5_median) + ' home_5_median'
        print str(home_6_median) + ' home_6_median'

        print str(home_1_median_c) + ' home_1_median_c'
        print str(home_2_median_c) + ' home_2_median_c'
        print str(home_3_median_c) + ' home_3_median_c'
        print str(home_4_median_c) + ' home_4_median_c'
        print str(home_5_median_c) + ' home_5_median_c'
        print str(home_6_median_c) + ' home_6_median_c'

        print str(home_1_median_h) + ' home_1_median_h'
        print str(home_2_median_h) + ' home_2_median_h'
        print str(home_3_median_h) + ' home_3_median_h'
        print str(home_4_median_h) + ' home_4_median_h'
        print str(home_5_median_h) + ' home_5_median_h'
        print str(home_6_median_h) + ' home_6_median_h'

        print str(home_1_median_th) + ' home_1_median_th'
        print str(home_2_median_th) + ' home_2_median_th'
        print str(home_3_median_th) + ' home_3_median_th'
        print str(home_4_median_th) + ' home_4_median_th'
        print str(home_5_median_th) + ' home_5_median_th'
        print str(home_6_median_th) + ' home_6_median_th'
        '''
        diff_1_bed = rat_1_bed = diff_1_bed_c = rat_1_bed_c = diff_1_bed_h = rat_1_bed_h = diff_1_bed_th = rat_1_bed_th = 0

        '''
        if rent_1_median != 0 and home_1_median != 0:
            diff_1_bed = rent_1_median - home_1_median
            rat_1_bed = float("{0:.3f}".format(home_1_median / rent_1_median))
        else:
            diff_1_bed = 0
            rat_1_bed = 0
        '''
        print rent_1_median
        print home_1_median


        def home_rent_diff(rent_median,home_median):
            if rent_median != 0 and home_median != 0:
                return int(rent_median) - int(home_median)
            else:
                return 0

        def home_rent_ratio(rent_median,home_median):
            if rent_median != 0 and home_median != 0:
                return float("{0:.3f}".format(home_median / rent_median))
            else:
                return 0

        rat_1_bed = home_rent_ratio(rent_1_median,home_1_median)
        diff_1_bed = home_rent_diff(rent_1_median,home_1_median)

        print rat_1_bed
        print diff_1_bed





        #rent_home_diff_ratio(rent_1_median,home_1_median_c,diff_1_bed_c,rat_1_bed_c)
        #print diff_1_bed_c
        #rent_home_diff_ratio(rent_1_median,home_1_median_h,diff_1_bed_h,rat_1_bed_h)
        #print diff_1_bed_h
        #rent_home_diff_ratio(rent_1_median,home_1_median_th,diff_1_bed_th,rat_1_bed_th)
        #print diff_1_bed_th


'''
        if rent_1_median != 0 and home_1_median != 0:
            diff_1_bed = rent_1_median - home_1_median
            rat_1_bed = float("{0:.3f}".format(home_1_median / rent_1_median))
        else:
            diff_1_bed = 0
            rat_1_bed = 0
        if rent_2_median != 0 and home_2_median !=0:
            diff_2_bed = rent_2_median - home_2_median
            rat_2_bed = float("{0:.3f}".format(home_2_median / rent_2_median))
        else:
            diff_2_bed = 0
            rat_2_bed = 0
        if rent_3_median != 0 and home_3_median != 0:
            diff_3_bed = rent_3_median - home_3_median
            rat_3_bed = float("{0:.3f}".format(home_3_median / rent_3_median))
        else:
            diff_3_bed = 0
            rat_3_bed = 0
        if rent_4_median != 0 and home_4_median != 0:
            diff_4_bed = rent_4_median - home_4_median
            rat_4_bed = float("{0:.3f}".format(home_4_median / rent_4_median))
        else:
            diff_4_bed = 0
            rat_4_bed = 0
        if rent_5_median != 0 and home_5_median != 0:
            diff_5_bed = rent_5_median - home_5_median
            rat_5_bed = float("{0:.3f}".format(home_5_median / rent_5_median))
        else:
            diff_5_bed = 0
            rat_5_bed = 0
        if rent_6_median != 0 and home_6_median != 0:
            diff_6_bed = rent_6_median - home_6_median
            rat_6_bed = float("{0:.3f}".format(home_6_median / rent_6_median))
        else:
            diff_6_bed = 0
            rat_6_bed = 0



        overall_list = [craigs_url,neigh,city,state,today_a,'UPDATED',rat_1_bed,diff_1_bed,rat_2_bed,diff_2_bed,rat_3_bed,diff_3_bed,rat_4_bed,diff_4_bed,rat_5_bed,diff_5_bed,rat_6_bed,diff_6_bed]

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
'''
