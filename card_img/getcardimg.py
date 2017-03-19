#encoding=utf8 
import HTMLParser
import urllib2
import urllib
import sys
def getHtml(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req=urllib2.Request(url, headers=headers)
    page=urllib2.urlopen(req)
    html=page.read()
    return html
class GwentWebParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.tagDIVFlag=False
        self.tagAFlag=False
        self.tagPFlag=False
        
        self._name=None
        self._path=None
    def handle_starttag(self, tag, attrs):
        if tag=='div':
            for name, value in attrs:
                if name=='class' and value=='sw-card-image-container ':
                    self.tagDIVFlag=True
        if tag=='a':
            if self.tagDIVFlag:
                self.tagAFlag=True
        if tag=='p':
           if self.tagDIVFlag:
                self.tagPFlag=True
        if tag=='img':
            if self.tagDIVFlag and self.tagAFlag:
                for name, value in attrs:
                    if name=='src':
                        self._path=value.encode('utf-8')
                        urllib.urlretrieve(self._path, '/home/huo/image2/%s.png'%self._name.encode('utf-8'))
                       # urllib.urlretrieve(self._path, '/home/huo/image2/%s.jpg'%self._name)
                       # print self._name
                    if name=='alt':
                        self._name=value
    def handle_endtag(self, tag):
        if tag=='div':
            self.tagDIVFlag=False
        if tag=='a':
            self.tagAFlag=False
        if tag=='p':
            self.tagPFlag=False
    def handle_data(self, data):
      if self.tagPFlag:
        print 'handle'
        print data.encode('utf-8')
#reload(sys)
#sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()
#print sys.path
count=1
org=u'http://www.gwentdb.com/cards?filter-display=2&page='
parser=GwentWebParser()
while count<=14:
    print count
    page=org+str(count)
    txt=getHtml(page)
    print u'html ok'
    parser.feed(txt)
    count+=1
print u'all work done'
