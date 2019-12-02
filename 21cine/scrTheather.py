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

#prepare logging file and do collect all data city, then di search by city
def scrapTheater(conn, url):
    logging.basicConfig(
            filename='theater.log',
            filemode ='w',
            format =FORMAT,
            level=logging.DEBUG)
    
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, "html5lib")
    #getLatestCity(conn,soup)
   
    try:
        i = 0
        n = 3
      
        while i < n:
            input = raw_input("search by city : ")
            resultVal = inputValidation(input)
           
            if resultVal == 0:
                i+=1
           
            else :
                print "do search [%s]" %input 
                srcByCity(conn, input)
                logging.info('do search by city ')  
                conn.close()
                break
   
            
            logging.info('var i %s' %i)
            if i == n:
                print 'Action canceled' 

    except Exception as err:
        logging.error(err)
        raise

#check for validation input city and theater
def inputValidation(word):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')  
    if len(word) == 0:
        print 'no city inserted, please enter valid input'
        logging.info('no city inserted') 
       
        return 0
    elif word.isdigit():
        print 'input is digit [%s], please enter valid input' %word
        logging.info('input is digit [%s]' %word)

        return 0
    elif regex.search(word) is not None :
        print 'input contain special character [%s], please enter valid input' %word
        logging.info('input is special char [%s]' %word)
      
        return 0
    else :
        return 1

#get all available city data 
def getLatestCity(db_cursor, soup):
    #start from section id='content'
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
                cityName = cityUrl[53:]
                cityName = list(cityName)
                commaIndex = cityName.index(',')
                cityName = cityName[0:commaIndex] 
                cityName = "".join(cityName)
                FileAccess.insertTheaterInfo(db_cursor, cityId, cityUrl, cityName)
    except Exception as err:
        logging.error(err)
        raise

#get all list theater type and search by category/type (XXI, Premiere, Imax)
def getTheaterbyUrl(conn, url, city):
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, "html5lib")
    #validation   
    try:
        i = 0
        n = 3
      
        while i < n:
            input = raw_input("choose theater -> XXI, Premiere, Imax : ")
            resultVal = inputValidation(input)
           
            if resultVal == 0:
                i+=1
           
            else :
                print "do search Theater [%s] with type [%s]" %(city, input) 
                searchTheaterType(conn,soup, input, city)
                logging.info('do search theater type ')  
                conn.close()
                break
   
            
            logging.info('var i %s' %i)
            if i == n:
                print 'Action canceled' 

    except Exception as err:
        logging.error(err)
        raise

#do search all theater based on type  
def searchTheaterType(conn, soup, input, city):
    #start from div class='tab-container'
    
    print 'list of theater with type [%s] in [%s] :' %(input, city)
    val = ''
    if input == 'XXI':
        val = 'tableXXI'
    elif input == 'Premiere':
        val = 'tablePREMIER'
    elif input =='Imax':
        val = 'tableIMAX'
  
    getStartDiv = soup.find("div", {"class": "tab-container"})
    getTheaterType = getStartDiv.find("tbody", {"id": ""+val+""}) 
    try :
        logging.info("select theater type [%s] " %val)
        if len(getTheaterType.find_all('tr')) == 0 :
            logging.info('no data found for [%s] '%val)
            print 'no data found'
        else :
            for link in getTheaterType.find_all('tr'):
              
                getNameTheater = link.find('td').text
                getUrlTheater = link.find('a').get('href')
                getNoneItem = link.find('td').next_sibling.next_sibling
                getTelpTheater =  getNoneItem.next_sibling.next_sibling.text
                logging.info(getNameTheater)
                logging.info(getUrlTheater)
                logging.info(getTelpTheater)
                FileAccess.insertAllTheater(conn, val, getNameTheater,
                                        getUrlTheater, getTelpTheater)
               
                print ' -'+getNameTheater+ ' : ' +getTelpTheater

    except Exception as err :
        logging.error(err)
        raise

#search by city like : 'jakarta' 
def srcByCity(conn, inputCity):
    urlRet = FileAccess.checkTheaterByCity(conn, inputCity)
    #if urlRet is not None :
    if urlRet != 0 :
        #record exist
        getTheaterbyUrl(conn, urlRet[0], inputCity)

    else : 
        #record not exist, berikan usulan pencarian 
        print 'no item found on that keyword %s'%inputCity
        logging.info('no item found on that keyword [%s]' %inputCity)



def main():
    db_cursor = FileAccess.Connect() 
    scrapTheater(db_cursor,url)

main()
