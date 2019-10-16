import mysql.connector
from conn import *

def getSeqId():
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT MAX(idseq) FROM TB_SEQ_ID")

    myresult = db_cursor.fetchone()

    return myresult

def checkMov(title):
    db_cursor = db_connection.cursor()
    stat_db = "SELECT title FROM TB_MOVIE_LIST where title = '"+title+"'"
   
    db_cursor.execute(stat_db)
    
    myresult = db_cursor.fetchone()

    return myresult

