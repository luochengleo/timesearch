#coding=utf8
__author__ = 'luocheng'

import urllib
import urllib2

import datetime
class SearchResultCrawler:
    def __init__(self):
        pass
    def crawl(self,query,index=1):
        url ='http://www.sogou.com/web?query='+urllib.quote(query.encode('utf8'))+'&num=50&page='+str(index)+'&ie=utf8'
        # print url
        try:
            webpage = urllib2.urlopen(url,timeout=20).read()
            return webpage

        except Exception, e:
            print e
            return ''


if __name__ == '__main__':
    src = SearchResultCrawler()
    open('../temp/webpage1.html','w').write(src.crawl(u'我们的故事',1))
    open('../temp/webpage2.html','w').write(src.crawl(u'我们的故事',2))
    open('../temp/webpage3.html','w').write(src.crawl(u'我们的故事',3))
    open('../temp/webpage4.html','w').write(src.crawl(u'我们的故事',4))
    open('../temp/webpage5.html','w').write(src.crawl(u'我们的故事',5))

