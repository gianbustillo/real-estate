import requests
from bs4 import BeautifulSoup
from time import gmtime, strftime
import time
import smtplib
import datetime

emailsent_two = emailsent_three = emailsent_four = emailsent_five = 0

def email(content):
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login('onenefautomation@gmail.com','!Password1')
    mail.sendmail('x','gianbustillo@gmail.com',content)
    mail.close()

datetime.datetime.today().weekday()

while strftime("%H:%M:%S") < '16:01:00' and datetime.datetime.today().weekday() not in [5,6]:
    finance_url = 'https://www.google.com/finance?q=INDEXSP%3A.INX'

    u = requests.get(finance_url)

    soup = BeautifulSoup(u.content, "html.parser")
    div = str(soup.find_all("div", {"class":"elastic"}))

    number_loc = div.find('ref_626307_l')
    number_loc_end = div.find('</span>',number_loc)
    number = float(div[number_loc+14:number_loc_end].replace(",",""))

    percent_loc = div.find('ref_626307_cp')
    percent_loc_end = div.find('%',percent_loc)
    percent = float(div[percent_loc+15:percent_loc_end].replace("(","").replace(")",""))
    print number
    print percent

    content_two = 'S&P500 has dropped more than 2 percent today. It is currently at ' + str(percent) + '%' + ' and at ' + str(number) + '.'
    content_three = 'S&P500 has dropped more than 3 percent today. It is currently at ' + str(percent) + '%' + ' and at ' + str(number) + '.'
    content_four = 'S&P500 has dropped more than 4 percent today. It is currently at ' + str(percent) + '%' + ' and at ' + str(number) + '.'
    content_five = 'S&P500 has dropped at least more than 5 percent today. It is currently at ' + str(percent) + '%' + ' and at ' + str(number) + '.'

    if percent < -5 and emailsent_five != 1:
        email(content_five)
        emailsent_five = emailsent_four = emailsent_three = emailsent_two = 1
    elif percent < -4 and emailsent_four != 1:
        email(content_four)
        emailsent_four = emailsent_three = emailsent_two = 1
    elif percent < -3 and emailsent_three != 1:
        email(content_three)
        emailsent_three = emailsent_two = 1
    elif percent < -2 and emailsent_four != 1:
        email(content_two)
        emailsent_two = 1

    time.sleep(300)
'''
mail = smtplib.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
mail.login('onenefautomation@gmail.com','!Password1')
mail.sendmail('x','gianbustillo@gmail.com','Stock Email Notification completed')
mail.close()
'''
