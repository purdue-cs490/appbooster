# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appbooster', '0002_auto_20141104_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='public_ssh',
            field=models.CharField(default='a', max_length=1024),
            preserve_default=False,
        ),
    ]
