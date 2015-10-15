# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0003_auto_20151012_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='stud_photo',
            field=models.ImageField(help_text='Можно загрузить фотографию позже', upload_to='', blank=True),
        ),
    ]
