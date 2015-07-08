# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='Course',
            new_name='ClassId',
        ),
        migrations.AddField(
            model_name='paper',
            name='MaxScore',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='paper',
            name='MinScore',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='paper',
            name='SubmitNum',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='paper',
            name='SumScore',
            field=models.FloatField(null=True),
        ),
    ]
