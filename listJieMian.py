import wx
import wx.grid
import urllib2
from sgmllib import SGMLParser
from mysql.connector import (connection)
#这是一个得到购书清单的软件。其主要功能是根据类别显示得到的清单（书名，价格，榜单）


###创建一个针对每一类的购书清单的类
class ListTable(wx.grid.PyGridTableBase):
    def __init__(self,bookKind,kindMoney):
        
        self.kindMoney = float(kindMoney)
        self.bookKind = bookKind
        wx.grid.PyGridTableBase.__init__(self)
        self.colLabels = ('rankNum','bookName','pricer','prices')

        ###设置一个从数据库得到数据的函数
        conn = connection.MySQLConnection(user="root",
                                         passwd="gh17",
                                         host = "localhost",
                                         database ="test")
        cursor = conn.cursor()#创建一个对象cursor

        ###执行一个查询
        sql = 'select * from %s'%self.bookKind####把对应数据库的内容查询出来
        cursor.execute(sql)

        datasql = cursor.fetchall()###把查询结果存到变量data里，这是一个元组
        conn.commit()
        cursor.close()#关闭游标
        ###对data元组进行转码操作
        rankNum = []
        name = []
        pricer = []
        prices = []
        ###对从数据库得到的数据进行行列交换
        l = len(datasql)
        for i in range(4):
            for j in range(l):
                if i == 0:
                    rankNum.append(datasql[j][i])
                elif i == 1:
                    name.append(datasql[j][i])
                elif i == 2:
                    pricer.append(datasql[j][i])
                elif i == 3:
                    prices.append(datasql[j][i])
        dataBook = (rankNum,name,pricer,prices)

        ###设置一个根据类金额得到类清单的函数
        ####bookData[2]表示每一本书的折后价
        for i in range(len(dataBook[2])):
            if self.kindMoney > 0:
                self.kindMoney = self.kindMoney-float(dataBook[2][i])
                l = i###记录能购买这类书的数量
            else:
                break
            
        rankNum2 = []
        name2 = []
        pricer2 = []
        prices2 = []
        for i in range(4):
            for j in range(l):
                if i == 0:
                    rankNum2.append(dataBook[i][j])
                elif i == 1:
                    name2.append(dataBook[i][j])
                elif i == 2:
                    pricer2.append(dataBook[i][j])
                elif i == 3:
                    prices2.append(dataBook[i][j])
        self.data = (rankNum2,name2,pricer2,prices2)
        self.collen = len(rankNum2)
    def GetNumberRows(self):
        return self.collen 
    def GetNumberCols(self):
        return 4
    def IsEmptyCell(self,row,col):
        return False
    def GetValue(self,row,col):
        return '%s'%self.data[col][row]
    def SetValue(self,row,col,value):
        pass
    def GetColLabelValue(self,col):
        return self.colLabels[col]
    def GetRowLabelValue(self,row):
        return row+1
    

    
