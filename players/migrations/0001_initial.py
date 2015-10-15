# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('email', models.EmailField(error_messages={'unique': "We've have already this"}, unique=True, max_length=255)),
                ('surname', models.CharField(max_length=25)),
                ('name', models.CharField(max_length=15)),
                ('university', models.CharField(max_length=15)),
                ('experience', models.PositiveSmallIntegerField()),
                ('vk_link', models.URLField(error_messages={'unique': "We've have already this"}, default='vk.com/', unique=True)),
                ('position', models.CharField(choices=[('han', 'Handler'), ('mid', 'Middle'), ('lon', 'Long'), ('sid', 'On sideline')], max_length=3)),
                ('fav_throw', models.CharField(max_length=15)),
                ('style', models.CharField(choices=[('slow', 'SlowPock'), ('regul', 'Regular'), ('cheek', 'cheeky'), ('uncon', 'Uncontrollable'), ('drunk', 'Drunk')], max_length=5)),
                ('size', models.CharField(choices=[('xs', 'XS'), ('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL')], max_length=2)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('data_joined', models.DateTimeField()),
                ('groups', models.ManyToManyField(related_query_name='user', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', to='auth.Group', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions', to='auth.Permission', related_name='user_set')),
            ],
            options={
                'permissions': ('check_payment', 'Payment checking'),
            },
        ),
    ]
