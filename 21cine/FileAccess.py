#########################################
# FILE   : CRUD access file to database #
# CREATOR: alvinChristianto             #
# DATE   : 20190901                     #
#########################################


import mysql.connector
import secret
import logging
import sys
from mysql.connector import Error
from mysql.connector import errorcode
#from secret import *


#functionName = sys._getframe().f_code.co_name

#------------
def Connect():
    db_connection = mysql.connector.connect(host=secret.HOST,
                    database=secret.DATABASE,
                    user=secret.USER,
                    password=secret.PASSWORD)
    return db_connection

def getSeqId(conn):
    try :
        stat_db = """SELECT MAX(idseq) FROM tb_seq_id"""
        db_cursor = conn.cursor()
        db_cursor.execute(stat_db)
        logging.info("executing --> "+stat_db) 
        myresult = db_cursor.fetchone()
    
        resultId = 0
        if myresult[0] is not None:   
            resultId = myresult[0]
        else:
            resultId = 100000

        resultId = resultId + 1    
        listResult = (resultId, "")
        return listResult
    except Exception as err:
        logging.error(err) 
        
  
def checkMov(conn, title):
    ret = 0
    try : 
        #db_cursor = db_connection.cursor(buffered=True)
        stat_db = """SELECT title FROM tb_movie_list where title = "%s" """ %title
     
        db_cursor = conn.cursor()
        db_cursor.execute(stat_db)
        logging.info("executing --> "+stat_db) 
      
        myresult = db_cursor.fetchone()

        if myresult == None :
            ret = 0
        else :
            ret = 1

        return ret

    except Exception as err:
        logging.error(err)

def checkTheater(conn, theaterId):
    try : 
        stat_db = """SELECT * FROM tb_theater where theaterId = "%s" """ %theaterId
     
        db_cursor = conn.cursor()
        db_cursor.execute(stat_db)
        logging.info("executing --> "+stat_db) 
      
        myresult = db_cursor.fetchone()

        if myresult == None :
            ret = 0
        else :
            ret = 1

        return ret

    except Exception as err:
        logging.error(err)

def checkTheaterByCity(conn, city):
    try : 
        stat_db = """SELECT * FROM tb_theater where  url like  "%%s%" """ %city
        logging.info("executing --> "+stat_db) 
     
        db_cursor = conn.cursor()
        db_cursor.execute(stat_db)
      
        myresult = db_cursor.fetchone()

        if myresult == None :
            ret = 0
        else :
            ret = 1

        return ret

    except Exception as err:
        logging.error(err)




#####*CREATE*##### 
def insertSeqId(conn, arg1, arg2):
    try:
        stat_db = """INSERT INTO tb_seq_id(
                        idseq,
                        info)
                    VALUES (%d, '%s')""" %(arg1, arg2)
        
        db_cursor = conn.cursor()
        db_cursor.execute(stat_db)
        logging.info("executing --> "+stat_db) 
        conn.commit()
    except Exception as err:
        logging.error(err)
    
def insertMovie(conn, entry):
    try:
        stat_db = """INSERT INTO tb_movie_list (
                            movie_id, 
                            title, 
                            rating,
                            movie_link) 
                        VALUES (%d, "%s", '%s', '%s')""" %(entry[0], entry[1], entry[2], entry[3])
       
        db_cursor = conn.cursor()
        db_cursor.execute(stat_db)
        logging.info("executing --> "+stat_db) 
        conn.commit()
    except Exception as err:
        logging.error(err)

def insertTheaterInfo(conn, cityId, url):
    city = ""
    try : 
        stat_db = """INSERT INTO tb_theater(theaterId, url, city)
                    VALUES (%s, '%s', '%s') """ %(cityId, url,city )
     
        db_cursor = conn.cursor()
        db_cursor.execute(stat_db)
        logging.info("executing --> "+stat_db) 
        conn.commit()
    except Exception as err:
        logging.error(err)
      
   



sql_insert_seq_id   = ("""INSERT INTO tb_seq_id (
                        idseq, 
                        info) 
                    VALUES (%s, %s)""")
####*READ*####


sql_show_movie = ("""select * from tb_movie_list""")
sql_show_movie_noId = ("""select * from tb_movie_list 
                          where movie_id = %s """)


####*UPDATE*#####
def updateMovie(conn, entry):
    try :
        stat_db    = """UPDATE tb_movie_list set 
                            genre = '%s',
                            produser = '%s', 
                            sutradara = '%s',
                            writer = '%s', 
                            rumah_produksi = '%s', 
                            cast = '%s', 
                            sinopsis = "%s"
                             where movie_id = %d """%(entry[0],entry[1], entry[2], entry[3],
                                                    entry[4],entry[5], entry[6], entry[7]) 
        db_cursor = conn.cursor()
        db_cursor.execute(stat_db)
        logging.info("executing --> "+stat_db)  
        conn.commit()
    
    except Exception as err:
        logging.error(err)
    

####*DELETE*####
sql_delete_movie_id = ("""delete from tb_seq_id where idseq > 10001""")
sql_delete_movie_noId    = ("""delete from tb_movie_list where movie_id = %s """)
sql_delete_movie    = ("""delete from tb_movie_list""")
