import requests
import logging
import re
import FileAccess

from bs4 import BeautifulSoup
from mysql.connector import Error
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
FORMAT = "%(asctime)s : %(levelname)s >> %(message)s"


url = "https://21cineplex.com/theaters"

def scrapTheather(url):
    logging.basicConfig(
            filename='theater.log',
            filemode ='w',
            format =FORMAT,
            level=logging.DEBUG)
    
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, "html5lib")
    #getSource(soup)
   
    try:
        i = 0
        n = 3
        while i < n:
            input = raw_input("search by city : ")
            if len(input) == 0:
                i += 1
                print 'no city inserted, please enter valid input'
                logging.info('no city inserted') 
            elif len(input) > 0 :
                regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]') 
                if input.isdigit():
                    i += 1
                    print 'input is digit [%s], please enter valid input' %input
                    logging.info('input is digit [%s]' %input)
                elif regex.search(input) is not None :
                    i += 1
                    print 'input contain special character [%s], please enter valid input' %input
                    logging.info('input is special char [%s]' %input)
                else :
                    print "do search [%s]" %input 
                    logging.info('do search by city ')  
                    break
            else :
               i += 1
               print 'unknown action, please input correct action :' 
               logging.info('trying [%s]' %i) 
            
            logging.info('var i %s' %i)
            if i == n:
                print 'Action canceled' 

    except Exception as err:
        logging.error(err)


def getSource(soup):
    db_cursor = FileAccess.Connect()

    getSectionContent = soup.find("section", {"id": "content"})
    getBaseCity = getSectionContent.find("div", {"class": "select-twenty dark-twenty"})
    getCity = getBaseCity.find("select", {"class": "custom-select"})
    try:
        for link in getCity.find_all('option'):
            cityUrl = link.get('value') 
            cityId = link.get('data-id')
        
            ret = FileAccess.checkTheater(db_cursor, cityId)       
            if ret == 1 :
                logging.info('theater exist %s'%cityId)
                continue
            else :
                logging.info('inserting : %s'%cityId)
                FileAccess.insertTheaterInfo(db_cursor, cityId, cityUrl)
    except exception as err:
        logging.error(err)
  


scrapTheather(url)
