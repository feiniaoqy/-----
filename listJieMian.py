import wx
import wx.grid
import urllib2
from sgmllib import SGMLParser
from mysql.connector import (connection)
#����һ���õ������嵥�����������Ҫ�����Ǹ��������ʾ�õ����嵥���������۸񣬰񵥣�


###����һ�����ÿһ��Ĺ����嵥����
class ListTable(wx.grid.PyGridTableBase):
    def __init__(self,bookKind,kindMoney):
        
        self.kindMoney = float(kindMoney)
        self.bookKind = bookKind
        wx.grid.PyGridTableBase.__init__(self)
        self.colLabels = ('rankNum','bookName','pricer','prices')

        ###����һ�������ݿ�õ����ݵĺ���
        conn = connection.MySQLConnection(user="root",
                                         passwd="gh17",
                                         host = "localhost",
                                         database ="test")
        cursor = conn.cursor()#����һ������cursor

        ###ִ��һ����ѯ
        sql = 'select * from %s'%self.bookKind####�Ѷ�Ӧ���ݿ�����ݲ�ѯ����
        cursor.execute(sql)

        datasql = cursor.fetchall()###�Ѳ�ѯ����浽����data�����һ��Ԫ��
        conn.commit()
        cursor.close()#�ر��α�
        ###��dataԪ�����ת�����
        rankNum = []
        name = []
        pricer = []
        prices = []
        ###�Դ����ݿ�õ������ݽ������н���
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

        ###����һ����������õ����嵥�ĺ���
        ####bookData[2]��ʾÿһ������ۺ��
        for i in range(len(dataBook[2])):
            if self.kindMoney > 0:
                self.kindMoney = self.kindMoney-float(dataBook[2][i])
                l = i###��¼�ܹ��������������
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
    

    
###����һ�������������
class KindMoneyTable(wx.grid.PyGridTableBase):
    #frame2 = TestFrame()
    def __init__(self,money):
        self.money = money
        
        #print self.money
        wx.grid.PyGridTableBase.__init__(self)
        self.kindMoney = []
        ###����İٷֱ�
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
        self.rowLabels = ('���������',)
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
        
        
        wx.Frame.__init__(self,None,title='ͼ��ɼ�ϵͳ֮�����嵥',size = (660,600))
        panel = wx.Panel(self,-1)##�������
        self.money = 0
        self.kindBookMoney = ('')
        self.bookKind = ''
        ###�ܽ�������ı���
        self.basicLabel = wx.StaticText(panel,-1,"�ܽ�",pos=(5,0),size=(60,20)
                                        )
        self.priceText= wx.TextCtrl(panel,-1,"2.00",pos=(70,0),size=(90,20),
                                    style = wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER,self.OnClick,self.priceText)
        ###����ȷ����ť
        buttonSure = wx.Button(panel,label='ȷ��',pos=(170,0),size=(80,20))
        self.Bind(wx.EVT_BUTTON,self.OnClickSure,buttonSure)
        ###�������ѡ�������˵�
        self.kindListLabel = wx.StaticText(panel,-1,"��ѡ��ͼ�����",
                                           pos=(260,0),size=(100,20))
        self.choice = wx.Choice(panel,-1,pos=(360,0),size=(80,20),
                                choices = kindList )
        
        ###�����嵥��ť
        buttonBookList = wx.Button(panel,label = '�����嵥',pos=(450,0),
                                   size =(80,20))
        self.Bind(wx.EVT_BUTTON,self.OnClickList,buttonBookList)
    

    def OnClickSure(self, event):
        ##�����ı��Ի���
        self.dlgEnter = wx.TextEntryDialog(None,'�Ƿ�ȷ��������ܽ��Ϊ:','������Ϣ',
                                           '%s'%(self.priceText.GetValue()),style=wx.OK|wx.CANCEL)
        if self.dlgEnter.ShowModal() == wx.ID_OK:
            self.priceText.SetValue(self.dlgEnter.GetValue())
            self.money = float(self.dlgEnter.GetValue())
            ###��ʾ���Ľ����������
            gridKindMoney = wx.grid.Grid(self,pos=(0,20),size=(660,68))
            kindMoneyTable = KindMoneyTable(self.money)
            
            self.kindBookMoney = kindMoneyTable.kindMoney
            gridKindMoney.SetTable(kindMoneyTable,True)
            #gridKindMoney.AutoSize()
    def OnClick(self, event):
        ##�����ı��Ի���
        self.dlgEnter = wx.TextEntryDialog(None,'�Ƿ�ȷ��������ܽ��Ϊ:','������Ϣ',
                                           '%s'%(self.priceText.GetValue()),style=wx.OK|wx.CANCEL)
        if self.dlgEnter.ShowModal() == wx.ID_OK:
            self.priceText.SetValue(self.dlgEnter.GetValue())
            self.money = float(self.dlgEnter.GetValue())
            gridKindMoney = wx.grid.Grid(self,pos=(0,20),size=(660,68))
            kindMoneyTable = KindMoneyTable(self.money)

            self.kindBookMoney = kindMoneyTable.kindMoney
            gridKindMoney.SetTable(kindMoneyTable,True)
            #gridKindMoney.AutoSize()
            
     #####�õ��嵥�Ĳ���
    def OnClickList(self,event):
        bookListIndex = self.choice.GetSelection()
        #wx.MessageBox('%s'%(kindList[bookListIndex])) 
        self.dlgEnter = wx.TextEntryDialog(None,'�Ƿ�ȷ��ѡ������Ϊ��','������Ϣ',
                                           '%s'%(kindList[bookListIndex]),style=wx.OK|wx.CANCEL)
        if self.dlgEnter.ShowModal() == wx.ID_OK:
            self.bookKind = kindListName.get(kindList[bookListIndex])
            #bookListData = List(self.money,bookKind)
            gridList = wx.grid.Grid(self,pos=(0,85),size=(660,512))
            listTable= ListTable(self.bookKind,self.kindBookMoney[bookListIndex])
            gridList.SetTable(listTable,True)
            gridList.AutoSize()

