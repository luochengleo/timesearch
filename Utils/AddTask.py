__author__ = 'defaultstr'

from anno.models import Task

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
