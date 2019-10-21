#########################################
# FILE   : CRUD access file to database #
# CREATOR: alvinChristianto             #
# DATE   : 20190901                     #
#########################################




import mysql.connector
import secret
from mysql.connector import Error
from mysql.connector import errorcode
#from secret import *


db_connection = mysql.connector.connect(host=secret.HOST,
                             database=secret.DATABASE,
                             user=secret.USER,
                             password=secret.PASSWORD)




#####*CREATE*##### 
sql_insert_movie    = ("""INSERT INTO tb_movie_list (
                        movie_id, 
                        title, 
                        rating,
                        movie_link) 
                    VALUES (%s, %s, %s, %s)""")
#select top 1 id, then add 1
sql_insert_seq_id   = ("""INSERT INTO tb_seq_id (
                        idseq, 
                        info) 
                    VALUES (%s, %s)""")
####*READ*####
sql_show_movie = ("""select * from tb_movie_list""")
sql_show_movie_noId = ("""select * from tb_movie_list 
                          where movie_id = %s """)


####*UPDATE*#####
sql_update_movie    = ("""UPDATE tb_movie_list set 
                        genre = %s,
                        produser = %s, 
                        sutradara = %s,
                        writer = %s, 
                        rumah_produksi = %s, 
                        cast = %s, 
                        sinopsis = %s
                         where movie_id = %s """)

####*DELETE*####
sql_delete_movie_id = ("""delete from tb_seq_id where idseq > 10001""")
sql_delete_movie_noId    = ("""delete from tb_movie_list where movie_id = %s """)
sql_delete_movie    = ("""delete from tb_movie_list""")
