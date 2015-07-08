# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classChoose', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='count',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=10)),
                ('value', models.IntegerField(default=0)),
            ],
        ),
    ]
