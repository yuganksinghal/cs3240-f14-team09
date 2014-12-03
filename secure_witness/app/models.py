from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Folder(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User)
    def __unicode__(self):
        return self.name

class Bulletin(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User)
    folder = models.ForeignKey(Folder)
    password = models.CharField(max_length=3000)
    anonymous = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

def get_upload_path(instance, filename):
    return str(instance.user) + '/' + filename

class File(models.Model):
    filename = models.CharField(max_length=50)
    path = models.FileField(upload_to=get_upload_path)
    bulletin = models.ForeignKey(Bulletin)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.filename
