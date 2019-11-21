import requests
import mysql.connector
import re
import logging
import FileAccess

from bs4 import BeautifulSoup
from mysql.connector import Error
from mysql.connector import errorcode
from secret import *
from conn import *

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def getPerPage(conn, url, movie_id):
    #db_cursor = conn.cursor()
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, "html5lib")

    header = soup.find("div", {"class": "main-content main-detail"})
    headerRow = header.find("div", {"class": "row"})
    headerCol8 = headerRow.find("div", {"class": "col-8"})
    headerDescBox = headerCol8.find("div", {"class": "desc-box"})
    headerDescMov = headerDescBox.find("ul",{"class": "desc-movie"})
    headerDescSynop = headerDescBox.find("div",{"class": "desc-synopsis"})

    #get Title on per page
    #print headerCol8.h2.text
    #print headerDescBox.

    #get All desc on per page
    listPage = []
    for link in headerDescMov.find_all('li'):
        link.span.clear() 
        linksplit = link.text
        linksplit = re.sub('\s+', ' ', linksplit)
       
        listPage.append(linksplit)
   
    #get sinopsis
    listPage.append(headerDescSynop.p.text)
    listPage.append(movie_id)
  
    logging.info('insert synopsis %s ' % str(listPage))
    #print listPage 
    #print sql_update_movie 
    FileAccess.updateMovie(conn,listPage)
    

