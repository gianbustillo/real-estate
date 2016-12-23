import os
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import time
import numpy as np
import csv
import logging

#minimum number count
minimum = 5
overall_filename = 'cities.csv'

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
    import_status = str(cities_states[line][column+5])
    if import_status != 'FAILED':
        if neigh != '':
            folder_and_file = str(craigs_url) + str("/") + str(neigh) + ".csv"
        else:
            folder_and_file = str(craigs_url) + str("/") + str(city) + ".csv"

        print folder_and_file

        datestamp = 0
        line_neigh_city = 0
        column = 0

        one_bed_rent_list, two_bed_rent_list, three_bed_rent_list, four_bed_rent_list, five_bed_rent_list, six_bed_rent_list = [],[],[],[],[],[]
        one_bed_home_list, two_bed_home_list, three_bed_home_list, four_bed_home_list, five_bed_home_list, six_bed_home_list = [],[],[],[],[],[]

        while True:
            try:
                line_neigh_city += 1
                neigh_city_file = open(folder_and_file,'rb')
                neigh_city_reader = csv.reader(neigh_city_file, delimiter = ',')
                group = []
                for row in neigh_city_reader:
                    group.append(row)

                date = group[line_neigh_city][column]
                if group[line_neigh_city][column+1] != '0' and int(group[line_neigh_city][column+2]) >= int(minimum):
                    one_bed_rent_list.append(int(group[line_neigh_city][column+1]))
                if group[line_neigh_city][column+3] != '0' and int(group[line_neigh_city][column+4]) >= int(minimum):
                    two_bed_rent_list.append(int(group[line_neigh_city][column+3]))
                if group[line_neigh_city][column+5] != '0' and int(group[line_neigh_city][column+6]) >= int(minimum):
                    three_bed_rent_list.append(int(group[line_neigh_city][column+5]))
                if group[line_neigh_city][column+7] != '0' and int(group[line_neigh_city][column+8]) >= int(minimum):
                    four_bed_rent_list.append(int(group[line_neigh_city][column+7]))
                if group[line_neigh_city][column+9] != '0' and int(group[line_neigh_city][column+10]) >= int(minimum):
                    five_bed_rent_list.append(int(group[line_neigh_city][column+9]))
                if group[line_neigh_city][column+11] != '0' and int(group[line_neigh_city][column+12]) >= int(minimum):
                    six_bed_rent_list.append(int(group[line_neigh_city][column+11]))

                if group[line_neigh_city][column+18] != '0' and int(group[line_neigh_city][column+19]) >= int(minimum):
                    one_bed_home_list.append(int(group[line_neigh_city][column+18]))
                if group[line_neigh_city][column+25] != '0' and int(group[line_neigh_city][column+26]) >= int(minimum):
                    two_bed_home_list.append(int(group[line_neigh_city][column+25]))
                if group[line_neigh_city][column+32] != '0' and int(group[line_neigh_city][column+33]) >= int(minimum):
                    three_bed_home_list.append(int(group[line_neigh_city][column+32]))
                if group[line_neigh_city][column+39] != '0' and int(group[line_neigh_city][column+40]) >= int(minimum):
                    four_bed_home_list.append(int(group[line_neigh_city][column+39]))
                if group[line_neigh_city][column+46] != '0' and int(group[line_neigh_city][column+47]) >= int(minimum):
                    five_bed_home_list.append(int(group[line_neigh_city][column+46]))
                if group[line_neigh_city][column+53] != '0' and int(group[line_neigh_city][column+54]) >= int(minimum):
                    six_bed_home_list.append(int(group[line_neigh_city][column+53]))

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
