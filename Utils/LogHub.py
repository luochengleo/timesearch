#coding=utf8
__author__ = 'luocheng'
from anno.models import Log
from Utils.LogParser import *

class LogHub:
    def __init__(self):
        pass

    def getQueriesWithSIDandTaskID(self,s,t):
        logs = Log.objects.filter(studentID=s, task_id=t)
        print 'log hub find log',len(logs)
        alreadyin = set()
        rtr = list()
        for l in logs:
            q  =l.query
            if q in alreadyin:
                pass
            else:
                alreadyin.add(q)
                rtr.append(q)
        return rtr

    def getClickedResults(self, sid, tid):
        clicked_logs = Log.objects.filter(studentID=sid,
                                            task_id=tid,
                                            action='CLICK')

        clicked_result_rank = []
        query = Task.objects.get(task_id= tid).init_query
        print 'length of clicked_logs',len(clicked_logs)
        print clicked_logs
        for l in clicked_logs:
            c = l.content
            clicked_result_rank.append(getRankOfClickResult(c))
        return SearchResult.objects.filter(rank__in=clicked_result_rank,query=query)