###创建一个金额分配表格的类
class KindMoneyTable(wx.grid.PyGridTableBase):
    #frame2 = TestFrame()
    def __init__(self,money):
        self.money = money
        
        #print self.money
        wx.grid.PyGridTableBase.__init__(self)
        self.kindMoney = []
        ###各类的百分比
        kindListPecent=(0.0002899947462618469, 0.06540992610128324, 0.06444327694707709,
                        0.00041952573292547185, 0.0007715471332488804, 0.00039278177299243485,
                        0.00010246481034585257, 0.03664832772112945, 4.237145459270319e-05,
                        0.02872953784987262, 0.007597540135675653, 0.35083427460794725,
                        3.6329897378914705e-05, 0.028124979358012853, 0.0723635973461614,
                        9.207333193813639e-05, 0.0002638146650020968, 2.0138524045961588e-06,
                        4.422419880493165e-05, 5.8965598406575535e-05, 4.430475290111549e-06,
                        0.0006711767294038079, 0.00021298503031008976, 0.0024671303038226624,
                        0.0553718385135256, 0.00025229542924780677, 0.039826509031966925,
                        0.05979852776111651, 0.002640804935195035, 2.76300549910593e-05,
                        1.151923575429003e-05, 0.009939892144509537, 0.0360701104187218,
                        0.0009016419985857923, 0.035114577729789015, 0.08664825522244289,
                        0.000368051665463994, 0.004015541140668557, 0.0008368765052539798,
                        0.007364094364934866, 0.0002978890476878638, 0.00040583153657421794,
                        8.482346328159021e-05)
        for i in range(len(kindListPecent)):
            self.m = '%.2f'%(kindListPecent[i]*self.money)
            self.kindMoney.append(str(self.m))
           # print str(kindListPecent[i]*self.money)
        self.data = (self.kindMoney,)
        print self.data
        for i in range(1):
            for j in range(43):
                print self.data[i][j]
        self.colLabels = kindList
        self.rowLabels = ('各类金额分配',)
    def GetNumberRows(self):
        return 1 
    def GetNumberCols(self):
        return len(kindList)
    def IsEmptyCell(self,row,col):
        return False
    def GetValue(self,row,col):
        return '%s'%self.data[row][col]
        #print float(self.data[col][row])
    def SetValue(self,row,col,value):
        pass
    def GetColLabelValue(self,col):
        return self.colLabels[col]
    def GetRowLabelValue(self,row):
        return self.rowLabels[row]

class ListFrame(wx.Frame):
    def __init__(self):
        
        
        wx.Frame.__init__(self,None,title='图书采集系统之购书清单',size = (660,600))
        panel = wx.Panel(self,-1)##创建面板
        self.money = 0
        self.kindBookMoney = ('')
        self.bookKind = ''
        ###总金额输入文本框
        self.basicLabel = wx.StaticText(panel,-1,"总金额：",pos=(5,0),size=(60,20)
                                        )
        self.priceText= wx.TextCtrl(panel,-1,"2.00",pos=(70,0),size=(90,20),
                                    style = wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER,self.OnClick,self.priceText)
        ###设置确定按钮
        buttonSure = wx.Button(panel,label='确定',pos=(170,0),size=(80,20))
        self.Bind(wx.EVT_BUTTON,self.OnClickSure,buttonSure)
        ###设置类别选择下拉菜单
        self.kindListLabel = wx.StaticText(panel,-1,"请选择图书类别：",
                                           pos=(260,0),size=(100,20))
        self.choice = wx.Choice(panel,-1,pos=(360,0),size=(80,20),
                                choices = kindList )
        
        ###设置清单按钮
        buttonBookList = wx.Button(panel,label = '购书清单',pos=(450,0),
                                   size =(80,20))
        self.Bind(wx.EVT_BUTTON,self.OnClickList,buttonBookList)
    

    def OnClickSure(self, event):
        ##创建文本对话框
        self.dlgEnter = wx.TextEntryDialog(None,'是否确定输入的总金额为:','标题信息',
                                           '%s'%(self.priceText.GetValue()),style=wx.OK|wx.CANCEL)
        if self.dlgEnter.ShowModal() == wx.ID_OK:
            self.priceText.SetValue(self.dlgEnter.GetValue())
            self.money = float(self.dlgEnter.GetValue())
            ###显示类别的金额分配的网格
            gridKindMoney = wx.grid.Grid(self,pos=(0,20),size=(660,68))
            kindMoneyTable = KindMoneyTable(self.money)
            
            self.kindBookMoney = kindMoneyTable.kindMoney
            gridKindMoney.SetTable(kindMoneyTable,True)
            #gridKindMoney.AutoSize()
    def OnClick(self, event):
        ##创建文本对话框
        self.dlgEnter = wx.TextEntryDialog(None,'是否确定输入的总金额为:','标题信息',
                                           '%s'%(self.priceText.GetValue()),style=wx.OK|wx.CANCEL)
        if self.dlgEnter.ShowModal() == wx.ID_OK:
            self.priceText.SetValue(self.dlgEnter.GetValue())
            self.money = float(self.dlgEnter.GetValue())
            gridKindMoney = wx.grid.Grid(self,pos=(0,20),size=(660,68))
            kindMoneyTable = KindMoneyTable(self.money)

            self.kindBookMoney = kindMoneyTable.kindMoney
            gridKindMoney.SetTable(kindMoneyTable,True)
            #gridKindMoney.AutoSize()
            
     #####得到清单的操作
    def OnClickList(self,event):
        bookListIndex = self.choice.GetSelection()
        #wx.MessageBox('%s'%(kindList[bookListIndex])) 
        self.dlgEnter = wx.TextEntryDialog(None,'是否确定选择的类别为：','标题信息',
                                           '%s'%(kindList[bookListIndex]),style=wx.OK|wx.CANCEL)
        if self.dlgEnter.ShowModal() == wx.ID_OK:
            self.bookKind = kindListName.get(kindList[bookListIndex])
            #bookListData = List(self.money,bookKind)
            gridList = wx.grid.Grid(self,pos=(0,85),size=(660,512))
            listTable= ListTable(self.bookKind,self.kindBookMoney[bookListIndex])
            gridList.SetTable(listTable,True)
            gridList.AutoSize()