kindListName = {
        'ͯ��':'tongshu',
        '�Ļ�':'wenhua',
        '����ѧ':'xinlixue',
        '����':'falv',
        '����':'jianzhu',
        '�����/����':'jisuanji',
        '����':'yishu',
        '�̲�':'jiaocai',
        '��ҵ���':'gonmgyesheji',
        '����':'kaoshi',
        '����':'guanli',
        '����ѧ':'shehuikexue',
        '����/��ͼ':'lvyou',
        '����':'waiyu',
        '���/��ʳ':'pengren',
        'ʱ��/��ױ':'shishang',
        '��ͥ/�Ҿ�':'jiating',
        '����/�ҽ�':'qinzi',
        '���Թ�ϵ':'liangxingguanxi',
        '�в�/̥��':'yunchan',
        '����/����':'baojian',
        '����/�˶�':'tiyu',
        '�ֹ�/DIY':'shougong',
        '��ʷ':'lishi',
        '����':'zhuanji',
        '��ѧ/�ڽ�':'zhexue',
        '����/����':'zhengzhi',
        '��ѧ':'wenxue',
        'Ͷ�����':'touzilicai',
        '����':'jingji',
        '���ն���':'kepuduwu',
        'С˵':'xiaoshuo',
        'ҽѧ':'yixue',
        'ũҵ/��ҵ':'nonglin',
        '��Ȼ��ѧ':'zirankexue',
        '��Сѧ�̸�':'zhongxiaoxuejiaofu',
        '������':'gongjushu',
        'Ӣ��ԭ����':'yinwenyuanbanshu',
        '�ഺ��ѧ':'qinchunwenxue',
        '����/��Ĭ':'dongman',
        '�ɹ�/��־':'chenggong',
        '����/����':'xiuxian',
        '����/���':'yuer',
        }

kindList = ('ͯ��','�Ļ�','����ѧ','����','����','�����/����',
            '����','�̲�','��ҵ���','����','����','����ѧ',
            '����/��ͼ','����','���/��ʳ','ʱ��/��ױ','��ͥ/�Ҿ�',
            '����/�ҽ�','���Թ�ϵ','�в�/̥��','����/����',
            '����/�˶�','�ֹ�/DIY','��ʷ','����','��ѧ/�ڽ�',
            '����/����','��ѧ','Ͷ�����','����','���ն���',
            'С˵','ҽѧ','ũҵ/��ҵ','��Ȼ��ѧ','��Сѧ�̸�',
            '������','Ӣ��ԭ����','�ഺ��ѧ','����/��Ĭ','�ɹ�/��־',
            '����/����','����/���')
if __name__ == "__main__":
    app = wx.App()
    frame = ListFrame()
    #print float(frame.priceText.GetValue())###ע��Ҫת����������
    frame.Show()
    app.MainLoop()

