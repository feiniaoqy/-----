from mysql.connector import (connection)
#连接数据库的操作
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
cursor = conn.cursor()#创建一个对象cursor
for s1 in kindList:
    ###创建数据表bookMessage
    sql1 = """create table `test`.%s(
            ranknum INT NOT NULL,
            name CHAR(50),
            pricer DOUBLE,
            prices DOUBLE);"""%s1
    sql = sql1
    ###ranknum:排名号
    ###name：书名
    ###pricer:原价
    ###prices:折后价
    cursor.execute(sql)
cursor.close()
conn.close()



