import requests
import logging

import FileAccess

from bs4 import BeautifulSoup
from mysql.connector import Error
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
FORMAT = "%(asctime)s : %(levelname)s >> %(message)s"


url = "https://21cineplex.com/theaters"

def scrapTheather(url):
    logging.basicConfig(
            filename='runlog.log',
            filemode ='w',
            format =FORMAT,
            level=logging.DEBUG)
    
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, "html5lib")
    
   
    try:
        getSource(soup)
    except Exception as err:
        logging.error(err)


def getSource(soup):
    getSectionContent = soup.find("section", {"id": "content"})
    getBaseCity = getSectionContent.find("div", {"class": "select-twenty dark-twenty"})
    getCity = getBaseCity.find("select", {"class": "custom-select"})
    for link in getCity.find_all('option'):
        cityValue = link.get('value')
        cityId = link.get('data-id')
       
        print "data = %s | %s " %(cityId, cityValue)


scrapTheather(url)
