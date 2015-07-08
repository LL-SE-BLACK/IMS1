# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_auto_20150613_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='Flag',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='Score',
            field=models.IntegerField(null=True),
        ),
    ]
