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
minimum = 5

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


#minimum number count

overall_filename = 'cities_list.csv'

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
    RentStatusLastRun = str(cities_states[line][column+5])
    RentDateLastRun = str(cities_states[line][column+6])
    HomeStatusLastRun = str(cities_states[line][column+7])
    HomeDateLastRun = str(cities_states[line][column+8])

    if RentStatusLastRun != 'FAILED' and HomeStatusLastRun != 'FAILED':
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
        one_bed_rent_list_c, two_bed_rent_list_c, three_bed_rent_list_c, four_bed_rent_list_c, five_bed_rent_list_c, six_bed_rent_list_c = [],[],[],[],[],[]
        one_bed_rent_list_h, two_bed_rent_list_h, three_bed_rent_list_h, four_bed_rent_list_h, five_bed_rent_list_h, six_bed_rent_list_h = [],[],[],[],[],[]
        one_bed_rent_list_th, two_bed_rent_list_th, three_bed_rent_list_th, four_bed_rent_list_th, five_bed_rent_list_th, six_bed_rent_list_th = [],[],[],[],[],[]

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

                if int(group_rent[line_neigh_city_rent][column_rent+14]) >= int(minimum):
                    one_bed_rent_list_c.append(int(group_rent[line_neigh_city_rent][column_rent+13]))
                if int(group_rent[line_neigh_city_rent][column_rent+16]) >= int(minimum):
                    two_bed_rent_list_c.append(int(group_rent[line_neigh_city_rent][column_rent+15]))
                if int(group_rent[line_neigh_city_rent][column_rent+18]) >= int(minimum):
                    three_bed_rent_list_c.append(int(group_rent[line_neigh_city_rent][column_rent+17]))
                if int(group_rent[line_neigh_city_rent][column_rent+20]) >= int(minimum):
                    four_bed_rent_list_c.append(int(group_rent[line_neigh_city_rent][column_rent+19]))
                if int(group_rent[line_neigh_city_rent][column_rent+22]) >= int(minimum):
                    five_bed_rent_list_c.append(int(group_rent[line_neigh_city_rent][column_rent+21]))
                if int(group_rent[line_neigh_city_rent][column_rent+24]) >= int(minimum):
                    six_bed_rent_list_c.append(int(group_rent[line_neigh_city_rent][column_rent+23]))

                if int(group_rent[line_neigh_hity_rent][column_rent+26]) >= int(minimum):
                    one_bed_rent_list_h.append(int(group_rent[line_neigh_city_rent][column_rent+25]))
                if int(group_rent[line_neigh_city_rent][column_rent+28]) >= int(minimum):
                    two_bed_rent_list_h.append(int(group_rent[line_neigh_city_rent][column_rent+27]))
                if int(group_rent[line_neigh_city_rent][column_rent+30]) >= int(minimum):
                    three_bed_rent_list_h.append(int(group_rent[line_neigh_city_rent][column_rent+29]))
                if int(group_rent[line_neigh_city_rent][column_rent+32]) >= int(minimum):
                    four_bed_rent_list_h.append(int(group_rent[line_neigh_city_rent][column_rent+31]))
                if int(group_rent[line_neigh_city_rent][column_rent+34]) >= int(minimum):
                    five_bed_rent_list_h.append(int(group_rent[line_neigh_city_rent][column_rent+33]))
                if int(group_rent[line_neigh_city_rent][column_rent+36]) >= int(minimum):
                    six_bed_rent_list_h.append(int(group_rent[line_neigh_city_rent][column_rent+35]))

                if int(group_rent[line_neigh_hity_rent][column_rent+38]) >= int(minimum):
                    one_bed_rent_list_th.append(int(group_rent[line_neigh_city_rent][column_rent+37]))
                if int(group_rent[line_neigh_city_rent][column_rent+40]) >= int(minimum):
                    two_bed_rent_list_th.append(int(group_rent[line_neigh_city_rent][column_rent+39]))
                if int(group_rent[line_neigh_city_rent][column_rent+42]) >= int(minimum):
                    three_bed_rent_list_th.append(int(group_rent[line_neigh_city_rent][column_rent+41]))
                if int(group_rent[line_neigh_city_rent][column_rent+44]) >= int(minimum):
                    four_bed_rent_list_th.append(int(group_rent[line_neigh_city_rent][column_rent+43]))
                if int(group_rent[line_neigh_city_rent][column_rent+46]) >= int(minimum):
                    five_bed_rent_list_th.append(int(group_rent[line_neigh_city_rent][column_rent+45]))
                if int(group_rent[line_neigh_city_rent][column_rent+48]) >= int(minimum):
                    six_bed_rent_list_th.append(int(group_rent[line_neigh_city_rent][column_rent+47]))



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

        if one_bed_rent_list_h != []:
            rent_1_median_h = int(np.median(one_bed_rent_list_h))
        else:
            rent_1_median_h = 0
        if two_bed_rent_list_h != []:
            rent_2_median_h = int(np.median(two_bed_rent_list_h))
        else:
            rent_2_median_h = 0
        if three_bed_rent_list_h != []:
            rent_3_median_h = int(np.median(three_bed_rent_list_h))
        else:
            rent_3_median_h = 0
        if four_bed_rent_list_h != []:
            rent_4_median_h = int(np.median(four_bed_rent_list_h))
        else:
            rent_4_median_h = 0
        if five_bed_rent_list_h != []:
            rent_5_median_h = int(np.median(five_bed_rent_list_h))
        else:
            rent_5_median_h = 0
        if six_bed_rent_list_h != []:
            rent_6_median_h = int(np.median(six_bed_rent_list_h))
        else:
            rent_6_median_h = 0

        if one_bed_rent_list_th != []:
            rent_1_median_th = int(np.median(one_bed_rent_list_th))
        else:
            rent_1_median_th = 0
        if two_bed_rent_list_th != []:
            rent_2_median_th = int(np.median(two_bed_rent_list_th))
        else:
            rent_2_median_th = 0
        if three_bed_rent_list_th != []:
            rent_3_median_th = int(np.median(three_bed_rent_list_th))
        else:
            rent_3_median_th = 0
        if four_bed_rent_list_th != []:
            rent_4_median_th = int(np.median(four_bed_rent_list_th))
        else:
            rent_4_median_th = 0
        if five_bed_rent_list_th != []:
            rent_5_median_th = int(np.median(five_bed_rent_list_th))
        else:
            rent_5_median_th = 0
        if six_bed_rent_list_th != []:
            rent_6_median_th = int(np.median(six_bed_rent_list_th))
        else:
            rent_6_median_th = 0

        if one_bed_rent_list_c != []:
            rent_1_median_c = int(np.median(one_bed_rent_list_c))
        else:
            rent_1_median_c = 0
        if two_bed_rent_list_c != []:
            rent_2_median_c = int(np.median(two_bed_rent_list_c))
        else:
            rent_2_median_c = 0
        if three_bed_rent_list_c != []:
            rent_3_median_c = int(np.median(three_bed_rent_list_c))
        else:
            rent_3_median_c = 0
        if four_bed_rent_list_c != []:
            rent_4_median_c = int(np.median(four_bed_rent_list_c))
        else:
            rent_4_median_c = 0
        if five_bed_rent_list_c != []:
            rent_5_median_c = int(np.median(five_bed_rent_list_c))
        else:
            rent_5_median_c = 0
        if six_bed_rent_list_c != []:
            rent_6_median_c = int(np.median(six_bed_rent_list_c))
        else:
            rent_6_median_c = 0


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



        rat_1_bed = home_rent_ratio(rent_1_median,home_1_median)
        diff_1_bed = home_rent_diff(rent_1_median,home_1_median)
        rat_2_bed = home_rent_ratio(rent_2_median,home_2_median)
        diff_2_bed = home_rent_diff(rent_2_median,home_2_median)
        rat_3_bed = home_rent_ratio(rent_3_median,home_3_median)
        diff_3_bed = home_rent_diff(rent_3_median,home_3_median)
        rat_4_bed = home_rent_ratio(rent_4_median,home_4_median)
        diff_4_bed = home_rent_diff(rent_4_median,home_4_median)
        rat_5_bed = home_rent_ratio(rent_5_median,home_5_median)
        diff_5_bed = home_rent_diff(rent_5_median,home_5_median)
        rat_6_bed = home_rent_ratio(rent_6_median,home_6_median)
        diff_6_bed = home_rent_diff(rent_6_median,home_6_median)

        rat_1_bed_c = home_rent_ratio(rent_1_median_c,home_1_median_c)
        diff_1_bed_c = home_rent_diff(rent_1_median_c,home_1_median_c)
        rat_2_bed_c = home_rent_ratio(rent_2_median_c,home_2_median_c)
        diff_2_bed_c = home_rent_diff(rent_2_median_c,home_2_median_c)
        rat_3_bed_c = home_rent_ratio(rent_3_median_c,home_3_median_c)
        diff_3_bed_c = home_rent_diff(rent_3_median_c,home_3_median_c)
        rat_4_bed_c = home_rent_ratio(rent_4_median_c,home_4_median_c)
        diff_4_bed_c = home_rent_diff(rent_4_median_c,home_4_median_c)
        rat_5_bed_c = home_rent_ratio(rent_5_median_c,home_5_median_c)
        diff_5_bed_c = home_rent_diff(rent_5_median_c,home_5_median_c)
        rat_6_bed_c = home_rent_ratio(rent_6_median_c,home_6_median_c)
        diff_6_bed_c = home_rent_diff(rent_6_median_c,home_6_median_c)


        rat_1_bed_h = home_rent_ratio(rent_1_median_h,home_1_median_h)
        diff_1_bed_h = home_rent_diff(rent_1_median_h,home_1_median_h)
        rat_2_bed_h = home_rent_ratio(rent_2_median_h,home_2_median_h)
        diff_2_bed_h = home_rent_diff(rent_2_median_h,home_2_median_h)
        rat_3_bed_h = home_rent_ratio(rent_3_median_h,home_3_median_h)
        diff_3_bed_h = home_rent_diff(rent_3_median_h,home_3_median_h)
        rat_4_bed_h = home_rent_ratio(rent_4_median_h,home_4_median_h)
        diff_4_bed_h = home_rent_diff(rent_4_median_h,home_4_median_h)
        rat_5_bed_h = home_rent_ratio(rent_5_median_h,home_5_median_h)
        diff_5_bed_h = home_rent_diff(rent_5_median_h,home_5_median_h)
        rat_6_bed_h = home_rent_ratio(rent_6_median_h,home_6_median_h)
        diff_6_bed_h = home_rent_diff(rent_6_median_h,home_6_median_h)

        rat_1_bed_th = home_rent_ratio(rent_1_median_th,home_1_median_th)
        diff_1_bed_th = home_rent_diff(rent_1_median_th,home_1_median_th)
        rat_2_bed_th = home_rent_ratio(rent_2_median_th,home_2_median_th)
        diff_2_bed_th = home_rent_diff(rent_2_median_th,home_2_median_th)
        rat_3_bed_th = home_rent_ratio(rent_3_median_th,home_3_median_th)
        diff_3_bed_th = home_rent_diff(rent_3_median_th,home_3_median_th)
        rat_4_bed_th = home_rent_ratio(rent_4_median_th,home_4_median_th)
        diff_4_bed_th = home_rent_diff(rent_4_median_th,home_4_median_th)
        rat_5_bed_th = home_rent_ratio(rent_5_median_th,home_5_median_th)
        diff_5_bed_th = home_rent_diff(rent_5_median_th,home_5_median_th)
        rat_6_bed_th = home_rent_ratio(rent_6_median_th,home_6_median_th)
        diff_6_bed_th = home_rent_diff(rent_6_median_th,home_6_median_th)

        overall_list = [craigs_url,neigh,city,state,zipcode,RentStatusLastRun,RentDateLastRun,HomeStatusLastRun,HomeDateLastRun,'||',today_a,rat_1_bed,diff_1_bed,rat_2_bed,diff_2_bed,rat_3_bed,diff_3_bed,rat_4_bed,diff_4_bed,rat_5_bed,diff_5_bed,rat_6_bed,diff_6_bed,rat_1_bed_c,diff_1_bed_c,rat_2_bed_c,diff_2_bed_c,rat_3_bed_c,diff_3_bed_c,rat_4_bed_c,diff_4_bed_c,rat_5_bed_c,diff_5_bed_c,rat_6_bed_c,diff_6_bed_c,rat_1_bed_h,diff_1_bed_h,rat_2_bed_h,diff_2_bed_h,rat_3_bed_h,diff_3_bed_h,rat_4_bed_h,diff_4_bed_h,rat_5_bed_h,diff_5_bed_h,rat_6_bed_h,diff_6_bed_h,rat_1_bed_th,diff_1_bed_th,rat_2_bed_th,diff_2_bed_th,rat_3_bed_th,diff_3_bed_th,rat_4_bed_th,diff_4_bed_th,rat_5_bed_th,diff_5_bed_th,rat_6_bed_th,diff_6_bed_th]

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
