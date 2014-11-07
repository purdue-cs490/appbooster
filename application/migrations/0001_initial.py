# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appbooster', '0003_appuser_public_ssh'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('container_id', models.CharField(max_length=100)),
                ('apptype', models.CharField(max_length=30)),
                ('port_num', models.IntegerField(unique=True)),
                ('wsgi_module', models.CharField(max_length=256)),
                ('git_repo', models.CharField(max_length=256)),
                ('appusers', models.ManyToManyField(to='appbooster.AppUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
