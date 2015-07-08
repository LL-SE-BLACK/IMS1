# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_auto_20150613_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='Deadline',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='OptionA',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='OptionB',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
