from mysql.connector import (connection)
w = []
Wi = []
sum = 0
jieyue = (3000,1000000,800000,5009,3334,4454,454,454555,545,434454,4534,5435443,454,435344,34543,343,3234,23,545,777,55,2332,3223,32423,3423,3332,32423,342343,32423,343,43,45354,546336,5353,543553,5433,4353,53453,4353,5435,4534,5435,453)
jiansuo = (6000,60000,800000,6005,34554,6566,4546,456545,454,45433,453445,34543,443,4345,4353443,4343,3443,33,567,555,55,32333,332,23443,3423243,2332,2342343,2342332,34223,345,543,435556,53533,34554,5353,5356534,5435,35434,34534,435354,354,3453,3454)
kindList = ('ͯ��','�Ļ�','����ѧ','����','����','�����/����',
            '����','�̲�','��ҵ���','����','����','����ѧ',
            '����/��ͼ','����','���/��ʳ','ʱ��/��ױ','��ͥ/�Ҿ�',
            '����/�ҽ�','���Թ�ϵ','�в�/̥��','����/����',
            '����/�˶�','�ֹ�/DIY','��ʷ','����','��ѧ/�ڽ�',
            '����/����','��ѧ','Ͷ�����','����','���ն���',
            'С˵','ҽѧ','ũҵ/��ҵ','��Ȼ��ѧ','��Сѧ�̸�',
            '������','Ӣ��ԭ����','�ഺ��ѧ','����/��Ĭ','�ɹ�/��־',
            '����/����','����/���')
print len (jieyue)
print len(jiansuo)
print len(kindList)


conn = connection.MySQLConnection(user="root",
                                  passwd="gh17",
                                  host = "localhost",
                                  database ="test")
cursor = conn.cursor()#����һ������cursor
###ɾ��ԭ������###
cursor1 = conn.cursor()
sql = "truncate table `bookDataFenxi`"

cursor1.execute(sql)
conn.commit()
cursor1.close()
for j in range(len(jieyue)):
    w.append(int(0.8*jieyue[j]+0.2*jiansuo[j]))
for m in range(len(jieyue)):
    sum = sum + w[m]
for n in range(len(jieyue)):
    Wi.append(w[n]*1.00/sum)
    
print w
print '.............'
print sum
print Wi
###��������###
for i in range(len(jieyue)):
    cursor = conn.cursor()
    s1 = 'insert into `bookDataFenxi`'
    
    sql2 = s1+'(kind,jieyue,jiansuo,w,Wi)values(%(kind)s,%(jieyue)s,%(jiansuo)s,%(w)s,%(Wi)s)'
    w1 = int(0.8*jieyue[i]+0.2*jiansuo[i])
    data = {
       'kind':kindList[i].decode('gbk').encode('utf8'),
        'jieyue':jieyue[i],
        'jiansuo':jiansuo[i],
        'w':w[i],
        'Wi':Wi[i],
        }
    cursor.execute(sql2,data)
    conn.commit()
    cursor.close()
conn.close()
