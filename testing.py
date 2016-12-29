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

craigs_url = line = column = 0

overall_filename = 'dalecity_forsale.html'

t = requests.get(overall_filename)
soup = BeautifulSoup(t.content,"html.parser")
div = str(soup.find_all("div", {"class":"buffer"}))
price_loc = div.find('ice margin-bottom-10">')
print price_loc
