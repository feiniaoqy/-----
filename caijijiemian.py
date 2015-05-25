import wx
import wx.grid
import urllib2
from sgmllib import SGMLParser
from mysql.connector import (connection)



       

###这是对价格的操作###
class GetPrice(SGMLParser):
    def reset(self):
        self.m=1#把原价和折后价分开的变量
        self.pricer = []#定义空的原价list(list)
        self.prices = []#定义空的折后价list(列表)
        self.flag = False
        self.getdata = False
        self.verbatim = 0
        SGMLParser.reset(self)
        
    def start_div(self, attrs):
        if self.flag == True:
            self.verbatim +=1 #进入子层div了，层数加1
            return
        for k,v in attrs:#遍历div的所有属性以及其值
            if k == 'class' and v == 'price':#确定进入了<div class='price'>
                self.flag = True
                return

    def end_div(self):#遇到</div>
        if self.verbatim == 0:
            self.flag = False
        if self.flag == True:#退出子层div了，层数减1
            self.verbatim -=1

    def start_p(self, attrs):
        if self.flag == False:
            return
        self.getdata = True
        
    def end_p(self):#遇到</p>
        if self.getdata:
            self.getdata = False

    def handle_data(self, text):#处理文本
        if self.getdata:
            if(text==')'):
                self.m=1
            elif text == '电子书：':
                self.m=0
            else:
                self.m+=1
                if(self.m>=2 and self.m<=3):
                    if(self.m==2):
                        self.pricer.append(text)
                    else:
                        self.prices.append(text)





###对书名的操作###
class GetName(SGMLParser):
    def reset(self):
        self.name = []
        self.flag = False
        self.getdata = False
        self.verbatim = 0
        SGMLParser.reset(self)
        
    def start_div(self, attrs):
        if self.flag == True:
            self.verbatim +=1 #进入子层div了，层数加1
            return
        for k,v in attrs:#遍历div的所有属性以及其值
            if k == 'class' and v == 'name':#确定进入了<div class='name'>
                self.flag = True
                return

    def end_div(self):#遇到</div>
        if self.verbatim == 0:
            self.flag = False
        if self.flag == True:#退出子层div了，层数减1
            self.verbatim -=1

    def start_a(self, attrs):
        if self.flag == False:
            return
        self.getdata = True
        
    def end_a(self):#遇到</p>
        if self.getdata:
            self.getdata = False

    def handle_data(self, text):#处理文本
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
            ###书名####
            lister1 = GetName()
            lister1.feed(content)
            self.name.extend(lister1.name)#lister1.name#
                            
                                    
            ###价格###
            lister2 = GetPrice()
            lister2.feed(content)
            self.pricer.extend(lister2.pricer)#lister2.pricer#折后价 
            self.prices.extend(lister2.prices)#lister2.prices#原价

            self.page += 1
        ##定义一个元组存数据                    
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
        wx.Frame.__init__(self,None,title='图书采集系统',size = (570,700))
        panel = wx.Panel(self,-1)##创建面板
        ###第一行
        self.kindListLabel = wx.StaticText(panel,-1,"请选择图书类别：",
                                           pos=(10,0),size=(100,20))
        self.choice = wx.Choice(panel,-1,pos=(110,0),size=(80,20),
                                choices = kindList)
        self.buttonSure = wx.Button(panel,label='确定',pos=(200,0),size=(80,20))
        self.Bind(wx.EVT_BUTTON,self.OnClickSure,self.buttonSure)
        ###第二行
        self.basicLabel = wx.StaticText(panel,-1,"采集网址：",
                                pos=(10,25),size=(60,20))
        self.basicText = wx.TextCtrl(panel,-1,'',
                                pos=(80,25),size=(300,20))
        
        
        
        self.buttonBegin = wx.Button(panel,label='开始采集',
                                     pos=(390,25),size=(80,20))
        
        self.buttonSave = wx.Button(panel,label='存入数据库',
                                    pos=(470,25),size=(80,20))

        
        

        ###绑定事件
        self.Bind(wx.EVT_BUTTON,self.OnClickBegin,self.buttonBegin)
        self.Bind(wx.EVT_BUTTON,self.OnClickSave,self.buttonSave)
    def OnClickSure(self,event):
        bookListIndex = self.choice.GetSelection()
        self.dlgEnter = wx.TextEntryDialog(None,'是否确定选择类别为：','标题信息',
                                           '%s'%(kindList[bookListIndex],),style=wx.OK|wx.CANCEL)
        if self.dlgEnter.ShowModal() == wx.ID_OK:
            self.basicText.SetValue(self.dlgEnter.GetValue())
            self.basicText.SetValue(url.get(kindList[bookListIndex]))
            self.url = self.basicText.GetValue()
            self.kindListName = kindListName.get(kindList[bookListIndex])###得到存入数据库的表名
    
    def OnClickBegin(self,event):
        
                
        grid = wx.grid.Grid(self,pos=(0,45),size=(560,780))
        
        table = TestTable(self.url)##
        grid.SetTable(table,True)
        grid.AutoSize()
        
        
    def OnClickSave(self,event):
        self.dlgEnter = wx.TextEntryDialog(None,'是否确定把数据存入数据库：','标题信息',
                                           '%s'%(self.kindListName),style=wx.OK|wx.CANCEL)
        if self.dlgEnter.ShowModal() == wx.ID_OK:
            table2 = TestTable(self.url)
            #连接数据库的操作
            conn = connection.MySQLConnection(user="root",
                                              passwd="gh17",
                                              host = "localhost",
                                              database ="test")
            ###删除原有数据###
            cursor1 = conn.cursor()
            sql = 'truncate table %s'%self.kindListName
            cursor1.execute(sql)
            conn.commit()
            cursor1.close()
            ###数据入库###
            for i in range(table2.collen):
                cursor = conn.cursor()#创建一个对象cursor
                s1 = 'insert into %s'%self.kindListName
                addBookMessage1 = s1 + '(ranknum,name,pricer,prices)values(%(ranknum)s,%(name)s,%(pricer)s,%(prices)s);'
                addBookMessage = addBookMessage1
               
                ##图书信息以及相应的转码###
                dataBookMessage = {
                    'ranknum':i+1,
                    'name':table2.name[i].decode('gbk').encode('utf8'),
                    'pricer':table2.pricer[i].decode('gbk').encode('utf8'),
                    'prices':table2.prices[i].decode('gbk').encode('utf8'),
                    }

                cursor.execute(addBookMessage,dataBookMessage)
                conn.commit()
                cursor.close()#关闭游标
            conn.close()
            #conn.close()关闭数据库连接
        
    
