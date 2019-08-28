import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from secret import *


db_connection = mysql.connector.connect(host=HOST,
                             database=DATABASE,
                             user=USER,
                             password=PASSWORD)

#select top 1 id, then add 1

sql_insert_movie    = ("""INSERT INTO TB_MOVIE_LIST (
                        movie_id, 
                        title, 
                        rating,
                        movie_link) 
                    VALUES (%s, %s, %s, %s)""")

sql_insert_seq_id   = ("""INSERT INTO TB_SEQ_ID (
                        idseq, 
                        info) 
                    VALUES (%s, %s)""")

sql_update_movie    = ("""UPDATE TB_MOVIE_LIST set 
                        genre = %s,
                        produser = %s, 
                        sutradara = %s,
                        writer = %s, 
                        rumah_produksi = %s, 
                        cast = %s, 
                        sinopsis = %s
                         where movie_id = %s """)

