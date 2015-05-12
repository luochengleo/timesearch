#coding=utf8
__author__ = 'defaultstr'
from anno.models import *
from django.db import transaction, models
import re


patterns = {key: re.compile('%s=(.*?)\\t' % key) for key in ['TIMESTAMP', 'USER', 'TASK', 'QUERY', 'ACTION']}
info_patterns = re.compile('INFO:\\t(.*?)$')
anno_info_patterns = {key: re.compile('%s=(.*?)\\t' % key) for key in ['id', 'src']}
anno_info_patterns['score'] = re.compile('score=(.*?)$')


def fromString(line):
    studentID = patterns['USER'].search(line).group(1)
    task_id = patterns['TASK'].search(line).group(1)
    query = patterns['QUERY'].search(line).group(1)
    info = info_patterns.search(line).group(1)
    result_id = anno_info_patterns['id'].search(info).group(1)
    result_url = anno_info_patterns['src'].search(info).group(1)
    score = int(anno_info_patterns['score'].search(info).group(1))
    anno_log_obj = Annotation.objects.create(studentID=studentID,
                                task_id=task_id,
                                query=query,
                                result_id=result_id,
                                result_url=result_url,
                                score=score,
                                content=line)
    return anno_log_obj


@transaction.commit_manually
def insertMessageToDB(message):
    try:
        for line in message.split('\n'):
            print line
            if line == '':
                continue
            log = fromString(line)
            log.save()
    except Exception:
        transaction.rollback()
    else:
        transaction.commit()
