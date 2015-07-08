# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0007_paper_full'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='StartTime',
            field=models.DateTimeField(null=True),
        ),
    ]
