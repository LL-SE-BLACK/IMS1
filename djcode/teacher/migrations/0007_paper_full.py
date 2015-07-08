# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0006_auto_20150614_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='Full',
            field=models.FloatField(null=True),
        ),
    ]
