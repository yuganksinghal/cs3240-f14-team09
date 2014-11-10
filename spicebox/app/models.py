from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)    

class Bulletin(models.Model):
    description = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User)
    #add date later
 
class File(models.Model):
    filename = models.CharField(max_length=50)
    path = models.CharField(max_length=200)
    bulletin = models.ForeignKey(Bulletin)
    users = models.ManyToManyField(User) 