kindListName = {
        '童书':'tongshu',
        '文化':'wenhua',
        '心理学':'xinlixue',
        '法律':'falv',
        '建筑':'jianzhu',
        '计算机/网络':'jisuanji',
        '艺术':'yishu',
        '教材':'jiaocai',
        '工业设计':'gonmgyesheji',
        '考试':'kaoshi',
        '管理':'guanli',
        '社会科学':'shehuikexue',
        '旅游/地图':'lvyou',
        '外语':'waiyu',
        '烹饪/美食':'pengren',
        '时尚/美妆':'shishang',
        '家庭/家居':'jiating',
        '亲子/家教':'qinzi',
        '两性关系':'liangxingguanxi',
        '孕产/胎教':'yunchan',
        '保健/养生':'baojian',
        '体育/运动':'tiyu',
        '手工/DIY':'shougong',
        '历史':'lishi',
        '传记':'zhuanji',
        '哲学/宗教':'zhexue',
        '政治/军事':'zhengzhi',
        '文学':'wenxue',
        '投资理财':'touzilicai',
        '经济':'jingji',
        '科普读物':'kepuduwu',
        '小说':'xiaoshuo',
        '医学':'yixue',
        '农业/林业':'nonglin',
        '自然科学':'zirankexue',
        '中小学教辅':'zhongxiaoxuejiaofu',
        '工具书':'gongjushu',
        '英文原版书':'yinwenyuanbanshu',
        '青春文学':'qinchunwenxue',
        '动漫/幽默':'dongman',
        '成功/励志':'chenggong',
        '休闲/爱好':'xiuxian',
        '育儿/早教':'yuer',
        }

kindList = ('童书','文化','心理学','法律','建筑','计算机/网络',
            '艺术','教材','工业设计','考试','管理','社会科学',
            '旅游/地图','外语','烹饪/美食','时尚/美妆','家庭/家居',
            '亲子/家教','两性关系','孕产/胎教','保健/养生',
            '体育/运动','手工/DIY','历史','传记','哲学/宗教',
            '政治/军事','文学','投资理财','经济','科普读物',
            '小说','医学','农业/林业','自然科学','中小学教辅',
            '工具书','英文原版书','青春文学','动漫/幽默','成功/励志',
            '休闲/爱好','育儿/早教')
if __name__ == "__main__":
    app = wx.App()
    frame = ListFrame()
    #print float(frame.priceText.GetValue())###注意要转换数据类型
    frame.Show()
    app.MainLoop()

