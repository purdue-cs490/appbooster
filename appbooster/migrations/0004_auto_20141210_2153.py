# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import appbooster.models


class Migration(migrations.Migration):

    dependencies = [
        ('appbooster', '0003_appuser_public_ssh'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='public_ssh',
            field=models.CharField(max_length=1024, validators=[appbooster.models.validate_pub]),
        ),
    ]
