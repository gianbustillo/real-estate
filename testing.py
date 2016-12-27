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

a = 5
b = 6
if (a ==5 and b ==6) or (b ==3 and a==4):
    print 'nooo'

'''

today_file = '2016-11-10'
today_file_format = datetime.datetime.strptime(today_file, '%Y-%m-%d').date()

today_minus_7 = datetime.date.today() - timedelta(days=7)

if today_file_format > today_minus_7:
    print 'e'
'''
#before_date_home = before_date_home.strftime('%m/%d/%Y')
#today_file = datetime.datetime.strptime(today_file, '%m/%d/%Y').date()
#print today_file
#if datetime.date.today() > before_date_home:

'''
today_file_plus7 = today_file_format + timedelta(days=7)

print today_file_format
print today_file_plus7
print today

if  today < today_file_plus7:
    print 'works'
'''
#file_date_seven = datetime.date.today(file_date) - timedelta(days=2)
#print file_date_seven

'''
def mortgage(median_price):
    ir = .04/float(12)
    return float("{0:.2f}".format((.8*(median_price))*((ir*((1+ir)**360))/(((1+ir)**360)-1))+((median_price*.01)/12)+((median_price*.01)/12)))

print mortgage(581000)


'''
#home_1_median = median_bd(home_1_median,home_1_bd)


'''

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
    return float("{0:.2f}".format((.8*(median_price))*((ir*((1+ir)**360))/(((1+ir)**360)-1))+((median_price*.01)/12)+((median_price*.01)/12)))

print mortgage(360000)


def median_bd(hoa,hoa_median):
    if hoa != []: return int(int(np.median(hoa)))
    else: return int(0)



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

overall_filename = 'cities_test.csv'


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

    url = 'http://www.estately.com/listings/info/1800-wilson-boulevard--109'
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html.parser")
    row = str(soup.find_all("div", {"class":"row margin-bottom-20"}))
    print row
    datestart = row.find(datestr)


    property_url = 'http://www.estately.com/listings/info/1800-wilson-boulevard--109'
    b = requests.get(property_url)
    soup = BeautifulSoup(b.content,"html.parser")
    home_site = str(soup.find_all("di", {"class":"row margin-bottom-20"}))
    print home_site
    hoa_loc = home_site.find('Condo Coop Fee:')
    print hoa_loc
    if hoa_loc != -1:
        hoa_loc_end = home_site.find('</p>',hoa_loc)
        hoa = int(home_site[hoa_loc+18:hoa_loc_end-2])
        print hoa




def eyo(a,b):
    if a == 3 and b==3 :
        return "no"
    else:
        return "yes"

print eyo(3,3)


hoa_6_bd = [4,5,6]
hoa_6_bd_median = 3

def median_bd(hoa,hoa_median):
    if hoa != []: return int(int(np.median(hoa)))
    else: return int(0)

def median_bd(hoa, hoa_median):
        if hoa: return int(np.median(hoa))

hoa_6_bd_median = median_bd(hoa_6_bd,hoa_6_bd_median)
print hoa_6_bd_median
print hoa_6_bd


home_2_bd_both = [5,2,4]
home_2_both_median = 0

def TWICE(one,two):
        if one != []:
            return two = int(np.median(one))
        else:
            return two = 0





print TWICE(home_2_bd_both,home_2_both_median)

home_1_bd_both = []
def mortgage(median_price):
    ir = .04/float(12)
    return float("{0:.2f}".format((.8*(median_price))*((ir*((1+ir)**360))/(((1+ir)**360)-1))+((median_price*.01)/12)+((median_price*.01)/12)))

home_price = 500000
hoa = 400
home_1_bd_both.append(int(mortgage(home_price)+hoa))
print home_1_bd_both


# extract the variables you want
names = data['name']
latitude = data['latitude']
longitude = data['longitude']

# pick out a subset of them
n = 25



city_list = ['Richmond','Norfolk','Falls Church']
diff = ['500','400','800']


# some random heights for each of the bars.
heights = np.random.randint(3, 12, len(city_list))


plt.figure(1)
h = plt.bar(xrange(len(city_list)), diff, label=city_list)
plt.subplots_adjust(bottom=0.3)

xticks_pos = [0.65*patch.get_width() + patch.get_xy()[0] for patch in h]

plt.xticks(xticks_pos, city_list,  ha='right', rotation=45)

plt.show()
'''
