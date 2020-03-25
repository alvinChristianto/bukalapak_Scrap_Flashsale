import sys
import time
import requests
import mysql.connector
import logging

import getSeqId
import scrPerPage
import FileAccess

from secret import *
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from mysql.connector import Error
from mysql.connector import errorcode
#from scrPerPage import getPerPage

#from getSeqId import getSeqId

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
FORMAT = "%(asctime)s : %(levelname)s >> %(message)s"


def getId():
    idSeq = getSeqId.getSeqId()
    newidSeq = idSeq[0] + 1
    listId = (newidSeq, "")
    return listId

def stringNeutral(movie_title):
    movie_title = list(movie_title)
    try:
        titleIndex = movie_title.index("'")
        if titleIndex:
            movie_title.insert(titleIndex, "'")
            print movie_title
    except Exception as e:
        pass
           
    movie_title = "".join(movie_title) 
    return movie_title

def getSource(header):
    #db_cursor = db_connection.cursor(buffered=True)
    db_cursor = FileAccess.Connect()            #connect to database

    for link in header.find_all('div'): 
        headerMov = link.find("div", {"class": "movie"}) 
     
        if (headerMov != None):
            headerMovDesc = headerMov.find("div", {"class": "movie-desc"})  
            headerMovLab = headerMovDesc.find("span", {"class": "movie-label"})
            
            headerlink = headerMov.find('a')
            headerHref = headerlink.get('href')
           
            #get title movie
            movie_title = headerMovDesc.h4.text
           
            #neutralize "'" EOL error
            #movie_title = stringNeutral(movie_title)

            checkmov = FileAccess.checkMov(db_cursor, movie_title)      #check db if title exist
            chkMov = checkmov
           
            
            if chkMov == 1:               #if return 1 then pass/already exist, 0 need to insert
                logging.info('movie title exist : '+str(movie_title))
                continue    
            else :
                logging.info('inserting : %s' %movie_title)
                #get rating on alt tag
                #handle nonetype getitem error
                if headerMovLab.img == None :
                    movie_rating = ""
                else :
                    movie_rating = headerMovLab.img['alt'] 
            
                #get link href
                movie_link =  headerHref
            
                getSeqId = FileAccess.getSeqId(db_cursor)       #get new id based on prev id 
                logging.info('creating id '+str(getSeqId))
              
                FileAccess.insertSeqId(db_cursor,getSeqId[0], getSeqId[1]) #insert new id [id,info]
          
                listEntry = (
                    getSeqId[0], 
                    movie_title, 
                    movie_rating, 
                    movie_link
                    )
                logging.info('id and link '+str(getSeqId[0]) + ", " +movie_link)
          
                logging.info('insert TITLE|RATING|LINK -> %s | %s | %s '
                        % (movie_title, movie_rating, movie_link))
   
                FileAccess.insertMovie(db_cursor, listEntry)        # insert movie list type
                
                scrPerPage.getPerPage(db_cursor, headerHref, getSeqId[0]) # get detail of that title
                logging.info('id '+ str(getSeqId[0]) + ' inserted succesfully')
                time.sleep(0.2) 
            logging.info("next record") 
    logging.info("All inserted successfully into python_users table")  
    db_cursor.close()              


def scrape(baseUrl): 
    logging.basicConfig(
            filename='runlog.log',
            filemode ='a',                      #set 'w' to overwrite/truncate file runlog.log
            format =FORMAT,
            level=logging.DEBUG) 
    
    try:                                        #check if requests can connect https to baseUrl
        r = requests.get(baseUrl, verify=False)       
        logging.info("succesfully connect to %s" %(baseUrl))
    except requests.exceptions.RequestException as e:
        logging.error(e) 
        raise SystemExit(e)

    soup = BeautifulSoup(r.text, "html5lib")
 
    header = soup.find("div", {"id": "now-playing"})
    #print soup.prettify()
    try: 
        getSource(header)
      
    except BaseException as e:
        logging.error('Error %s' % str(e))

if __name__ == "__main__":
    url ="https://www.21cineplex.com"

    scrape(url)

