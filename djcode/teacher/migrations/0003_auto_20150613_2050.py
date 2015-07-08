# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_auto_20150612_1049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='ClassId',
        ),
        migrations.AddField(
            model_name='question',
            name='CourseId',
            field=models.CharField(max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='Difficulty',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='Type',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='paper',
            name='ClassId',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='question',
            name='Chapter',
            field=models.IntegerField(),
        ),
    ]