kindList = ('童书','文化','心理学','法律','建筑','计算机/网络',
                    '艺术','教材','工业设计','考试','管理','社会科学',
                    '旅游/地图','外语','烹饪/美食','时尚/美妆','家庭/家居',
                    '亲子/家教','两性关系','孕产/胎教','保健/养生',
                    '体育/运动','手工/DIY','历史','传记','哲学/宗教',
                    '政治/军事','文学','投资理财','经济','科普读物',
                    '小说','医学','农业/林业','自然科学','中小学教辅',
                    '工具书','英文原版书','青春文学','动漫/幽默','成功/励志',
                    '休闲/爱好','育儿/早教')
url = {
        '童书':'http://bang.dangdang.com/books/newhotsales/01.41.00.00.00.00-recent30-0-0-1-',
        '文化':'http://bang.dangdang.com/books/newhotsales/01.34.00.00.00.00-recent30-0-0-1-',
        '心理学':'http://bang.dangdang.com/books/newhotsales/01.31.00.00.00.00-recent30-0-0-1-',
        '法律':'http://bang.dangdang.com/books/newhotsales/01.26.00.00.00.00-recent30-0-0-1-',
        '建筑':'http://bang.dangdang.com/books/newhotsales/01.55.00.00.00.00-recent30-0-0-1-',
        '计算机/网络':'http://bang.dangdang.com/books/newhotsales/01.54.00.00.00.00-recent30-0-0-1-',
        '艺术':'http://bang.dangdang.com/books/newhotsales/01.07.00.00.00.00-recent30-0-0-1-',
        '教材':'http://bang.dangdang.com/books/newhotsales/01.49.00.00.00.00-recent30-0-0-1-',
        '工业设计':'http://bang.dangdang.com/books/newhotsales/01.63.00.00.00.00-recent30-0-0-1-',
        '考试':'http://bang.dangdang.com/books/newhotsales/01.47.00.00.00.00-recent30-0-0-1-',
        '管理':'http://bang.dangdang.com/books/newhotsales/01.22.00.00.00.00-recent30-0-0-1-',
        '社会科学':'http://bang.dangdang.com/books/newhotsales/01.30.00.00.00.00-recent30-0-0-1-',
        '旅游/地图':'http://bang.dangdang.com/books/newhotsales/01.12.00.00.00.00-recent30-0-0-1-',
        '外语':'http://bang.dangdang.com/books/newhotsales/01.45.00.00.00.00-recent30-0-0-1-',
        '烹饪/美食':'http://bang.dangdang.com/books/newhotsales/01.10.00.00.00.00-recent30-0-0-1-',
        '时尚/美妆':'http://bang.dangdang.com/books/newhotsales/01.11.00.00.00.00-recent30-0-0-1-',
        '家庭/家居':'http://bang.dangdang.com/books/newhotsales/01.14.00.00.00.00-recent30-0-0-1-',
        '亲子/家教':'http://bang.dangdang.com/books/newhotsales/01.15.00.00.00.00-recent30-0-0-1-',
        '两性关系':'http://bang.dangdang.com/books/newhotsales/01.16.00.00.00.00-recent30-0-0-1-',
        '孕产/胎教':'http://bang.dangdang.com/books/newhotsales/01.06.00.00.00.00-recent30-0-0-1-',
        '保健/养生':'http://bang.dangdang.com/books/newhotsales/01.18.00.00.00.00-recent30-0-0-1-',
        '体育/运动':'http://bang.dangdang.com/books/newhotsales/01.19.00.00.00.00-recent30-0-0-1-',
        '手工/DIY':'http://bang.dangdang.com/books/newhotsales/01.20.00.00.00.00-recent30-0-0-1-',
        '历史':'http://bang.dangdang.com/books/newhotsales/01.36.00.00.00.00-recent30-0-0-1-',
        '传记':'http://bang.dangdang.com/books/newhotsales/01.38.00.00.00.00-recent30-0-0-1-',
        '哲学/宗教':'http://bang.dangdang.com/books/newhotsales/01.28.00.00.00.00-recent30-0-0-1-',
        '政治/军事':'http://bang.dangdang.com/books/newhotsales/01.27.00.00.00.00-recent30-0-0-1-',
        '文学':'http://bang.dangdang.com/books/newhotsales/01.05.00.00.00.00-recent30-0-0-1-',
        '投资理财':'http://bang.dangdang.com/books/newhotsales/01.24.00.00.00.00-recent30-0-0-1-',
        '经济':'http://bang.dangdang.com/books/newhotsales/01.25.00.00.00.00-recent30-0-0-1-',
        '科普读物':'http://bang.dangdang.com/books/newhotsales/01.52.00.00.00.00-recent30-0-0-1-',
        '小说':'http://bang.dangdang.com/books/newhotsales/01.03.00.00.00.00-recent30-0-0-1-',
        '医学':'http://bang.dangdang.com/books/newhotsales/01.56.00.00.00.00-recent30-0-0-1-',
        '农业/林业':'http://bang.dangdang.com/books/newhotsales/01.66.00.00.00.00-recent30-0-0-1-',
        '自然科学':'http://bang.dangdang.com/books/newhotsales/01.62.00.00.00.00-recent30-0-0-1-',
        '中小学教辅':'http://bang.dangdang.com/books/newhotsales/01.43.00.00.00.00-recent30-0-0-1-',
        '工具书':'http://bang.dangdang.com/books/newhotsales/01.50.00.00.00.00-recent30-0-0-1-',
        '英文原版书':'http://bang.dangdang.com/books/newhotsales/01.58.00.00.00.00-recent30-0-0-1-',
        '青春文学':'http://bang.dangdang.com/books/newhotsales/01.01.00.00.00.00-recent30-0-0-1-',
        '动漫/幽默':'http://bang.dangdang.com/books/newhotsales/01.09.00.00.00.00-recent30-0-0-1-',
        '成功/励志':'http://bang.dangdang.com/books/newhotsales/01.21.00.00.00.00-recent30-0-0-1-',
        '休闲/爱好':'http://bang.dangdang.com/books/newhotsales/01.04.00.00.00.00-recent30-0-0-1-',
        '育儿/早教':'http://bang.dangdang.com/books/newhotsales/01.17.00.00.00.00-recent30-0-0-1-',
        }
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

app = wx.App()
frame = TestFrame()



    
##定义一个元组存数据

frame.Show()
app.MainLoop()
