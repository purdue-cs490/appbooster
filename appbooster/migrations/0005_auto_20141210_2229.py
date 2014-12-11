# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appbooster', '0004_auto_20141210_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='public_ssh',
            field=models.CharField(max_length=1024),
        ),
    ]
