import requests
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import time
import numpy as np
import csv
import logging
import os
import os.path
import smtplib



os.system('washingtondc_rent.py')

os.system('miami_rent.py')

os.system('richmond_rent.py')

os.system('sf_rent.py')

os.system('baltimore_rent.py')

content = 'rent_craigslist.py - COMPLETED'
mail = smtplib.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
mail.login('onenefautomation@gmail.com','!Password1')
mail.sendmail('x','gianbustillo@gmail.com',content)
mail.close()
