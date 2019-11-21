import mysql.connector
from conn import *

def getSeqId():
    db_cursor = db_connection.cursor()
    stat_db = "SELECT MAX(idseq) FROM tb_seq_id"
    db_cursor.execute(stat_db)
    
    myresult = db_cursor.fetchone()

    return myresult

def checkMov(cursor, title):
    ret = 0
    #db_cursor = db_connection.cursor(buffered=True)
    stat_db = """SELECT title FROM tb_movie_list where title = "%s" """ %title
    print stat_db
    #db_cursor.execute(stat_db)
    cursor.execute(stat_db)

    myresult = cursor.fetchone()

    if myresult == None :
        ret = 0
    else :
        ret = 1
   
    return ret

