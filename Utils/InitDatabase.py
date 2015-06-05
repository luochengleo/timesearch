__author__ = 'defaultstr'

from anno.models import Task
from anno.models import Setting
def importTasks(filename):
    print 'import tasks',filename
    fin = open(filename, 'r')
    for line in fin:
        print line
        task_id, init_query, content,question,filename = line.split(',')
        task_id = int(task_id)
        t = Task(content=content, task_id=task_id, init_query=init_query, question=question,audiofilename='static/audio/'+filename)
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
def importTestSettings():
    options = ['SAT','MIDSAT','UNSAT']
    import random
    for i in range(1,21,1):
        rit = random.randint(0, 2)
        _set = Setting(idx = 51,taskidx = i, option = options[rit],temporal='HIGH',status=0)
        _set.save()
    for i in range(1,21,1):
        rit = random.randint(0, 2)
        _set = Setting(idx = 52,taskidx = i, option = options[rit],temporal='LOW',status=0)
        _set.save()


def init_default():
    importSettings('temp/setting.csv',25)
    importTasks('temp/tasksforimport.csv')
    importTestSettings()