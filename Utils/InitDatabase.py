__author__ = 'defaultstr'

from anno.models import Task
from anno.models import Setting
def importTasks(filename):
    print 'import tasks',filename
    fin = open(filename, 'r')
    for line in fin:
        print line
        task_id, init_query, content,question = line.split(',')
        task_id = int(task_id)
        t = Task(content=content, task_id=task_id, init_query=init_query, question=question)
        print content,task_id,init_query
        t.save()

def importSettings(filename,offset=25):
    numSetting = 0
    for l in open(filename):
        numSetting +=1
        numTask = 0
        segs = l.strip().split(',')
        for s in segs:
            numTask += 1
            if s =='0':
                _set = Setting(idx = numSetting,taskidx = numTask, option = 'HIDDEN',temporal='HIGH',status=0)
                _set.save()
                _set = Setting(idx = numSetting+offset,taskidx = numTask, option = 'HIDDEN',temporal='LOW',status=0)
                _set.save()
            if s =='1':
                _set = Setting(idx = numSetting,taskidx = numTask, option = 'SAT',temporal='HIGH',status=0)
                _set.save()
                _set = Setting(idx = numSetting+offset,taskidx = numTask, option = 'SAT',temporal='LOW',status=0)
                _set.save()
            if s =='2':
                _set = Setting(idx = numSetting,taskidx = numTask, option = 'MIDSAT',temporal='HIGH',status=0)
                _set.save()
                _set = Setting(idx = numSetting+offset,taskidx = numTask, option = 'MIDSAT',temporal='LOW',status=0)
                _set.save()
            if s =='3':
                _set = Setting(idx = numSetting,taskidx = numTask, option = 'UNSAT',temporal='HIGH',status=0)
                _set.save()
                _set = Setting(idx = numSetting+offset,taskidx = numTask, option = 'UNSAT',temporal='LOW',status=0)
                _set.save()
    def default():
        importSettings('temp/setting.csv',25)