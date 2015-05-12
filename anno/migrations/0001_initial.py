# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('studentID', models.CharField(max_length=50)),
                ('task_id', models.IntegerField()),
                ('query', models.CharField(max_length=100)),
                ('result_id', models.CharField(max_length=50)),
                ('result_url', models.CharField(max_length=1024)),
                ('score', models.IntegerField()),
                ('content', models.CharField(max_length=5000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FillingQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('studentID', models.CharField(max_length=50)),
                ('task_id', models.IntegerField()),
                ('action', models.CharField(max_length=20)),
                ('query', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=5000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=100)),
                ('resultnum', models.IntegerField()),
                ('recomm', models.CharField(max_length=1000)),
                ('lastcrawledpage', models.IntegerField()),
                ('stopCrawl', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuerySatisfaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('studentID', models.CharField(max_length=50)),
                ('task_id', models.IntegerField()),
                ('query', models.CharField(max_length=100)),
                ('score', models.IntegerField()),
                ('content', models.CharField(max_length=5000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionnaireAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('studentID', models.CharField(max_length=50)),
                ('task_id', models.IntegerField()),
                ('answer', models.CharField(max_length=5000)),
                ('content', models.CharField(max_length=5000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('query', models.CharField(max_length=100)),
                ('result_id', models.CharField(max_length=50)),
                ('rank', models.IntegerField()),
                ('content', models.CharField(max_length=2000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SessionAnnotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('studentID', models.CharField(max_length=50)),
                ('task_id', models.IntegerField()),
                ('score', models.IntegerField()),
                ('content', models.CharField(max_length=5000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SingleChoiceQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1000)),
                ('choices', models.CharField(max_length=5000)),
                ('answer', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=1000)),
                ('task_id', models.IntegerField()),
                ('init_query', models.CharField(max_length=1000)),
                ('question', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='singlechoicequestion',
            name='task',
            field=models.ManyToManyField(to='anno.Task'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fillingquestion',
            name='task',
            field=models.ManyToManyField(to='anno.Task'),
            preserve_default=True,
        ),
    ]
