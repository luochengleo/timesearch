#coding=utf8
__author__ = 'cheng'

from anno.models import *
from django.db import transaction, models
from Utils.SearchResultCrawler import SearchResultCrawler
from Utils.SearchResultPageParser import SearchResultPageParser
from bs4 import BeautifulSoup

import time


class SearchResultHub:
    def __init__(self):
        pass

    def getResult(self, query, beginIndex, number):

        print 'searching in database'

        queries = Query.objects.filter(content=query)

        if len(queries) ==0:
            q = Query(content=query,resultnum=0,recomm='',lastcrawledpage=0,stopCrawl=0)
        else:
            q = queries[0]



        src = SearchResultCrawler()
        srpp = SearchResultPageParser()
        results = list()
        crawlIndex =q.lastcrawledpage+1
        resultnum = q.resultnum


        if resultnum <=beginIndex+number or resultnum< beginIndex+2*number:
            if q.stopCrawl == 1:
                print 'STOP CRAWLING'
                sr_list = SearchResult.objects.filter(query=query)
                return sorted(sr_list, key=lambda x:x.rank)[beginIndex:min(beginIndex+number,len(sr_list))]
            else:
                print 'BEGIN CRAWLING'
                content = src.crawl(query, crawlIndex)
                print 'FINISH CRAWLING'
                parsedResults = srpp.parse(content)
                if len(parsedResults) == 0:
                    print 'WARNING: No Results on Web Page',crawlIndex
                    open(str(beginIndex)+'-'+str(crawlIndex)+'.html','w').write(content)
                    print 'WRITING CONTENT'
                    q.stopCrawl = 1
                    q.resultnum = resultnum
                    q.lastcrawledpage = crawlIndex-1
                    q.save()
                    sr_list = SearchResult.objects.filter(query=query)
                    return sorted(sr_list, key=lambda x:x.rank)[beginIndex:min(beginIndex+number,len(sr_list))]
                else:
                    print 'MERGING RESULTS', len(parsedResults)
                    resultnum = self.insert_into_db(parsedResults, query, resultnum)
                    print 'INSERT INTO DATABASE', resultnum
                    crawlIndex += 1
                    q.resultnum = resultnum
                    # TODO recheck  the lastcrawledpage
                    q.lastcrawledpage =  crawlIndex -1
                    q.save()
                    sr_list = SearchResult.objects.filter(query=query)
                    return sorted(sr_list, key=lambda x:x.rank)[beginIndex:min(beginIndex+number,len(sr_list))]


        else:
            sr_list = SearchResult.objects.filter(query=query)
            print 'ENOUGH RESULTS', beginIndex, number, len(sr_list)

            return sorted(sr_list, key=lambda x:x.rank)[beginIndex:beginIndex+number]


    def getCount(self, query):
        sr_list = SearchResult.objects.filter(query=query)
        # modified by luocheng;

        # return 90
        return min(len(sr_list), 90)


    @transaction.commit_manually
    def insert_into_db(self, parsedResults, query, resultnum):
        num = resultnum
        try:
            for r in parsedResults:
                soup = BeautifulSoup(r,from_encoding='utf8').find('div', class_='rb')
                if soup.has_attr('id'):
                    soup['id'] = 'rb_'+str(num)
                    robj = SearchResult.objects.create(query=query,
                                                       rank=num,
                                                       result_id='rb_'+str(num),
                                                       content=str(soup))
                    robj.save()
                    num += 1
                else:
                    print "THE RESULT IS NOT VALID", resultnum
        except Exception as e:
            print "roll back!"
            print e
            transaction.rollback()
            return resultnum
        else:
            print "commit success!"
            transaction.commit()
            return num

    def test(self):
        for item in self.getResult(query='清华大学',beginIndex=1,number=10):
            print '--------------------'
            print item.rank
            print '--------------------'











