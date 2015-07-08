# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0005_auto_20150614_0725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='StudentId',
        ),
        migrations.AddField(
            model_name='history',
            name='QuestionId',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='history',
            name='QIdError',
            field=models.IntegerField(null=True),
        ),
    ]
