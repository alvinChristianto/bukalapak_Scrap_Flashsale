import mysql.connector
import sys

from mysql.connector import Error
from mysql.connector import errorcode
from conn import *
from secret import * 

try :
    noId = sys.argv[1]
except IndexError:
    noId = None

def showMovieToDel(noId):
    db_cursor = db_connection.cursor()  
    if noId:
        print "displaying all Data movie with id "+noId
        db_cursor.execute(sql_show_movie_noId, (noId,))
        record = db_cursor.fetchone()
        
    else:
        print "displaying all Data movie"
        db_cursor.execute(sql_show_movie)
        record = db_cursor.fetchall()
    
    if record is None:
        print "no data show or there is no data at all"
    else:
        print record
        print "\n"
        deleteMovieList(noId) 

def deleteMovieList(noId):
    db_cursor = db_connection.cursor()
    input = raw_input("do you want to remove the data ? (y/n)")
    if input == 'Y' or input == 'y' : 
        if noId:  
            db_cursor.execute(sql_delete_movie_noId, (noId,)) 
            db_connection.commit()      
        else :
            db_cursor.execute(sql_delete_movie) 
            db_cursor.execute(sql_delete_movie_id) 
            db_connection.commit()      
        print "data deleted "
    elif input == 'N' or input == 'n' : 
        print "Action Canceled !"
    else :
        print "Unidentified action response, Action Canceled !"

   
  
    

showMovieToDel(noId)

