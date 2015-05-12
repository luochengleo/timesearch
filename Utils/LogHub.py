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

    def getClickedResults(self, studentID, taskid, query):
        clicked_logs = Log.objects.filter(studentID=studentID,
                                            task_id=taskid,
                                            query=query,
                                            action='CLICK')
        clicked_result_rank = []
        for l in clicked_logs:
            c = l.content
            clicked_result_rank.append(getRankOfClickResult(c))

        return SearchResult.objects.filter(query=query, rank__in=clicked_result_rank)


