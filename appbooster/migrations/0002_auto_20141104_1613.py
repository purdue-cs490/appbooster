# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appbooster', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appuser',
            old_name='verify_code',
            new_name='verifycode',
        ),
    ]
