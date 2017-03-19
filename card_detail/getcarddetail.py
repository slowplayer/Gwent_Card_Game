import HTMLParser
import urllib2
import xlwt
import sys
import socket
def getHtml(url):
    socket.setdefaulttimeout(2)
    headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    try:
        req=urllib2.Request(url, headers=headers)
        page=urllib2.urlopen(req)
        html=page.read()
    except Exception, e:
        return None
    return html
class GwentWebParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.tagDIVFlag=False
        self.tagTRFlag=False
        self.tagAFlag=False
        self.tagSpanFlag=False
        
        self.tag_name=False
        self.tag_faction=False
        self.tag_power=False
        self.tag_row=False
        self.tag_type=False
        self.tag_layalty=False
        self.tag_abilities=False
       # self._name=None
       # self._path=None
        self.row=0
        self.col=1
        self.txt=''
        
        self.book=xlwt.Workbook(encoding='utf8')
        self.table=self.book.add_sheet('Gwent', cell_overwrite_ok=True)
    def init_table(self):
        self.table.write(0, 0, 'id')
        self.table.write(0, 1, 'name')
        self.table.write(0, 2, 'Faction')
        self.table.write(0, 3, 'Power')
        self.table.write(0, 4, 'Row')
        self.table.write(0, 5, 'Type')
        self.table.write(0, 6, 'Loyalty')
        self.table.write(0, 7, 'Ability')
    def save_table(self, str):
        self.book.save(str)
    def handle_starttag(self, tag, attrs):
        if tag=='div':
            for name, value in attrs:
                if name=='class' and value=='listing-body':
                    self.tagDIVFlag=True
        if tag=='tr':
            for name, value in attrs:
                if name=='class' and value=='card-row':
                    self.tagTRFlag=True
                    self.row+=1
                    self.col=0
                    self.table.write(self.row, self.col, str(self.row))
                    self.col+=1
        if tag=='a':
            if self.tag_name:
                self.tagAFlag=True
        if tag=='span':
            if self.tag_row:
                self.tagSpanFlag=True
      #      flag=False
            for name, value in attrs:
              #      if  name=='class' and  value=='no-loyalty' and  self.tag_layalty:
             #           flag=True
                    if  name=='title' and value=='Loyal' and self.tag_layalty:
                        self.txt+='L'
             #           flag=True
                    if  name=='title' and value=='Disloyal' and self.tag_layalty:
                        self.txt+='D'
          #              flag=True
                    if name=='title' and self.tag_abilities:
                        self.txt+= value
        #                flag=True
     #       if flag:
         #       self.col+=1
        if tag=='td':
            for name, value in attrs:
                if name=='class' and value=='col-name ':
                    self.tag_name=True
                if name=='class' and 'col-faction faction-' in value:
                    self.tag_faction=True
                  
                if name=='class' and value=='col-power':
                    self.tag_power=True
                 
                if name=='class' and value=='col-row':
                    self.tag_row=True
                   
                if name=='class' and value=='col-type':
                    self.tag_type=True
                
                if name=='class' and value=='col-loyalty':
                    self.tag_layalty=True
                
                if name=='class' and  value=='col-abilities':
                    self.tag_abilities=True
    def handle_endtag(self, tag):
        if tag=='div':
            self.tagDIVFlag=False
        if tag=='tr':
            self.tagTRFlag=False
        if tag=='a':
            self.tagAFlag=False
        if tag=='span':
            self.tagSpanFlag=False
        if tag=='td':
            if self.tag_name or self.tag_faction or self.tag_abilities or self.tag_type or self.tag_layalty or self.tag_power or self.tag_row:
                self.table.write(self.row, self.col,self.txt)
                self.col+=1
                self.txt=''
                self.tag_name=False
                self.tag_faction=False
                self.tag_power=False
                self.tag_row=False
                self.tag_type=False
                self.tag_layalty=False
                self.tag_abilities=False
       
    def handle_data(self, data):
        if (self.tag_name and self.tagAFlag) or (self.tag_faction)or (self.tag_power) or (self.tag_row and self.tagSpanFlag)or (self.tag_type) :
            self.txt+=data
         #   self.col+=1
count=1
org=u'http://www.gwentdb.com/cards?filter-display=1&page='
parser=GwentWebParser()
parser.init_table()
print sys.getdefaultencoding()
while count<=14:
    print count
    page=org+str(count)
    txt=getHtml(page)
    print 'html ok'
    if txt!=None:
        parser.feed(txt)
        count+=1
print 'rdy'
parser.save_table('/home/huo/Gwent.xls')
print u'all work done'
