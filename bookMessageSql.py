from mysql.connector import (connection)
#�������ݿ�Ĳ���
kindList = ['`shehuikexue`',
            '`lvyou`','`waiyu`','`pengren`','`shishang`','`jiating`',
            '`qinzi`','`liangxingguanxi`','`yunchan`','`baojian`',
            '`tiyu`','`shougong`','`lishi`','`zhuanji`','`zhexue`',
            '`zhengzhi`','`wenxue`','`touzilicai`','`jingji`','`kepuduwu`',
            '`xiaoshuo`','`yixue`','`nonglin`','`zirankexue`','`zhongxiaoxuejiaofu`',
            '`gongjushu`','`yinwenyuanbanshu`','`qinchunwenxue`','`dongman`','`chenggong`',
            '`xiuxian`','`yuer`']
conn = connection.MySQLConnection(user="root",
                                  passwd="gh17",
                                  host = "localhost",
                                  database ="test")
cursor = conn.cursor()#����һ������cursor
for s1 in kindList:
    ###�������ݱ�bookMessage
    sql1 = """create table `test`.%s(
            ranknum INT NOT NULL,
            name CHAR(50),
            pricer DOUBLE,
            prices DOUBLE);"""%s1
    sql = sql1
    ###ranknum:������
    ###name������
    ###pricer:ԭ��
    ###prices:�ۺ��
    cursor.execute(sql)
cursor.close()
conn.close()



