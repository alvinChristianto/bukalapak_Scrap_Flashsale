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

def scrapTheater(conn, url):
    logging.basicConfig(
            filename='theater.log',
            filemode ='w',
            format =FORMAT,
            level=logging.DEBUG)
    
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, "html5lib")
    getLatestCity(conn,soup)
   
    try:
        i = 0
        n = 3
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]') 
        while i < n:
            input = raw_input("search by city : ")
            if len(input) == 0:
                print 'no city inserted, please enter valid input'
                logging.info('no city inserted') 
                i += 1
            elif input.isdigit():
                print 'input is digit [%s], please enter valid input' %input
                logging.info('input is digit [%s]' %input)
                i += 1
            elif regex.search(input) is not None :
                print 'input contain special character [%s], please enter valid input' %input
                logging.info('input is special char [%s]' %input)
                i += 1
            else :
                searchTheaterByCity(conn, input)
                print "do search [%s]" %input 
                logging.info('do search by city ')  
                break
   
            
            logging.info('var i %s' %i)
            if i == n:
                print 'Action canceled' 

    except Exception as err:
        logging.error(err)


def getLatestCity(db_cursor, soup):
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
    except Exception as err:
        logging.error(err)
  
def searchTheaterByCity(conn, inputCity):
    print FileAccess.checkTheaterByCity(conn, inputCity)

def main():
    db_cursor = FileAccess.Connect() 
    scrapTheater(db_cursor,url)

main()
