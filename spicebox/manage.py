#!/usr/bin/env python
import os
import sys
from django.db import models

class User(models.Model):
    type = models.CharField(max_length= 50)
    username = models.CharField(max_length= 50)
class File(models.Model):
    name = models.CharField(max_length= 50)
    location = models.CharField(max_length= 200)

class Bulletin(models.Model):
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    location = models.CharField(max_length=200)
    author = models.ForeignKey(User)
    file = models.ForeignKey(File)


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spicebox.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
