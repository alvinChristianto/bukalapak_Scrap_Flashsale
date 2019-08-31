import sys
import time
import requests
import mysql.connector

from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from mysql.connector import Error
from mysql.connector import errorcode
from scrPerPage import getPerPage
from secret import *
from conn import *
from getSeqId import getSeqId

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def getId():
    idSeq = getSeqId()
    newidSeq = idSeq[0] + 1
    listId = (newidSeq, "")
    return listId

def getSource(header):
    db_cursor = db_connection.cursor()

    for link in header.find_all('div'): 
        headerMov = link.find("div", {"class": "movie"}) 
        if (headerMov != None):
            headerMovDesc = headerMov.find("div", {"class": "movie-desc"})  
            headerMovLab = headerMovDesc.find("span", {"class": "movie-label"})
            headerlink = headerMov.find('a')
            headerHref = headerlink.get('href')
            
            #get title movie
            movie_title = headerMovDesc.h4.text
           
            #get rating on alt tag
            movie_rating = headerMovLab.img['alt']
            
            #get link href
            movie_link =  headerHref
           
            #get all info on href
            #getPerPage(headerHref)

         
            getOnlyId = getId() 
            db_cursor.execute(sql_insert_seq_id, getId())  
            

            listEntry = (getOnlyId[0], movie_title, movie_rating, movie_link)
   
            print listEntry
   
            db_cursor.execute(sql_insert_movie, listEntry)  
        
            db_connection.commit()
           
            time.sleep(0.2)
            getPerPage(headerHref, getOnlyId[0])
            print ("ALL Record inserted successfully into python_users table")  
    db_cursor.close()              


def scrape(baseUrl): 
    r = requests.get(baseUrl, verify=False)
    soup = BeautifulSoup(r.text, "html5lib")
    
    header = soup.find("div", {"id": "now-playing"})
    #print soup.prettify()
    try: 
        getSource(header)   
    except BaseException as e:
        print "Error : " +str(e)
        print "line : {}".format(sys.exc_info()[-1].tb_lineno)

if __name__ == "__main__":
    url ="https://www.21cineplex.com"

    print(scrape(url))

