import mysql.connector

from mysql.connector import Error
from mysql.connector import errorcode
from conn import *
from secret import * 

def showMovie():
    db_cursor = db_connection.cursor()
    print "displaying all Data movie"
    db_cursor.execute(sql_show_movie)
    record = db_cursor.fetchall()
    print record


def deleteMovieList():
    db_cursor = db_connection.cursor()
    input = raw_input("do you want to remove all data (movie list)? (y/n)")
    if input == 'Y' or input == 'y' : 
        print "all record has ben deleted !"
    elif input == 'N' or input == 'n' : 
        print "Action Canceled !"
    else :
        print "Unidentified action response, Action Canceled !"

    #db_cursor.execute(sql_delete_movie)
    #db_cursor.execute(sql_delete_movie_id)
    #db_connection.commit()
  
    

showMovie()
deleteMovieList()
