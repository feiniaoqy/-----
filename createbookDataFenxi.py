from mysql.connector import (connection)
#�������ݿ�Ĳ���

conn = connection.MySQLConnection(user="root",
                                  passwd="gh17",
                                  host = "localhost",
                                  database ="test")
cursor = conn.cursor()#����һ������cursor

###�������ݱ�bookMessage
sql1 = """create table `test`.`bookDataFenxi`(
        kind CHAR(50) NOT NULL,
        jieyue INT,
        jiansuo INT,
        w DOUBLE,
        Wi DOUBLE);"""
sql = sql1
    ###ranknum:������
    ###name������
    ###pricer:ԭ��
    ###prices:�ۺ��
cursor.execute(sql)
cursor.close()
conn.close()



