# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='path',
            field=models.FileField(upload_to=b'Bulletins/user/%Y/%m/%d'),
            preserve_default=True,
        ),
    ]
