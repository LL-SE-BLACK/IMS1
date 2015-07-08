# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0008_paper_starttime'),
    ]

    operations = [
        migrations.AddField(
            model_name='onauth',
            name='UserId',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
