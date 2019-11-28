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
                searchTheaterByCity(conn, input)
                logging.info('do search by city ')  
                conn.close()
                break
   
            
            logging.info('var i %s' %i)
            if i == n:
                print 'Action canceled' 

    except Exception as err:
        logging.error(err)


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
                FileAccess.insertTheaterInfo(db_cursor, cityId, cityUrl)
    except Exception as err:
        logging.error(err)

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
                searchTheaterType(conn,soup, input)
                logging.info('do search theater type ')  
                conn.close()
                break
   
            
            logging.info('var i %s' %i)
            if i == n:
                print 'Action canceled' 

    except Exception as err:
        logging.error(err)

    
def searchTheaterType(conn, soup, input):
    #start from div class='tab-container'
    val = ''
    if input == 'XXI':
        val = 'tableXXI'
    elif input == 'Premiere':
        val = 'talePREMIERE'
    elif input =='Imax':
        val = 'tableIMAX'
  
    getStartDiv = soup.find("div", {"class": "tab-container"})
    getTheaterType = getStartDiv.find("tbody", {"id": ""+val+""}) 
    try : 
        for link in getTheaterType.find_all('tr'):
            getNameTheater = link.find('td').text
            getUrlTheater = link.find('a').get('href')
            getNoneItem = link.find('td').next_sibling.next_sibling
            getTelpTheater =  getNoneItem.next_sibling.next_sibling.text
            logging.info(getNameTheater)
            logging.info(getUrlTheater)
            logging.info(getTelpTheater)
            #getUrlTheater = link.find('a')
            #getTelpTheater = link 
    except Exception as err :
        logging.error(err)

    
def searchTheaterByCity(conn, inputCity):
    urlRet = FileAccess.checkTheaterByCity(conn, inputCity)
    if urlRet is not None :
        #record exist
        getTheaterbyUrl(conn, urlRet[0], inputCity)

    else : 
        #record not exist, berikan usulan pencarian 
        logging.info('no item found on that keyword')



def main():
    db_cursor = FileAccess.Connect() 
    scrapTheater(db_cursor,url)

main()
