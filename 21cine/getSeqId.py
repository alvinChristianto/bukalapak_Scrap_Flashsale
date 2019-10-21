import mysql.connector
from conn import *

def getSeqId():
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT MAX(idseq) FROM tb_seq_id")

    myresult = db_cursor.fetchone()

    return myresult

def checkMov(title):
    ret = 0
    db_cursor = db_connection.cursor(buffered=True)
    stat_db = "SELECT title FROM tb_movie_list where title = '"+title+"'"
   
    db_cursor.execute(stat_db)
    
    myresult = db_cursor.fetchone()

    if myresult == None :
        ret = 0
    else :
        ret = 1
   
    return ret

