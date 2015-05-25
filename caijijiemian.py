import wx
import wx.grid
import urllib2
from sgmllib import SGMLParser
from mysql.connector import (connection)



       

###���ǶԼ۸�Ĳ���###
class GetPrice(SGMLParser):
    def reset(self):
        self.m=1#��ԭ�ۺ��ۺ�۷ֿ��ı���
        self.pricer = []#����յ�ԭ��list(list)
        self.prices = []#����յ��ۺ��list(�б�)
        self.flag = False
        self.getdata = False
        self.verbatim = 0
        SGMLParser.reset(self)
        
    def start_div(self, attrs):
        if self.flag == True:
            self.verbatim +=1 #�����Ӳ�div�ˣ�������1
            return
        for k,v in attrs:#����div�����������Լ���ֵ
            if k == 'class' and v == 'price':#ȷ��������<div class='price'>
                self.flag = True
                return

    def end_div(self):#����</div>
        if self.verbatim == 0:
            self.flag = False
        if self.flag == True:#�˳��Ӳ�div�ˣ�������1
            self.verbatim -=1

    def start_p(self, attrs):
        if self.flag == False:
            return
        self.getdata = True
        
    def end_p(self):#����</p>
        if self.getdata:
            self.getdata = False

    def handle_data(self, text):#�����ı�
        if self.getdata:
            if(text==')'):
                self.m=1
            elif text == '�����飺':
                self.m=0
            else:
                self.m+=1
                if(self.m>=2 and self.m<=3):
                    if(self.m==2):
                        self.pricer.append(text)
                    else:
                        self.prices.append(text)





###�������Ĳ���###
class GetName(SGMLParser):
    def reset(self):
        self.name = []
        self.flag = False
        self.getdata = False
        self.verbatim = 0
        SGMLParser.reset(self)
        
    def start_div(self, attrs):
        if self.flag == True:
            self.verbatim +=1 #�����Ӳ�div�ˣ�������1
            return
        for k,v in attrs:#����div�����������Լ���ֵ
            if k == 'class' and v == 'name':#ȷ��������<div class='name'>
                self.flag = True
                return

    def end_div(self):#����</div>
        if self.verbatim == 0:
            self.flag = False
        if self.flag == True:#�˳��Ӳ�div�ˣ�������1
            self.verbatim -=1

    def start_a(self, attrs):
        if self.flag == False:
            return
        self.getdata = True
        
    def end_a(self):#����</p>
        if self.getdata:
            self.getdata = False

    def handle_data(self, text):#�����ı�
        if self.getdata:
            if(text[len(text)-3:]!='...'):
                self.name.append(text)    



class TestTable(wx.grid.PyGridTableBase):
    #frame2 = TestFrame()
    def __init__(self, url1):
        self.url1 = url1
        wx.grid.PyGridTableBase.__init__(self)
        self.page = 1
        self.name = []
        self.pricer = []
        self.prices = []
        while self.page<3:
                        
            #url2=frame.basicText.GetValue()+str(page)
            self.url2 = self.url1+ str(self.page)      
            content = urllib2.urlopen(self.url2).read()
            ###����####
            lister1 = GetName()
            lister1.feed(content)
            self.name.extend(lister1.name)#lister1.name#
                            
                                    
            ###�۸�###
            lister2 = GetPrice()
            lister2.feed(content)
            self.pricer.extend(lister2.pricer)#lister2.pricer#�ۺ�� 
            self.prices.extend(lister2.prices)#lister2.prices#ԭ��

            self.page += 1
        ##����һ��Ԫ�������                    
        self.data = (self.name,self.pricer,self.prices)
            
        self.colLabels = ['name','pricer','prices']
        self.collen = len(self.name)
    def GetNumberRows(self):
        return self.collen 
    def GetNumberCols(self):
        return 3
    def IsEmptyCell(self,row,col):
        return False
    def GetValue(self,row,col):
        return '%s'%(self.data[col][row])
    def SetValue(self,row,col,value):
        pass

    def GetColLabelValue(self,col):
        return self.colLabels[col]
    def GetRowLabelValue(self,row):
        return row+1

  

