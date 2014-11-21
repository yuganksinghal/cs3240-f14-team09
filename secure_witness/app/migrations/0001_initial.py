# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bulletin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options=None,
            bases=None,
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=50)),
                ('path', models.CharField(max_length=200)),
                ('bulletin', models.ForeignKey(to='app.Bulletin')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options=None,
            bases=None,
        ),
    ]
