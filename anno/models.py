from django.db import models

# Create your models here.

# MongoEngine	Django
# StringField	CharField
# URLField	URLField
# EmailField	EmailField
# IntField	IntegerField
# FloatField	FloatField
# DecimalField	DecimalField
# BooleanField	BooleanField
# DateTimeField	DateTimeField
# EmbeddedDocumentField	--
# DictField	--
# ListField	--
# SortedListField	--
# BinaryField	--
# ObjectIdField	--
# FileField	FileField
class Task(models.Model):
    content = models.CharField(max_length=1000)
    task_id = models.IntegerField()
    init_query = models.CharField(max_length=1000)
    question = models.CharField(max_length=1000)

class Query(models.Model):
    content = models.CharField(max_length=100)
    resultnum = models.IntegerField()
    recomm = models.CharField(max_length=1000)
    lastcrawledpage = models.IntegerField()
    stopCrawl = models.IntegerField()


class SearchResult(models.Model):
    # query = models.ForeignKey(Query)
    query = models.CharField(max_length=100)
    result_id = models.CharField(max_length=50)
    rank = models.IntegerField()
    content = models.CharField(max_length=2000)

class SingleChoiceQuestion(models.Model):
    description = models.CharField(max_length=1000)
    choices = models.CharField(max_length=5000)
    answer = models.IntegerField()
    task = models.ManyToManyField(Task)

class FillingQuestion(models.Model):
    description = models.CharField(max_length=1000)
    task = models.ManyToManyField(Task)

class Log(models.Model):
    studentID = models.CharField(max_length=50)
    task_id = models.IntegerField()
    action = models.CharField(max_length=20)
    query = models.CharField(max_length=100)
    content = models.CharField(max_length=5000)

class Annotation(models.Model):
    studentID = models.CharField(max_length=50)
    task_id = models.IntegerField()
    query = models.CharField(max_length=100)
    result_id = models.CharField(max_length=50)
    result_url = models.CharField(max_length=1024)
    score = models.IntegerField()
    content = models.CharField(max_length=5000)


class SessionAnnotation(models.Model):
    studentID = models.CharField(max_length=50)
    task_id = models.IntegerField()
    score = models.IntegerField()
    content = models.CharField(max_length=5000)

class QuerySatisfaction(models.Model):
    studentID = models.CharField(max_length=50)
    task_id = models.IntegerField()
    query = models.CharField(max_length=100)
    score = models.IntegerField()
    content = models.CharField(max_length=5000)

class QuestionnaireAnswer(models.Model):
    studentID = models.CharField(max_length=50)
    task_id = models.IntegerField()
    answer = models.CharField(max_length=5000)
    content = models.CharField(max_length=5000)


if __name__ == '__main__':
    task = Task(connect='hello world', task_id=0)
    task.save()






