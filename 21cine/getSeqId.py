import mysql.connector
from conn import *

def getSeqId():
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT MAX(idseq) FROM TB_SEQ_ID")

    myresult = db_cursor.fetchone()

    return myresult
