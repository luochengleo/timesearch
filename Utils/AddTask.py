__author__ = 'defaultstr'

from anno.models import Task

def importTasks(filename):
    with open(filename, 'r') as fin:
        next(fin)
        for line in fin:
            task_id, init_query, content,question = line.split(',')
            task_id = int(task_id)
            t = Task(content=content, task_id=task_id, init_query=init_query, question=question)
            t.save()
