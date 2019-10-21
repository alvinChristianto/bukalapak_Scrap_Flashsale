import sys
import time
import requests
import mysql.connector
import logging

import getSeqId
import scrPerPage

from secret import *
from conn import *
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

def getSource(header):
    db_cursor = db_connection.cursor(buffered=True)

    for link in header.find_all('div'): 
        headerMov = link.find("div", {"class": "movie"}) 
     
        if (headerMov != None):
            headerMovDesc = headerMov.find("div", {"class": "movie-desc"})  
            headerMovLab = headerMovDesc.find("span", {"class": "movie-label"})
            
            headerlink = headerMov.find('a')
            headerHref = headerlink.get('href')
            
            #get title movie
            movie_title = headerMovDesc.h4.text
            
            checkmov = getSeqId.checkMov(movie_title) 
            chkMov = checkmov
            #if return 1 then pass/already exist, 0 need to insert
            if chkMov == 1:
                logging.info('movie title exist : '+str(movie_title))
                continue    
            else :
                logging.info('inserting : '+str(movie_title))
                #get rating on alt tag
                #handle nonetype getitem error
                if headerMovLab.img == None :
                    movie_rating = ""
                else :
                    movie_rating = headerMovLab.img['alt'] 
            
                #get link href
                movie_link =  headerHref
            
                getOnlyId = getId() 
                logging.info('creating id '+str(getOnlyId))
                db_cursor.execute(sql_insert_seq_id, getId())  
           
          
                listEntry = (
                    getOnlyId[0], 
                    movie_title, 
                    movie_rating, 
                    movie_link
                    )
                logging.info('id and link '+str(getOnlyId[0]) + ", " +movie_link)
          
                logging.info('insert TITLE|RATING|LINK -> %s | %s | %s '
                        % (movie_title, movie_rating, movie_link))
   
                db_cursor.execute(sql_insert_movie, listEntry)  
                db_connection.commit()
           
                scrPerPage.getPerPage(headerHref, getOnlyId[0])
                logging.info('id '+ str(getOnlyId[0]) + ' inserted succesfully')
                time.sleep(0.2) 
            logging.info("next ") 
    logging.info("All inserted successfully into python_users table")  
    db_cursor.close()              


def scrape(baseUrl): 
    logging.basicConfig(
            filename='runlog.log',
            filemode ='w',
            format =FORMAT,
            level=logging.DEBUG) 
   
    r = requests.get(baseUrl, verify=False)
    soup = BeautifulSoup(r.text, "html5lib")
    
    header = soup.find("div", {"id": "now-playing"})
    #print soup.prettify()
    try: 
        getSource(header)
      
    except BaseException as e:
        logging.error('Error %s' % str(e))
        logging.error('line '.format(sys.exc_info()[-1].tb_lineno))
        
        #print "Error : " +str(e)
        #print "line : {}".format(sys.exc_info()[-1].tb_lineno)

if __name__ == "__main__":
    url ="https://www.21cineplex.com"

    scrape(url)