class TestFrame(wx.Frame):
    def __init__(self):
        
        self.url = ''
        self.kindListName = ''
        wx.Frame.__init__(self,None,title='ͼ��ɼ�ϵͳ',size = (570,700))
        panel = wx.Panel(self,-1)##�������
        ###��һ��
        self.kindListLabel = wx.StaticText(panel,-1,"��ѡ��ͼ�����",
                                           pos=(10,0),size=(100,20))
        self.choice = wx.Choice(panel,-1,pos=(110,0),size=(80,20),
                                choices = kindList)
        self.buttonSure = wx.Button(panel,label='ȷ��',pos=(200,0),size=(80,20))
        self.Bind(wx.EVT_BUTTON,self.OnClickSure,self.buttonSure)
        ###�ڶ���
        self.basicLabel = wx.StaticText(panel,-1,"�ɼ���ַ��",
                                pos=(10,25),size=(60,20))
        self.basicText = wx.TextCtrl(panel,-1,'',
                                pos=(80,25),size=(300,20))
        
        
        
        self.buttonBegin = wx.Button(panel,label='��ʼ�ɼ�',
                                     pos=(390,25),size=(80,20))
        
        self.buttonSave = wx.Button(panel,label='�������ݿ�',
                                    pos=(470,25),size=(80,20))

        
        

        ###���¼�
        self.Bind(wx.EVT_BUTTON,self.OnClickBegin,self.buttonBegin)
        self.Bind(wx.EVT_BUTTON,self.OnClickSave,self.buttonSave)
    def OnClickSure(self,event):
        bookListIndex = self.choice.GetSelection()
        self.dlgEnter = wx.TextEntryDialog(None,'�Ƿ�ȷ��ѡ�����Ϊ��','������Ϣ',
                                           '%s'%(kindList[bookListIndex],),style=wx.OK|wx.CANCEL)
        if self.dlgEnter.ShowModal() == wx.ID_OK:
            self.basicText.SetValue(self.dlgEnter.GetValue())
            self.basicText.SetValue(url.get(kindList[bookListIndex]))
            self.url = self.basicText.GetValue()
            self.kindListName = kindListName.get(kindList[bookListIndex])###�õ��������ݿ�ı���
    
    def OnClickBegin(self,event):
        
                
        grid = wx.grid.Grid(self,pos=(0,45),size=(560,780))
        
        table = TestTable(self.url)##
        grid.SetTable(table,True)
        grid.AutoSize()
        
        
    def OnClickSave(self,event):
        self.dlgEnter = wx.TextEntryDialog(None,'�Ƿ�ȷ�������ݴ������ݿ⣺','������Ϣ',
                                           '%s'%(self.kindListName),style=wx.OK|wx.CANCEL)
        if self.dlgEnter.ShowModal() == wx.ID_OK:
            table2 = TestTable(self.url)
            #�������ݿ�Ĳ���
            conn = connection.MySQLConnection(user="root",
                                              passwd="gh17",
                                              host = "localhost",
                                              database ="test")
            ###ɾ��ԭ������###
            cursor1 = conn.cursor()
            sql = 'truncate table %s'%self.kindListName
            cursor1.execute(sql)
            conn.commit()
            cursor1.close()
            ###�������###
            for i in range(table2.collen):
                cursor = conn.cursor()#����һ������cursor
                s1 = 'insert into %s'%self.kindListName
                addBookMessage1 = s1 + '(ranknum,name,pricer,prices)values(%(ranknum)s,%(name)s,%(pricer)s,%(prices)s);'
                addBookMessage = addBookMessage1
               
                ##ͼ����Ϣ�Լ���Ӧ��ת��###
                dataBookMessage = {
                    'ranknum':i+1,
                    'name':table2.name[i].decode('gbk').encode('utf8'),
                    'pricer':table2.pricer[i].decode('gbk').encode('utf8'),
                    'prices':table2.prices[i].decode('gbk').encode('utf8'),
                    }

                cursor.execute(addBookMessage,dataBookMessage)
                conn.commit()
                cursor.close()#�ر��α�
            conn.close()
            #conn.close()�ر����ݿ�����
        
    
kindList = ('ͯ��','�Ļ�','����ѧ','����','����','�����/����',
                    '����','�̲�','��ҵ���','����','����','����ѧ',
                    '����/��ͼ','����','���/��ʳ','ʱ��/��ױ','��ͥ/�Ҿ�',
                    '����/�ҽ�','���Թ�ϵ','�в�/̥��','����/����',
                    '����/�˶�','�ֹ�/DIY','��ʷ','����','��ѧ/�ڽ�',
                    '����/����','��ѧ','Ͷ�����','����','���ն���',
                    'С˵','ҽѧ','ũҵ/��ҵ','��Ȼ��ѧ','��Сѧ�̸�',
                    '������','Ӣ��ԭ����','�ഺ��ѧ','����/��Ĭ','�ɹ�/��־',
                    '����/����','����/���')
