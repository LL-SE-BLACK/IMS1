# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0011_auto_20150707_1424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='H',
        ),
    ]
