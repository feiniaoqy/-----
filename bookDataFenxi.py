from mysql.connector import (connection)
#连接数据库的操作

conn = connection.MySQLConnection(user="root",
                                  passwd="gh17",
                                  host = "localhost",
                                  database ="test")
cursor = conn.cursor()#创建一个对象cursor

###创建数据表bookMessage
sql1 = """create table `test`.`bookDataFenxi`(
        kind CHAR(50) NOT NULL,
        jieyue INT,
        jiansuo INT,
        w DOUBLE,
        Wi DOUBLE);"""
sql = sql1
    ###ranknum:排名号
    ###name：书名
    ###pricer:原价
    ###prices:折后价
cursor.execute(sql)
cursor.close()
conn.close()