url = {
        'ͯ��':'http://bang.dangdang.com/books/newhotsales/01.41.00.00.00.00-recent30-0-0-1-',
        '�Ļ�':'http://bang.dangdang.com/books/newhotsales/01.34.00.00.00.00-recent30-0-0-1-',
        '����ѧ':'http://bang.dangdang.com/books/newhotsales/01.31.00.00.00.00-recent30-0-0-1-',
        '����':'http://bang.dangdang.com/books/newhotsales/01.26.00.00.00.00-recent30-0-0-1-',
        '����':'http://bang.dangdang.com/books/newhotsales/01.55.00.00.00.00-recent30-0-0-1-',
        '�����/����':'http://bang.dangdang.com/books/newhotsales/01.54.00.00.00.00-recent30-0-0-1-',
        '����':'http://bang.dangdang.com/books/newhotsales/01.07.00.00.00.00-recent30-0-0-1-',
        '�̲�':'http://bang.dangdang.com/books/newhotsales/01.49.00.00.00.00-recent30-0-0-1-',
        '��ҵ���':'http://bang.dangdang.com/books/newhotsales/01.63.00.00.00.00-recent30-0-0-1-',
        '����':'http://bang.dangdang.com/books/newhotsales/01.47.00.00.00.00-recent30-0-0-1-',
        '����':'http://bang.dangdang.com/books/newhotsales/01.22.00.00.00.00-recent30-0-0-1-',
        '����ѧ':'http://bang.dangdang.com/books/newhotsales/01.30.00.00.00.00-recent30-0-0-1-',
        '����/��ͼ':'http://bang.dangdang.com/books/newhotsales/01.12.00.00.00.00-recent30-0-0-1-',
        '����':'http://bang.dangdang.com/books/newhotsales/01.45.00.00.00.00-recent30-0-0-1-',
        '���/��ʳ':'http://bang.dangdang.com/books/newhotsales/01.10.00.00.00.00-recent30-0-0-1-',
        'ʱ��/��ױ':'http://bang.dangdang.com/books/newhotsales/01.11.00.00.00.00-recent30-0-0-1-',
        '��ͥ/�Ҿ�':'http://bang.dangdang.com/books/newhotsales/01.14.00.00.00.00-recent30-0-0-1-',
        '����/�ҽ�':'http://bang.dangdang.com/books/newhotsales/01.15.00.00.00.00-recent30-0-0-1-',
        '���Թ�ϵ':'http://bang.dangdang.com/books/newhotsales/01.16.00.00.00.00-recent30-0-0-1-',
        '�в�/̥��':'http://bang.dangdang.com/books/newhotsales/01.06.00.00.00.00-recent30-0-0-1-',
        '����/����':'http://bang.dangdang.com/books/newhotsales/01.18.00.00.00.00-recent30-0-0-1-',
        '����/�˶�':'http://bang.dangdang.com/books/newhotsales/01.19.00.00.00.00-recent30-0-0-1-',
        '�ֹ�/DIY':'http://bang.dangdang.com/books/newhotsales/01.20.00.00.00.00-recent30-0-0-1-',
        '��ʷ':'http://bang.dangdang.com/books/newhotsales/01.36.00.00.00.00-recent30-0-0-1-',
        '����':'http://bang.dangdang.com/books/newhotsales/01.38.00.00.00.00-recent30-0-0-1-',
        '��ѧ/�ڽ�':'http://bang.dangdang.com/books/newhotsales/01.28.00.00.00.00-recent30-0-0-1-',
        '����/����':'http://bang.dangdang.com/books/newhotsales/01.27.00.00.00.00-recent30-0-0-1-',
        '��ѧ':'http://bang.dangdang.com/books/newhotsales/01.05.00.00.00.00-recent30-0-0-1-',
        'Ͷ�����':'http://bang.dangdang.com/books/newhotsales/01.24.00.00.00.00-recent30-0-0-1-',
        '����':'http://bang.dangdang.com/books/newhotsales/01.25.00.00.00.00-recent30-0-0-1-',
        '���ն���':'http://bang.dangdang.com/books/newhotsales/01.52.00.00.00.00-recent30-0-0-1-',
        'С˵':'http://bang.dangdang.com/books/newhotsales/01.03.00.00.00.00-recent30-0-0-1-',
        'ҽѧ':'http://bang.dangdang.com/books/newhotsales/01.56.00.00.00.00-recent30-0-0-1-',
        'ũҵ/��ҵ':'http://bang.dangdang.com/books/newhotsales/01.66.00.00.00.00-recent30-0-0-1-',
        '��Ȼ��ѧ':'http://bang.dangdang.com/books/newhotsales/01.62.00.00.00.00-recent30-0-0-1-',
        '��Сѧ�̸�':'http://bang.dangdang.com/books/newhotsales/01.43.00.00.00.00-recent30-0-0-1-',
        '������':'http://bang.dangdang.com/books/newhotsales/01.50.00.00.00.00-recent30-0-0-1-',
        'Ӣ��ԭ����':'http://bang.dangdang.com/books/newhotsales/01.58.00.00.00.00-recent30-0-0-1-',
        '�ഺ��ѧ':'http://bang.dangdang.com/books/newhotsales/01.01.00.00.00.00-recent30-0-0-1-',
        '����/��Ĭ':'http://bang.dangdang.com/books/newhotsales/01.09.00.00.00.00-recent30-0-0-1-',
        '�ɹ�/��־':'http://bang.dangdang.com/books/newhotsales/01.21.00.00.00.00-recent30-0-0-1-',
        '����/����':'http://bang.dangdang.com/books/newhotsales/01.04.00.00.00.00-recent30-0-0-1-',
        '����/���':'http://bang.dangdang.com/books/newhotsales/01.17.00.00.00.00-recent30-0-0-1-',
        }
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

app = wx.App()
frame = TestFrame()



    
##����һ��Ԫ�������

frame.Show()
app.MainLoop()
