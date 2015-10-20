# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200, default='post')),
                ('direct_link', models.URLField(default='')),
                ('element_id', models.CharField(max_length=200)),
                ('owner_id', models.IntegerField(default=0)),
                ('post_id', models.IntegerField(default=0)),
                ('post_hash', models.CharField(max_length=200)),
            ],
        ),
    ]
