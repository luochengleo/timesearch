# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anno', '0004_auto_20150604_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeEstimation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('studentID', models.CharField(max_length=50)),
                ('task_id', models.IntegerField()),
                ('time', models.CharField(max_length=5000)),
                ('content', models.CharField(max_length=5000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
