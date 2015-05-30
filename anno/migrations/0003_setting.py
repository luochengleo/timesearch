# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anno', '0002_task_audiofilename'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idx', models.IntegerField()),
                ('taskidx', models.IntegerField()),
                ('option', models.CharField(max_length=1000)),
                ('temporal', models.CharField(max_length=1000)),
                ('status', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
