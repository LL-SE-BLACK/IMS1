# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0009_onauth_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='H',
            field=models.IntegerField(null=True),
        ),
    ]
