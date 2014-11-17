from django.db import models
django.contrib.admin.models import User

class Bulletin(models.Model):
    title = models.Charfield(max_length = 250)
    description = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User)
    
    def __str__(self):
        return self.title
    
class File(models.Model):
    filename = models.CharField(max_length=50)
    path = models.CharField(max_length=200)
    bulletin = models.ForeignKey(Bulletin)
    users = models.ManyToManyField(User)
    def __str__(self):
        return self.filename
